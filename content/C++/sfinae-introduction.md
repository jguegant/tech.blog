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

In C++ you also have some sink-hole functions that accept everything: the function templates that accept any kind of parameter (let's say T). But the true black-hole your compiler, the variable vacuum, the oblivion of the forgotten types are the [variadic functions](http://en.cppreference.com/w/cpp/utility/variadic). Yes, exactly like the horrible C **printf**.

	:::c++
	std::string f(...); // Variadic functions are so "untyped" that...
	template <typename T> std::string f(const T& t); // ...even a templated function got the precedence!

	f(1); // Call the templated function version of f.
The fact that function templates are less generic than variadic functions is the first point you must remember!

#### SFINAE:
I am already teasing you with the power for already few paragraphs and here finally comes the explanation of this not so complex acronym. **SFINAE** stands for **S**ubstitution **F**ailure **I**s **N**ot **A**n **E**rror. In rough terms, a **substitution** is the mechanism that tries to replace the template parameters with the provided types or values. In some cases, if the **substitution** leads to an invalid code, the processor shouldn't throw a massive amount of errors but simply continue to try the other available **overloads**. The **SFINAE** concept simply guaranties such a "sane" behavior in a "sane" compiler. For instance:

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

	std::cout << (sizeof(f1()) == sizeof(f2())) << std::endl; // Output 0
    std::cout << (sizeof(f1()) == sizeof(f1())) << std::endl; // Output 1

####Combining everything:
Now we have all the tools to create a solution to check the existence of a method within a type at compile time. You might even have already figured it out most of it by yourself. So let's create it:

	:::c++
	template <class T> struct hasSerialize
	{
	    // For the compile time comparison.
	    typedef char yes[1];
	    typedef yes no[2];

	    // This helper struct permits us to check two properties of a template argument.
	    // The first argument must match the second one.
	    // &C::serialize is actually the same as its signature!
	    template <typename U, U> struct reallyHas;

	    // Two overloads for yes: one for the signature of a normal method, one is for the signature of a const method.
	    // Note that we accept a pointer to our helper struct, 
	    // in order to avoid to instantiate a real instance of this type.
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

The **reallyHas** struct is kinda tricky but necessary to ensure that serialize is a method and not a simple member of the type. You can way more tests on a type using variants of this solution (test a member, a sub-type...) and I suggest you to google a bit more about **SFINAE**. Note: if you truly want a pure compile-time constant and avoid some errors on old compilers, you can replace the last value evaluation by: "**enum { value = sizeof(test<T>(0)) == sizeof(yes) };**". 


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
	std::cout << testHasSerialize(d) << std::endl; // Output 1
    std::cout << testHasSerialize(a) << std::endl; // Output 0

####Time to use it:
std::enable_if 


###When C++11 came to our help:
decltype, declval, more failure, std::true_type, etc

### The supremacy of C++14:
constrexpr and auto lambda/functions