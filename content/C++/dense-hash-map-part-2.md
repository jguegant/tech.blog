Title: Making a STL-compatible hash map from scratch - Part 2 - Growth Policies & The Schrodinger std::pair
Date: 17:40 04-13-2020 
Modified: 17:40 04-13-2020
Tags: C++17, hash map, unordered_map. 
Slug: dense-hash-map2

This post is part of a series of posts:

- [Part 1 - Beating std::unordered_map]({filename}../C++/dense-hash-map.md)
- **Part 2 - Growth Policies & The Schrodinger std::pair (Current)**
- Part 3 - Writing iterators (Coming Soon)
- Part 4 - ... (Coming Soon)

In the [previous post]({filename}../C++/dense-hash-map.md), we started a quest that consists in implementing an associative container similar to `std::unordered_map` in the C++ standard library. We saw two approaches that could help us in beating the performance of most `std::unordered_map` implementations: freeing ourselves from stable-addressing and swapping the modulo operation with some bitwise operations.
Due to its layout, we called this new associative container a `dense_hash_map`. You can find a reference implementation [right here](https://github.com/Jiwan/dense_hash_map).

Let's carry-on and start our own implementation right now!

# Part 2 - Structuring our code & Dealing with value_type:

## Preparing for the adventure:

Disclaimer: this section starts very gently, if your C++ e-beard or e-hair is already pretty long, you may want to skip to the **Structuring our code** section. 

Like any heroe starting her/his journey, we need to ensure we have the right items in our inventory.

For C++, here is my list of handy things to have when working on some standard-ish looking code:

- [eel.is C++ draft](http://eel.is/c++draft/), the holly bible of C++ itself (the latest draft of the C++ standard).
eel.is's transformation of the standard latex source files to a clean HTML version is a godsent gift. You can navigate in each of the sections of the standard with ease. In our case, we will mainly refer ourselves to the sections [unord.map](http://eel.is/c++draft/unord.map), [associative.reqmts](http://eel.is/c++draft/associative.reqmts) and [container](http://eel.is/c++draft/containers).
- [cppreference](https://en.cppreference.com), the tuned-down version of the standard. This wiki is of great help when the lawyer language of the standard is too advanced for your taste (sometimes the standard feels downright insulting to your intellectual abilities). On some rare occasions, I have seen **cppreference** have slightly innacurate descriptions of the standard. It always nice to cross-check the holly bible and this wiki. In our case, we will most refer to the [unordered_map section](https://en.cppreference.com/w/cpp/container/unordered_map).
- [godbolt](https://godbolt.org/) to experiment quickly your ideas on different compilers and check how the standard reacts for certain use-cases. With the recently added feature that permits you to run code, **godbolt** is extremly handy. **Goldbot's** grand cousin, [cppinsights](https://cppinsights.io/) can help you to explore complicated expressions. 
- [The C++ core guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), a bunch of C++ precepts written or more or less by those behind the holly C++ standard. When given multiples way of doing one task, the core guidelines will direct you towards the better way to achieve that task.
- Some linter and formatting tools. I personally like [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) and [clang-format](https://clang.llvm.org/docs/ClangFormat.html). 
- A good unit-test framework like [catch2](https://github.com/catchorg/Catch2). Writing such standard-like code without writing unit-tests is like running naked towards a level 100 creature and expecting to beat it with a simple bamboo stick. Good luck to you to achieve that!
- A bunch of warnings applied on your compiler. For the unix-like compilers (GCC or clang), a bare minimum would be  `-Wall -Wextra -pedantic -Werror`.

<center><img width=50% height=50% src="{filename}/images/the-holly-cpp-standard.jpg" alt="The Holly C++ Standard"/></center>

And, some optional items:

- A recent compiler that supports a recent version of the language (C++17 in my case). Technically, nothing prevents you to write standard-library-like code with ancient C++, but each version of the standard made it a lot simpler. This is especially true for the meta-programming part.
- [cmake](https://cmake.org/). Whether you find cmake's syntax an abomination or poetry, it is currently the de-facto standard build tool for any C++ projects.
Just for that sake of consistency in the C++ ecosystem, I would advise to support some sort of **cmake** bindings for your project. 

## Structuring our code:

### A header only Library:

Given that most of of the classes, functions or even variables will have template parameters, there will be very little code that could end-up in its own compilation unit. So the `dense_hash_map` will be header library. The file layout is fairly standard:

```bash
├── CMakeLists.txt                                # Main CMakeLists.txt file that defines.
├── include
│   └── jg
│       ├── dense_hash_map.hpp                    # Main file to be included by users.
│       └── details                               # Folder that contains internal structures that users should not depend-on.
│           ├── bucket_iterator.hpp
│           ├── dense_hash_map_iterator.hpp
│           ├── node.hpp
│           ├── power_of_two_growth_policy.hpp
│           └── type_traits.hpp
├── tests                                         # Unit-tests folder.
│   ├── CMakeLists.txt
│   └── src
│       └── dense_hash_map_tests.cpp
```
Note: as any C++ egonomaniac would do when facing the hard issue of choosing a namespace for his/her project, I went for my initial "jg".


### Our main class in dense_hash_map.hpp:

To be able to organise our code correctly, let's have look at the "dense" layout we saw in the last [post]({filename}../C++/dense-hash-map.md): 

<center><img width=60% height=60% src="{filename}/images/dense_hash_map_layout2.png" alt="The definitive layout"/></center>

We will have **two vectors**:

- One for the **buckets**. More precisely, these are the indices for the first node of the linked-list of each of our buckets.
- One for all the **nodes**. These are the nodes in the interleaved linked-lists that hold the key/value pairs.

While we are crafting our `dense_hash_map` from scratch, it doesn't mean that we cannot reuse some of the other containers in the standard library.
Naturally, our **two vectors** will be some good old `std::vector`. Both of those will be members of our [dense_hash_map class](https://github.com/Jiwan/dense_hash_map/blob/master/include/jg/dense_hash_map.hpp#L892). If we inspire ourselves from [std::unordered_map's signature](https://en.cppreference.com/w/cpp/container/unordered_map), this gives us our first piece of code:

```c++
template <
    class Key, 
    class T, 
    class Hash = std::hash<Key>, 
    class Pred = std::equal_to<Key>,
    class Allocator = std::allocator<std::pair<const Key, T>>,
    class GrowthPolicy = details::power_of_two_growth_policy
>
class dense_hash_map : private GrowthPolicy
{
private:
    // Define some aliases to avoid further typing later on.
    using node_type = details::node<Key, T>; // A node type that contains our key/value.
    using nodes_container_type = std::vector<node_type>;
    using nodes_size_type = typename nodes_container_type::size_type;
    using buckets_container_type = std::vector<nodes_size_type>;

public:
    // ...

private:
    nodes_container_type nodes_;
    buckets_container_type buckets_;
};
```
The `buckets_container_type` is dependent on the `size_type` of the `nodes_container_type`. In a `std::vector`, `size_type` is the type used for accessing elements using the subscript operator `operator[]`. It makes sense, since **buckets_** contains indices for **nodes_**. Traditionnaly, and to the [dismay of plenty](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1428r0.pdf), `size_type` is `std::size_t` which is an unsigned integer. We will use the value of `std::numeric_limits<nodes_size_type>::max()` to represent an invalid index into **nodes_** or the end of our linked-lists:

```c++
static inline constexpr nodes_size_type node_end_index = std::numeric_limits<nodes_size_type>::max();
```

For instance, **buckets_** will be initialized, at the construction of an empty `dense_hash_map`, with `node_end_index` since all the buckets are empty.

If you were attentive, you also noticed that there was also an extra template parameter `GrowthPolicy` to `dense_hash_map`. Let's have a closer look at it!

### Growth Policy:

In the last [post]({filename}../C++/dense-hash-map.md), we discovered some bitwise operation tricks to increase the speed when mapping a **key** to its **bucket**.
We also saw that there was drawbacks in doing so. So instead of forcing this design choice on our `dense_hash_map` users, we can make this behaviour a [policy](https://en.wikipedia.org/wiki/Modern_C%2B%2B_Design#Policy-based_design). The default policy will be the [power_of_two_growth_policy](https://github.com/Jiwan/dense_hash_map/blob/master/include/jg/details/power_of_two_growth_policy.hpp):

```c++
// power_of_two_growth_policy.hpp
namespace jg::details
{
struct power_of_two_growth_policy
{
    // Given a hash and the current capacity, use bitwise trick to return the bucket index.
    static constexpr auto compute_index(std::size_t hash, std::size_t capacity) -> std::size_t
    {
        return hash & (capacity - 1); // We saw that trick in the previous post.
    }

    // Given a desired new capacity for the bucket container, pick the closest power of two. 
    static constexpr auto compute_closest_capacity(std::size_t min_capacity) -> std::size_t
    {
         // We didn't see that trick yet.
        --min_capacity;                  

        min_capacity |= min_capacity >> 1;
        min_capacity |= min_capacity >> 2;
        min_capacity |= min_capacity >> 4;
        min_capacity |= min_capacity >> 8;
        min_capacity |= min_capacity >> 16;  

        if constexpr (sizeof(min_capacity) == 8)
        {
            min_capacity |= min_capacity >> 32;
        }

        return ++min_capacity;
    }

    // Returns the minimum capacity (~= initial capacity) the bucket container must have.
    static constexpr auto minimum_capacity() -> std::size_t { return 8u; }
};
}
```

All the growth policies will have to respect an implicit [C++ concept](https://en.cppreference.com/w/cpp/language/constraints): it must have the three static member functions `compute_index`, `compute_closest_capacity` and `minimum_capacity`. 

These specific `compute_index` and `minimum_capacity` functions are self-explanatory. But `compute_closest_capacity` is interesting: it tries to find the closest upper power of two given a random capacity.
A clever way that achieve that task is to fill your capacity number in its bit representation with `1` starting from the right until you reach the highest bit already toggled on with `1`. Afterwards you can just increment and tadam... you get your upper power of two.
Here is an example with the number 18 to clarify a bit (no pune intended):
```text

18 (decimal) == 0001 0010 (binary)
                   ^ Highest bit already toggle on.

After filling starting from the right:
0001 1111 (binary)

And if we add one:
0010 0000 (binary) == 32 (decimal)
```
`compute_closest_capacity` is doing exactly that with the operator `|=` and some bit-shifting with the operator `>>`. It handles the case where we already have a power two by substracting one before processing the number. Finally, by sprinkling a bit of `if constexpr` we can detect whether `std::size_t` is made of 32  or 64 bits. The more bits we have, the more filling we need to do.

Note: you can also achieve a similar effect with some built-ins in your conpiler. For instance, GCC provides [__builtin_clz](https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html) which can be of great help.

Afterwards, we rely on the growth policy in our `dense_hash_map` by "using" its functions:

```c++
class dense_hash_map : private GrowthPolicy
{
    using GrowthPolicy::compute_closest_capacity; // "Import" the policy's functions in this scope.
    using GrowthPolicy::compute_index;
    using GrowthPolicy::minimum_capacity;
    
    // ...

    constexpr void rehash(size_type count)
    {
        // ...
        count = compute_closest_capacity(count);
        // ...
    }
};
```

So what's left of the first code snippet that we didn't dive into? The node type: `details::node<Key, T>`. By now, you should have a vague feeling that there is something is fishy with this one, it has its own class in the detail namespace. But is that so complicated to make a node holding a key/value pair?
If so, do you really want to enter this C++ dungeon?

## Dealing with a const value_type:

So here is the deal, `std::unordered_map` has a peculiar `value_type` (`value_type` is the type you obtain as a reference when querying most containers in the standard library when using iterators) which is `std::pair<const Key, T>`. Whenever you supply a template argument `Key`, all the key/value pairs you obtain from `std::unordered_map` will have their first member, which is the key, stored as `const Key`. And, this, ladies and gentlemen, is can of giant worms ready to devore your last bits of sanity. So... let's open it!

<center><img width=40% height=40% src="{filename}/images/dark-soul-open-door.jpg" alt="Opening the const value_type door"/></center>

When you think a bit more about it, this design prevents you to put yourself in serious troubles. You cannot mutate the keys in your associative container once you have inserted them. Typically, without a `const Key`, you would be able to do such crazy moves: 

```c++
jg::dense_hash_map<std::string, heroe> my_map{{"spongebob", heroe{}}, {"chuck norris", heroe{}}};
auto it = my_map.find("chuck norris");

it->first = "Chuck Norris"; // We are mutating the key to properly capitalise the venerable chuck.
// my_map after that would be in sad state.

```
When mutating a key, your key will very likely have a new hash (unless you are the lucky winner of a collision...) which means that it probably belongs to a new bucket (unless both hashes belong to the same bucket...). Sadly, there is no way for your container to be aware that you mutated a `std::pair<const Key, T>` it gave you as reference, which implies that the container cannot handle properly the hash change. Its internal data-structure would be in a broken state rather quickly. By having a `const Key`, the standard shields itself from this issue: the key becomes immutable.

Now, let's assume that our `details::node<Key, T>` has a `std::pair<const Key, T>`:

```c++
template <class Key, class T>
struct node {
    std::pair<const Key, T> pair;          // Our glorious pair.
    nodes_size_type next = node_end_index; // Next index of the node in the linked-list.
};
```

With our "dense" design, this becomes a **performance issue**. Our `std::pair<const Key, T>` will have its **move-constructor** and **move-assignment operator** disabled forever and ever, and so does the node type. All our nodes are stored in a packed vector `nodes_`, which sometimes reallocate itself and send all its content into a bigger buffer. Not being to able to **move** our objects accross memory is a huge bummer. We would have to copy them around. That's unacceptable! Even more irritating, **std::unordered_map** does not suffer from this as its design allocates each nodes separately.

Big problems require big <strike>solutions</strike> hacks. Here are our two choices:

- We make a `std::pair` type on steroids that communicates back and forth with the container when the key change.
  This also requires our new type to be interoperable with `std::pair`. It might be possible to partially fake a `std::pair` with some implicit conversions, but we will never make our `dense_hash_map` a drop-in replacement that way.
- We circumvent the type system with some [type punning](https://en.wikipedia.org/wiki/Type_punning) and create a schrodinger `std::pair` that has both a `Key` and a `const Key` as its first member. In other words, we store internally a `std::pair<Key, T>` in our node but expose it as a `std::pair<const Key, T>` to the user.

Obviously, the schrodinger `std::pair` sounds the most dangerous creature of the two. So... let's pick it!

#### The schrodinger **std::pair**:

C++ offers at least two official ways to perform type-punning: [reinterpret_cast](https://en.cppreference.com/w/cpp/language/reinterpret_cast) and [unions](https://en.cppreference.com/w/cpp/language/union).


##### reinterpret_cast:

**reinterpret_cast** sounds quite attractive: "it is purely a compile-time directive which instructs the compiler to treat expression as if it had the type new_type.". But if you read closely along the standard lines, it has a very restricted usage. It is often used when casting to `const char*` (`const std::byte*`) to manipulate your types as raw data. But even doing so is harder than you expect. A fun-fact is that the classic pattern in many C++ code-base of reinterpret_casting a memory buffer to a [POD](https://en.cppreference.com/w/cpp/named_req/PODType) is actually not [allowed](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0593r2.html):
```c++
struct A {
    int x;
};

const char* network_buffer = get_buffer();

// The following code is not allowed as explained by, you would need std:bless from p0593r2.
const A* my_a = reinterpret_cast<const A*>(network_buffer);
```

Clearly, **reinterpret_cast** is not our friend here. [cppreference](https://en.cppreference.com/w/cpp/language/reinterpret_cast) even gently warn us:

```text
The behavior is undefined unless one of the following is true:
- AliasedType and DynamicType are similar.
...
std::pair<int, int> and std::pair<const int, int> are not similar.
```

##### union:

We are left with C++'s [unions](https://en.cppreference.com/w/cpp/language/union) to perform our type-punning. Let's write one:
```c++
template <class Key, class T>
union union_key_value_pair
{
    using pair_t = std::pair<Key, T>;
    using const_key_pair_t = std::pair<const Key, T>;

    template <class... Args>
    union_key_value_pair(Args&&... args) : pair_(std::forward<Args>(args)...) {}

    union_key_value_pair(const union_key_value_pair& other) {}

    union_key_value_pair(union_key_value_pair&& other) {}

    auto operator=(const union_key_value_pair& other) -> union_key_value_pair&
    {
        pair_ = other.pair_;
        return *this;
    }

    auto operator=(union_key_value_pair&& other) -> union_key_value_pair&
    {
        pair_ = std::move(other).pair_;
        return *this;
    }

    ~union_key_value_pair() { pair_.~pair_t(); }

    pair_t pair_;
    const_key_pair_t const_key_pair_;
};
```
At this point, you would expect that we are always constructing a `std::pair<Key, T>`


Note: If you are a C++ purist that never abuse the standard or write his own undefined behaviour, here is the exact point in this post where you should use your jetpack and fly away to a better place. 


## Conclusion:

Move onto iterators.
