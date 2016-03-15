Title: My favorite pizzeria is event-driven... my back-end server too (C++, Python)
Date: 14:00 01-10-2016 
Modified: 14:00 01-10-2016
Tags: C++14, Python, event-driven, asynchronous architecture
Slug: asynchronous-pizzeria
Status: draft

## About this post:
Computer programming is a science, or even an art, and as such its community follows trends for better or worse. Today, I am highly positive in our future so let's speak about the new holy grail of any back-end developer, the panacea for web servers: an **asynchronous** **event-driven** architecture. Forget about your old synchronous habits, now we enter in the era of **non-blocking I/O** models, **coroutines**, **callbacks**, hacky **generators**, and all-mighty **asynchronous calls**. [Node.js](https://nodejs.org/en/) is conquering the market partly due to its full embrace of such an architecture. Google's latest child, the [Go](https://golang.org/) Programming Language, was designed around this concept. Why would we not do the same?

I could directly dive into some funky tricks to implement **stackless coroutines** in **C++14**, or explain **epoll** in details. Yet the very basic internals of such technologies are pretty mysterious for some of us, when it actually has a very straightforward explanation. Why is it more efficient than old-fashioned technologies? There must be a thread somewhere? Where is the loop then?

As a developer, it is also sometimes handy to explain why spending 4 developers to rework a software architecture is actually cheaper than scaling with hardware. Especially, if your interlocutor is a greedy stakeholder or any kind of non-technical-boss on top of you. 

This post will focus on these fundamentals questions, and it will a base for some coming topics. I would not dare to simply throw you **spaghetti code**, so let's first explain these concepts using **pizzas**.

### **Apach' Hut** vs **Ngin O' Pepperonix**:
In the 21th century, there are two domains where **servers** are forestanding: restaurants and computer science. If the former domain was the inspiration for the second-one, it must be quite straightforward to do an analogy of the two worlds. In any case, we want to deliver FAST our clients' requests.

We will soon discover the Secret Recipe that **Ngin O' Pepperonix** used to conquer a great part of **Apach' Hut's** market shares. Or is it the recipe?

#### **Apach' Hut's** traditional management:

**Apach' Hut** was the favorite pizza food delivery brand in the Silicon Valley for the past decade. Everyone love the quality of their pizzas, the staff and its clean online menu. Everyone recognise that the on-call delivery of **Apach' Hut** is usually pleasing, but it simply can't cope the amount of clients during rush hours. From an external point of view, it looks like the pizza delivering process is satured very quickly at lunch time. Their web-service becomes equally unreachable. On contrary, some pretend that **Ngin O' Pepperonix** is flawless on these points.

##### In the kitchen:
Let's take a look on how is a phone request served in **Apach' Hut**:

1. A client grabs his phone, dials **Apach' Hut's** phone number and wait for an answer whilst glancing at the menu.  
2. Once available, a call center agent available picks up the call and takes note of the client's request. Most of the calls last in average **5min**. The agent then dispatches the request to a cook, **IF** available.
3. Cooks, themselves, are waiting **passively** in room for a request. Sometimes, they may have time to read a book for **20min** ; but in rush hours, they barely enter the waiting-room that the call center center yells at them a new request.
4. Once a cook acquires a pizza request, he will head to the warehouse to get ingredients. If lucky, the warehouse contains enough tomatoes, shrooms, bacon... But it is not unusual that the warehouse is out of stock in one of the precious substance for an amazing pizza. The agent must therefore **wait passively** for the next delivery from the main warehouse between **0 to 30min**.
5. After the warehouse detour, finally starts the cook's mission. The cook shines for **15min**, during which he magically executes his own recipe.
6. Time to put the pizza in the oven and... light a cigarette. Anyway the cook must wait **30min**, **taskless**.
7. Finally, the cook wraps the pizza in its box and gives it to one of these crazy delivery boys we are used to in Europe. Sadly, the cook cannot process to another pizza before he ensures that the client is satisfied, a **20min** lost in average...

![Apach' Hut Strategy Scheme]({filename}/images/apachehut.svg)

Did you catch any problem in this strategy? Anything else than the fact that a traditional pizza would be burn after 20min at 210°C? 

Effectively this management is inefficient as Apach' cooks spend a good part of their days doing nothing more than waiting, they are truly **idle**. On a good day, they might work **15 minutes** per hour, it gives them enough time to **sleep** half of the day. Dare not to say that they are sloths, they are actually very skillful employees limited by the company's strategy, a strategy issued by the administration. Apach' is therefore quickly running out of control if it receives more calls than the cooks can handle. 

If this workload management seems counterintuitive, it actually reflects the architecture behind a synchronous web-server. Let's see how we could compare **Apach' Hut** kitchen nightmare with their online infrastructure.

##### In the datacenter:
An online order triggers the following flow in **Apach' Hut** architecture:

1. A client press the order button after selecting his pizzas and entering his credentials. A SOAP request is sent to the pizza-reservation server.
2. A thread is accepting TCP connections using [accept](http://man7.org/linux/man-pages/man2/accept.2.html) through a loop. Some connections can be put in a queue if the loop is not fast enough, or simply discarded if the queue is full.
3. The accepted socket is passed as a task to a thread. This **worker-thread** is issued from a [thread-pool](https://en.wikipedia.org/wiki/Thread_pool) and will manage the client socket for the rest of the reservation process. Sometimes all the worker-threads from the pool are **busy** and the the accepting-thread must **wait** before forwarding its newly created task, wasting precious time!
4. The worker-thread needs more information regarding the client and must also validate the credentials. In order to do so, the worker-thread will do a REST call to a dedicated internal API. The HTTP communication is implemented using curl in synchronous mode. The worker-thread **waits** in average 500ms to obtain an answer.
5. Using the client details, the worker-thread will then **compute** the delivery price according to his proximity, the price of the menu, the estimated-time... in less than 10ms.
6. Now, the reservation must be stored within a database file. Usually, writing a full record to such a database file takes within 10ms to 50ms, but when the Hard Disk Controller is overloaded, the worker-thread can **wait** even longer.
7. Finally, the reservation has been successfully processed, a HTTP Response is sent to the client's browser and the connection closed. The worker-thread can be placed back to the pool, awaiting for a new task.

No needs to be sherlock holmes himself to understand that the same problem arise in their web-service as in their kitchen. The worker-threads are sadly waiting more than they should, similarly to the cooks. In the meantime, no requests can be served. At lunch time, running the **top** command on their Unix workstation would depress you, all the threads are idle, but the reservation process is highly saturated. If the strategy or architecture of their web-service were better designed, it would squeeze out a maximum of computation power from every thread.

##### Scaling analysis:
Considering the following architecture, could you easily scale according to the number of clients? The answer is, sadly, no!

Why could we not either spawn a thread per client or simply increase the size of the pool? It boils down to the price of such a tactic. Likewise a cook has a salary, a thread from your operating system is not cheap. Too many cooks would explose your yearly budget, too many threads will consume all your resources. For instance, a Linux thread needs its own stack with a default memory footprint of 2 megabytes. A server with 4 Gigabytes of RAM would have a limit of 2000 simultaneous threads... but that's only considering the stack size. A thread creation implies some costly system calls, a tricky manipulation of various descriptors. Finally, if a kitchen had 2000 cooks, there would be a very high number of collisions, smashed toes and bad words, it would the same mess for the [scheduling](https://en.wikipedia.org/wiki/Scheduling_(computing)) of a massive amount of threads.

Scaling by spawning processes is also a no go. Threads and processes in Linux are actually very similar, you will fight the same problems concerning resources usage. Another solution would be to scale by hardware. But, well, if all the restaurant chains were to rent a new spot everytime they need to handle 10 more clients, they would quickly bankrup... isn't it?



Some threads can be lightweights, see green threads.
A special usage.

#### **Ngin O' Pepperonix** solution:

![Ngin O' Pepperonix Strategy Scheme]({filename}/images/nginxopepperoni.svg)

If I am not waiting, then who will do it for me?


How would it scale?
Bring some curves!





#### Time for a bit of code:
