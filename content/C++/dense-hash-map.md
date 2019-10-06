Title: Making a STL-compatible hash map from scratch in C++20.
Date: 17:40 06-10-2019 
Modified: 17:40 06-10-2019
Tags: C++20, hash map. 
Slug: dense-hash-map 
Status: 

## Trivia:
If C++ had an equivalent in the video game world, it would be similar to Dark Souls: a dark, violent, punishing game.
Yet, the emotion you get after successfully assimilating all the moves required to overcome a challenge is absolutely impossible to replicate.
You are able to reproduce a sort of dance to defeat any boss in your way.
Speaking of which... what could be the final boss of C++?
According to [Stephan T. Lavavej (STL)](https://twitter.com/stephantlavavej) this would be the [Floating-Point charconv of the C++17's standard](https://cppcon2019.sched.com/event/Sft8/floating-point-charconv-making-your-code-10x-faster-with-c17s-final-boss).
While I wouldn't be able to beat this boss by myself, I can tackle a smaller boss: making a standard-compatible `unordered_map` from scratch.
I would like to share with you how to beat this smaller boss by yourself!

<center><img width=35% height=35% src="{filename}/images/dark-souls.webp" alt="Dark Souls"/></center>

Disclaimer: there are lot of extremely talented people (abseil team with their Swiss Tables, Malte Skarupke's flat hash map...) 
that have been researching for years how to make the perfect associative container.
While the one I am presenting here has decent performance (more so than the standard ones at least), it is not bleeding-edge.
I encourage you after this post to have a look at what these talented people have produced recently.

### Freeing ourselves from the standard constraints:

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
**Stable addressing** means that the insertion or deletion of a **key/value pair** in a `std::unordered_map` should not affect the memory location of other **key/value** pairs in the same `std::unordered_map`. More precisely, the standard does not mention, in the [Effects](https://eel.is/c++draft/unord.map.modifiers) sections of std::unordered_map's modifiers, anything about reference, pointer or iterator invalidation.

This forces any standard implementation of `std::unordered_map` to use linked-list for the buckets of pairs rather than contiguous memory.
`std::unordered_map` should look roughly like this in memory:

<center><img width=50% height=50% src="{filename}/images/unordered_map_layout.png" alt="unordered_map layout"/></center>

As you can see, the **entries** are stored in a giant **linked-list**. Each of the **buckets** are themselves **sub-parts** of the linked-list.
Here each colors represent different buckets of key/value pairs.
When a **key/value pair** is **inserted**, the **key** somehow **hashed** and adjusted (usually using modulo on the hash) to find which bucket it belongs to, and the key/value pair gets inserted into that bucket. 
Here, the **key1** and **key2** somehow ended-up belonging to the **bucket 1**.
Whereas the **key3** belongs to the **bucket 5**.  
When doing a lookup using a key, the key is hashed and adjusted to find the bucket it should belong to
The bucket of the key is iterated until the key is found or the end of the bucket is reached (meaning no key is in the map). 
Finally, the buckets are linked between each others to be able to do a traversal of all the key/value pairs within the `std::unordered_map`.

This memory layout is **really bad** for your CPU!
Each of the nodes of the linked-lists could be spread accross memory.
This makes could jam all the caches of your CPU.
On other hand, since each node are separately allocated, they can stay wherever they are in memory , which provides **stable addressing**.

Sure, but what if I really wanted stable addressing?


#### Controlling the growth

### Design

####
####

#### Implementation



#####

#####

#####

### Conclusion:

- If you are inserting a new pair into an **associative container** consider using `try_emplace` first.
- If you cannot use **C++17**, prefer to use `emplace` over `insert`.
- If you are cannot use **C++11**, I feel sorry for you!
- You can borrow my `lazy_convert_construct` if you are dealing with smart pointers and `try_emplace`, to get a blazzing fast insertion.

A special thanks to my colleague Yo Anes with whom I had a lot of fun discussing this specific topic.
