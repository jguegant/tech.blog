Title: How to make your maps, try_emplace and unique_ptrs play nicely with each others in C++.
Date: 14:00 17-11-2018 
Modified: 14:00 17-11-2018 
Tags: C++17, std::map, std::unordered_map. 
Slug: performing-try-emplace 

## Trivia:
Lately, I have been working on the reincarnation of a **class** at work: a hash map. 
While this class had interesting internals (a sort of dense hash map) and performed really well, its interface was not up to standard both literaly and metaphorically.
After much of lipstick applied to it, the **class** now fully mimic the interface of the beloved [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map) from the standard library.
A close look on `std::unordered_map` and its sister [std::map](https://en.cppreference.com/w/cpp/container/map) reveals few interesting design choices.
Combining this interface with some smart pointer types can present some challenges to squeeze performance out of your maps.
We will explore these challenges in this blog post, and try to figure out some solutions.

Disclaimer: C++ being C++, I would not be suprise if 1) I wrote some unacurracies here 2) Some guru could reduce this entire article in a phantasmagoric one liner.

### Some peculiar modifier member functions:


Note: This part of the post will serve as a reminder for some of the folks that are not well versed in the **associative containers** of the standard. If you are confident, you can always jump straight to the dilemma part. 

<center><img width=25% height=25% src="{filename}/images/container-ship.png" alt="A container"/></center>

