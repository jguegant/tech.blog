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

**Apach' Hut** was the favorite pizza food delivery brand in the Silicon Valley for the past decade. Everyone love the quality of their pizzas, the staff and its clean online menu. Everyone recognise that the on-call delivery of **Apach' Hut** is usually pleasing, but it simply can't cope the amount of clients during rush hours. From an external point of view, it looks like the pizza delivering process is saturated very quickly at lunch time. Their web-service becomes equally unreachable. On contrary, some pretend that **Ngin O' Pepperonix** is flawless on these points.

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
Considering the following architecture, could you easily scale according to the number of clients? The answer is, sadly, **no**!

Why could we not either spawn a thread per client or simply increase the size of the pool? It boils down to the price of such a tactic. Likewise a cook has a salary, a thread from your operating system is not cheap. Too many cooks would explode your yearly budget, too many threads will consume all your resources. For instance, a Linux thread needs its own stack with a default memory footprint of 2 megabytes. A server with 4 Gigabytes of RAM would have a limit of 2000 simultaneous threads... but that's only considering the stack size. A thread creation implies some costly system calls, a tricky manipulation of various descriptors. Finally, if a kitchen had 2000 cooks, there would be a very high number of collisions, smashed toes and bad words, it would the same mess for the [scheduling](https://en.wikipedia.org/wiki/Scheduling_(computing)) of a massive amount of threads.

Scaling by spawning processes is also a no go. Threads and processes in Linux are actually very similar, you will fight the same problems concerning resources usage. Another solution would be to scale by hardware. But, well, if all the restaurant chains were to open a new spot every time they need to handle 10 more clients, they would quickly bankrupt... isn't it?

