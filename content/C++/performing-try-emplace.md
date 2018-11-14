Title: How to make your maps, try_emplace and unique_ptrs play nicely with each others in C++.
Date: 14:00 17-11-2018 
Modified: 14:00 17-11-2018 
Tags: C++17, std::map, std::unordered_map. 
Slug: performing-try-emplace 

## Trivia:
Lately, I have been working on the reincarnation of a **class** at work: a hash map. 
While this class had interesting internals (a sort of dense hash map) and performed really well, its interface was not up to standard both literaly and metaphorically.
After much of lipstick applied to it, the **class** now fully mimic the interface of the beloved [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map) from the standard library.
A close look on **std::unordered_map** and its sister [std::map](https://en.cppreference.com/w/cpp/container/map) reveals few interesting design choices.
Combining this interface with some smart pointer types can present some challenges to squeeze performance out of your maps.
We will explore these challenges in this blog post, and try to figure out some solutions.

Disclaimer: C++ being C++, I would not be suprise if 1) I wrote some unacurracies here 2) Some guru could reduce this entire article in a phantasmagoric one liner.

### Some peculiar modifier member functions:

Note: This part of the post will serve as a quick reminder for some of the folks that are not well versed in the associative containers of the standard. If you are confident, jump straight to the dilemna part. 

If you observe the interface of the associative containers (like [std::map](https://en.cppreference.com/w/cpp/container/map) or [std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map)) in the current standard you will notice that there are 6 member functions to map a value to a given key: **insert**, **insert_or_assign**, **emplace**, **emplace_hint**, **try_emplace** and the **subscript operator** (operator[]). That number does not include all the overloads for each of these member functions. It is not a wonder that a lot of C++ users will tend to do suboptimal calls to insert values in their associative containers, the choice is not always obvious when you have 6 different functions with slightly different behaviour. 


Typically, you will often this pattern within a code-base:
```c++
std::unordered_map<std::string, std::string> m;

// Check if the key is already in m.
if (m.find("johannes") == m.end()) { // Often written as m.count("johannes") == 0
	m["johannes"] = "lucio"; // If not insert they key
}
```

Little did your colleague, boss, or tired ego know that such a code will do twice a relatively costly job: checking the existence of the key in the map.
Indeed, in the case of a **std::unordered_map**, the key **"Johannes"** will be hashed twice: in **find** and in the **operator[]**. In both member functions, the **std::unoredered_map** has to know in which bucket the key will fall into. Worst! If you are having collisions between your keys, checking the existence of a key may induce up to N comparisons (even your hash function can be drunk sometimes) where N is the amount of stored key-value pairs. Potentially mutiplying these comparisons by two is not something you should desire. Such a situation in **std::map** is even worst, this will always bring roughly O(log(N)) comparisons. Comparing two **std::string** is not as cheap as it may seem and if you add on top of that the cost of jumping through a linked list of nodes, this is NOT great.

Obviously the answer to this problem is to use [insert](https://en.cppreference.com/w/cpp/container/map/insert). **insert** as it names imply, will only work if it can insert the key in the associative container, meaning that the insertion will not happen if the same key is already in the map. If you really care to know whether the insertion happend, **insert** will return a **pair** of an iterator and a boolean that you can query. The iterator points to the inserted key-value pair or the already existing one, the boolean indicates whether the iterations happened.
```c++
// Use C++17 structured bindings and class template argument deduction (CTAD)
// See more on my previous post on that topics
auto [it, result] = m.insert(std::pair("johannes", "lucio"));
```
Here only one check for the existence will be done, that is much better, isn't it?
Well, while this snippet is shorter and performs better, there is still room for improvement. 

Speak about emplace to optimize for constructing and avoid mentioning pair.

Then bring **try_emplace** as a stronger guaranty that things won't be moved. 

### The dilemna of map of unique_ptrs:
### Early memory allocation or comparisons:

#### A hacky solution:

#### The results:

### The missing constructor:

### Conclusion:
Thanks to my colleague Yo Anes who I had a lot of fun discussing this topics.