#### insert:
If you observe the interface of the **associative containers** (like [std::map](https://en.cppreference.com/w/cpp/container/map) or [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map)) in the current standard you will notice that there are 6 member functions to map a value to a given key: `insert`, `insert_or_assign`, `emplace`, `emplace_hint`, `try_emplace` and the **subscript operator** (operator[]). That number does not include all the overloads for each of these member functions. It is not a wonder that a lot of C++ users will tend to do suboptimal calls to insert values in their **associative containers**, the choice is not always obvious when you have 6 different functions with slightly different behaviour. 


Typically, you will often this pattern within a code-base:
```c++
std::unordered_map<std::string, std::string> m;

// Check if the key is already in m.
if (m.find("johannes") == m.end()) { // Often written as m.count("johannes") == 0
	m["johannes"] = "lucio"; // If not insert they key
}
```

Little did your colleague, boss, or tired ego know that such a code will do twice a relatively costly job: checking the existence of the key in the map.
Indeed, in the case of a `std::unordered_map`, the key `"johannes"` will be hashed twice: in `find` and in the `operator[]`. In both member functions, the `std::unoredered_map` has to know in which bucket the key will fall into. Worst! If you are having collisions between your keys, checking the existence of a key may induce up to N comparisons (even your hash function can be drunk sometimes) where N is the amount of stored key-value pairs. Potentially mutiplying these comparisons by two is not something you should desire. Such a situation in `std::map` is even worst, this will always bring roughly O(log(N)) comparisons. Comparing two keys may not always be as cheap as it seems and if you add on top of that the cost of jumping through a linked list of nodes, this should be considered harmful.

Obviously the answer to this problem is to use [insert](https://en.cppreference.com/w/cpp/container/map/insert). `insert` as its name implies, will only work if it can insert the key in the **associative container**, meaning that the insertion will not happen if the same key is already in the map. If you really care to know whether the insertion happend, `insert` will return a `pair` of an iterator and a boolean that you can query. The iterator points to the newly inserted key-value pair or the already existing one, the boolean indicates whether the insertion happened or not.
```c++
// Use C++17 structured bindings and class template argument deduction (CTAD)
// See more on my previous post on that topics
auto [it, result] = m.insert(std::pair("johannes", "lucio")); // Construct a pair and insert it if needed.
// Do whatever you want with it and result.
```
Here only one check for the existence will be done, that is much better, isn't it?
Well, while this snippet is shorter and performs better, there is still room for improvement.
Here we are constructing a `pair` out of the map, the same `pair` that needs to be created in a node of the `map`.
Internally a call to the **move-constructor** of the `pair` will be done, or way worst a call to the **copy-constructor** if one of the two types in the `pair` cannot be moved.
Relying on the **move-constructor** of a `pair` to exist AND to be performant is too much of a wishful thinking. 

#### emplace:
Thanksfully, C++11 added on many containers a new member function called [emplace](https://en.cppreference.com/w/cpp/container/map/emplace). Given a container of type `T`, `emplace` will accept the arguments necessary for an in-situ construction of a new instance of `T`. Meaning that we can easily improve our insertion in this way: 
```c++
auto [it, result] = m.emplace("johannes", "lucio"); // Construct the pair of "johannes", "lucio" straight into m.
```
I will go slightly against [abseil's recommendation](https://abseil.io/tips/112) and say that `emplace` should be prefered over `insert` in **C++11** for at least all the **associative containers**. It will perform better (as explained previously) and it also feels more natural (most users think of a key and a value, not a std::pair)! 

Now `emplace` on **associative containers** has a vicious specification which [cppreference gently warns you about](https://en.cppreference.com/w/cpp/container/map/emplace). For some obscure reasons, even if the **emplace operation** does not succeed since the key already exists, your arguments passed as a **r-value** may have been moved anyway.
More vaguely, the standard mandates effects only on whether the insertion will happen or not and the return value:
```text
Effects: Inserts a value_­type object t constructed with std::forward<Args>(args)... if and only if there is no element in the container with key equivalent to the key of t.
The bool component of the returned pair is true if and only if the insertion takes place, and the iterator component of the pair points to the element with key equivalent to the key of t.
```
This cryptic language-lawyer text does not explain in any way what happens to the arguments in the case of failure. For what we know, they could be sent over smoke signal up to Hong-Kong and inserted into some fortune cookies. Why would we care about that? Well, because that will restrain you to write such code:

```c++
std::unordered_map<std::string, std::unique_ptr<int>> m;
auto my_precious_int = std::make_unique<int>(42);

auto [it, result] = m.emplace("ricky", std::move(my_precious_int)); // We need to move unique pointers.

if (!result) { // Alright the insertion failed, let's do something else with my_precious_int.
	do_something_else(*my_precious_int); // Or can we?
}
``` 
Here `my_precious_int` is unusable right after the call to `emplace`, it may have been moved-from forever and ever, **EVEN** if the insertion result is `false`.
Some confused souls will tell you that this is evident, we called `std::move`, so it MUST be moved-from. Like the famous cake, `std::move` is a lie! It does not move anything, it simply casts objects to **a x-value** which makes them POTENTIALLY moveable-from (this world would have been better if `std::move` was named `std::to_xvalue`, `std::moveable`, `std::to_be_moved`...).

#### try_emplace:
This unleashed `emplace` is a real pain when you are trying to store move-only types in any **associative container**.
The standard committee was aware of the issue and fixed it in **C++17** with another member function called [try_emplace](https://en.cppreference.com/w/cpp/container/map/try_emplace§).
Here are the expected effects:
```text
Effects: If the map already contains an element whose key is equivalent to k, there is no effect.
Otherwise inserts an object of type value_type constructed with piecewise_construct, forward_as_tuple(std::move(k)), forward_as_tuple(std::forward<Args>(args)...).
```
It effectively prevents your arguments to be moved-from (as well as being packaged into fortune cookies) in the case of an insertion failure.
Why wasn't `emplace` simply patched?
If you take a look at the definition of [emplace](https://en.cppreference.com/w/cpp/container/map/emplace§), you will understand that it accepts as a key argument any object with a **type compatible** with your **key type**.
Unlike the value argument, the key argument ALWAYS need to be somehow converted to the **key type** to check for its existence in the map.
The potential conversion would defeat the "there is no effect" policy. 
`try_emplace` is stricter and only takes a key of type **key type**, which guarantees that no conversion sequence will be triggered.
At least `try_emplace` can help us to safely rewrite the previous example:
```c++
std::unordered_map<std::string, std::unique_ptr<int>> m;
auto my_precious_int = std::make_unique<int>(42);

auto [it, result] = m.try_emplace("ricky", std::move(my_precious_int)); // We need to move unique pointers.

if (!result) { // Alright the insertion failed, let's do something else with my_precious_int.
	do_something_else(*my_precious_int); // It is safe! 
}
``` 


Hurray! After three corrections in the standard, we can effectively mix associative containers with `unique_ptrs` for a maximum of fun and profit!
Well... no. **C++ being C++**, it cannot be that easy. There is one last boss to slain.

### The last dilemma of a map of unique_ptrs:


<img width=20% height=20% style="float: right;" src="{filename}/images/dilemma.jpg" alt="A container"/>

Before I start on this topic, I would like to remind everyone a basic rule: you should try to avoid heap allocations.
You should always strive to get a `std::map<T1, T2>` over a `std::map<T1, std::unique_ptr<T2>>`.
Now that being said, you may have situations where you cannot do otherwise:

- If you need runtime polymorphism. For instance, you may need to store services into a `std::map<std::string, std::unique_ptr<service>>` where `service` is an interface with multiples concrete implemetations. Although, there are always ways to hide the inheritance as explained by [Sean Parent](https://www.youtube.com/watch?v=QGcVXgEVMJg)... 
- If your weapon of choice is a map following closely the interface of `std::unordered_map` or `std::map` minus the stable addressing part of it.
This is often the case for all the hash map with excellent performance, like [skarupe's one](https://github.com/skarupke/flat_hash_map/blob/master/flat_hash_map.hpp).
Not having stable addressing means that querying the address of a value in the map `&map["jeremy"]` might give you different results if you do any modifying operations (insert, erase...) on the map. In such case, having an extra indirection (heap allocation) will bring back stable addressing. 


Not only dealing with pointers (even smart ones) is often tedious, but it can also ruin the `try_emplace` member function of your class.
You will have to choose between a costly object creation or the dreaded double key lookup I mentioned right at the beggining of this post. 
Pick your poison!


#### Uncessary object creation or double key lookup:

Let's keep the idea of a map of services: `std::map<std::string, std::unique_ptr<service>>`, and you would like to register a service "file_locator" only if there was none registered earlier.
Hastily, you may write such code:
```c++
std::map<std::string, std::unique_ptr<service>> m;
// ...

// Create a file locator that explore a file system on a remote server.
// remote_file_locator implements the service interface.
auto [it, result] = m.try_emplace("file_locator", std::make_unique<remote_file_locator>("8.8.8.8", "/a_folder/"));

if (!result) {
	// Print which file_locator is already in there. 
	log("Could not register a remote_file_locator, it has been overridden by: ", it->second.name());
}
```
If the `remote_file_locator` is successfully registered, everything is fine!
But in the other scenario where a `file_locator` is already in the map, this code has a huge pessimisation.
Here your compiler will emit code that allocate enough memory for a `remote_file_allocator`, then it will construct it, under any circumstances.
If allocating can be seen as slow in the C++ world, starting a connection to a server is pure hell when it comes to speed.
If you are not planning to use the instance of this really costly object, why would you create it in the first place?

So shall we revert to the double lookup?

```c++
auto it = m.find("file_locator");
if (it == m.end()) {
	m["file_locator"] = std::make_unique<remote_file_locator>("8.8.8.8", "/a_folder/");
} else {
	log("Could not register a remote_file_locator, it has been overridden by: ", it->second.name());
}
```
Hell no! I already explained why I discourage you to use such a pattern in the first part of this post.
You could argue that here we will only pay this double lookup overhead only once, when we try to create the "remote_file_locator".
Given more time and coffee, I should be able to come up with an architecture where you could do such insertions of unique_ptrs in a loop.
In any case, C++ is all about not paying in performance for uncessary things. 

But don't worry, C++ being C++, there surely are ways to get around this impediment.

#### Two clumsy solutions:

I, personally, could come up with two solutions. If you have a better one, you are welcome to express it in the comments.

The first one is actually not so hacky. You can start by trying to emplace an empty `unique_ptr`, if the insertion works you can always fix it afterwards with a real allocation:
```c++
// Try to emplace an empty `unique_ptr` first.
auto [it, result] = m.try_emplace("file_locator", nullptr);

if (result) {
	// The insertion happened, now we can safely create our remote_file_locator without wasting any performance. 
	it->second = std::make_unique<remote_file_locator>("8.8.8.8", "/a_folder/");
}
```

I somehow dislike this solution. It is not consistent with the usage of `try_emplace` on more classic types, which do not require any extra step. 
It really smells like some kind of two-phases initialisation pattern which are usually frowned upon.
We are temporarily putting our map into a state where "file_locator" cannot be trusted. What if the actual creation of the `remote_file_locator` throws an exception?
That would leave the map with a empty "file_locator", that's not great.

My second solution consists in trying to delay the construction of the `remote_file_locator`.
To do so, I wrote a very simple helper struct that I called `lazy_convert_construct`.
This struct wraps any kind of lambda that acts like factory: the **lambda factory** returns an instance of a given type, `"result_type"`, when called.
If at any point the struct needs to be converted to `result_type`, it will call the internal lambda to generate an instance of `result_type`.
Any code should speaks for itself, so here is the `lazy_convert_construct` beast in all its beauty:
```c++
template<class Factory>
struct lazy_convert_construct
{
	using result_type = std::invoke_result_t<Factory>; // Use some traits to check what would be the return type of the lambda if called.
	
	constexpr lazy_convert_construct(Factory&& factory) 
		: factory_(std::move(factory)) // Let's store the factory for a latter usage.
	{
	}
	
	//                                     ↓ Respect the same nowthrow properties as the lambda factory.
	constexpr operator result_type() const noexcept(noexcept(std::declval<Factory>()())) 
	//		  ^ enable       ^ the type this struct can be converted to 
	//          conversion
	{
		return factory_();	// Delegate the conversion job to the lambda factory.
	}

	Factory factory_;
};

// Example of usage:
auto l = lazy_convert_construct([]{ return 42; });
//		  ^ CTAD again					  ^ Factory lambda that returns an int.
int x = l;
//		^ Here l is forced to be converted to an int and will therefore call the lambda to do so.
std::cout << x; // Prints 42. 
```

Note that the lambda will not be called if there is no conversion needed, this makes it having a [lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation).
Note also: after turning all optimisations on, the `lazy_convert_construct` entirely disappears and x will be simply initialised by 42 when needed. 

The next step is to combine this `lazy_convert_construct` with `try_emplace`, which works like a charm:

```c++
auto [it, result] = m.try_emplace("file_locator", lazy_convert_construct([]{ return std::make_unique<remote_file_locator>("8.8.8.8", "/a_folder/"); }));
```

`lazy_convert_construct` is now able to create a `unique_ptr<remote_file_locator>` on-demand. Even with `lazy_convert_construct`, `try_emplace` will respect its contract: it will not have any side effect on the `lazy_convert_construct` object if the key `"file_locator"` is already present. Meaning that no conversion will happen if the key already exists.
This rather elegant solution fixes one of the main drawback of the previous one: it never leaves the map in a state with a `file_locator` being null.
It is also a one liner!

#### Benchmark results:

Some of you may still be a bit skeptical on the importance of optimising your queries in your associative containers.
So I wrote a very simple benchmark which explores multiple insertion scenarios on a `std::map<std::string, std::unique_ptr<T>>`.
You can fetch it [here](https://github.com/Jiwan/benchmarks_map_insertion).

Using clang 6.0 on my Linux laptop, I obtain the following results:
```text
2018-11-18 14:16:17
Running ./fast_try_emplace
Run on (8 X 3600 MHz CPU s)
CPU Caches:
  L1 Data 32K (x4)
  L1 Instruction 32K (x4)
  L2 Unified 256K (x4)
  L3 Unified 8192K (x1)
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
-----------------------------------------------------------------------------
Benchmark                                      Time           CPU Iterations
-----------------------------------------------------------------------------
insertion_double_lookup                      636 ns        638 ns    1085075
insertion_construct_before_try_emplace       503 ns        506 ns    1387818
insertion_lazy_convert_try_emplace           503 ns        506 ns    1380488

no_insertion_double_lookup                   107 ns        107 ns    6300180
no_insertion_construct_before_try_emplace   8642 ns       8641 ns      80478
no_insertion_lazy_convert_try_emplace         32 ns         32 ns   22393508
```
Clearly, a sucessful insertion using the double lookup is more expensive than it should. The cost will change depending on the amount of **key-value pairs** already in the map.
For a failed insertion scenario, my `lazy_convert_construct` is also faster than the double lookup. I cannot explain why! Internally, `find` and `try_emplace` should have the same lookup mechanims.
And of course, creating a costly object and destroying right after is really bad choice. That explains why `no_insertion_construct_before_try_emplace`'s record is so damn huge compared to the two others cases (I purposely made the type very costly to create for the no insertion cases).


GCC offers similar results, without the mysterious advantage of the `try_emplace` + `lazy_convert_construct` over the double lookup in a no insertion scenario.
```text
2018-11-18 14:17:53
Running ./fast_try_emplace
Run on (8 X 3600 MHz CPU s)
CPU Caches:
  L1 Data 32K (x4)
  L1 Instruction 32K (x4)
  L2 Unified 256K (x4)
  L3 Unified 8192K (x1)
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
-----------------------------------------------------------------------------
Benchmark                                      Time           CPU Iterations
-----------------------------------------------------------------------------
insertion_double_lookup                      547 ns        543 ns    1310711
insertion_construct_before_try_emplace       493 ns        496 ns    1394343
insertion_lazy_convert_try_emplace           495 ns        500 ns    1000000

no_insertion_double_lookup                    44 ns         44 ns   15787599
no_insertion_construct_before_try_emplace   8659 ns       8658 ns      78869
no_insertion_lazy_convert_try_emplace         44 ns         44 ns   15895884
```

Now we can proudly claim that we solved all the insertion issues (at least those that I am aware of).
But somehow it still feels like something is off with the smart pointer types of the standard library.
Are we missing something here?

#### An in_place constructor:

Warning: here you will enter the somehow controversial and imaginary part of my post. I am not claiming that this is the direction **C++** should take on these issues, but merely raising my questions on that topic. 



Indeed, `unique_ptr` and its other smart pointers counsins (`shared_ptr`...)  are rather special types.
On one hand you could see them as simple RAII wrappers that take care of a basic resource: a pointer. 
On the other hand, you could, __very arguably__ (<== note this bold statement), see them as some funky **value wrappers** with a very special storage (one that implies pointer semantics). 

**Value wrappers** are types that enhance the property of another type(s). The most recent ones in the standard are: [std::optional](https://en.cppreference.com/w/cpp/utility/optional), [std::variant](https://en.cppreference.com/w/cpp/utility/variant) and [std::any](https://en.cppreference.com/w/cpp/utility/any). 
As expected, all of these new **value wrappers** have constructors that accepts an instance of the type they are wrapping:
```c++
struct A {
    A(int args1, std::vector<int> args2) { /* do some with the args */}
};

// Move construct the newly created A into o.
std::optional o(A{42, std::vector<int>{42}});
``` 

While such constructors might be sufficient for most of the usages of your **value wrappers**, sometimes you really want to avoid any move or copy constructors.
The standard committee was proactive and provided another set of constructors to build the wrapped value **in-place**.
In order to disambiguate with the usual constructors, these new constructors take as a first argument a [tag type](https://www.fluentcpp.com/2018/04/27/tag-dispatching/): [std::in_place](https://en.cppreference.com/w/cpp/utility/in_place) or [std::in_place_type](https://en.cppreference.com/w/cpp/utility/in_place). Here is how `std::in_place` works with `std::optional`:
```c++
//            ↓ No CTAD            ↓ The arguments needed for constructing a new instance of A.
std::optional<A> o(std::in_place, 42, std::vector<int>{42});
//                   ^ dispatch to in place constructor.
``` 
With such a constructor, we can safely assume that the wrapped instance of `A` was built directly in its storage place.
Of course, you can also use this constructor if you are dealing with `map::try_emplace`:
```c++
std::map<std::string, std::optional<A>> m;
m.try_emplace("bruno", std::in_place, 42, std::vector<int>{42});
//						     ^ Will construct the wrapped A deep down in the map.
```


At this point, if you are following my anology between `std::unique_ptr` and **value wrappers**, you could start to question yourself on why we could not get a similar set of constructors for our smart pointers. Maybe something similar to this:
```c++
std::unique_ptr<service> x{std::allocate_in_place<remote_file_locator>, 42, std::vector<int>{42}};
//							^ tag                   ^ concret instance   ^ following args.
```
I intentionally chose a different **tag type** than `std::in_place` for two reasons:

- This constructor is doing more than constructing in place, it does allocate. The user should be informed.  
- In a similar fashion to [std::in_place_type ](https://en.cppreference.com/w/cpp/utility/in_place), we somehow need to encode the concret type we want to instantiate.

With such a constructor in the standard for `unique_ptr`, our issue with `try_emplace` would become trivial to solve. Just call it!

```c++
auto [it, result] = m.try_emplace("file_locator", std::allocate_in_place<remote_file_locator>, "8.8.8.8", "/a_folder/");
```

The constructor of `unique_ptr` that accept the tag `allocate_in_place` would be called only if only the key "file_locator" is not in there.
No overhead, simple syntax,  you could not ask for more!

As a side effect,  my guess is that we could also fully deprecate the usage of `make_unique` and `make_shared`:
```c++
// Before:
auto x = std::make_shared<something>("michel", "christian");
// After
auto x = std::shared_ptr(std::allocate_in_place<something>, "michel", "christian"); 
```

Obviously the syntax is far from being **terse**. The invented feature also does not take in consideration the **allocator arguments** you could receive in a smart pointer.
Me and a colleague promised ourselves to look a bit more into this topic. Whether we will formulate a proposal or just have some afterthoughts, be sure that I will let you informed on that in a further post! 

### Conclusion:

- If you are inserting a new pair into an **associative container** consider using `try_emplace` first.
- If you cannot use **C++17**, prefer to use `emplace` over `insert`.
- If you are cannot use **C++11**, I feel sorry for you!
- You can borrow my `lazy_convert_construct` if you are dealing with smart pointers and `try_emplace`, to get a blazzing fast insertion.

A special thanks to my colleague Yo Anes with whom I had a lot of fun discussing this specific topic.
