Title: Meta Crush Saga: a C++17 compile-time game
Date: 14:00 04-10-2018 
Modified: 14:00 04-10-2018 
Tags: C++17, TMP, meta programming, constexpr
Slug: meta-crush-saga

## Trivia:
As a quest to obtain the highly coveted title of **Lead Senior C++ Over-Engineer**, I decided last year to rewrite the game I work on during daytime (Candy Crush Saga) using the quintessence of modern C++ (C++17). And... thus was born [Meta Crush Saga](https://github.com/Jiwan/meta_crush_saga): a **compile-time game**. I was highly inspired by [Matt Bernier's Nibbler game](https://blog.mattbierner.com/stupid-template-tricks-snake/) that used pure template meta-programming to recreate our the famous snake game we could play on our Nokia 3310 back in the days.

"What the <s>hell</s> heck is a **compile-time game**?", "What **C++17** features did you use in this project?", "What was your learnings?" might come to your mind. To answer these questions you can either read the rest of this post or accept your inner laziness and watch this talk I made during a Meetup in Stockholm:

<iframe width="560" height="315" src="https://www.youtube.com/embed/XV1lXtB3sqg" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Disclaimer: for the sake of your sanity and the fact that *errare humanum est*, this article might contain some alternative facts.

## A compile-time game you said?

<img width=20% height=20% src="{filename}/images/what-does-this-mean.png"/>

I believe that it's easier to understand what I mean by the "concept" of a **compile-time game** if you compare the life cycle of such a game with the life cycle of a normal game. So here it is!

### Life cycle of a normal game:

As a normal game developer with a normal life working at a normal job with a normal sanity level you would usually start by writing your **game logic** using your favorite language (C++ of course!), then fire your **compiler** to transform this, far too often spaghetti-like, logic into an **executable**. As soon as you double-click on your **executable** (or use the console), a **process** will be spawned by your operating system. This **process** will execute your **game logic** which 99.42% of time consists of a **game loop**. A **game loop** will **update** the state of your game according to some rules and the **user inputs**, **render** the newly computed state of your game in some flashy pixels, again, again and again.

![Life cycle of a normal game]({filename}/images/life-cycle-normal-game.png)

### Life cycle of a compile-time game:

As an over-engineer cooking the next big compile-time game, you will still have use of your favorite language (still C++ of course!) to write your **game logic**. You will still have a **compilation phase** but... then... here comes the plot twist: you will **execute** your **game logic** within this compilation step. This is where your favorite language C++ truly comes in handy ; it has a some features like [Template Meta Programming (TMP)](https://en.wikipedia.org/wiki/Template_metaprogramming) or [constexpr](http://en.cppreference.com/w/cpp/language/constexpr) to actually have **computations** happening during the **compilation phase**. We will dive later on the features you can use to do so. As we are executing the **logic** of the game during this phase, we must also inject the **user inputs** at that point in time. Obviously, our compiler will still output an **executable**. What could it be used for? Well, the executable will not contain any **game loop** anymore, but it will have a very simple mission: output the newly **computed state**. Let's name this **executable** a **renderer** and its **output** the **rendering**. Our **rendering** won't contain any fancy particule effect nor ambiant occlusion shadows, it will be in ASCII. An ASCII **rendering** of your newly computed **state** has the nice property that you can easily show it to your player, but you also copy it into a text file. Why a text file? Obviously because you can combine it with your **code** in some way, redo all the previous steps and therefore have a **loop**.

As you may understand now, a **compile-time** game is made of a **game-loop** where each **frame** of your game is a **compilation step**. Each **compilation step** is computing a new **state** of your game, that you can present to your player and also inject to the following **frame** / **compilation step**. 

I let you contemplate this magnificient diagram for as much time as it takes you to understand what I just wrote above:
![Life cycle of a compile-time game]({filename}/images/life-cycle-compile-time-game.png)

Before we move on the implementation details of such a loop, I am sure that you have one question you would like to throw at me...

### Why would you even do that?
<img width=25% height=25% src="{filename}/images/why-would-you-even-do-that.png"/>

Well, it's pretty easy:

- <s> Safer than Rust</s>
