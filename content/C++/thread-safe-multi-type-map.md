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

**Tuples** are that kind of **C++11** jewelry that should decide your old-fashioned boss to upgrade your team's compiler (and his ugly tie). Not only I could store a **const char* ** and two **ints** without any compiling error, but I could also access them using compile-time mechanisms. In some way, you can see tuples as a compile-time map using indexes or types as keys to reach its elements. You cannot use an index out of bands, it will be catched at compile-time anyway! Sadly, using a type as a key to retrieve an element is only possible if the type is unique in the **tuple**. At my work, we do have few config objects sharing the same class. Anyway, tuples weren't feeting our needs regarding thread safety and update events. Let's see what we could create using tasty **tuples** as an inspiration.

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

You may also notice that every slot is actually a [std::shared_ptr](http://en.cppreference.com/w/cpp/memory/shared_ptr). It enforces a clean ressource management: in a multithreaded application, one must be really careful of the lifetime of heap objects. **std::shared_ptr** in this case permits me to ensure that even if someone replaces a value in a slot, other components on other threads manipulating the old value won't end up with a **dangling pointer/reference** bomb in their hands. Another solution would be to use plain value objects, but not only it would require copying big objects in every other components but it would also remove polymorphism.

As for the updates signalisation, you first create a watcher object that establishes a contract between a desired slot to watch and your context. You can thereafter query in thread-safe way weither an update has been made and, if so, poll the latest changes. The watcher object is actually a [std::unique_ptr](http://en.cppreference.com/w/cpp/memory/unique_ptr) for a special class, it cannot be moved nor copied without your permission and will automagically disable the signalisation contract between the slot and your context, once destroyed. We will dive deeper in this topic in the comming sections.

Within our application, the repository object is encapsulated into a RuntimeContext object. This RuntimeContext object is created explicitely within our main entry point and passed as a reference to a great part of our components. We therefore keep the possibility to test our code easily by setting this RuntimeContext with different implementations. Here is a simplified version of our usage:

    :::c++
    // runtimecontext.hpp
    #include "repository.hpp"

    // Incomplete types used as compile-time keys.
    struct Key1;
    struct Key2;

    class ConfigType1; // Defined in another file.
    class ConfigType2; // Defined in another file.

    // Create a type for our repository.
    using ConfigRepository = Repository
        <
            RepositorySlot<ConfigType1>,
            RepositorySlot<ConfigType2, Key1>,
            RepositorySlot<ConfigType2, Key2>
        >;

    struct RuntimeContext
    {
        ILogger* logger;
        // ...
        ConfigRepository configRepository;
    };

    // Main.cpp

    #include "runtimecontext.hpp"

    int main()
    {
        RuntimeContext runtimeContext;
        // Setup:
        runtimeContext.logger = new StdOutLogger();
        // ...

        // Let's take a reference to the context and change the configuration repository when necessary. 
        startConfigurationMonitorThread(runtimeContext);

        // Let's take a reference and pass it down to all our components in various threads.
        startOurApplicationLogic(runtimeContext); 

        return EXIT_SUCCESS;
    }


### Time for a C++11 implementation:
We can decompose the solution in 3 steps: at first we need to implement a map that accepts **multiple types**, we then need to work on the **thread safety** and finish by the **watcher mechanism**. Let's first fulfill the mission of this post: introducing you to **variadic templates** to solve the multiple-type problem.

#### Variadic templates:
You may not have heard of **variadic templates** in **C++11** but I bet that you already used **variadic functions** like **printf** in **C** (maybe in a previous unsafe life). As [wikipedia](https://en.wikipedia.org/wiki/Variadic_function) kindly explains "a variadic function is a function of indefinite which accepts a variable number of arguments". In other words, a **variadic function** has potentially an infinite number of **parameters**. Likewise, a **variadic template** has potentially an infinite number of **parameters**. Let's see how to use them!

##### Usage for variadic function templates:
Let's say that you wish to create a template that accept an infinite number of class as arguments. You will use the following notation:

    :::c++

    template <class... T>

You specify a group of template parameters using the ellipsis notation named **T**. Note that this **ellipsis** notation is consistent with the C's variadic function notation. This group of parameters, called a **parameter-pack**, can then be used in your function template or your class template by **expanding** them. One must use the **ellipsis** notation again (this time after T) to **expand** the parameter pack **T**:

    :::c++
    template <class... T> void f(T...)
    //              ^ pack T       ^expansion
    {
        // Your function content.
    }

Now that we have expanded **T**, what can we do Sir? Well, first you give to your expanded parameter **types**, a fancy **name** like **t**.
    
    :::c++
    template <class... T> void f(T... t)
    //                                ^ your fancy t.
    {
        // Your function content.
    }

If **T = T1, T2**, then **T... t = T1 t1, T2 t2** and **t = t1, t2**. Brilliant, but is that all? Sure no! You can then **expand** again **t** using an "suffix-ellipsis" again:

    :::c++
    template <class... T> void f(T... t)
    {
        anotherFunction(t...);
        //                ^ t is expanded here! 
    }

Finally, you can call this function **f** as you would with a normal function template:
    
    :::c++
    template <class... T> void f(T... t)
    {
        anotherFunction(t...);
    }

    f(1, "foo", "bar"); // Note: the argument deduction avoids us to use f<int, const char*, const char*>
    // f(1, "foo", "bar") calls a generated f(int t1, const char* t2, const char* t3)
    // with T1 = int, T2 = const char* and T3 = const char*,
    // that itself calls anotherFunction(t1, t2, t3) equivalent to call anotherFunction(1, "foo", "bar");

Actually, the **expansion mechanism** is creating **comma-separated** replication of the **pattern** you apply the **ellipsis** onto. If you think I am tripping out with template-related wording, here is a much more concret example:

    :::c++
    template <class... T> void g(T... t)
    {
        anotherFunction(t...);
    }

    template <class... T> void f(T*... t)
    {
        g(static_cast<double>(*t)...);
    }

    int main()
    {
        int a = 2;
        int b = 3;

        f(&a, &b); // Call f(int* t1, int* t2).
        // Do a subcall to g(static_cast<double>(*t1), static_cast<double>(*t2)).

        return EXIT_SUCCESS;
    }

I could use the pattern **'*'** for **f** parameters and therefore take them as a pointer! In the same manner, I applied the pattern **'static_cast< double>(*)** to get the value of each arguments and cast them as doubles before forwarding them to **g**.

One last example before moving to **variadic class templates**. One can combine "normal" template parameters with parameter packs and initiate a compile recursion on function templates. Let's take a look at this printing function:

    :::c++

    #include <iostream>

    template <class HEAD> void print(HEAD head)
    {
        std::cout << "Stop: " << head << std::endl;
    }

    template <class HEAD, class... TAIL> void print(HEAD head, TAIL... tail)
    {
        std::cout << "Recurse: " << head << std::endl;
        print(tail...);
    }

    int main()
    {
        print(42, 1337, "foo");

        // Print:
        // Recurse: 42
        // Recurse: 1337
        // Stop: foo

        // Call print<int, int, const char*> (second version of print).
        // The first int (head) is printed and we call print<int, const char*> (second version of print).
        // The second int (head again) is printed and we call print<const char*> (first version of print).
        // We reach recursion stopping condition, only one element left.

        return EXIT_SUCCESS;
    }

**Variadic templates** are very interesting and I wouldn't be able to cover all their features within this post. It roughly feels like functional programming using your compiler, and even some **Haskellers** might listen to you if you bring that topic during a dinner. For those interested, I would challenge them to write a type-safe version **printf** using variadic templates and take a look at this [reference](http://en.cppreference.com/w/cpp/language/parameter_pack). After that, you will run and scream of fear at the precense of **C**'s **vargs**.

##### "Variadic" inheritance:
Sometimes during my programming sessions, I have a very awkward sensation that my crazy code will never compile and, yet, I finally see "build finished" in my terminal. I am talking about that kind of Frankenstein constructions:

    :::c++

    struct A { };

    struct B { };

    template <class... T>
    struct C: public T... // Variadic inheritance
    {

    };

    C<A, B> c;

Yes, we can now create a class inheriting of an infinite number of bases. If you remember my explanation about pattern replications separated by commas, you can imaginge that **struct C: public T...** will be "transformed" in **struct C: public A, public B**, **public T** being the pattern. We start to be able to combine multiple types, each exposing a small amount of methods, to create a flexible concret type. That's one step closer to our multi-type map, and if you are interested in this concept, take a look at [mixins](https://en.wikipedia.org/wiki/Mixin).

Instead of inheriting directly from multiple types, couldn't we inherit from some types that encapsulate our types? Absolutely! A traditional map has some **slots** accessible using keys and these slots contain a value. If you give me base-class you are looking for, I can give you access to the value it contains:

    :::c++
    #include <iostream>

    struct SlotA
    {
        int value;
    };

    struct SlotB
    {
        std::string value;
    };

    // Note: private inheritance, no one can access directly to the slots other than C itself.
    struct Repository: private SlotA, private SlotB
    {

        void setSlotA(const int& value)
        {
            // I access the base-class's value
            // Since we have multiple base with a value field, we need to "force" the access to SlotA.
            SlotA::value = value;
        }

        int getSlotA()
        {
            return SlotA::value;
        }

        void setSlotB(const std::string& b)
        {
            SlotB::value = b;
        }

        std::string getSlotB()
        {
            return SlotB::value;
        }
    };


    int main()
    {
        Repository r;

        r.setSlotA(42);
        std::cout << r.getSlotA() << std::endl; // Print: 42.

        r.setSlotB(std::string("toto"));
        std::cout << r.getSlotB() << std::endl; // Print: "toto".

        return EXIT_SUCCESS;
    }

This code is not generic at all! We know how to create a generic **Slot** using a simple template, and we acquired the magic "create varidiac inheritance" skill, let's fix that ugly copy-paste code:

    :::c++

    #include <iostream>
    #include <string>

    template <class T>
    class _Slot
    {
    protected:
        T& doGet() // A nice encapsulation, that will be usefull later on.
        {
            return value_;
        }

        void doSet(const T& value) // Same encapsulation.
        {
            value_ = value;
        }
    private:
        T value_;
    };

    template <class... Slots>
    class Repository : private _Slot<Slots>... // Here the pattern is _Slot<   >...
    {
    public:
        template <class Type> // Give me a type and,
        Type& get()
        {
            return _Slot<Type>::doGet(); // I can select the base class.
        }

        template <class Type>
        void set(const Type& value)
        {
            _Slot<Type>::doSet(value);
        }
    };

    using MyRepository = Repository // Let's pick the type of our slots.
    <
            int,
            std::string
    >;

    int main()
    {
        MyRepository myRepository;

        myRepository.set<std::string>("toto");
        myRepository.set(42); // Notice the type deduction: we pass an int, so it writes in the int slot.

        std::cout << myRepository.get<int>() << std::endl; // Print: "toto".
        std::cout << myRepository.get<std::string>() << std::endl; // Print: 42.


        return EXIT_SUCCESS;
    }


Another sub-key, emplace

#### Let's play safe:
Threads safety, etc...


#### Our own watchers:

### A touch of C++14:

Final code.

### Conclusion:
todo