Title: Let's unravel C++17's structured bindings 
Date: 17:40 05-17-2020 
Modified: 17:40 05-17-2020
Tags: C++17, structured bindings. 
Slug: structured-bindings

## Trivia:

I had a good intuition on how structured bindings worked when C++17 came out. The feature is quite intuitive to use and provides great help.
But it is not until recently that I actually read [the part of the standard](http://eel.is/c++draft/dcl.struct.bind) that describes how this trully works under the hood. As always, the standard is rather cryptic with all its language lawyer terms and for once [cppreference](https://en.cppreference.com/w/cpp/language/structured_binding) is not so succinct either.

For future me, I decided to write a dumbed-down version of what happens here!

## Destructuring the structured bindings:

Similar to the [range-based for loops](https://en.cppreference.com/w/cpp/language/range-for), this new "structured binding" feature can be seen a syntax-sugar. This mean that we can produces a code equivalent to what a structured binding declaration would do.

So let's start with a simple case:

```c++
auto [x, y] = foo();
```

The way you should interpret this code is the following:

- I am declaring a new **anonymous** variable that encompass `[x, y]`.
- This new variable will have its type deduced and be a copy of what foo returns since we have `auto`. 

In other words, your compiler starts by producing a code very similar to this:

```c++
auto a_secret_variable = foo();
```

What this implies is the `auto` keyword is **applied to the anonymous variable** and **NOT** the identifier `x` and `y` as some may think.
The anonymous variable itself is not visible to anyone except the compiler, it is not possible to actually check its type, but you have to trust me here! 

Now let's assume that `foo` is returning type by **value** - `T foo()` - and therefore produce a **temporary** variable. This means that we can only use `auto`, `const auto&` or `auto&&` but NOT `auto&`. `auto` will do a copy of that temporary, `const auto&` and `auto&&` will bind to that temporary and [prolong its life until the end of the scope](https://en.cppreference.com/w/cpp/language/reference_initialization#Lifetime_of_a_temporary). `auto&` would not work here as l-value references cannot bind to temporary values. `auto&` will be useful only if your (member) function `foo` returns a l-value reference - `T& foo()` - and you want to avoid a copy while having non-const access.

Note that the expression on the right part of the equal operator can be more complicated than just a call to a function like `foo`.
Anything that could assign `a_secret_variable` could belong there, like `auto&& a_secret_variable =  std::pair(2, "bob");`.

Now that the compiler produced the anonymous variable, how do we obtain `x` and `y` from it? This will depend on the type of expression on the right.
There are three cases: one for array types, one for simple types and one for types that act like tuples.
The two first ones are pretty straightforwards, while the later one requires a bit more explanations.

### Arrays:

Let's try to bind to an array:

```c++
int an_array[] = {1337, 1337};
auto& [x, y] = an_array;

x = 42;
y = 42;

std::cout << an_array[0] << "," << an_array[1]; // What happen here?
```

After substitution of `[x, y]` with our anonymous variable we obtain:

```c++
int an_array[] = {1337, 1337};
auto& a_secret_variable = an_array;

a_secret_variable[0] = 42;
a_secret_variable[1] = 42;

std::cout << an_array[0] << "," << an_array[1];
```

As you can see, `x` and `y` do not really exist as variables, they don't have their own storage! Rather, they should be seen as special identifiers ; what the standard call "the names of lvalues that refer to some elements". In this scenario, `x` is a special identifier that refers to `a_secret_variable[0]`. And `y` is a special identifier that refers to `a_secret_variable[1]`.
Since `a_secret_variable` is a l-value reference to `an_array`, mutating `a_secret_variable` is equivalent to mutating `an_array`. Therefore, this snippet will print `42,42`.

Note that the number of special identifiers must match the size of your array! Your compiler will yield an error otherwise.

### Simple types: 

What I call 

Work in a very similar same way than arrays. But in this scenario the special identifer refer to members of the struct. 

```c++
struct A {
    int a;
    int b;
};

A foo() {
    return {1337, 1337};
}

const auto& [x, y] = foo();

std::cout << x << "," << y;
```

### Tuple-like types:


## First conclusion

TODO.
