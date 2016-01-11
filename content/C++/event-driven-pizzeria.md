Title: My favorite pizzeria is asynchronous and event-driven... my C++ server too
Date: 14:00 01-10-2016 
Modified: 14:00 01-10-2016
Tags: C++14, Python, event-driven, asynchronous architecture
Slug: asynchronous-pizzeria

## About this post:
Computer programming is a science, or even an art, and as such its community follows trends for better or worse. Today, I am highly positive in our future so let's speak about the new holy grail of any back-end developer, the panacea for web servers: an **asynchronous** **event-driven** architecture. Forget about your old synchronous habits, now we enter in the era of **non-blocking I/O** models, **coroutines**, **callbacks**, hacky **generators**, and all-mighty **asynchronous calls**. [Node.js](https://nodejs.org/en/) is conquering the market partly due to its full embrace of such an architecture. Google's latest child, the [Go](https://golang.org/) Programming Language, was designed around this concept. Why would we not do the same?

I could directly dive into some funky tricks to implement **stackless coroutines** in **C++14**, or explain **epoll** in details. Yet the very basic internals of such technologies are pretty mysterious for some of us, when it actually has a very straightforward explanation. Why is it more efficient than old-fashioned technologies? There must be a thread somewhere? Where is the loop then?

This post will focus on these fundamentals questions, and it will a base for some coming topics. I would not dare to simply throw you **spaghetti code**, so let's first explain these concepts using **pizzas**.

### **Apache Hut** vs **Nginx O' Pepperoni**:
In the 21th century, there are two domains where **servers** are forestanding: restaurants and computer science. If the former domain was the inspiration for the second-one, it must be quite straightforward to do an analogy of the two worlds. In any case, we want to deliver FAST our clients' requests.

We will soon discover the Secret Recipe that **Nginx O' Pepperoni** used to conquer a great part of **Apache hut's** market shares. Or is it the recipe?

### The traditional way:
**Apache Hut** was the favorite pizzeria in the Silicon Valley for the past decade. Everyone love the quality of its pizzas, the staff and its clean menu. Everyone recognise that the delivery of **Apache Hut** is usually pleasing, but it simply can't cope the amount of clients during rush hours. From an external point of view, it looks like the restaurant is satured very quickly. On contrary, some pretend that **Nginx O' Pepperoni** is flawless on that point: hell, it even handled Gooogle's event.  

Let's take a look on how is a request served in **Apache Hut**:
![Apache Hut Strategy Scheme]({filename}/images/apachehut.svg){: style="float:right"}

Odly enough, 


![Nginx O' Pepperoni Strategy Scheme]({filename}/images/nginxopepperoni.svg)

#### Real code:
