Title: My favorite pizzeria is asynchronous and event-driven... my C++ server too
Date: 14:00 01-10-2016 
Modified: 14:00 01-10-2016
Tags: C++14, Python, event-driven, asynchronous architecture
Slug: asynchronous-pizzeria

## About this post:
Computer programming is a science, or even an art, and as such its community follows trends for better or worse. Today, I am highly positive in our future so let's speak about the new holy grail of any back-end developer, the panacea for web servers: an **asynchronous** **event-driven** architecture. Forget about your old synchronous habits, now we enter in the era of **non-blocking I/O** models, **coroutines**, **callbacks**, hacky **generators**, and all-mighty **asynchronous calls**. [Node.js](https://nodejs.org/en/) is conquering the market partly due to its full embrace of such an architecture. Google's latest child, the [Go](https://golang.org/) Programming Language, was designed around this concept. Why would we not do the same?

I could directly dive into some funky tricks to implement **stackless coroutines** in **C++14**, or explain **epoll** in details. Yet the very basic internals of such technologies are pretty mysterious for some of us, when it actually has a very straightforward explanation. Why is it more efficient than old-fashioned technologies? There must be a thread somewhere? Where is the loop then?

As a developer, it is also sometimes handy to explain why spending 4 developers to rework a software architecture is actually cheaper than scaling with hardware. Especially, if your interlocutor is a greedy stakeholder or any kind of non-technical-boss on top of you. 

This post will focus on these fundamentals questions, and it will a base for some coming topics. I would not dare to simply throw you **spaghetti code**, so let's first explain these concepts using **pizzas**.

### **Apach' Hut** vs **Ngin O' Pepperonix**:
In the 21th century, there are two domains where **servers** are forestanding: restaurants and computer science. If the former domain was the inspiration for the second-one, it must be quite straightforward to do an analogy of the two worlds. In any case, we want to deliver FAST our clients' requests.

We will soon discover the Secret Recipe that **Ngin O' Pepperonix** used to conquer a great part of **Apach' Hut's** market shares. Or is it the recipe?

#### **Apach' Hut's** traditional management:

**Apach' Hut** was the favorite pizza food delivery brand in the Silicon Valley for the past decade. Everyone love the quality of their pizzas, the staff and its clean online menu. Everyone recognise that the on-call delivery of **Apach' Hut** is usually pleasing, but it simply can't cope the amount of clients during rush hours. From an external point of view, it looks like the pizza delivering process is satured very quickly at lunch time. Their website becomes equally unreachable. On contrary, some pretend that **Ngin O' Pepperonix** is flawless on that point: hell, it even handles gaming events.

##### In the kitchen:
Let's take a look on how is a phone request served in **Apach' Hut**:

1. A client grabs his phone, dials **Apach' Hut's** phone number and wait for an answer whilst glancing at the menu.  
2. Once available, a call center agent available picks up the call and takes note of the client's request. Most of the calls last in average **5min**. The agent then dispatches the request to a cook, **IF** available.
3. Cooks, themselves, are waiting **passively** in room for a request. Sometimes, they may have time to read a book for **20min** ; but in rush hours, they barely enter the waiting-room that the call center center yells at them a new request.
4. Once a cook acquires a pizza request, he will head to the warehouse to get ingredients. If lucky, the warehouse contains enough tomatoes, shrooms, bacon... But it is not unusual that the warehouse is out of stock in one of the precious substance for an amazing pizza. The agent must therefore **wait passively** for the next delivery from the main warehouse between **0 to 30min**.
5. After the warehouse detour, finally starts the cook's mission. The cook shines for **15min**, during which he magically executes his own recipe (his grand-parent, Mario, would be proud of his Italian skills on margherita pizzas).
6. Time to put the pizza in the oven and... light a cigarette. Anyway the cook must wait **30min**, **taskless**.
7. Finally, the cook wraps the pizza in its box and gives it to one of these crazy delivery boys we are used to in Europe. Sadly, the cook cannot process to another pizza before he ensures that the client is satisfied, **20min** lost in average...

![Apach' Hut Strategy Scheme]({filename}/images/apachehut.svg)

Did you catch any problem in this strategy? Anything else than the fact that a traditional pizza would be burn after 20min at 210°C? 

Effectively this management is inefficient as Apach' cooks spend a good part of their days doing nothing more than waiting. 

#### **Ngin O' Pepperonix** solution:

![Ngin O' Pepperonix Strategy Scheme]({filename}/images/nginxopepperoni.svg)

If I am not waiting, then who will do it for me?

#### Real code:
