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
that have been researching for years how to make the quintessence of an associative container.
While the one I am presenting here has really decent performance (more so than the standard ones at least), it is not bleeding-edge.
I encourage you to read this post as an introduction to the wonderful world of hash maps then explore a bit more what these talented people have produced recently.

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
When a **key/value pair** is **inserted**, the **key** is somehow **hashed** and adjusted (usually using modulo on the amount of buckets) to find which bucket it belongs to, and the key/value pair gets inserted into that bucket. 
Here, the **key1** and **key2** somehow ended-up belonging to the **bucket 1**.
Whereas the **key3** belongs to the **bucket 5**.  
When doing a lookup using a key, the key is hashed and adjusted to find the bucket it should belong to.
The bucket of the key is **iterated** until the key is found or the end of the bucket is reached (meaning no key is in the map). 
Finally, the buckets are linked between each others to be able to do a traversal of all the key/value pairs within the `std::unordered_map`.

This memory layout is **really bad** for your CPU!
Each of the nodes of the linked-list(s) could be spread accross memory and that would play against all the caches of your CPU.
Traversing buckets made of a linked-list is slow, but you could pray that your hash function save you by spreading keys as much as possible and therefore have tiny buckets.
But even the most brilliant hash function will not help you with a common use-case of an associative container: iterating through all the key/value pairs.
Each dereference of the pointer to the next node will be a huge drag on your CPU.
On other hand, since each node are separately allocated, they can stay wherever they are in memory even if others are added or removed, which provides **stable addressing**.

So what could we obtain if we were to free ourselves from **stable addressing**?
Well, we could wrap our buckets into contiguous memory like so:

<center><img width=50% height=50% src="{filename}/images/dense_hash_map_layout.png" alt="dense_hash_map layout"/></center>

Here we are still keeping a linked-list for each buckets, but all the nodes are stored in a vector, therefore one after each others in memory.
Let's call this a **dense hash map.**
Instead of using pointers between nodes, we are expressing their relations with indexes within the vector: here the node with **key1** store a "next index" having a value of **2** which is the index of the node with **key2**. And all of that is a huge improvement! We are gaining on all fronts:
- Iterating over all the key/value pairs is as fast as iterating over a vector, which is lightning fast.
- We are saving a pointer on all nodes - the "prev pointer". We don't need any sort of reverse-traversal of the bucket. 
- We don't need to maintain a begin and end pointer for the list of nodes.
- Even iterating over a bucket could be faster as the node shouldn't be too scattered in memory since they all belong to one vector.

With that said, the **stable addressing** is now gone: any insertion into the vector could produce a reallocation of its internal buffer, ending in a massive move of all the nodes accross memory. So what if your user really need stable addressing? As **David Wheeler** would say: "just use another level of indirection".
Instead of a using a `dense_hash_map<Key, Value>`, your user can always use a `dense_hash_map<Key, unique_ptr<Value>>`: 

<center><img width=50% height=50% src="{filename}/images/dense_hash_map_unique_ptr_layout.png" alt="layout"/></center>

We are reintroducing pointers, which is obviously not great for the cache again.
But this time when iterating over all the key/value pairs you will very likely see a substantial improvement over the first layout.
The pattern of the nodes is clearly more predictable and some sort of prefetching CPU minions may come to your help. 

#### Controlling the growth


### Design
No node interface...


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
