Title: Trip report - Meeting C++ 2019 
Date: 23:09 11-18-2019
Modified: 23:09 11-19-2019
Tags: C++, event, meetingcpp
Slug: trip-report-meetingcpp-2019


Time to go back to the roots!
Me and quite a few colleagues have been travelling across the old continent to attend the renowned [Meeting C++](https://meetingcpp.com/) conference in Berlin.  
Fully backed by our employer, [King](https://discover.king.com/about/), we were able to enjoy a yearly dose of C++ talks at an excellent venue.
I was thrilled at the idea of retrying the "German C++ experience" and my expectation were once again met! 
**C++20** being right at the corner, I also had in mind to prioritise talks concerning this topic as much as possible.

As the tradition goes, I will relate a bit my experience of the event and dress-up a list of the talks I would highly suggest to search for! 

<center><img width=50% height=50% src="{filename}/images/berlin-night.jpg"/></center>

# A tour of Meeting (2019):

I did a decent [introduction of the event two years ago]({filename}../C++/trip-report-meetingcpp.md) and most of it stand true.
So rather than doing another summary, I will compare and contrast my experience at **Meeting C++** with the one I had last year at **Cppcon**. 


## The venue:

When it comes to the facilities of the venue, I found the rooms in the Andels Hotel to have unequal quality.
While the two big rooms on the lower floors are excellent, the upper floor ones are really long and narrow. 
If the nature made you of a short stature or you don't have the best eyesight (or both like me), you will have a hard time following some of the slides.
I cannot remember having any issue with that at **CppCon**. Having a rooms with inclined rows helps a lot!

Probably to avoid having crammed rooms and irritating noises, **Meeting C++** also has this concept of closing doors of the tracks as soon as the talk starts and not letting annoying enter. I am not quite convinced by this idea, it extremely frustrating to not be able to move to another talk if the current one is not to your taste. 

## The German cuisine:

Being French, a detail often comes to my mind... the food provided during the event!
Unlike **CppCon**, this event offers catering all day long, and tasty one mind you. 
Obviously you cannot expect conference meals to deserve a [Michelin stars's](https://en.wikipedia.org/wiki/Michelin), but there was plenty and with a lot of variety. Is that a must-do for a conference? Probably not, but it is both really convenient and it also brings a LOT of interactions between members of the community. People will tend to have more casual conversations if dinning in the same place rather than going out. From what I can recall, **CppCon** provided snacks here and there, but nothing worth remembering.

## The talks:

Last but not least, the speakers! On one hand, **Meeting C++** has more diversity: the speakers are coming from all around Europe and you may discover a lot of new names and some hidden gems that didn't/wouldn't make it to **CppCon** - not everyone is willing or can afford to travel to the USA. On the other hand, the amount of C++ committee members and famous speakers per square kilometer felt higher at **CppCon** which probably made the talks of a slightly better quality overall.

**Meeting C++** offers you the possibility to go to four different tracks for a given time slot.
It is enough choices that you will always find a talk to your liking.
The talks are also explicitely tagged with a level of experience required to enjoy them: beginner to advanced.
Once again, going only to talks with topics that you like is often not the best strategy to fully enjoy this conference.
It can be very rewarding to go out of your comfort zone and try a talk not a single word on its title make sense to you. 
Likewise, do not underestimate the quality of beginner talks. You may learn more than you would expect!


I have had a first hand, albeit short, experience on what it takes to be a speaker at such an event.
I gave a lightning talk highly inspired on the [performing try emplace post]({filename}../C++/trip-report-meetingcpp.md) I did at the beginning of this year.
While it went rather smoothly (if not for a small technical issue with my slides), I felt intimidated when I went on stage in front of maybe 300 people (best-guess estimation). 

<center><img width=50% height=50% src="{filename}/images/my-lightning-talk-meeting-cpp-2019.jpg"/></center>

You can find a pdf version of the slides right [here]({filename}../images/associative-containers-the-art-of-inserting-gracefully.pdf) and maybe a YouTube record of that talk will pop at one point on the [Meeting C++ channel](https://www.youtube.com/user/MeetingCPP).
It was interesting to see that the **lightning talks** were a lot more formal than at **CppCon** where jokes and bad-puns are a constant.
I believe that the lightning talks format was changed recently at **Meeting C++**: it used to be its own dedicated track on a full afternoon, whereas now it became a more casual evening event. We, the lightning speakers, were also informed a bit late on where, when and how should the talks happen.

Doing a presentation on a innovative topic, interesting and understandable by all requires a lot of upfront work.
Having to do it in a foreign language, for one hour, in front of a rather massive crowd is even more demanding.
I am still amazed by what all these speakers gave us during these three days! 

# The chief's suggestions of the year:

Here comes again the menu of the talks I particularly enjoyed. The legend follow the usual rules:

- 💀 : The difficulty of the talk (💀: Beginner friendly, 💀💀: Intermediate, 💀💀💀: High exposure to C++'s dark corners)
- ★ : My interest for the talk (★: Good talk, ★★: Tasty talk, ★★★: Legendary talk)

 No need to say that I will not spoil everything in the talks, but I will simply try to give an idea of what the talk was about. If the talk seems to be of your taste, I highly encourage you to watch the video record of it or the slides. 
 If your talk or a talk that you liked very much is not part of this menu, do not feel too disenchanted about it.
 I had to curate this list to a few talks or I would have to write an entire novel.
 Feel free to post your opinion about the talks in the comment section.

### [Keynote] Design Rationale for <chrono> - Howard Hinnant - 💀💀★★:

- Slides: [link](https://meetingcpp.com/mcpp/slides/2019/Hinnant.pdf)
- Video: [coming soon]()

The Howard Hinnant, himself, came to present his new-born baby: the support of dates, calendars and timezones in the [https://en.cppreference.com/w/cpp/chrono](chrono header). 
For those out-of-the-loop, [Howard Hinnant](https://howardhinnant.github.io/HowardHinnant.html) has been a massive contributor to what C++ is nowadays.
He is known for bringing move semantics to the language, introducing `std::unique_ptr`, being lead author of libc++... a myriad of things... and the notion of time in the standard through the header `<chrono>`. It should not come as surprise that **Howard** is also the man being the dates and calendars coming to the new C++ standard. 

**Howard's** talk was very educating on this addition to C++20. Within two hours, I had a fairly good overview of what we will get and more importantly why "chrono" is so verbose.
Here is the gist of what we will have:

- [std::chrono::time_point](https://en.cppreference.com/w/cpp/chrono/time_point) (already in C++11) get a specialized alias `sys_days` equal to `std::chrono::time_point<std::chrono::system_clock, std::chrono::days>`. In other word `sys_days` represent a time point using the system clock and expressed in days. This `sys_days` can be thought as an integer representing a value in days.
- We can convert this `sys_days` time point into a [year_month_day](https://en.cppreference.com/w/cpp/chrono/year_month_day) representation and vice-versa.
This is the same representation of that time point but in a much more human-friendly way: it uses the Gregorian calendar to express that point in time. 
A time point in the Gregorian calendar is made of three parts: a year, a month and a day of the month.
The new standard offers lots of arithmetic operators, conversion operators, helpers structs... to manipulate these parts easily.
- A new type, with a self-explanatory name, [std::chrono::time_zone](https://en.cppreference.com/w/cpp/chrono/time_zone) has been introduced.
If you combine a `sys_days` with a `time_zone`, you obtain a `zoned_time`. `zoned_time` handles convertion from one `time_zone` to another for you.
It is highly convenient! 
- Finally, almost all the types in the `<chrono>` header have convertion facilities to and from strings. It even works with the new [std::format](https://en.cppreference.com/w/cpp/utility/format) library. 

Equipped with this extended `<chrono>` header, you can easily write such things:

```c++
for (auto d = January/9/2019; d.year() < 2020y; d = sys_days{d} + weeks{2}) {
	zoned_time london{"Europe/London", local_days{d} + 18h};    
	cout << london << '\n';    
	cout << zoned_time{"America/New_York", london} << "\n\n";
}
```

In this example, we are displaying the time in "New York" every two weeks, starting from the 9th of January, for the year 2019, when it is 18.00 in "London".
As Howard pointed out, this is far from being trivial to do by hand: both the UK and USA have different daylight savings rules.

Some people may complain of the **verbosity**. Firstly, I find the code very readable even without prior knowledge of this new part of `<chrono>`
Second, **safety** was a key-point in Howard's design. At multiple time, he gave us example on how his design prevents wrongdoings at compile-time. 
For instance: what is a time difference? Can this be considered a date? Can `2 hours` be translated to a date in a calendar? Probably not! 

I am quite eager to get this part of C++20! 

### [Talk] 10 techniques to understand existing code - Jonathan Boccara - 💀★★★:

- Slides: [link](https://meetingcpp.com/mcpp/slides/2019/understand_code.pdf)
- Video: [coming soon]()

**Jonathan Boccara**, known for his awesome blog [fluentcpp.com](https://www.fluentcpp.com/), is always a safe bet when it comes to C++ talks.
You should not necessarily expect learning bleeding-edge techniques with Jonathan, but he is extremely talented at putting words on things!

This time, he was presenting us his favorite approaches to code you have never seen before. Especially, when it comes to intricate code-bases.
My favorite analogy was the **stronghold** one: start your exploration of the code from a place (a function, a routine...) that is crucial in the code-base and that you can easily understand. Like a fog of war in a video-game, the rest of the code is unknown to you at first. But slowly, you can explore the rest of the map/code-base by sending minions/yourself into the callers or the callees related to that function. One strategy to know where to "expand your territory for a maximum of profit" is by looking at call stacks: by jumping in the frames above the current function, this can give you an idea of what is the critical path of your program.
 
Here is an awesome representation, from Jonathan, of callstacks in a video-game universe:

<center><img width=50% height=50% src="{filename}/images/call-stack-fog-of-war.png"/></center>

Not only this applies to decipher a code-base, but it is also a very efficient technique in **reverse engineering**.
When trying to reverse a native application, it is often quite rewarding to put a breakpoint on the system calls: these are your strongholds.
Without source-code, you have very little places where you know what the assembly you are reading does.
System calls are well documented and exposed, so it is naturally a good place to start.

I believe that I am already applying most of these techniques on a daily-basis.
But if I had to explain to a junior programmer what programming on a large code-base is all about, 
I would probably recommend that person to have a look at this talk.

### [Talk] Testing Legacy Code - Fuzzing for Better Input Data - Tina Ulbrich, Niel Waldren - 💀💀★★★:

- Slides: [link](https://meetingcpp.com/mcpp/slides/2019/Testing%20Legacy%20Code%20-%20Fuzzing%20for%20Better%20Input%20Data.pdf)
- Video: [coming soon]()

During such conferences, you may end-up for various reasons (entering the wrong door, following someone, not getting on time to a room...) into a talk that you did not expect on your schedule. Sometimes, you may regret your unfortunate choice as much as `std::vector<bool>` being in the standard, but it can also turn out into your favor: you may discover one of the best presentation of that day. This is exactly what happened to me with the talk from **Tina Ulbrich** and **Niel Waldren** about [fuzzing](https://en.wikipedia.org/wiki/Fuzzing) and unit-testing.
 
Usually, **fuzzing** consists in feeding an application or part of an application with pseudo-random data to explore as much code-path as possible.
The end-goal is to find code-paths that lead to crashes or bugs which can be exploit for malicious purposes.  
Once a exploit found, the fuzzer will often try to reduce the "buggy input" to a minimal set to clearly isolate the corner case.

I have heard about fuzzing for a while, but I never had the opportunity to use it myself.
This technique is really appealing if you are working in the security business or if your application is critical part of system.
If you are developing an application a bit less demanding on the stability, like video-games, fuzzing is not necessarily the number one priority.
**Tina** and **Niel** twisted the usage of fuzzing to find exploits to improve the test-coverage of their library.
They used [libFuzzer](https://llvm.org/docs/LibFuzzer.html) which is, from what I understand, a LLVM library that combine (LLVM's code coverage tool - SanitizerCoverage)[https://clang.llvm.org/docs/SanitizerCoverage.html] with a fuzzer engine like [AFL](http://lcamtuf.coredump.cx/afl/).
**libFuzzer** will try to maximize the code-coverage with the minimum input data.
This is really appealing for all projects relying on unit-tests, which is 

**Tina** and **Niel** did a step by step explanation on how to use **libFuzzer** and what are its benefits:
- How to tweak the random data you receive to valid parameters.
- How to reuse the best input data corpus to write new unit-tests for your application.
- Why you can use this to detect very subtle changes in your API's behaviour. Changes that you would not necessarily wrap with unit-tests.
- ...

I will have a second watch of their talk as soon as their video is available on the conference's Youtube channel.
It was a very innovative topic to me!

### [Talk] Modules - The Beginner's Guide - Daniela Engert - 💀💀★★:

- Slides: [link](https://meetingcpp.com/mcpp/slides/2019/modules-the-beginners-guide-meetingcpp2019.pdf)
- Video: [coming soon]()

Out of the three major language features coming to C++20 (concepts, coroutines and modules), I was the least familiar with **modules**.
The committee is often very active on the standard until the last months before the release of a version. 
While I had a rough idea of module were about in C++, I did not bother to learn about the syntax and the exact implementation.
You never know if the feature you read about in a white paper while look any different in the actual standard!
So, I was very grateful that [Daniela Engert](https://github.com/DanielaE) came up with that talk right before 2020.
Being so close to the standard release, the module part was unlikely to change too much! 

So what are modules in a few words?
Traditionnaly, a C++ code-base is separated into multiple compilation units which are in most case your `.cpp` files.
These compilation units are compiled seperately and combined by the linker.
If you want to share functions or objects between two compilation units, you must have a common interface for them: one or more header files (.h/.hpp) that declare what is available.
The problem is that header files are:

1) Shared in a very primitive way. The `#include` directive is doing dumb copy-paste of the header content into your cpp file.
2) Often full of complicated content for the compiler and not just few declarations. In those, you can have macros, templates, inline functions, include of includes... 

This result in your compiler doing a lot of unecessary work parsing these headers for all the compilation units. 
Wouldn't it be better if compilation units themselves could expose directly what the provide instead of using these hackish headers?
This is exactly what modules try to solve!

So writing a very basic module becomes as simple as writing a `.cpp` file with few annotations to expose what we want:
```
export module my.module; // This is the name of our module
export int e = 42; // Expose a variable.
export int bar() { return foo(e); } // Expose a function.
int foo(int x){ return x; } // No export keyword == no exposition.
``` 

When compiling this `.cpp` file, this will create two others files: an object file that contains binary code (OBJ) and a file for interfacing with that module called Binary Module Interface. Unlike a header file, the BMI file and its associated OBJ file can have a highly **optimized representation** of what is avaible in the module. 

As a user of a module into another compilation unit, you will pass this BMI file as parameter to your compiler and write an import statement:

```
import module my.module; // Ask the compiler to use that module in here.

int main() {  
	std::cout << bar(); // This is using bar from the other module.
}
``` 

And voilà! These are the new C++ module in all their glory.
Except that it gets quite a lot more complicated when you are mixing old header includes, namespaces, special support for standard headers...
**Daniela** was really good at explaining all these quirks that you may encounter in the rough transition that will happen from headers to modules.

As for performance, she observed an improvement from 1546 milliseconds to 62 milliseconds when using a library as a module on a huge-scale project at work. 
This give a lot of hope on what modules will offer to us when avaible on all major compilers!

### [Talk] Compile Time Regular Expressions with Deterministic Finite Automaton - Hana Dusíková - 💀💀★:

### [Talk] C++20 The small things - Timur Doumler - :

### [Talk] The Dawn of a New Error - Phil Nash - :




### [Other]:

There are lot of other talks that would be worth using your **Google-Fu** to find them:

- Using C++20's Three-way Comparison <=> - Jonathan Müller
- Oh No! More Modern CMake - Deniz Bahadir
- C++20 Coroutines - Milosz Warzecha  
- And many more...

You will surely find the **lightning talks** on the [Meeting C++'s Youtube Channel](https://www.youtube.com/user/MeetingCPP/videos) at one point.
These short talks are like snack foods, they vary a lot in their content and quality and don't take long to process. 

# Conclusion:

This was another very fruitful event for the **C++** community. I am glad that our beloved C++ language receive so much attention by its users and the committee. 
It will be interesting to see how long it will take for the major compiler to be fully C++20 compliant: this release is massive!
I was slightly overwhelmed by the quantity of new features.  
I am also wondering how much of the newly acquired C++20 knowledge will stay true once the standard is released.
I guess that I will have to check that by going to another C++ event next year ;) 