![Ngin O' Pepperonix Strategy Scheme]({filename}/images/bad-scaling.png)

In all these solutions, if you observe the resource consumption regarding the number of clients, in the best case you will see a **<span style='color:blue'>linear complexity</span>**. It can easily turn out into a much worse complexity like a **<span style='color:red'>polynomial one</span>**. As a software engineer, such a graph must make you frown, none of us want to see a polynomial memory usage in his system especially when correlated to such a trivial entity that is a user. If you replace the word **resource** with **operating costs**, even your shareholders might have a stroke.

One must keep in mind that this kind of architecture is really **bad** if you are expecting to scale with the number of **clients**. If you have a **fixed maximum** number of clients or you are working on **one to one** communications, this architecture is actually relevant. For instance, in High Frequency Trading, where **latency** is much more precious than **scalability** it is not uncommon to opt for [busy waiting](https://en.wikipedia.org/wiki/Busy_waiting). In other words, if you are cooking a pizza for yourself, it does not matter if you spend 45min in front of your oven.

Some languages and platforms offer lite threads, handled by a runtime or a virtual machine instead of the operating system. Even if these [green threads](https://en.wikipedia.org/wiki/Green_threads) are considerably less costly, they usually freeze all the other threads during synchronous I/O operations. It is still crucial to understand how we could almost reach a **<span style='color:green'>constant complexity</span>**, using asynchronous I/O operations, like in the following graph:

![Ngin O' Pepperonix Strategy Scheme]({filename}/images/good-scaling.png)


#### **Ngin O' Pepperonix** solution:

##### An event-driven kitchen:

Back to the kitchen! **Ngin O' Pepperonix** solved this problem by providing to each of its employees a tablet with a to-do list application and upgrading its equipments. For instance, ovens can raise an **event** when the pizza has been baked enough, the food delivery can trigger another kind of event and same goes for client calls. All the events are broadcasted on the workers' tablets. When a worker is dealing with a task that requires him to wait, he can **poll** the most urgent **event** and continue to work on something else instead. Even if he cannot finish his new task before the waiting period elapse, someone else might receive the event and handle the rest of the process.

![Ngin O' Pepperonix Strategy Scheme]({filename}/images/nginxopepperoni.svg)

Workers are now as efficient as possible. They must spend a bit of their time checking their tablet, but they have absolutely no wait-periods anymore unless no events are available (but it is perfectly sane to relax in that case). Instead of waiting blatantly all the day, **cooks** are now mainly **cooking**. **Ngin O' Pepperonix** can easily handle **50 clients** with only **1 cook**, that sounds much better!

If we still consider the analogy **cook** =~ **thread**. In order to recreate such a successful architecture, we would need "news technologies" for generating and managing events from a thread and the "long operations". Using **events**, the number of threads must be increased only if it reaches the max CPU usage of some cores. Thanksfully, as we saw previously, the process has never been much CPU-bound, getting the right delivery price was the only computation ever done. This kind of architecture is therefore almost not bound to number of clients, we finally reach the **<span style='color:green'>constant complexity</span>**. For instance, **Node.js** only uses one and only one thread and yet perform quite with a huge number of clients!

Any drawback? Well, event-driven architectures might seems more intuitive to us humans used to [multitask](https://en.wikipedia.org/wiki/Human_multitasking) everything in our daily-life. But first, the technologies required for the **tablets** and the **connected-ovens** have a **price**, in our programming world this cost is express in the shape of some more complex operating system internals and libraries. Second, it is actually harder than you may think to **decouple** everything in events/handlers without ending with some race-conditions, a callbacks hell or unreliable performances.

##### Asynchronous weapons:

Here is a quick overview of the various technologies that can be used to achieve such an architecture. It is not that usual to manipulate them directly, most of us will prefer to use an abstracted library for his favorite language as we will see later on. If you are greatly interested in such internals, I highly suggest you to read the really famous [C10K problem post](http://www.kegel.com/c10k.html) or for instance this [post from George Y.](http://www.ulduzsoft.com/2014/01/select-poll-epoll-practical-difference-for-system-architects/)

###### Proactor & reactor, edge triggered & level triggered:

We should start with a bit of vocabulary that you may encounter if you are digging into event-driven architectures or [I/O multiplexing](https://en.wikipedia.org/wiki/Asynchronous_I/O). 

The base of every event-driven architecture consists of **operations** and **events**. Two patterns exists when it comes to mix both of these concepts. The first one, **Proactor**, is for me the easiest to grasp. As a user you initiate asynchronous operations, these operations will be performed soon or later by the underlying system. Most of the time these operations are **Input/Output operations** (I/O operations), but it can also be a timer for instance. Once the operations are done, you will receive **events** in a queue telling you which of your operations are done and so that you can react accordingly.

The second one, **Reactor**, is slightly more awkward. As a user you have the possibility to query the underlying system to know whether the operation you wish to do will be blocking due to the resource not being available, or not. By constantly **polling** the underlying system, you can wait for the right time to do a synchronous operation without blocking, the resource being available at that time.

If **Proactor** looks more promising, you can actually express **Proactor** using **Reactor** facilities. Using another **queue**, one can store the operations to be done and their associated **event types**. Once the underlying system express the possibility to do a synchronous operation without blocking, the first operation in the queue can be taken, executed and the associated event can be push in the event queue. From a user point of view, pushing a "to-be-done operation" is asynchronous and the right event will be raised once the operation is done ; that is exactly **Proactor**.

Now if your **operation** consist in waiting for a given **quantity** of a resource using a **Reactor** pattern, you may want an event to be raised until you successfully acknowledges that **quantity**, that is a **level-triggered** behavior. You may also choose to receive a **single-shot event** when the quantity is available and none afterward whether you acknowledged the whole quantity or not, which is equivalent to a **edge-triggered** behavior. For example, if you express the desire to do a read operation on a [pipe](https://en.wikipedia.org/wiki/Anonymous_pipe), and partially read the data available, two scenarios can happen. If you are using a **level-triggered** behavior, the underlying system will kindly "remind you" that your forget some data. With a **edge-triggered** behavior, the underlying system will be silent until more data arrives in the pipe ; that is pretty troublesome if the process at the end of the pipe is expecting a reaction from the data it already pushed!

Still alive with this vocabulary? Here comes the tools exposed by your operating systems, following either the **Reactor** or the **Proactor** pattern, to craft asynchronous operations.

###### At the operating system level:

The questions that often arise are "Isn't it necessary for the underlying system to **wait actively** for any operation to be done? Aren't we just pushing the problem into the kernel?". Well, yes! But the kernel itself could be able to push the problem to the hardware level. For instance, a file read operation might just be forwarded by the kernel to the disk controller ; using [interruptions](https://en.wikipedia.org/wiki/Interrupt_request_(PC_architecture)) the disk controller can signal asynchronously the kernel that the disk request has been fulfilled. This signal can be bubbled back to the [userland](https://en.wikipedia.org/wiki/User_space) in the shape of an event. **A lot** can be done by an application during the lapse of time of a disk operation!

- **Select**:

I was telling you that these technologies are brand new, I am partly a liar. In the **Unix** & **POSIX** world, a function called [select](https://en.wikipedia.org/wiki/Select_(Unix)) existed even before I was born. Using **select**, one can inspect the status of multiple file descriptors, like some **sockets**. In order to do so, you pass to **select** three different sets of file descriptors: a **read** set, a **write** set, and an **exception** set. The call to **select** will block until one of this set has been updated or after a **timeout** (Note that the timeout is really important here, otherwise we would come back to a simple synchronous solution!). Afterwards, one must iterate on each set to check which file descriptor became ready for a read or write operation (hopefully not blocking) or if any error has been encountered. **Select** is intrinsically a **Reactor** pattern.

**Select** shines for its avaibility almost everywhere: on your Linux server, on your windows laptop (yes, windows has a Berkeley Sockets API), on your Android Phone or even your <del>smart-fridge</del>. On the other hand, **select** sets manipulations are not really user-friendly. But the main drawbacks of **select** are the maximum number of items in a set, the manual iteration on the sets. On a standard **Linux kernel**, the limit of items is 1024, which is fairly low if you plan to handle 20 000 connections simultaneously. The mandatory iteration on the sets to pin-point the interesting file descriptors has a complexity of **O(n)**, a complexity that could be **O(1)** if the kernel were pruning the unchanged file descriptors directly. As we will see, the teams behind **Windows NT**, **FreeBSD** and **Linux** unsatisfied with **select** authored their own solutions to solve these problems.

- **Poll, epoll & AIO**:

The [poll](http://man7.org/linux/man-pages/man2/poll.2.html) system call is an "upgraded version" of **select**: it can handle as many file descriptors as desired and more finely. Sadly, **poll** still requires a manual iterations on the file descriptor set and has a clumsy interface. **Poll** is also less portable than **select**.

Starting with the version 2.5.44 of the **Linux kernel** (at the beginning of this century), a new poll API on steroid appeared: namely [epoll](http://man7.org/linux/man-pages/man7/epoll.7.html). It fixes all the major problems of its predecessors with a trade-off of being more convoluted. **Epoll** is using the **Reactor** pattern and offers the possibility to choose between a **edge-triggered** or **level-triggered** behavior. If you are a **Linux** guru in needs of challenges with a low-level API, **epoll** is the way to go in 2016 for building a scalable network solution with this kernel (and most likely in 2017).

If you are targeting more than the **Linux** world, **epoll** is sadly not portable on any other platform, as far as I know. Even if **epoll** is certainly better than **select** or **poll** on **Linux**, it is also the least flexible solution compared to all its counterparts on other operating systems. **Epoll** is deeply rooted to the Unix philosophy that "everything is a file": it can only handle file descriptors. Some asynchronous operations must be bent to be expressed as file descriptors, like timers ([timerfd](http://man7.org/linux/man-pages/man2/timerfd_create.2.html)), signals ([signalfd](http://man7.org/linux/man-pages/man2/signalfd.2.html)) or custom events ([eventfd](http://man7.org/linux/man-pages/man2/eventfd.2.html)). Ironically, **epoll** was not designed to manage file disk operations. Instead, one must use a completely different POSIX API [AIO](http://man7.org/linux/man-pages/man7/aio.7.html) following a **Proactor** pattern.


- **Kqueue**:

If you are running an operating system from the BSD family like FreeBSD, OpenBSD, NetBSD or OSX, your best bet is to try [kqueue](https://en.wikipedia.org/wiki/Kqueue). In the async-API-war (if such a war ever existed), **kqueue** clearly beats **epoll**. While it roughly works in the same way as **epoll** (a Reactor), it is not restricted to file descriptors! I, sadly, never played with this API with such a solid reputation.

- **IOCP**:

I once read on the internets that [IOCP]( https://msdn.microsoft.com/en-us/library/windows/desktop/aa365198.aspx ), standing for **I/O Completion Ports**, is one of the best feature of **Windows NT**'s kernel, and I can only agree on this fact. Unlike all the other solutions, **IOCP** uses a **Proactor** pattern. In **IOCP**, all your operations are tied to an [IoCompletionPort](https://msdn.microsoft.com/en-us/library/windows/desktop/aa363862.aspx), which is fancy name for a smart **event-queue**. All the operations (like ReadFile, or WSASend) must accept an [OVERLAPPED](https://msdn.microsoft.com/en-us/library/windows/desktop/ms684342.aspx) structure as a parameter, which carries all the informations necessary for executing the operation and generating an completion event once done. One can wait for an event using [GetQueuedCompletionStatus](https://msdn.microsoft.com/en-us/library/windows/desktop/aa364986.aspx), or even manually trigger an event using [PostQueuedCompletionStatus](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365198.aspx) which is amazing for asynchronous thread communications.

Like **kqueue**, **IOCP** handles all kind of operations which is very convenient, at the price of using Win32 specific functions. By following a **Proactor** pattern, **IOCP** is for some of us easier to wrap our head around. **IOCP** is the base for all the asynchronous technologies on Windows's paltform including the .Net framework and the **async/await** keywords in C#. Finally, for the Microsoft haters, **IOCP** was successful enough to be included into **Solaris 10**!

- **Third-party libraries**:

Let's face it, most of us do not want to manipulate OS-specific APIs. Nowadays, almost all the languages have at least one library or framework to write portable event-driven architectures. A quick search on google like "asynchronous _INSET_YOUR_LANGUAGE_" will usually raise fruitful results. In the last part of this post, I will briefly introduce you to both the de-facto libraries for **C++** and **python**.

At a low-level, all of these libraries still rely on the aforementioned APIs. Usually, these libraries encapsulate these low-level features into a nice **event-loop** pattern as we will see right now!

###### Event loop:

Now that we have the possibility to construct a **Proactor** pattern for our long operations using low-level APIs, we can wrap its **event-queue** into an **event-loop**.

An **event-loop** is the base for an event-driven architecture. **Event loops** are actually fairly common in **UI programming** and **video-games** where user inputs are injected asynchronously in the application logic. A game or UI loop is generally constructed in the following way: check for user inputs ==> update logic accordingly ==> render ==> restart. Thinking about a game where the main loop would **wait** for user inputs instead of some **checks** gives me chills. If an **event-loop** makes sense in these use-cases, so does it for anything else dealing with other external inputs (networking, file, timers).

In a server, an **event-loop** would look closely to this:

    :::c++
    // Pseudo-code for an event-loop:

    DoAsynchronousOperationA(); // A first operation!

    while (true) {
        if (!eventsQueue.empty()) {
            auto event = eventsQueue.pop();

            switch (event) {
                case EVENT_A: // In reaction of the EVENT_A...
                    DoSomeComputation(); // ...I will do some computations...

                    DoAsynchronousOperationB(); // ...and do another asynchronous operation that will raise an EVENT_B.

                    DoSomeOtherBigComputation(); // .. we can do something not linked to OperationB without waiting.
                break;
                case EVENT_B:
                    DoSomeComputation();
                    
                    DoAsynchronousOperationA();
                break;
                ...
            }
        }
    }

You will notice that you must start a **first asynchronous operation**, before entering the loop, as a **bootstrap**. Otherwise, the queue **eventsQueue** would be forever empty, and your processus would never change its state. Speaking of **state**, you can observe that our logic is now expressed in the shape of a [state machine](https://en.wikipedia.org/wiki/Finite-state_machine), each change of state being the result of an asynchronous operation. Note also that in the state "EVENT_A happened", a big computation could have been done meanwhile an Operation B was processed. One thread and is enough for running this **event-loop** without staling!

In a more refined version, you would express your states as <a href="https://en.wikipedia.org/wiki/Callback_(computer_programming)"> callback </a> functions:

    :::c++
    // Pseudo-code for a refined event-loop using callbacks:

    void aCallBackForA() // A callback in reaction of the EVENT_A...
    {
        DoSomeComputation(); // ...I will do some computations...
        
        DoAsynchronousOperationB(aCallBackForB); // ...and do another asynchronous operation that will aCallBackForB.
        
        DoSomeOtherBigComputation(); // .. something not linked to OperationB.
    }

    void aCallBackForB() // A callback in reaction of the EVENT_B...
    {
        DoSomeComputation();
        
        DoAsynchronousOperationA(aCallBackForA);
    }

    DoAsynchronousOperationA(aCallBackForA); // A first operation still needed!

    while (true) {
        if (!eventsQueue.empty()) {
            auto event = eventsQueue.pop(); // Fetch any new event.
            auto callback = getCallBackAssociatedToThatEvent(event); // Find the right callback.
            callback(); // Execute the callback.
        }
    }

Easy right? Well, most of the libraries or frameworks for **event-driven architectures** expose a such interfaces for running **event-loops**, with some attached **asynchronous operations** and **callbacks**. Now that these internals have no secret anymore for you, we can relax a bit and enjoy a bit of code together.

#### Time for a bit of code:

##### C++ & Asio:

In the **C++** world

##### Python & Twisted:

**Python**

#### Conclusion:

Starting from a running joke, during our lunch time at work, that the personal of the kebab shop close to us are more asynchronous than 

A good introduction for some other posts.
Running joke test