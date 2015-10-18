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

At compile time? Your compiler has all the type information, reflection ==>.
