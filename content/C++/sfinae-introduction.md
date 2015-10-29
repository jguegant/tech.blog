Title: An introduction to C++'s SFINAE concept: compile-time introspection of a class member
Date: 14:00 10-18-2015 
Modified: 14:00 10-18-2015
Tags: C++11, C++14, TMP, meta programming
Slug: sfinae-introduction
Status: draft

<!-- http://stackoverflow.com/questions/18570285/using-sfinae-to-detect-a-member-function -->
###Trivia:
As a C++ enthusiast, I usually follow the annual C++ conference [cppconf](http://cppcon.org/) or at least try to keep myself up-to-date with the major events that happen there. One way to catch up, if you can't afford a plane ticket or the ticket, is to follow the [youtube channel](https://www.youtube.com/channel/UCMlGfpWw-RUdWX_JbLCukXg) dedicated to this conference. This year, I was impressed by **Louis Dionne** talk entitled "C++ Metaprogramming: A Paradigm Shift". One feature called **is_valid** that can be found in Louis's [Boost.Hana](http://ldionne.com/hana/) library particulary caught my attention. This genious **is_valid** function heavily rely on an even more "magic" C++ programming technique coined with the term **SFINAE** discovered at the end of the previous century. If this acronym doesn't speak to you, don't be scared, we are going to dive straight in the subject.

###Introspection in C++?
Before explaining what is **SFINAE**, let's explore one of its main usage: **introspection**. As you might be aware, C++ doesn't excel when it comes to examine the type or properties of an object at runtime. The best ability provided by default would be [RTTI](https://en.wikipedia.org/wiki/Run-time_type_information). Not only **RTTI** isn't always available, but it also gives you barely more than the current type of the manipulated object. Dynamic languages or those having **reflection** on the other hand are really convenient in some situations like **serialization**.

For instance, in Python, using reflection, one can do the following:

	:::python
	class A(object):
	    # Simply overrides the 'object.__str__' method.
	    def __str__(self):
	        return "I am a A"

	class B(object):
	    # A custom method for my custom objects that I want to serialize.
	    def serialize(self):
	        return "I am a B"

	class C(object):
	    def __init__(self):
	        # Oups! 'serialize' is not a method. 
	        self.serialize = 0

	    def __str__(self):
	        return "I am a C"

	def serialize(obj):
	    # Let's check if obj has an attribute called 'serialize'.
	    if hasattr(obj, "serialize"):
	        # Let's check if this 'serialize' attribute is a method.
	        if hasattr(obj.serialize, "__call__"):
	            return obj.serialize()

	    # Else we call the __str__ method.
	    return str(obj)

	a = A()
	b = B()
	c = C()

	print(serialize(a)) # output: I am a A.
	print(serialize(b)) # output: I am a B.
	print(serialize(c)) # output: I am a C.

As you can see, during serialization, it comes pretty handy to be able to check if an object has an attribute and if to query the type of this attribute. In this case, it permits us to use the **serialize** method if available and fall back to the more generic method **str** otherwise. Powerful, isn't it? Well, we can do it **in plain C++**!

Here is the **C++14** solution mentionned in **Boost.Hana** documentation, using **is_valid**:

	:::c++
	#include <boost/hana.hpp>
	#include <iostream>
	#include <string>

	using namespace std;
	namespace hana = boost::hana;

	// Check if a type has a serialize method.
	auto hasSerialize = hana::is_valid([](auto&& x) -> decltype(x.serialize()) { });

	// Serialize any kind of objects.
	template <typename T>
	std::string serialize(T const& obj) {
	    return hana::if_(hasSerialize(obj), // Serialize is selected if available!
	                     [](auto& x) { return x.serialize(); },
	                     [](auto& x) { return to_string(x); }
	    )(obj);
	}

	// Type A with only a to_string overload.
	struct A {};

	std::string to_string(const A&)
	{
	    return "I am a A!";
	}

	// Type B with a serialize method.
	struct B
	{
	    std::string serialize() const
	    {
	        return "I am a B!";
	    }
	};

	// Type C with a "wrong" serialize member (not a method) and a to_string overload.
	struct C
	{
	    std::string serialize;
	};

	std::string to_string(const C&)
	{
	    return "I am a C!";
	}

	int main() {
	    A a;
	    B b;
	    C c;

	    std::cout << serialize(a) << std::endl;
	    std::cout << serialize(b) << std::endl;
	    std::cout << serialize(c) << std::endl;
	}

As you can see, it only requires a bit more of boilerplate than Python, but not as much as you would expect from a language as complexe as C++. How does it work? Well if you are too lazy to read the rest, here is the simplest answer I can give you: unlike dynamically typed languages, your compiler has access a lot of static type information once fired. It makes sense that we can constraint your compiler to do a bit of work on these types! The next question that comes to your mind is "How to?". Well, right below we are going to explore the various options we have to enslave our favorite compiler for fun and profit! And we will eventually recreate our own **is_valid** and static **if_**.

###The old-fashioned C++98-way:
Whether your compiler is a dinosaur, your boss refuses to pay for the latest Visual Studio license or you simply love archeology, this chapter will interest you. It's also interesting for the people stuck between C++11 and C++14. The solution in C++98 relies on 3 key concepts: **overload resolution**, **SFINAE** and the static behavior of **sizeof**. 

####Overload resolution:
A simple function call like **f(obj);** in C++ activates a mechanism to figure out which **f** function shoud be called according to the argument **obj**. If a **set** of **f** functions could accept **obj** as an argument, the compiler must choose the most appropriate function, or in other words **resolve** the best **overload**! Here is a good cppreference page explaining the full process: [Overload resolution](http://en.cppreference.com/w/cpp/language/overload_resolution). The rule of thumb in this case is that the compiler picks *the candidate function whose parameters match the arguments most closely is the one that is called*. Nothing is better than a good example:

	:::c++
	void f(std::string s); // int can't be convert into a string.
	void f(double d); // int can be implicitly convert into a double, so this version could be selected, but...
	void f(int i); // ... this version using the type int directly is even more close!

	f(1); // Call f(int i);

In C++ you also have some sink-hole functions that accept everything: the function templates that accept any kind of parameter (let's say T). But the true black-hole of your compiler, the devil variable vacuum, the oblivion of the forgotten types are the [variadic functions](http://en.cppreference.com/w/cpp/utility/variadic). Yes, exactly like the horrible C **printf**.

	:::c++
	std::string f(...); // Variadic functions are so "untyped" that...
	template <typename T> std::string f(const T& t); // ...even a templated function got the precedence!

	f(1); // Call the templated function version of f.
The fact that function templates are less generic than variadic functions is the first point you must remember!

#### SFINAE:
I am already teasing you with the power for already few paragraphs and here finally comes the explanation of this not so complex acronym. **SFINAE** stands for **S**ubstitution **F**ailure **I**s **N**ot **A**n **E**rror. In rough terms, a **substitution** is the mechanism that tries to replace the template parameters with the provided types or values. In some cases, if the **substitution** leads to an invalid code, the compiler shouldn't throw a massive amount of errors but simply continue to try the other available **overloads**. The **SFINAE** concept simply guaranties such a "sane" behavior in a "sane" compiler. For instance:

	:::c++
	/*
	 The compiler will try this overload since it's less generic than the variadic.
	 T will be replace by int which gives us void f(int::B* b);
	 int doesn't have a B sub-type, but the compiler doesn't throw a bunch of errors.
	 It simply tries the next overload.
	*/
	template <typename T> void f(typename T::B* b) { }

	// The sink-hole.
	void f(...) { }

	f(1); // Calls void f(...) { }

All the expressions won't lead to a **SFINAE**. A broad rule would be to say that all the **substitution** out of the function/methods **body** are "safes". For a better list, please take a look at this [wiki page](http://en.cppreference.com/w/cpp/language/sfinae). For instance, a wrong substitution within a function **body** will lead to a horrible C++ template error:

	:::c++
	// The compiler will be really unhappy when it will later discover the call to hahahaICrash. 
	template <typename T> void f(T t) { t.hahahaICrash(); }
	void f(...) { } // The sink-hole wasn't even considered.

    f(1);

####The operator sizeof:
The **sizeof operator** is really a nice tool! It permits us to returns the size in bytes of a type or an expression at compilation time. **sizeof** is really interesting as it accurately evaluates an expression as precisely as if it were compiled.
One can for instance do:

	:::c++
	typedef char type_test[42];
	type_test& f();

	// In the following lines f won't even be truly called but we can still access to the size of its return type.
	// Thanks to the "fake evaluation" of the sizeof operator.
	char arrayTest[sizeof(f())];
    std::cout << sizeof(f()) << std::endl; // Output 42.
But wait! If we can manipulate some compile-time integers, couldn't we do some compile-time comparison? The answer is: absolutely yes my dear! Here we are:

	:::c++
	typedef char yes;
	typedef yes no[2];

	yes& f1();
	no& f2();

	std::cout << (sizeof(f1()) == sizeof(f2())) << std::endl; // Output 0.
    std::cout << (sizeof(f1()) == sizeof(f1())) << std::endl; // Output 1.

####Combining everything:
Now we have all the tools to create a solution to check the existence of a method within a type at compile time. You might even have already figured it out most of it by yourself. So let's create it:

	:::c++
	template <class T> struct hasSerialize
	{
	    // For the compile time comparison.
	    typedef char yes[1];
	    typedef yes no[2];

	    // This helper struct permits us to check that serialize is truly a method.
	    // The second argument must be of the type of the first.
	    // For instance reallyHas<int, 10> would be substituated by reallyHas<int, int 10> and works!
	    // reallyHas<int, &C::serialize> would be substituated by reallyHas<int, int &C::serialize> and fail!
	    // Note: It only works with integral constants and pointers (so function pointers work).
	    // In our case we check that &C::serialize has the same signature as the first argument!
	    // reallyHas<std::string (C::*)(), &C::serialize> should be substituated by 
	    // reallyHas<std::string (C::*)(), std::string (C::*)() &C::serialize> and work!
	    template <typename U, U u> struct reallyHas;

	    // Two overloads for yes: one for the signature of a normal method, one is for the signature of a const method.
	    // We accept a pointer to our helper struct, in order to avoid to instantiate a real instance of this type.
	    // std::string (C::*)() is function pointer declaration.
	    template <typename C> static yes& test(reallyHas<std::string (C::*)(), &C::serialize>* /*unused*/) { }
	    template <typename C> static yes& test(reallyHas<std::string (C::*)() const, &C::serialize>* /*unused*/) { }

	    // The famous C++ sink-hole.
	    // Note that sink-hole must be templated too as we are testing test<T>(0).
	    // If the method serialize isn't available, we will end up in this method.
	    template <typename> static no& test(...) { /* dark matter */ }

	    // The constant used as a return value for the test.
	    // The test is actually done here, thanks to the sizeof compile-time evaluation.
	    static const bool value = sizeof(test<T>(0)) == sizeof(yes);
	};

	// Using the struct A, B, C defined in the previous hasSerialize example.
    std::cout << hasSerialize<A>::value << std::endl;
    std::cout << hasSerialize<B>::value << std::endl;
    std::cout << hasSerialize<C>::value << std::endl;

The **reallyHas** struct is kinda tricky but necessary to ensure that serialize is a method and not a simple member of the type. You can do a lot of test on a type using variants of this solution (test a member, a sub-type...) and I suggest you to google a bit more about **SFINAE**. Note: if you truly want a pure compile-time constant and avoid some errors on old compilers, you can replace the last value evaluation by: "**enum { value = sizeof(test<T>(0)) == sizeof(yes) };**". 


You might also wonder why it doesn't work with **inheritence**. **Inheritence** in C++ and **dynamic polymorphism** is a concept available at runtime, or in other words, a data that the compiler won't have and can't guess! However, compile time type inspection is much more efficient (0 impact at runtime) and almost as powerful as if it were at runtime.
For instance:

	:::c++
	// Using the previous A struct and hasSerialize helper.

	struct D : A
	{
	    std::string serialize() const
	    {
	        return "I am a D!";
	    }
	};

	template <class T> bool testHasSerialize(const T& /*t*/) { return hasSerialize<T>::value; }

    D d;
    A& a = d; // Here we lost the type of d at compile time.
	std::cout << testHasSerialize(d) << std::endl; // Output 1.
    std::cout << testHasSerialize(a) << std::endl; // Output 0.

Last but no least, our test cover the main cases but not the tricky ones like a Functor: 

	:::c++
	struct E
	{
	    struct Functor
	    {
	        std::string operator()()
	        {
	            return "I am a E!";
	        }
	    };

	    Functor serialize;
	};

    E e;
    std::cout << e.serialize() << std::endl; // Succefully call the functor.
    std::cout << testHasSerialize(e) << std::endl; // Output 0.

The trade-off for a full coverage would be the readability. As you will see, C++11 shines in that domain!

####Time to use our genius idea:
Now you would think that it will be super easy to use our **hasSerialize** to create a **serialize** function! Okay let's try it:

	:::c++
	template <class T> std::string serialize(const T& obj)
	{
	    if (hasSerialize<T>::value) {
	        return obj.serialize(); // error: no member named 'serialize' in 'A'.
	    } else {
	        return to_string(obj);
	    }
	}

    A a;
    serialize(a);

It might be hard to accept, but the error raised by your compiler is absolutely normal! If you consider the code that you will obtain after substitution and compile-time evaluation:
	
	:::c++
	std::string serialize(const A& obj)
	{
	    if (0) { // Dead branching, but the compiler will still consider it!
	        return obj.serialize(); // error: no member named 'serialize' in 'A'.
	    } else {
	        return to_string(obj);
	    }
	}

Your compiler is really a good guy and won't drop any dead-branch, and obj must therefore have both a **serialize method** and a **to_string overload** in this case. The solution is to split the serialize function into two different functions: one where we solely use **obj.serialize()** and one where we use **to_string** according to **obj's type**. We come back to an earlier problem that we already solved, how to split according to a type? **SFINAE**, for sure! At that point we could re-work our **hasSerialize** function into a **serialize** function and make it return a std::string instead of compile time boolean. But we won't do it that way! It's cleaner to separate the **hasSerialize** test from its usage **serialize**.


We need to find a clever **SFINAE** solution on the signature of "**template <class T\> std::string serialize(const T& obj)**". I bring you the last piece of the puzzle called **enable_if**.

	:::c++
	template<bool B, class T = void> // Default template version.
	struct enable_if {}; // This struct doesn't define "type" and the substitution will fail if you try to access it.  

	template<class T> // A specialisation used if the expression is true. 
	struct enable_if<true, T> { typedef T type; }; // This struct do have a "type" and won't fail on access.

	// Usage:
    enable_if<true, int>::type t1; // Compiler happy. t's type is int.
    enable_if<hasSerialize<B>::value, int>::type t2; // Compiler happy. t's type is int.

    enable_if<false, int>::type t3; // Compiler unhappy. no type named 'type' in 'enable_if<false, int>';
    enable_if<hasSerialize<A>::value, int>::type t4; // no type named 'type' in 'enable_if<false, int>';

As you can see, we can trigger a substitution failure according to a compile time expression with **enable_if**. Now we can use this failure on the "**template <class T\> std::string serialize(const T& obj)**" signature to dispatch to the right version. Finally, we have the true solution of our problem:

	:::c++
	template <class T> typename enable_if<hasSerialize<T>::value, std::string>::type serialize(const T& obj)
	{
	    return obj.serialize();
	}

	template <class T> typename enable_if<!hasSerialize<T>::value, std::string>::type serialize(const T& obj)
	{
	    return to_string(obj);
	}

    A a;
    B b;
    C c;
    
    // The following lines work like a charm!
    std::cout << serialize(a) << std::endl;
    std::cout << serialize(b) << std::endl;
    std::cout << serialize(c) << std::endl;
Two details worth being noted! Firstly we use **enable_if** on the return type, in order to keep the paramater deduction, otherwise we would have to specify the type explicitely "**serialize<A\>(a)**". Second, even the version using **to_string** must use the **enable_if**, otherwise **serialize(b)** would have two potential overloads available and raise an ambiguity. If you want to check the full code of this C++98 version, here is a [Gist](https://gist.github.com/Jiwan/2573fc47e4fa5025306b).
Life is much easier in C++11, so let's see the beauty of this new standard!



###When C++11 came to our help:
SFINAE enforced
decltype
auto
constrexpr
std::true_type

template <typename T, typename = void>
struct has_toString
  : std::false_type
{ };
template <typename T>
struct has_toString<T, decltype((void)std::declval<T>().toString())>
  : std::true_type
{ };

####Other interesting features:
	declval
	nullptr
	lambda

### The supremacy of C++14:
constrexpr and auto lambda/functions, enable_if_t