Title: Making a STL-compatible hash map from scratch - Part 3 - The wonderful world of iterators and allocators
Date: 17:40 04-21-2020 
Modified: 17:40 04-21-2020
Tags: C++17, hash map, unordered_map, iterator, allocator
Slug: dense-hash-map3

This post is part of a series of posts:

- [Part 1 - Beating std::unordered_map]({filename}../C++/dense-hash-map.md)
- [Part 2 - Growth Policies & The Schrodinger std::pair]({filename}../C++/dense-hash-map-part-2.md)**
- **Part 3 - The wonderful world of iterators and allocators (Current)**
- Part 4 - ... (Coming Soon)

In the [previous post]({filename}../C++/dense-hash-map-part-2.md), we prepared our data-structure to be able to store our key/value pairs in a performant way: our design permit us to expose, for safety, immutable keys to our users while internally having mutable access for speed. We also had fun with more bit magic to create a special growth policy for our bucket container. You can find a reference implementation [right here](https://github.com/Jiwan/dense_hash_map).

At this point, you are probably eager to start working on the algorithms of our `dense_hash_map`. Alas, we are not there yet! Two new kind of challengers entered the arena: **allocators** and **iterators**. Like any word finishing by "or" (Terminator, Alligator, Abductor, Debtor, Elevator, Moderator, Emperor...) there is a certain violence or authority coming out of it of these twos. And rightfully so, having those in your project is a good indicator that you will spend nights banging your head against a brick wall.

Let me be your mentor and I will guide you through these tough areas!

<center><img width=40% height=40% src="{filename}/images/terminator.jpg" alt="Terminator"/></center>

# Part 3 - The wonderful world of iterators and allocators:

## Two iterators with two different endeavors:

If we base ourselves on the [unordered_map's interface](https://en.cppreference.com/w/cpp/container/unordered_map), we should have at least four different sorts of iterator:

| *Name*                   | *Description*                                                      |
|--------------------------|--------------------------------------------------------------------|
| **iterator**             | Iterate through all key/value pairs of the map                     |
| **const_iterator**       | Similar to iterator but yields const references to the pairs       |
| **local_iterator**       | Iterator through all the key/value pairs in one bucket             |
| **const_local_iterator** | Similar to local_iterator but yields const references to the pairs |


It becomes clear that we will actually need to create only two types of iterators: **iterator** and **local_iterator**. The other two can be easily derived from the first ones. We will just sprinkle some `const` where we should.

### The interior of iterator:

If you wonder which kind of iterator to tackle first, `iterator` and its little bro `const_iterator` are probably the more interesting ones for our users.
Quite often you will want to iterate through all key/value pairs to perform some operations and this is what `iterator` is dedicated for.
More precisely, `iterator` is the type returned by [begin](https://en.cppreference.com/w/cpp/container/unordered_map/begin), [end](https://en.cppreference.com/w/cpp/container/unordered_map/end) & Co. which permits you to create a range-based for loop such as:

```c++
for (auto& [key, value] : my_map) {
    std::cout << key << ", " << value << "\n";
}
```

The modern picasso in me decided to show you what this range-loop would do internally:

<center><img width=50% height=50% src="{filename}/images/dense-hash-map-iterator.webp" alt=""/></center>

Yes, it should be as simple as iterating in our `nodes_` container. No, it won't be as easy you may think.

To iterate over the `nodes_` container, we can simply use its own... iterators. Conveniently, `nodes_`'s iterator type is also following the concept
[LegacyForwardIterator](https://en.cppreference.com/w/cpp/named_req/ForwardIterator) which is also needed for our `dense_hash_map::iterator` type.
Even better, it actually follows the [LegacyRandomAccessIterator concept](https://en.cppreference.com/w/cpp/named_req/RandomAccessIterator) which is a powerful subset of the **LegacyForwardIterator** concept.

On the other hand, `nodes_`'s iterator type has `node<Key, T>&` as its `reference` type when we need `std::pair<const Key, T>&` for `dense_hash_map::iterator`.
What we need is a projection onto the member `pair` of `node<Key, T>` while iterating over `nodes_`.

#### C++20 in all its splendor:

In an ideal world, we would have a **C++20** compiler shipped with a fully **C++20** compliant standard library. Within it, we would have the [holly range library](https://en.cppreference.com/w/cpp/ranges), which would permit to lazily transform our `nodes_` into another one:

```c++
// ...
class dense_hash_map {
    // ...
    auto begin() {
        return projected_range().begin();
    }

    auto end() {
        return projected_range().end();
    }
    // ...
private:
    auto projected_range() {
        return nodes_ | std::views::transform([](auto& node){ return node.pair; });
    }
    // ...
};
```
The range library has its quirks and limitations as some fervent members of the lost C++ society will point out.
But for this kind of scenario, it is of great help. It is vastly superior to the C++17 solution as we will see.
You can easily implement `cbegin` and `cend` in a similar way: just make your `projected_range` function const.
`std::views::transform` even retains the concept of the range/iterators it is applied to, meaning that iterators it output in our case are still `LegacyRandomAccessIterator`.

In **C++20**, you can easily ensure that your iterator will be compliant using the newly adopted [constraints and concepts features](https://en.cppreference.com/w/cpp/language/constraints). Somewhere in your library, you could forge a `static_assert` such as:

```c++
static_assert(std::random_access_iterator<dense_hash_map_iterator<...>);
```

Let's assume that `std::random_access_iterator` had a **compound requirement** that ensure your iterator has a prefix increment operator as follow:

```c++
template <class It>
concept random_access_iterator = requires(It it) {
    // ...
    { ++it } -> std::same_as<It&>; // Ensure that we can apply `++` to it and that it would return a reference.
    // ...
};
```

If, in a moment of inadvertence, you were to remove that operator, your compiler would gently remind you about it. Here is how **GCC** puts you in the right track:

```txt
note: constraints not satisfied
required by the constraints of 'template<class It> concept random_access_iterator' in requirements with 'dense_hash_map_iterator it'

note: the required expression '++ it' is invalid
    { ++it } -> std::same_as<It&>;
```

C++ concepts are not just for **meta-programming**, it is also an elegant way to test your code with the help of your compiler.
One could also hope that IDEs will in the future provide a convenient way to generate stubs from a concept.
Of course, concepts have their limits when it comes to asserting actual runtime behaviour. Unit-tests are still your best ally for that!

#### The inferior C++17 solution:

As the Lieutenant-Colonel Bear Grylls would say: "the rules of survival never change, whether you're in a desert or in an old C++ project.".
We are left on our own without any ranges at our disposal. We must forge our own iterator type by hand quickly!

While iterators are quite simple to use, writing them can be tedious. One has to scrupulously respect the concept your iterator supports.
So in our case, we must implement all the contrainsts a [LegacyRandomAccessIterator](https://en.cppreference.com/w/cpp/named_req/RandomAccessIterator) has.
Which in turn means implementing all the constraints a [LegacyBidirectionalIterator](https://en.cppreference.com/w/cpp/named_req/BidirectionalIterator) has.
Which in turn means implementing all the constraints a [LegacyForwardIterator](https://en.cppreference.com/w/cpp/named_req/ForwardIterator) has.
Which in turn means implementing... okkkk...ay... you get it. It's a list of constraints that no sane person would remember under normal circumstances.

Another old-school solution to avoid introducing any mistake in your iterator class is to cross-check all the members and free functions related to your class against an iterator of the same concept from a venerable library out there. In our case, we are writing an adaptor to `std::vector`'s iterator. A good candidate for cross-checks could be [libc++'s std::vector](https://github.com/llvm/llvm-project/blob/2f3e86b31818222a0ab87c4114215e86b89c9dfc/libcxx/include/vector#L486) [iterator](https://github.com/llvm/llvm-project/blob/f82dba019253ced73ceadfde10e5f150bdb182f3/libcxx/include/iterator). To do so, you would write unit-tests for all the members function for that iterator then try to apply them onto your own iterator.

/!\ Important note - I would strongly advise NOT TO COPY-PASTE from a library for various reasons:

1. You could easily fall into plagiarism and all the legal issues around it.
2. Your library probably does not have all the constraints a standard library has (naming, compatibilities...).
3. You will not learn much out of it.


Given that **C++20** is not fully mature in all major compilers, I went for the tedious **C++17** solution. Thus was born [dense_hash_map_iterator](https://github.com/Jiwan/dense_hash_map/blob/d80d3da01d9981154e78ea85b3135b4a66a150a3/include/jg/details/dense_hash_map_iterator.hpp#L13).

My iterator class takes 5 templates parameters:

```c++
template <class Key, class T, class Container, bool isConst, bool projectToConstKey>
class dense_hash_map_iterator {
// ...
};
```

The three first template parameters are rather obvious, it handles which `Key` / `T` pairs we will deal with and which `Container` type stores them.
The last two template parameters are here to kill multiple birds with one stone. Our iterator class will both represent `iterator` and `const_iterator` by setting the first parameter `isConst`. It also gives you the choice on which version of [the Schrodinger std::pair]({filename}../C++/dense-hash-map-part-2.md) we want to project onto with the `projectToConstKey` parameter.

Afterwards we can start to define some important **usings** we can re-use within our class: 

```c++
class dense_hash_map_iterator {
    // ...
    using projected_type = std::pair<
        std::conditional_t<            // Which version of the Schrodinger pair we want.
            projectToConstKey,         
            const Key,                 // We want the one with an immutable key.
            Key                        // We want the one with an mutable key that can be move around.
        >, 
        T
    >;
    
    using sub_iterator_type = std::conditional_t<    // Choose the underlying iterator type we want to work on: const or non-const.
        isConst, 
        typename Container::const_iterator, 
        typename Container::iterator
    >;

    using value_type = std::conditional_t<      // The value type our iterator will return depends on:
        isConst,                                // <== The constness of our iterator `isConst`.
        const projected_type,                   // <== The version of the Schrodinger pair we choose `projected_type`.
        projected_type
    >;

    using reference = value_type&;
    using pointer = value_type*;
    // ...
};
```

Our usings form, in some way, a matrix of all iterator types we can get from the class template `dense_hash_map_iterator`. As the output of the matrix is the `value_type` type we will return and sub-iterator type `sub_iterator_type` we will work on. Writing the rest of the `dense_hash_map_iterator` becomes a rather boring task where almost every single calls gets forwarded to a `sub_iterator_` member. Here is a very mundane implementation of the prefix increment operator:

```c++
class dense_hash_map_iterator {
    // ...
    dense_hash_map_iterator() noexcept // Our main constructor that takes the sub-iterator we will project from.
        : sub_iterator_(sub_iterator_type{}) {} 

    auto operator++() noexcept -> dense_hash_map_iterator&
    {
        ++sub_iterator_;   // Increment our sub-i... zZZzz zzZZZzzzzz
        return *this;
    }

private:
    sub_iterator_type sub_iterator_; // Our sub iterator member.
};
```

I can predict that you are already virtually yawning at the idea of implementing the rest of this class. So instead of doing a long and monotonous listing of all these member functions, here are the "highlights" you should look for.

** [Some conditional operators](https://github.com/Jiwan/dense_hash_map/blob/d80d3da01d9981154e78ea85b3135b4a66a150a3/include/jg/details/dense_hash_map_iterator.hpp#L52) **

Given that `value_type`, `reference` and `pointer` depend on `projectToConstKey`, all the members functions (operator*, operator[], operator->) returning one of these types need to adapt their body to `projectToConstKey`. Our beloved `if constexpr` is back at it:

```c++
auto operator*() const noexcept -> reference // As soon as we observe the Schrodinger pair...
{
    if constexpr (projectToConstKey) {       // ... its state quantum state gets resolved. 
        return sub_iterator_->pair.const_key_pair();
    } else {
        return sub_iterator_->pair.pair();
    }
}
```

This will correctly dispatch to the correct version of [the Schrodinger std::pair]({filename}../C++/dense-hash-map-part-2.md) at compile time.
I am really glad that we do not rely on [SFINAE]({filename}../C++/sfinae-introduction.md) for these constructions.

** [A conversion constructor](https://github.com/Jiwan/dense_hash_map/blob/d80d3da01d9981154e78ea85b3135b4a66a150a3/include/jg/details/dense_hash_map_iterator.hpp#L47) **

It is very handy to be able to assign an `iterator` to a `const_iterator` but not the other way around. The magic recipe behind such mechanisms consists in writing a rather awkward constructor:

```c++
template <bool DepIsConst = isConst, std::enable_if_t<DepIsConst, int> = 0>
                                                      // ^^^ Only if isConst is true....
dense_hash_map_iterator(const dense_hash_map_iterator<Key, T, Container, false, projectToConstKey>& other) noexcept
    : sub_iterator_(other.sub_iterator_)                                // ^^ ... we have a constructor that take non-const iterator.
{}
```

Once again, the absence of **C++20** can be felt here. We want this constructor to be available only when `isConst` is `true`: in other words only a `const_iterator` has this extra constructor. In **C++20**, a well-placed [requires clause](https://en.cppreference.com/w/cpp/language/constraints#Requires_clauses) would conditionally enable that constructor. But in **C++17** we have to resort to an disgusting **SFINAE** trick using [std::enable_if_t](https://en.cppreference.com/w/cpp/types/enable_if). To make the matter uglier, [the complicated rules of template substition](https://stackoverflow.com/questions/14603163/how-to-use-sfinae-for-selecting-constructors) forces us to have the somewhat useless default argument `DepIsConst` instead of using `isConst` directly.


** [Some external operators](https://github.com/Jiwan/dense_hash_map/blob/d80d3da01d9981154e78ea85b3135b4a66a150a3/include/jg/details/dense_hash_map_iterator.hpp#L133) **

If you want to benefit from your conversion constructor within all your operators of arity 2 (operator==, operator<...), you must be careful on how to craft those. You have different options here: members, non-members, friends, non friends, template or not template... I find [Natasha Jarus explanations on the subject](https://web.mst.edu/~nmjxv3/articles/templates.html) pretty good.

I opted for the option ["give access to a const reference of my sub-iterator to everyone"](https://github.com/Jiwan/dense_hash_map/blob/d80d3da01d9981154e78ea85b3135b4a66a150a3/include/jg/details/dense_hash_map_iterator.hpp#L126), including my operators defined as free functions. It avoids a creating a cluster-fudge of forward declarations and `friend`s at the price of exposing my private parts. No fame, no shame as they say!

##### A quick note for some detractors:

Our beautiful **C++20** solution expressed in few expressive lines, became 207 lines of pure... iterator chaos. Certainely, ranges, concepts or coroutines can do more harm than good [under some circumstances](https://aras-p.info/blog/2018/12/28/Modern-C-Lamentations/), but entirely discarding their usage due to these limitations is not a smart move either. They do bring a lot of value as clearly shown here!

### local iterator - a forward iterator without glamor:

I hate this name. For the users it is probably used to debug the map.

<center><img width=50% height=50% src="{filename}/images/dense-hash-map-local-iterator.webp" alt=""/></center>

`ForwardIterator`


## A special constructor for allocators:


In the C++ lore, we have another 

<center><img width=40% height=40% src="{filename}/images/gladiator.jpg" alt="Gladiator"/></center>


## Conclusion:

We survived this first day of our journey! We can control the growth of our container using a policy pattern.
We also have a **Schrodinger std::pair** at our disposal to move our key/value pairs blazingly fast accross memory while preventing our users to shoot themselves in the feet.

Be ready for the next phase: the dreaded iterators and allocators are waiting for you!
