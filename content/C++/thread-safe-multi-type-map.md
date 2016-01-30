Title: An introduction to C++'s variadic templates: a thread-safe multi-type map
Date: 14:00 02-01-2016 
Modified: 14:00 02-01-2016
Tags: C++11, C++14, variadic templates, meta programming
Slug: thread-safe-multi-type-map

### Trivia:
One of our favorite motto in our C++ team at work is: you shall use **dependency injections** instead of **singletons**! It actually comes with our unit-testing strategy. If the various components of your architecture are too tightly coupled, it becomes a tremendous effort to deeply test small critical chunks of your code. **Singletons** are that kind of beast that revives itself without your permission and comes from hell to haunt your lovely unit-tests. Our main project being multi-threaded (hence highly bug-prone) and vital for the company, "**singleton**" became a forbidden word. Yet, our team recently started going down the dark path. Thanks to C++11 and its variadic templates, I carefully crafted a **thread-safe multi-type map container** that simplified our configuration reloading system and saved us from the dark side of the coder force. If you always wondered what are **variadic templates**, how **C++11's tuples** can be implemented, I am going to present these concepts in this post using my container as a cobaye.

Note: for the sake of your sanity and the fact that *errare humanum est*, this article might not be 100% accurate!

### Why would I use a thread-safe multi-type map?
Let me explain our odyssey: we are working on a highly modular and multi-threaded application. One of its core feature is the ability to reload various configuration files or assets used by some components spread accross many threads and a giant hierarchy of objects. The reloading process is automic using Linux's [inotify](http://man7.org/linux/man-pages/man7/inotify.7.html) monitoring filesystem events. One thread is dedicated to the reception of filesystem events and must react accordingly by parsing any changes and pushing them to other threads. At first, we used, to pass-by any newly parsed asset, some thread-safe **queues** or something analog to [go channels](https://tour.golang.org/concurrency/2). Since we did not want to use **singletons**, we had to pass references to our queues all along our object hierarchy. Sadly, our **queue** implementation is **one to one** and supports only **one type**, none of our config/asset types share the same **base-type**. For each asset type and each component using this asset, we had to create a new **queue** and pass-it all along our hierarchy. That is certainely not convenient! What we really wanted was a hybrid class between a [std::map](http://en.cppreference.com/w/cpp/container/map) and a [std::tuple](http://en.cppreference.com/w/cpp/utility/tuple).

We could have used a **std::map** with [Boost.Variant](http://www.boost.org/doc/libs/1_60_0/doc/html/variant.html) to store our items, using a type like the following **"std::map< std::string, std::shared_ptr< Boost.Variant < ConfigType1, ConfigType2>>>"**. **Boost.Variant** permits to encapsulate a **heterogeneous set of types** without **common base-type or base-class**, which solves one of our point. Another solution would be to encapsulate manually all our configuration classes in the same familly of classes, that is pretty cumbersome. But anyway, **std::map** does not guaranty any safety if you are writing and reading at the same time on a map slot. Secondly, **std::shared_ptr** does guaranty a thread-safe destruction of the pointee object (i.e: the reference counter is thread-safe) but nothing for the **std::shared_ptr** object itself. It means that copying a **std::shared_ptr** that could potentially be modified from another thread, might lead to an undefined behaviour. Even if we were to encapsulate all these unsafe access with mutexes, we are still lacking a nice mechanism to get update notifications for our objects. We do not want to constantly poll the latest version and propagate it through our code. And finally, if that solution were elegant enough, why would I currently write this blog post?

**C++11** brings another collection type called **std::tuple**. It permits to store a set of elements of **heterogeneous types**. Take a look at this short example:
	
	:::c++
	auto myTuple = std::make_tuple("Foo", 1337, 0xb0b);

    std::cout << std::get<0>(myTuple) << std::endl; // Access element by index: "Foo"
    std::cout << std::get<1>(myTuple) << std::endl; // Access element by index: 1337
    std::cout << std::get<const char*>(myTuple) << std::endl; // Access element by type: "Foo"

    // compilation error: static_assert failed "tuple_element index out of range"
    std::cout << std::get<3>(myTuple) << std::endl;

    // compilation error: static_assert failed "type can only occur once in type list"
    std::cout << std::get<int>(myTuple) << std::endl;

**Tuples** are that kind of **C++11** jewelry that should decide your old-fashioned boss to upgrade your team's compiler (and his ugly tie). Not only I could store a **const char* ** and two **ints** without any compiling error, but I could also access them using compile-time mechanisms. In some way, you can see tuples as a compile-time map using indexes or types as keys to reach its elements. You cannot use an index out of bands, it will be catched at compile-time anyway! Sadly, using a type as a way to retrieve an element is only possible if the type is unique in the **tuple**. In my work project, we do have few config objects sharing the same class. Anyway, tuples weren't feeting our needs regarding thread safety and update events. Let's see what we could create using tasty **tuples** as an inspiration.

Note that some **tuples** implementations were already available before **C++11**, notably in [boost](http://www.boost.org/doc/libs/1_60_0/libs/tuple/doc/tuple_users_guide.html). **C++11** variadic templates are just very handy, as you will see, to construct such class.

### A teaser for my repository class:
To keep your attention for the rest of this post, here is my **thread-safe multi-type map** in action:

First and foremost, its name **repository** might not be well-suited for its responsibility. If you native language is the same as shakespeare and come-up with a better term, please feel free to submit it. In our internal usage, **config repository** sounded great!

As you can see, I am using types as a key for accessing elements in this **repository**. In case of contetion, I use two keys...
. I use **std::shared_ptr** for . We will see later on why. 

Show how we use it: class ConfigA, class ConfigB, passed in a context along the hierarchy class.
