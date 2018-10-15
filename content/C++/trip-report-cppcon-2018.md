Title: Trip report - CppCon 2018 
Date: 23:09 10-07-2018
Modified: 23:09 10-07-2018
Tags: C++, event, cppcon 
Slug: trip-report-cppcon-2018


New year, new conference! 
This time, my employer [King](https://discover.king.com/about/) helped me to organize a first pilgrimage to [CppCon](https://cppcon.org/) for me and another colleague.
You can fathom how enthusiastic I was to finally making it there!
Although I might be a bit late on the "trip-report-race", I think that it is still worth to relate my overall experience of the event and then move onto a list of recommended talks you should watch-out on Youtube. 

# About CppCon (2018):

## The event:


**CppCon** is the most renowned conference for all the C++ afficionados. So far held anually in the cozy city center of Bellevue, Washington (or less precisely somewhere close-by to Seattle for those like me that are not into north-american geography), **CppCon** let you explore the **C++** world with various talks, keynotes and other activities provided by some accomplished members of the community. The event is usually happening at the end of September and lasts 5 days, or even more for those attending the training sessions. The program is really plentiful and you would need to watch presentations from 8.00am to 10.00pm, have an ubiquity capacity to be simultaneously in 6 rooms at the same time, and have infinite memory to be able to absorbe all the C++ knowledge flowing during these days.

Do not get me wrong, while the conference is impressive when it comes to the amount of content, that do not imply that this content is out of the reach of the commoners. On one hand you have hairy topics like "Compile-time programming" being discussed, and on the other hand you have acces to gentle introductions to some features of the language. Dedicated or novice C++ users will appreciate as much the conference but for different reasons. A novice will bring back home a lot of new keywords/concepts to plunge into. Someone who follow C++ news, may not make as many discoveries at **CppCon** than at [CppNow](http://cppnow.org/), but she/he will gain a lot of inspiration/motivation from other C++ fellows and will be exposed to other point of views on the language.

<center><img width=50% height=50% src="{filename}/images/bellevue.jpg"/></center>

Does this sound exciting to you, but you missed the opportunity to come this year? No worries, **CppCon** has one of the best [Youtube channel](https://www.youtube.com/user/CppCon/videos) where they upload all the talks. I have always been impressed by the quality of their videos and the frequency at which they can produce such material. Now, I can say that behind the scene (or actually in front...), they have an excellent video-shooting crew in each of the conference rooms. On a side note, all keynotes were introduced by a live rock-band, which you can see at the beggining of the videos. Whether you appreciated the music or not, it is hard to deny that CppCon organizers really put a lot of efforts in the entire event! 

# My experience over there:

Right before leaving Stockholm, I had the great idea to listen to my favorite C++ podcast [CppCast](http://cppcast.com/). The guest for that week was **Bryce Adelstein Lelbach** who is one of the organiser of CppCon. Bryce had four advices for any new attendee of the conference, which matched my experience at [Meeting C++]({filename}../C++/trip-report-meetingcpp.md) last year and turn out to be valid for CppCon too:

- Have no regrets! Indeed, as an attendee you will quickly discover that two or three appealing talks will be on the same time slot. Just randomly pick one of the talk or none if you need to rest a bit. If luck is not on your side that day and you missed a terrific talk, you will naturally hear about it from others and you will have plenty of time to binge-watch it on Youtube later on. Having that in mind, I was much more relax at this conference than I was at my very intense days at **Meeting C++**. If you really dislike to choose you will anyway ends-up following someone, you just chit-chated with within the corridors, to the talk of his choice. Which brings us to the second advice you should follow...
- Engage with the community! If you are planning to go to CppCon to appreciate a better version of the talks than on YouTube, you are doing it wrong! By going over there, you actually loose the possibility to watch the talk at your own pace... What you gain instead, as an attendee, is the opportunity to mingle with people with very different backgrounds, exchange tips and tricks and feel part of community bigger than the few C++ colleagues you are working with. Programmers seldom have the reputation of being extroverts, but you will always find someone that can introduce to his connections and slowly build relationships. I met quite a few people from **SwedenCpp** over there and it was really fun to see them in another context!
- Be confused! You should not be afraid to be out of your confort zone when it comes to the content of the talks. You may be mortified at the idea that a guru will suddenly drop a very complicated C++ concept on stage, and you will be there lonely, not knowing what on earth he/she/it is talking about. Truth is, very few people (if not none) can claim knowing everything about such a vaste language that is C++. Usually during a "productive" C++ conference, you will dress-up a list of keywords / ideas that you will explore later-on. This year, I promised myself to look further on the edge-cases of Class Template Argument Deduction (CTAD), prepare myself for C++20's **contracts** and play with clang's tooling internals.
- Be bold! The concentration of "legendary C++ devs" per square meter is even higher than in **Meeting C++**. While I did not shoot any selfie (not that I wanted to either) with any of these legends, I discussed briefly with few of them, and you can too! People at **CppCon** are here to celebrate their favorite language, not to act as elitists, which make everyone very approachable. One of the talk I attended was on a [proposal](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0052r8.pdf) (Woes of Scope Guards and Unique Resource - 5+ years in the making - By Peter Sommerland) I implemented at work. During the talk, Peter mentioned a relatively serious bug introduced in one of the revision. Right after that talk, I had the unique chance to have a face-to-face discussion with him. It turns out, my implementation did not suffer from that bug, but was instead hiding another one. I was so glad that I could access to that person so easily! 

Following these precepts, I experienced a very wonderful week made of C++ and human interactions, and I would highly recommend **CppCon** to anyone having a slight interest in the language.

<center><img width=50% height=50% src="{filename}/images/cppcon.jpg"/></center>

I still have one and only one complain about the event: the time slot for the lightning talks.
For those that are not aware, the lightning talks are short presentations of roughly 5min, easier to submit, often light-minded but also damn interesting.
Due to the short format, people often go straight to the point which is really pleasant to watch.
For instance, this year there was an epic lightning talk battle on [East Const vs West Const](https://arne-mertz.de/2018/05/trailing-return-types-east-const-and-code-style-consistency/) or a touching "Thank You" speech from **Dr. Walter E. Brown**. 
If that sounds interesting to you, you will have to stay awake from 8.30pm to 10.00pm which is where my grudge comes from.
After absorbing some C++ since roughly 9.00am, and with a pretty strong jetlag (=~9h for central Europeans) you really need to channel all your inner motivation to attend any of these late activities.
The lightning talks being such joyfull part of **CppCon**, I would argue that some of them could be moved to an earlier slot in the day...

Enough of my pseudo-rant on an almost perfect event and let's continue with some more concrete reporting! 

# The chief's suggestions of the year:

Once again, here is a menu of most of the talks I particulary enjoyed. The legend follow the same rules:

- 💀 : The difficulty of the talk (💀: Begginer friendly, 💀💀: Intermediate, 💀💀💀: High exposure to C++'s dark corners)
- ★ : My interest for the talk (★: Good talk, ★★: Tasty talk, ★★★: Legendary talk)

I promise you not to spoil everything in the talks, but simply try to give an overview of what you can expect within them or some conclusions. Although most of the talks are most likely worth to be seen, I forced my-very-subjective-self to pick very few of them. I have seen people with very different "favorite talk" and you should not feel sad if your own talk is not part of this not-so-prestigious list.

### [Keynote] Concepts: The Future of Generic Programming (the future is here) - Bjarne Stroustrup - 💀★★★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Keynotes/concepts_the_future_of_generic_programming/concepts_the_future_of_generic_programming__bjarne_stroustrup__cppcon_2018.pdf)
- Video: [link](https://youtu.be/HddFGPTAmtU)

The Bjarne himself, creator of C++ (for those really out of the loop), kick-started the conference with a keynote on a long-overdue C++ feature: [Concepts](https://en.wikipedia.org/wiki/Concepts_(C%2B%2B)).
Indeed, as early as 2003, Bjarne and some members of the committee have been pushing for Concepts as an extension to C++ templates to simplify the life of us poor template consumers.
Sadly, a first version, dimmed too complicated, of the feature was rejected for **C++11**. Nine years later, Bjarne and his crew is back with a version "Concepts Lite" that will be integrated into **C++20**.  

Let's face it, C++ templates have always been a pain to use due to the absence of constraints on the template parameter types.
Take a look at this very simple piece of code:
```c++
template <class T>
void foo(T&& t) {
    t.print();
}

template <class T>
void bar(T&& t) {
	foo(t);
}

struct A {};

int main() {
    A a;
    bar(a);
}
```
Your never-satisfied compiler will refuse to compile it with the following error message:
```
<source>: In instantiation of 'void foo(T&&) [with T = A&]':
<source>:10:8:   required from 'void bar(T&&) [with T = A&]'
<source>:17:10:   required from here
<source>:5:7: error: 'struct A' has no member named 'print'
     t.print();
     ~~^~~~~
```
This is an horrifying warning message as we often see nowadays.
Your compiler do warn you about the absence of a **print** method in **A** far down in **foo**!
In this specific case, we only have two layers in the call stack which is very reasonable. 
But most often when using functions provided by the Standard Library, your type will violate some constraints reaaallly deep down.
As a newcommer you will often struggle with your compiler vomiting a bizarre message of 100 lines when using templates, which is not the best first experience (to say the least). 
Moreover, by looking at the signature of **bar**, nothing tells you that the template parameter **T** needs to have a **print** member function. That's frustrating!

With concepts you can define in elegant way the constraints that your parameters must respect. Have a look at we could do with Concepts in this case:
```c++
template <class T> concept bool IsPrintable = requires (T a) { // Define a reusable concept "IsPrintable".
    a.print(); // Any template parameter of T respecting "IsPrintable" must have a print function. 
};

template <IsPrintable T> // Explicitely tells that T must respect the concept.
void foo(T&& t) {
    t.print();
}

template <IsPrintable T> // Same here!
void bar(T&& t) {
    foo(t);
}
```
Which would give us the following much more accurate error message:
```
<source>:19:10: error: cannot call function 'void bar(T&&) [with T = A&]'
     bar(a);
          ^
<source>:11:6: note:   constraints not satisfied
 void bar(T&& t) {
      ^~~
<source>:1:33: note: within 'template<class T> concept const bool IsPrintable<T> [with T = A&]'
 template <class T> concept bool IsPrintable = requires (T a) {
                                 ^~~~~~~~~~~
<source>:1:33: note:     with 'A& a'
<source>:1:33: note: the required expression 'a.print()' would be ill-formed
``` 
Some sceptical gurus will tell you that this can be emulated with some witch-crafted [SFINAEs]({filename}../C++/sfinae-introduction.md). 
Concepts were not christmas wish-list for **C++**, but I have to admit that Bjarne's talk hipped me a lot! 

### [Talk] How to Write Well-Behaved Value Wrappers - Simon Brand - 💀💀💀 ★★:

- Slides: [coming soon]()
- Video: [coming soon]()

Good speakers are like good wine, you are seldom disappointed.
Having attended Simon's talk on debugger internals last year and enjoyed it a lot, I took the chance to hear what he had to say on value wrappers.
You may not know what is a value wrapper, but I surely bet that you already manipulated some provided by the Standard Library: [std::pair](https://en.cppreference.com/w/cpp/utility/pair), [std::tuple](https://en.cppreference.com/w/cpp/utility/tuple), [std::optional](https://en.cppreference.com/w/cpp/utility/optional)... 

It might be a breeze to work with most of these wrappers (certainely not you verbose [std::variant](https://en.cppreference.com/w/cpp/utility/variant)), but the poor souls writting implementations of these must go to great lengths to make them behave as they should. Value wrappers, as their name imply, try to mimic as closely as possible the type of a given value. All the types have some basic properties: can it be explicitely constructed? Are the [special member functions](https://en.wikipedia.org/wiki/Special_member_functions) noexcept? Can it be called in a constant expression? Can it be compared? And much more... A wrapper must react exactly in the same way when it comes to these properties. 

In this talk, Simon compares the old fashioned way to tackle these issues and present how it will look like as soon as the concepts and bunch of other proposals arrive in C++20:

- Explicit operator akin to the noexcept operator
- [P0748R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0848r0.html) to use **concepts-based require clauses** on these member functions to enable or disable them. A.K.A goodbye a lot of uncessarry conditional inheritance. 
- [P0847R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0847r0.html) which permits to deduce correctly the implicit **this** parameter type of a member function. A.K.A goodbye all the methods overloading on const, volatile and ref qualifiers. 
- [P0515R2](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0515r2.pdf) that unify all the comparison operators into one. A.K.A goodbye all the operator overloads.
- ... Some more that I surely forgot.

Regardless if you are planning to write such wrappers or not, I would suggest to watch the talk to refresh yourself on some tricky C++ mechanisms.

### [Talk] Fancy Pointers for Fun and Profit - Bob Steagall - 💀💀 ★★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/fancy_pointers_for_fun_and_profit/fancy_pointers_for_fun_and_profit__bob_steagall__cppcon_2018.pdf)
- Video: [coming soon]()

**Bob Steagall** promoted his own talk on **fancy pointers** in an early September **CppCast** episode.
So here I was, ready to learn more about these mystical beasts!

**Allocators** in C++ are rather infamous for their over-engineered interface, which is not useful 99.42% of the time. This even forced the committee to come-up, in **C++17**, with a lighter interface called [PMR](https://youtu.be/v3dz-AKOVL8). But this time, the good old full-blown interface found a very clever usage in Bob's hands. Indeed, [std::allocator_traits](https://en.cppreference.com/w/cpp/memory/allocator_traits) has a nice type property **pointer**. Which means that the Standard offers a nice [customization point](https://quuxplusone.github.io/blog/2018/03/19/customization-points-for-functions/) to switch normal pointers **T\*** for a given allocator to a type that acts like a pointer would. These wanna-be pointers are what you call **fancy pointers**. Somehow, you can think of **fancy pointers** as more generalized concept of [smart pointers](https://en.wikipedia.org/wiki/Smart_pointer).   

Now let's say that you would like to serialise to / deserialise from binary a container-like object (vector, list...) with a bunch of [trivial objects](https://msdn.microsoft.com/en-us/library/mt767760.aspx?f=255&MSPPError=-2147217396) inside and send it through a network. Providing that you are targeting one and only one architecture, which is often the case for servers, you may be able to use [std::memcpy](https://en.cppreference.com/w/cpp/string/byte/memcpy) to transfer the representation of this container into a **char\*** buffer. Then, the whole buffer can be wired to another machine. At the endpoint, to deserialise the container from that buffer you can re-use **std::memcpy** to copy back the binary representation into a container ([note that you cannot rely reinterpret_cast in C++ for that purpose](https://www.reddit.com/r/cpp/comments/5fk3wn/undefined_behavior_with_reinterpret_cast/)...). This will work smoothly as long as none of the stored PODs have pointers as members referencing each others! Indeed, pointers are usually not valid as soon as you cross the boundary of a process or a machine. This huge drawback can be avoided by introducing **fancy pointers** to your code-base. 

For instance, Bob brings **offset_ptr** to the table, which permits to express some reference between two elements using their distance from each others:
```
struct obj
{
	value_type v;
	offset_ptr<value_type> p; // optional
}; 

Example of the layout of a container of objs:

                               -2
                +-----------------------------+
                |        1                    |
                |     +-----+                 |
 +--------------v-----------v--------------------------------+
 |  v  |  p  |  v  |  p  |  v  |  p  |  V  |  p  |  v  |  p  |
 +-----------------------------------------------------------+
          |                             ^
          |                             |
          +-----------------------------+
                       3

```
With a bit of boilerplate, this **offset_ptr** can be handled by a custom allocator that can be injected into a container, making different address mappings a non-issue.
I find this solution pretty elegant and is a good showcase on how extensible the Standard Library is. 


### [Talk] RVO is Harder than it Looks: the story of -Wreturn-std-move - Arthur O'Dwyer - 💀💀 ★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/return_value_optimization_harder_than_it_looks/return_value_optimization_harder_than_it_looks__arthur_odwyer__cppcon_2018.pdf)
- Video: [coming soon]()

It is commonly admitted that returning by value seldom has a performance impact in C++. Two mechanisms [(N)RVO](https://en.wikipedia.org/wiki/Copy_elision#Return_value_optimization) and [move semantics](http://thbecker.net/articles/rvalue_references/section_02.html) will most likely kick in to avoid unecessary copies:

```c++

struct A
{
// ... some members
};

A foo() {
	A a;
	// ...
	return a;
}

A a = foo(); // The return value is directly constructed in a's stack location (RVO), can fall back onto the move-constructor otherwise. 
```

As time goes by, the C++ standard has stronger and stronger guarantees that copy ellision (RVO) will happen in these situations.
At the same time, forcefully moving the return value can a pretty huge pessimisation and is taught as an anti-pattern:
```c++
A foo() {
	A a;
	// ...
	return std::move(a); // Will hinder the compiler to choose RVO instead of move constructor.
}
```
In the worst case scenario, if the object has no move-constructor, the compiler might resort to use the copy constructor, which could have been avoided with RVO.


Now in the **C++ land** nothing really holds true if you look closer at some corner cases. And "no-move-on-return-values" rule mentioned right above can be debated for that reason. Arthur was valiant enough to inquire into this topic and found few cases where a call to **std::move** will BE an optimization. Notably, if you return a value with a type convertible to the function's return type thanks to an [explicit conversion operator](https://en.cppreference.com/w/cpp/language/cast_operator), you should apply **std::move**. Arthur introduced a new warning in clang [-Wreturn-std-move](https://reviews.llvm.org/D43322) to avoid this pitfall. I will gadly turn that warning on as soon as I can.

I liked the talk for delving into such precise topics ; although, Arthur rushed on quite a few slides and even skipped a whole bunch of them, meaning that there was more to say on this theme. 

### [Talk] State Machines Battlefield - Naive vs STL vs Boost - Kris Jusiak - 💀💀 ★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/state_machines_battlefield_naive_vs_stl_vs_boost/state_machines_battlefield_naive_vs_stl_vs_boost__kris_jusiak__cppcon_2018.pdf)
- Video: [link](https://www.youtube.com/watch?v=yZVby-PuXM0)

**Kris Jusiak** is the proud author of two library aspiring to be into [Boost](https://www.boost.org/): [Boost.DI](http://boost-experimental.github.io/di/) and [Boost.SML](https://github.com/boost-experimental/sml). This talk was partly based on the later one. More precisely **Kris** compared how different implementations of a state machine would fare in term of performance and ease to maintain.

**Kris** started with a good ol' implementation designed around a giant switch case roughly similar to this code:
```c++
class connection {
	// ...
	void update(event e) {
		switch(state_) {
			case connecting:
				if (e && e->type == event_type::established) {
					state_ = state::connected;	
					log("connected");	
				}
			break;
			case connected:
				// ...
				do_connected_things();
				// ...
			break;
			// ...
			default:
				throw runtime_exception("bad state");
			break;
		}
	}
	// ...

	int variable_for_connected_state;
	int another_variable_for_connected_state;
	int variable_for_disconnected_state;
	// ...
	state state_;
};
```
Surely, this implementation will perform rather decently, but at the cost of being extremely hard to maintain if the amount of states increase. Sadly, a lot of code-bases for games or networking have plenty of these ugly state machines sprinkled around. **C++** is all about **zero-cost abstractions**, which means that if you want to avoid some serious posttraumatic stress disorders after working on such projects, you may want to look at other choices than switch.

Therefore, **Kris** jumped onto other implementations. One of the them is using [std::variant](https://en.cppreference.com/w/cpp/utility/variant) which reminded me a lot a blog post from [Kalle Huttunen](https://khuttun.github.io/2017/02/04/implementing-state-machines-with-std-variant.html). **std::variant** will permit you to isolate the variables necessary for your different states and will enforce a stricter handling of your state with [std::visit](https://en.cppreference.com/w/cpp/utility/variant/visit). In my opinion this solution is huge improvement compared to using a switch and does not require the introduction of an external library into your project. As I will explain later, **std::variant** may or may not have a slight performance impact.

After dwelling with two oldish and rather slow Boost libraries that can help to design state machines, Kris presented us his work. I have to admit that the [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) provided by his library looks very pleasant to use: 

```c++
// Coming straight from Kris's slides:
sml::sm connection = []{
	using namespace sml;
	return transition_table{
		* "Disconnected"_s + event<connect> / establish = "Connecting"_s,
		"Connecting"_s + event<established> = "Connected"_s,
		"Connected"_s + event<ping> [ is_valid ] / reset_timeout,
		"Connected"_s + event<timeout> / establish = "Connecting"_s,
		"Connected"_s + event<disconnect> / close = "Disconnected"_s
	};
};
```

**Boost.DI** is performing very well according to Kris and is on par with the switch solution according to his benchmark.
**Boost.DI** offers different dispatch strategies to get the current state:  **recursive branching**, [jump table](https://mpark.github.io/programming/2015/07/07/variant-visitation/), [fold expressions](https://en.cppreference.com/w/cpp/language/fold)... It turns out that the **recursive branching** is amongst the fastest yelding results as close as if writing a giant switch by hand. I am not so surprised by these results, since we observed a similar pattern at work with our custom implementation of **std::visit**. As far as I know, **clang** and **gcc** visit their **std::variant** using a **jump table**, which may explain the slight performance drop compared to a giant switch. These are good news though, it means that there is room to improve the Quality of Implementation (QoI) of **std::visit** in our favorite libraries.  

### [Talk] Compile-time programming and reflection in C++20 and beyond - Louis Dionne - 💀💀💀 ★★★:

- Slides: [coming soon]()
- Video: [link](https://www.youtube.com/watch?v=CRDNPwXDVp0)

Three skulls, three stars, nothing unusual when it comes to my judgement on **Louis Dionne's** talks. I am very fond (template) meta-programming, and I have always been in awe of Louis's work on [Boost.Hana](https://www.boost.org/doc/libs/1_61_0/libs/hana/doc/html/index.html) and more recently [dyno](https://github.com/ldionne/dyno). This year, he was on stage to give us an overview on what we could expect in the upcomming standards concerning [constexpr](https://en.cppreference.com/w/cpp/language/constexpr), and how this would unlock a better interface for reflection.

We are slowly but surely reaching the point where we will be able to "allocate" at compile-time and convert most of our code-bases to **constexpr** within a blink. Louis explained what are the necessary changes we need to apply to [constexpr](https://en.cppreference.com/w/cpp/language/constexpr) to be able to use it in expressions where we do allocate:

- Allowing constexpr non-trivial destructors, allowing heap allocation and placement new that you will find in [P0784R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0784r0.md).
- Having the new trait **std::is_constant_evaluated** from [P0595R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0595r1.html) that queries whether the compiler is currently evaluating the function in a constexpr context or not. Surprisingly, you will NOT use that trait within a **if constexpr** statement ; this would always be evaluated as constexpr and return **true**, a simple **if** does the job. This trait is an absolute necessity if we want to share a single interface for both a **constexpr** and runtime implementation of a feature (a std::vector...). Behind the scene, **constexpr** code usually has very different demands to perform corretly than standard runtime code.  
- Support **try-catch** statements within a **constexpr** expression which we would get from [P1002R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1002r0.pdf). Note that this does imply that the compiler
- Some other minor changes that must appear in some other hairy white papers ...

Taking all these changes in consideration, we should be able to slap **constexpr** on many containers and algorithms from the STL (vector, string...). That would make the usage of **constexpr** very trivial to any decent **C++** developer.

It will also be a great paradigm shift for the planned reflection within the language. The standard committee used to formulate a reflection proposal based on **template meta-programming**, which dreadfully reminds you some kind of [Boost.MPL](https://www.boost.org/doc/libs/1_68_0/libs/mpl/doc/index.html). 
While templates are powerfull, the syntax to manipulate types appears alienesque to most of the human coders. 
**Constexpr-based metaprogramming** looks a lot more natural and having proper containers was the last missing part of the puzzle to use that syntax for reflection. 
If you are in doubt, have a look at this very short example from Louis: 
```c++
struct my_struct
{
	int x;
	std::string y;
	// ...
};

// Get the type of the first member of my_struct using the old template-based syntax:
using my_struct_meta = reflexpr(my_struct);
using members = std::reflect::get_data_members_t<my_struct>; // Some weird template list-like type.
using x_meta = std::reflect::get_element_t<0, members>; // Some ideaous index accessor.
using x_type = std::reflect::get_reflected_type_t<x_meta>;

// Get the type of the first member of my_struct with the new fancy constexpr-based syntax:
constexpr std::reflect::Record my_struct_meta = reflexp(my_struct);
constexpr std::vector members = my_struct_meta.get_data_members(); // Uses the good ol' vector and class template argument deduction guides from C++17.
constexpr std::reflect::RecordMember x_meta = members[0]; // Just use the operator[] as usual... 
using type = unreflexpr(x_meta.get_reflected_type()); // Get that actual type of x.
```

If you want to have a better understanding on the proposed syntax, have a look at [P0962R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0953r0.html).

### [Keynote] Thoughts on a More Powerful and Simpler C++ (5 of N) - Herb Sutter - 💀💀 ★★★:

- Slides: [coming soon]()
- Video: [link](https://www.youtube.com/watch?v=80BZxujhY38)

The last two years, at CppCon, Herb brought us his vision on a future **C++** full of promises.
Both of these talks were accompanied with some concrete actions (white-papers, guidelines, proof-of-concepts..) that Herb was working on with the rest of the fellowship of the C++s. This year, Herb shared with us some more results on his goals.
It might not sound like a thrilling talk... but that would be under-appreciating the two main ideas Herb was initially pushing for: lifetimes and meta-classes.


Lifetimes are some implicit or explicit rules that directly concern the ownership of an object.
If such lifetime rules are adjusted correctly, your code should be bulletproof when it comes to huge range of bugs related to memory: user after free, dandling pointers...
Some languages like **Rust** even make it a core concept of the language. Arguably, Herb's lifetimes will be slightly more relaxed (no annotations on everything) and natural to use, at the price of not covering some extreme cases. 
Let's have a look at what these so-called lifetimes may protect you from:

```c++
int& foo() {
	int a;
	return a; // Oups I am returning a reference to a local variable that will die right after that function execution.
	// Some compilers may warn you about it, some may not! 
}

std::reference_wrapper<int> foo() {
	int a;
	return std::reference_wrapper<int>(a); // Same issue. No compiler warns you about it! 
}
```
After applying the rules elaborated by Herb and his crew, the lifetime of **a** would be dimmed as ending at the end of foo and the compiler would yield a strong warning or a plain error.
Here [std::reference](https://en.cppreference.com/w/cpp/utility/functional/reference_wrapper) is considered as a pointer/reference type and will be highly scrutinised by the compiler.
If you combine the lifetimes and the concepts, your compiler or linter may be able to discover the pointer types automagically!

Another trivial bug yet often spawning nastily in your code is the dreaded "use-after-move" situation. Here again, lifetimes would avoid an easy shoot in the feet situation:
```c++
my_class my_obj;
my_class another_obj = std::move(my_obj);

my_obj.x->bla = 42; // lifetime warning: using a moved-from obj is seldom a good idea.
```  
All these smart lifetime rules are often based on recommendations that you may find in [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).
Having them enforced within your projects is amazing. I am eager to try the clang implementation of it. Later in the day **Matthias Gehre** and **Gabor Horvath** did show us the internals clang that will support this new feature.

After mesmering the crowd with the lifetimes, Herb gave us some updates on the [meta-classes](https://www.youtube.com/watch?v=4AfRAVcThyA&t=4016s), which were mainly some changes in the syntax.
While I really appreciate the efforts put into **meta-classes**, I still have doubts that I will enjoy such a feature before I am retiring (roughly in 50 years from now). The lifetimes were much more concrete and fathomable when it comes to my daily C++ life.  

### Better C++ using Machine Learning on Large Projects - Nicolas Fleury and Mathieu Nayrolles - 💀 ★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/better_cpp_using_machine_learning_on_large_projects/better_cpp_using_machine_learning_on_large_projects__nicolas_fleury_mathieu_nayrolles__cppcon_2018.pdf)
- Video: [coming soon]()

You can certainely rely on C++ to improve your AI projects, but can you use an AI or machine learning to improve your C++ project?
The two "cousin-frenchies" **Nicolas** and **Mathieu** had the smart idea to detect bugs in pull-requests using some kind of machine learning by analysing previous issues in their code-base.

The presentation did not contain much of actual C++ code, but was more focused on the process they invented to automatically fetch, analyse and post feedback on any submitted code.
I am not an expert on these topics and would not dare to emit any comment on what they presented us.
It seems that after training, the classifying algorithm they put in place was able to predict with a success rate of 70% whether a piece of code would have a negative impact or not.
Their next step would be to add some automatic code correction facilities by applying machine learning on the fixed cases.
Triple A games tend to reuse a lot of variations of the same code across multiple titles, WITHOUT actually sharing it (new games are just cloned from old ones). With this process in place, the projects are spreading the awareness of some issues very easily. It seems like a huge time saver.

In any case, it was a breeze to attend a slightly less C++ oriented talk.
There was a lot of questions regarding the human aspect of that technology.
Is 70% of success rate high enough not to piss-off the users experimenting with the bot?
My experience is that a lot of false positive in a linter, will invariably make people turn it off at earliest opportunity...
Would you be able to spot the bad programmers in your team with such a tool? Thanksfully, the labor rights in Canada (Montréal) should protect the employees on that topic...
And many other interesting facts that you can discover in the video.

### Class Template Argument Deduction for Everyone - Stephan T. Lavavej - 💀💀 ★★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/class_template_argument_deduction_for_everyone/class_template_argument_deduction_for_everyone__stephan_t_lavavej__cppcon_2018.pdf)
- Video: [coming soon]()

[Class Template Argument Deduction](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction), also known as CTAD, is new tiny feature added into the C++17.
While not being an amazing game changer, CTAD can been seen as some very tasty syntaxic sugar that avoid you to specific the template argument of a class template when instiating it.
In other simpler words: it can avoid you to call **make_xxx** function when there is enough information for the compiler to deduce the template paramters of a class template.
Here it what the CTAD lipstick looks like on [std::pair](https://en.cppreference.com/w/cpp/utility/pair):
```c++
// Before C++17:
std::pair<int, const char*> p1 = {42, "test"};
auto p2 = std::make_pair(42, "test");

// After C++17, with CTAD:
std::pair p3 = {42, "test"}; // No needs to specify the template argument "int" and "const char*".
auto p4 = std::pair(42, "test"); // Another way to construct following the always auto rule.
```

In many instances, you do not have to update your class template to benefit from CTAD.
But when you do, one must understand how to help the compiler using some deduction guides.
**STL**'s (known as Stephan T. Lavavej) dedicated and still dedicate his life to maintain the **STL** (also known as Standard Template Library) for MSVC.
**Stephan** apparently had a first hand experience on the deduction guides when adding CTAD to the standard containers in the STL and wanted to explain the gist of it.

Deduction guides are "pseudo-constructors" declared out of the targeted class, that are evaluated right before going to the steps of template parameter deduction, substitution and all the subsequent mess.
When instantiating a given class, all the deduction guides follow the overload resolution and template argument deduction rules that you would expect if applied on normal functions.
The return type of the chosen deduction guide, will be the one used for by the following steps.
Now this sounds very wordy, but it is actually fairly trivial to write:

```c++
template <class T> 
struct foo			// A trivial class template.	
{
	foo(T&& t) {}	// Do something with t...
};

template <class T>
foo(T t) -> foo<T&>; // Declare a deduction guide: given a type T, I will help to deduce a foo with a first parameter being a reference to this type T. 

int a = 42;
auto bar = foo(a); // Bar will be foo<int&> thanks to the CTAD and this deduction guide.
```

I chose this example as it has two interesting tidbits. First you will notice that I apply a transformation on **T** in the return type: the template parameter becomes a **T\***.
It turns out that you can do a lot more in this place: you can invoke <s>satan</s> some traits or inject a SFINAE expression (Oh my...! I really have to push that idea further).
The second unexpected part is that my guide does not have the same signature as my constructor. Indeed, one takes T as an r-value reference, the other one by value.
That's really fortunate, unlike the **make_xxx** functions which would take universal references and [decay](https://en.cppreference.com/w/cpp/types/decay) the arguments, the deductions guides can rely on the automatic decaying of template parameters taken by value. **Stephan** has a lot more of nitty-gritty details on how **deduction guides** behave and it would take a full a post to explain some of them!

### The Bits Between the Bits: How We Get to main() - Matt Godbolt - 💀💀 ★★★:

- Slides: [link](https://github.com/CppCon/CppCon2018/blob/master/Presentations/better_cpp_using_machine_learning_on_large_projects/better_cpp_using_machine_learning_on_large_projects__nicolas_fleury_mathieu_nayrolles__cppcon_2018.pdf)
- Video: [coming soon]()

Your linker is made off a pseudo-language *à la* make. 
LD_DEBUG

# Conclusion:

Would I have infinite time and knowledge,  There was a  
- Spectre: Secrets, Side-Channels, Sandboxes, and Security - Chandler Carruth - :

