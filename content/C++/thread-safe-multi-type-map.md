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
	auto myTuple = std::make_tuple("Foo", 1337, 42);

    std::cout << std::get<0>(myTuple) << std::endl; // Access element by index: "Foo"
    std::cout << std::get<1>(myTuple) << std::endl; // Access element by index: 1337
    std::cout << std::get<2>(myTuple) << std::endl; // Access element by index: 42
    std::cout << std::get<const char*>(myTuple) << std::endl; // Access element by type: "Foo"

    // compilation error: static_assert failed "tuple_element index out of range"
    std::cout << std::get<3>(myTuple) << std::endl;

    // compilation error: static_assert failed "type can only occur once in type list"
    std::cout << std::get<int>(myTuple) << std::endl;

**Tuples** are that kind of **C++11** jewelry that should decide your old-fashioned boss to upgrade your team's compiler (and his ugly tie). Not only I could store a **const char* ** and two **ints** without any compiling error, but I could also access them using compile-time mechanisms. In some way, you can see tuples as a compile-time map using indexes or types as keys to reach its elements. You cannot use an index out of bands, it will be catched at compile-time anyway! Sadly, using a type as a key to retrieve an element is only possible if the type is unique in the **tuple**. In my work project, we do have few config objects sharing the same class. Anyway, tuples weren't feeting our needs regarding thread safety and update events. Let's see what we could create using tasty **tuples** as an inspiration.

Note that some **tuples** implementations were already available before **C++11**, notably in [boost](http://www.boost.org/doc/libs/1_60_0/libs/tuple/doc/tuple_users_guide.html). **C++11** variadic templates are just very handy, as you will see, to construct such a class.

### A teaser for my repository class:
To keep your attention for the rest of this post, here is my **thread-safe multi-type map** in action:

    :::c++

    #include <iostream>
    #include <memory>
    #include <string>

    #include "repository.hpp"

    // Incomplete types used as compile-time keys.
    struct Key1;
    struct Key2;

    // Create a type for our repository.
    using MyRepository = Repository
        <
            RepositorySlot<std::string>, // One slot for std::string.
            RepositorySlot<int, Key1>, // Two slots for int.
            RepositorySlot<int, Key2> // Must be differentiate using "type keys" (Key1, Key2).
        >;

    int main()
    {
        MyRepository myRepository;

        myRepository.emplace<std::string>("test"); // Construct the shared_ptr within the repository.
        myRepository.emplace<int, Key1>(1337);
        myRepository.set<int, Key2>(std::make_shared<int>(42)); // Set the shared_ptr manually.

        // Note: I use '*' as get returns a shared_ptr.
        std::cout << *myRepository.get<std::string>() << std::endl; // Print "test".
        std::cout << *myRepository.get<int, Key1>() << std::endl; // Print 1337.
        std::cout << *myRepository.get<int, Key2>() << std::endl; // Print 42.

        std::cout << *myRepository.get<int>() << std::endl;
        //             ^^^ Compilation error: which int shall be selected? Key1 or Key2?

        auto watcher = myRepository.getWatcher<std::string>(); // Create a watcher object to observe changes on std::string.
        std::cout << watcher->hasBeenChanged() << std::endl; // 0: no changes since the watcher creation.

        myRepository.emplace<std::string>("yo"); // Emplace a new value into the std::string slot.
        std::cout << watcher->hasBeenChanged() << std::endl; // 1: the std::string slot has been changed.

        std::cout << *watcher->get() << std::endl; // Poll the value and print "yo".
        std::cout << watcher->hasBeenChanged() << std::endl; // 0: no changes since the last polling.

        return EXIT_SUCCESS;
    }


First and foremost, its name **repository** might not be well-suited for its responsibility. If your native language is the same as shakespeare and come-up with a better term, please feel free to submit it. In our internal usage, **config repository** sounded great!

I start by describing the slots necessary for my application by creating a new type **MyRepository** using a [type alias](http://en.cppreference.com/w/cpp/language/type_alias). As you can see, I use the type of the slots as a key for accessing elements. But in case of contention, I must use a second key: an "empty type" ; like **Key1** and **Key2** in this example.
If using types as keys seems odd for you, fear not! Here is the most rational explanation I can share with you: we are trying to benefit from our "know-it-all compiler". Your compiler is mainly manipulating types, one can change its flow using these types during the compilation process. Note that these structs are not even complete (no definition), it has **no impact** for the **runtime memory** or **runtime execution** and that's the amazing part of **meta-programming**. The dispatch of an expression such as **"myRepository.get< int, Key1>()"** is done during your build-time.

You may also notice that every slot is actually a [std::shared_ptr](http://en.cppreference.com/w/cpp/memory/shared_ptr). It enforces a clean ressource management: in a multithreaded application, one must be really careful of the lifetime of heap objects. **std::shared_ptr** in this case permits me to ensure that even someone replace a value in a slot, other components on other threads manipulating the old value won't end up with a **dangling pointer/reference** bomb in their hands. Another solution would to use plain value object, but not only it would require copying big objects in every other components but it would also remove polymorphism.

As for the updates signalisation, you first create a watcher object that establishes a contract between a desired slot to watch and your context. You can thereafter query in thread-safe way weither an update has been made and, if so, poll the latest changes. The watcher object is actually a [std::unique_ptr](http://en.cppreference.com/w/cpp/memory/unique_ptr) for a special class, it cannot be moved nor copied without your permission and will automagically remove the singalisation contract between the slot and your context, once destroyed. We will dive deeper in this topic in the comming sections.

Show how we use it: class ConfigA, class ConfigB, passed in a context along the hierarchy class.
