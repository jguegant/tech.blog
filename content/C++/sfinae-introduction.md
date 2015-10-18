Title: An introduction to C++'s SFINAEs: compile-time introspection of a class member
Date: 14:00 10-18-2015 
Modified: 14:00 10-18-2015
Tags: C++11, C++14, TMP, meta programming
Slug: sfinae-introduction
Status: draft

<!-- http://stackoverflow.com/questions/18570285/using-sfinae-to-detect-a-member-function -->
###Trivia:
As a C++ enthusiast, I usually follow the annual C++ conference [cppconf](http://cppcon.org/) or at least try to keep myself up-to-date with the major events that happen there. One way to catch up, if you can't afford a plane ticket or the ticket, is to follow the [youtube channel](https://www.youtube.com/channel/UCMlGfpWw-RUdWX_JbLCukXg) dedicated to this conference. I was impressed by **Louis Dionne** talk entitled "C++ Metaprogramming: A Paradigm Shift". One feature called **is_valid** that can be found in Louis's [Boost.Hana](http://ldionne.com/hana/) library particulary caught my attention. This genious **is_valid** function heavily rely on an even more "magic" C++ programming technique coined with the term **SFINAE** discovered at the end of the previous century. If this acronym doesn't speak to you, don't be scared, we are going to dive straight in the subject.

###The problem: