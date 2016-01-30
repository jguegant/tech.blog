Title: An introduction to C++'s variadic templates: a thread-safe multi-type map
Date: 14:00 02-01-2016 
Modified: 14:00 02-01-2016
Tags: C++11, C++14, variadic templates, meta programming
Slug: thread-safe-multi-type-map

###Trivia:
One of our favorite motto in our C++ team at work is: you shall use **dependency injections** instead of **singletons**! It actually comes with our unit-testing strategy. If the various components of your architecture are too tightly coupled, it becomes a tremendous effort to deeply test small critical chunks of your code. **Singletons** are that kind of beast that revives itself without your permission and comes from hell to haunt your lovely unit-tests. Our main project being multi-threaded (hence highly bug-prone) and vital for the company, "**singleton**" became a forbidden word. Yet, our team recently started going down the dark path. Thanks to C++11 and its variadic templates, I carefully crafted a **thread-safe multi-type map container** that simplified our configuration reloading system and saved us from the dark side of the coder force. If you always wondered what are **variadic templates**, how **C++11's tuples** can be implemented, I am going to present these concepts in this post with my map container as a cobaye. 

### Why would I use a thread-safe multi-type map container?
Let me explain our odyssey: we are working on a highly modular and . One





Note: for the sake of your sanity and the fact that *errare humanum est*, this article might not be 100% accurate!