Title: Meta Crush Saga: a C++17 compile-time game
Date: 14:00 04-10-2018 
Modified: 14:00 04-10-2018 
Tags: C++17, TMP, meta programming, constexpr
Slug: meta-crush-saga

## Trivia:
As a quest to obtain the highly coveted title of **Lead Senior C++ Over-Engineer**, I decided last year to rewrite the game I work on during daytime (Candy Crush Saga) using the quintessence of modern C++ (C++17). And... thus was born [Meta Crush Saga](https://github.com/Jiwan/meta_crush_saga): a **compile-time game**. I was highly inspired by [Matt Bernier's Nibbler game](https://blog.mattbierner.com/stupid-template-tricks-snake/) that used pure template meta-programming to recreate our the famous snake game we could play on our Nokia 3310 back in the days.

"What the <s>hell</s> heck is a **compile-time game**?", "How does it looks like?", "What **C++17** features did you use in this project?", "What was your learnings?" might come to your mind. To answer these questions you can either read the rest of this post or accept your inner laziness and watch the video version of this post, a talk I made during a Meetup event in Stockholm:

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

Before we move on the implementation details of such a loop, I am sure that you have one question you would like to shoot at me...

### "Why would you even do that?"
<img width=25% height=25% src="{filename}/images/why-would-you-even-do-that.png"/>

Do you really think I would let you break my C++ meta-programming idyll with such a fundamental question? Never!

- First and foremost, a **compile-time game** will have amazing runtime performances since most of the computations are done during the **compilation phase**. Runtime performance is a key to the success of your AAA game in ASCII art! 
- You lessen the probability that a wild crustacean appears in your github repository and ask you to rewrite your game in **Rust**. His well-prepared speech on security will fall appart as soon as you explain that a dangling pointer cannot exist at compile-time. Smug **Haskell** programmers might even approve the **type-safety** of your code.
- You will gain respect from the **Javascript** hipster kingdom, where any over-complicated framework with a strong NIH syndrom can reign as long as it has a catchy name.
- One of my friend used to say that any line of code from a Perl program provides you de-facto a very strong password. I surely bet that he never tried generating credentials from **compile-time C++**.

So what? Aren't you satisfied with my answers? Maybe your question should have been: "Why could you even do that?".

As a matter of fact, I really wanted to play with the features introduced by C++17. Quite a few of them focus on improving the expressiveness of the language as well as the meta-programming facilities (mainly constexpr). Instead of writing small code samples, I thought that it would be more fun to turn all of this into a game. Pet projects are a nice way to learn concepts that you may not use before quite some time at work. Being able to run the core logic of your game at compile-time proves once a again that templates and constepxr are [turing complete](https://en.wikipedia.org/wiki/Turing_completeness) subsets of the C++ language.


## Meta Crush Saga: an overview

### A Match-3 game:

**Meta Crush Saga** is a [tiled-matching game](https://en.wikipedia.org/wiki/Tile-matching_video_game) similar to **Bejeweled** or **Candy Crush Saga**. The core of the rules consists in matching three or more tiles of the same pattern to increase your scores. Here is sneak peek of a **game state** I "dumped" (dumping ASCII is pretty damn easy): 

    :::c++
    R"(
        Meta crush saga      
    ------------------------  
    |                        | 
    | R  B  G  B  B  Y  G  R | 
    |                        | 
    |                        | 
    | Y  Y  G  R  B  G  B  R | 
    |                        | 
    |                        | 
    | R  B  Y  R  G  R  Y  G | 
    |                        | 
    |                        | 
    | R  Y  B  Y (R) Y  G  Y | 
    |                        | 
    |                        | 
    | B  G  Y  R  Y  G  G  R | 
    |                        | 
    |                        | 
    | R  Y  B  G  Y  B  B  G | 
    |                        | 
    ------------------------  
    > score: 9009
    > moves: 27
    )"

The game-play of this Match-3 is not so interesting in itself, but what about the architecture running all of this? To understand it, I will try to explain each part of the life cycle of this **compile-time** game in term of code.

### Injecting the game state:
<img width=70% height=70% src="{filename}/images/injecting-game-state.png"/>

As a C++ afficionados or a nitpicker, you may have noticed that my previous dumped game state started with the following pattern: **R"(**. This is indeed a [C++11 raw string literal](http://en.cppreference.com/w/cpp/language/string_literal), meaning that I do not have to escape special characters like **line feed**. This raw string literal is stored in a file called "current_state.txt".

How do we inject this current game state into a compile state? Let's include it into the loop inputs!

    :::c++
    // loop_inputs.hpp

    constexpr KeyboardInput keyboard_input = KeyboardInput::KEYBOARD_INPUT;

    constexpr auto get_game_state_string = []() constexpr
    {
        auto game_state_string = constexpr_string(
                #include "current_state.txt"
        );
        return game_state_string;
    };



### Compile time computation of the new state:
<img width=40% height=40% src="{filename}/images/compile-time-computation-new-state.png"/>


## My C++17 learnings

## Meta Crush Saga II: looking for a pure compile-time experience