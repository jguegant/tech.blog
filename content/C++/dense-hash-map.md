Title: Making a STL-compatible hash map from scratch in C++20.
Date: 17:40 06-10-2019 
Modified: 15:35 18-11-2018 
Tags: C++20, hash map. 
Slug: dense-hash-map 
Status: draft

## Trivia:
If C++ had an equivalent in the video game world, it would be similar to Dark Souls: a dark, violent, punishing game.
Yet, the emotion you get after successfully assimilating all the moves required to overcome a challenge is absolutely impossible to replicate.
You are able to replicate a sort of dance to defeat any boss in your way.
Speaking of which... what could be the final boss of C++?
According to [Stephan T. Lavavej (STL)](https://twitter.com/stephantlavavej) this would be the [Floating-Point charconv of the C++17's standard](https://cppcon2019.sched.com/event/Sft8/floating-point-charconv-making-your-code-10x-faster-with-c17s-final-boss).
While I wouldn't be able to beat this boss by myself, I can tackle a smaller boss: making a standard-compatible `unordered_map` from scratch.
I would like to share with you how to beat this smaller boss by yourself!

Disclaimer: there are lot of extremely talented people (abseil team with Swiss Tables, Malte Skarupke's flat hash map...) 
that have been researching for years how to make the perfect associative container.
While the one I am presenting here has decent performance (more so than the standard ones at least), it is not bleeding-edge.
I encourage you after this post to have a look at what these talented people have produced recently.

### Unleashing the standard constraints:

Implementing a standard associative container like `std::unordered_map` wouldn't be satisfying enough.
We have to do better! Let's make a faster one! 

The standard library (and its ancestor the STL) is almost as old as me.
You would think that the people working on an implementation of it (libc++, libstdc++...) would have had enough to polish it until there is no room to improvement.
So how could we beat them in their own domain? Well... we are going to cheat... but in a good way.

The standard library is made to be used by the commoners.
The noble ladies and gentlemen in the standard committee instored some constraints to protect us from killing ourselves while using their `std::unordered_map`. 
May this over-protective behaviour be damned! We know better! 

#### Breaking stable addressing

The standard implicitely mandates **stable addressing** for any implementation of `std::unordered_map`.
**Stable addressing** means that the insertion or deletion of a **key/value pair** in a `std::unordered_map` should not affect the memory location of other **key/value** pairs in the same `std::unordered_map`. More precisely, the standard does not mention in the [Effects](https://eel.is/c++draft/unord.map.modifiers) sections of std::unordered_map's modifiers anything about iterator invalidation.


Sure, but what if I really wanted stable addressing?


#### Controlling the growth


#### 

### Conclusion:

- If you are inserting a new pair into an **associative container** consider using `try_emplace` first.
- If you cannot use **C++17**, prefer to use `emplace` over `insert`.
- If you are cannot use **C++11**, I feel sorry for you!
- You can borrow my `lazy_convert_construct` if you are dealing with smart pointers and `try_emplace`, to get a blazzing fast insertion.

A special thanks to my colleague Yo Anes with whom I had a lot of fun discussing this specific topic.
