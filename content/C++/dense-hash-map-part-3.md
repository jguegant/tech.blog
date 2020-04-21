Title: Making a STL-compatible hash map from scratch - Part 2 - The wonderful world of iterators and allocators
Date: 17:40 04-21-2020 
Modified: 17:40 04-21-2020
Tags: C++17, hash map, unordered_map, iterator, allocator
Slug: dense-hash-map3

This post is part of a series of posts:

- [Part 1 - Beating std::unordered_map]({filename}../C++/dense-hash-map.md)
- [Part 2 - Growth Policies & The Schrodinger std::pair]({filename}../C++/dense-hash-map-part-2.md)**
- **Part 3 - The wonderful world of iterators and allocators (Current)**
- Part 4 - ... (Coming Soon)

In the [previous post]({filename}../C++/dense-hash-map-part-2.md), we prepared our data-structure to be able to store our key/value pairs in a performant way: our design permit us to expose, for safety, immutable keys to our users while internally having mutable access for speed. We also had fun with more bit magic to create a special growth policy for our bucket container. You can find a reference implementation [right here](https://github.com/Jiwan/dense_hash_map).

At this point, you are probably eager to start working on the algorithms of our `dense_hash_map`. Alas, we are not there yet! Two new kind of challengers entered the arena: **allocators** and **iterators**. Like any word finishing by "or" (Terminator, Alligator, Abductor, Debtor, Elevator, Moderator, Emperor...) there is a certain violence or authority coming out of it of these twos. And rightfully so, having those in your project is a good indicator that you will spend nights banging your head against a brick wall.

Let me be your mentor and I will guide you through these tough areas!

<center><img width=40% height=40% src="{filename}/images/terminator.jpg" alt="Terminator"/></center>

# Part 3 - The wonderful world of iterators and allocators:

## Two iterators with two different endeavors:

If we base ourselves on the [unordered_map's interface](https://en.cppreference.com/w/cpp/container/unordered_map), we should have at least four different sorts of iterator:


| *Name*                   | *Description*                                                      |
|--------------------------|--------------------------------------------------------------------|
| **iterator**             | Iterate through all key/value pairs of the map                     |
| **const_iterator**       | Similar to iterator but yields const references to the pairs       |
| **local_iterator**       | Iterator through all the key/value pairs in one bucket             |
| **const_local_iterator** | Similar to local_iterator but yields const references to the pairs |



It becomes clear that we will actually need to create only two types of iterators: **iterator** and **local_iterator**. The other two can be easily derived from the first ones. We will just sprinkle some `const` where we should.

### Crafting an iterator:

If you wonder which kind of iterator to tackle first, `iterator` and its little bro `const_iterator` are probably the more interesting ones for our users.
Quite often you will want to iterate through all key/value pairs to perform some operations and this is what `iterator` is dedicated for.
More precisely, `iterator` is the type returned by [begin](https://en.cppreference.com/w/cpp/container/unordered_map/begin), [end](https://en.cppreference.com/w/cpp/container/unordered_map/end) & Co. which permits you to create a range-based for loop such as:

```c++
for (auto& [key, value] : my_map) {
    std::cout << key << ", " << value << "\n";
}
```

The modern picasso in me decided to show you what this range-loop would do internally:

<center><img width=50% height=50% src="{filename}/images/dense-hash-map-iterator.webp" alt=""/></center>

Yes, it should be as simple as iterating in our `nodes_` container. No, it won't be as easy you may think.

To iterate over the `nodes_` container, we can simply use its own... iterators. Conveniently, `nodes_`'s iterator type is also following the concept
[LegacyForwardIterator](https://en.cppreference.com/w/cpp/named_req/ForwardIterator) which is also needed for our `dense_hash_map::iterator` type.
On the other hand, `nodes_`'s iterator type has `node<Key, T>&` as its `reference` type when we need `std::pair<const Key, T>&` for `dense_hash_map::iterator`.
What we need is a projection onto the member `pair` of `node<Key, T>` while iterating over `nodes_`.

In an ideal world, we would have a **C++20** compiler shipped with a fully **C++20** compliant standard library. Within it, we would have the [holly range library](https://en.cppreference.com/w/cpp/ranges), which would permit to lazily transform our `nodes_` into another one:

```c++
// ...
class dense_hash_map {
    // ...
    auto begin() {
        return projected_range().begin();
    }

    auto end() {
        return projected_range().end();
    }

private:
    auto projected_range() {
        return nodes_ | std::views::transform([](auto& node){ return node.pair; });
    }
    // ...
};
```
With all the fuss around the range library...


### Crafting a local iterator:

I hate this name. For the users it is probably used to debug the map.

<center><img width=50% height=50% src="{filename}/images/dense-hash-map-local-iterator.webp" alt=""/></center>

`ForwardIterator`


## A special constructor for allocators:



## Conclusion:

We survived this first day of our journey! We can control the growth of our container using a policy pattern.
We also have a **Schrodinger std::pair** at our disposal to move our key/value pairs blazingly fast accross memory while preventing our users to shoot themselves in the feet.

Be ready for the next phase: the dreaded iterators and allocators are waiting for you!
