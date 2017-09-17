Title: From strings to types in C++: a compile-time maze
Date: 14:00 01-10-2016 
Modified: 14:00 01-10-2016
Tags: C++11, C++14, C++17, TMP, meta programming, constexpr
Slug: meta-crush-saga
Status: draft

### Trivia:
As a quest to obtain the hihgly coveted title of **Lead Senior C++ Over-Engineer**, I recently decided to rewrite the game I work on during daytime (Candy Crush Saga) using the quintessence of modern C++. And... thus was born [Meta Crush Saga](https://github.com/Jiwan/meta_crush_saga). I was highly inspired by [Matt Bernier's Nibbler game](https://blog.mattbierner.com/stupid-template-tricks-snake/) that used pure template meta-programming to recreate our the famous snake game we could play on our Nokia 3310 back in the days.

**C++17** is offering us new tools ~~to shoot yourself in the foot~~ ease our pain when practicing the dark art of computing at compile-time: constexpr lambdas, if constexpr, std::variant... Implementing a simple game was a nice hobby project to master the features of this new C++ standard.

I will try to share my learnings with this blog post. Hopefully this will inspire you to delve into this dark art too!

Disclaimer: for the sake of your sanity and the fact that *errare humanum est*, this article might contain some alternative facts.

### A compile-time game?

A traditional game is made to be compiled and run in this way:


![Normal flow of a game]({filename}/images/normal-game.svg)

First you compile the **source code** of your game using your favorite **compiler** in order to get an **executable**. Then, when you are in the mood of playing your game, you start the **executable** and interact with the game. The game usually consits of a **game-loop**: get new **inputs** => **update** => **draw** => get new **inputs** => ... 

A **compile-time game** would look like this:
![Compile time game]({filename}/images/meta-game.svg)

![Compile time game]({filename}/images/meta-game-advanced.svg)

Safer than Rust, faster than C, more hipster than the latest web framework to divide booleans in JavaScript. When you live in a cold scandinavian country like me, you might want to heat up the CPU.