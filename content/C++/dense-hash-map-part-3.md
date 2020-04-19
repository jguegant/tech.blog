Title: Making a STL-compatible hash map from scratch - Part 2 - The wonderful world of iterators and allocators
Date: 17:40 04-21-2020 
Modified: 17:40 04-21-2020
Tags: C++17, hash map, unordered_map, iterator, allocator
Slug: dense-hash-map3

This post is part of a series of posts:

- [Part 1 - Beating std::unordered_map]({filename}../C++/dense-hash-map.md)
- [Part 2 - Growth Policies & The Schrodinger std::pair]({filename}../C++/dense-hash-map-2.md)**
- **Part 3 - The wonderful world of iterators and allocators (Current)**
- Part 4 - ... (Coming Soon)

In the [previous post]({filename}../C++/dense-hash-map-2.md), we prepared our data-structure to be able to store our key/value pairs in a performant way: our design permit us to expose, for safety, immutable keys to our users while internally having mutable access for speed. We also had fun with more bit magic to create a special growth policy for our bucket container.

At this point, you are probably eager to start working on the algorithms of our `dense_hash_map`. Alas, we are not there yet! Two new kind of challengers entered the arena: **allocators** and **iterators**. Like any word finishing by "or" (Terminator, Alligator, Abductor, Debtor, Elevator, Moderator, Emperor...) there is a certain violence or authority coming out of it of these twos. And rightfully so, having those in your project is a good indicator that you will spend nights banging your head against a brick wall.

Let me be your mentor and I will guide you through these tough times!

# Part 3 - The wonderful world of iterators and allocators:

## Two iterators with two different endeavors:

If we base ourselves on the [standard](https://en.cppreference.com/w/cpp/container/unordered_map), we should have at least four different sort of iterators:

| name                 | description |
|----------------------|-------------|
| iterator             |             |
| const_iterator       |             |
| local_iterator       |             |
| const_local_iterator |             |


<center><img width=40% height=40% src="{filename}/images/terminator.jpg" alt="Terminator"/></center>


### Full range iterator:

### Bucket iterator


## A special constructor for allocators:



## Conclusion:

We survived this first day of our journey! We can control the growth of our container using a policy pattern.
We also have a **Schrodinger std::pair** at our disposal to move our key/value pairs blazingly fast accross memory while preventing our users to shoot themselves in the feet.

Be ready for the next phase: the dreaded iterators and allocators are waiting for you!
