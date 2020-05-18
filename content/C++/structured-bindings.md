Title: Let's unravel the secrets behind C++17's structured bindings 
Date: 17:40 05-17-2020 
Modified: 17:40 05-17-2020
Tags: C++17, structured bindings. 
Slug: structured-bindings

## Trivia:

I had a good intuition on how structured bindings worked when C++17 came out. The feature is quite intuitive to use and provides great help.
But it is not until recently that I actually read [the part of the standard](http://eel.is/c++draft/dcl.struct.bind) that describes how this truly works under the hood. As always, the standard is rather cryptic with all its language lawyer terms and for once [cppreference](https://en.cppreference.com/w/cpp/language/structured_binding) is not so succinct either.

For future me, I decided to write a dumbed-down version of what happens here!

Disclaimer: this post reflects my humble understanding of the standard, feel free to reach me if I got anything wrong in there.

## Destructuring the structured bindings:

Similar to the [range-based for loops](https://en.cppreference.com/w/cpp/language/range-for), this new "structured binding" feature can be seen a syntax-sugar. This means that we can produce a code equivalent to what a structured binding declaration would do.

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

Now let's assume that `foo` is returning a type by **value** - `T foo()` - and therefore produce a **temporary** variable. This means that we can only use `auto`, `const auto&` or `auto&&` but NOT `auto&`. `auto` will do a copy of that temporary, `const auto&` and `auto&&` will bind to that temporary and [prolong its life until the end of the scope](https://en.cppreference.com/w/cpp/language/reference_initialization#Lifetime_of_a_temporary). `auto&` would not work here as l-value references cannot bind to temporary values. `auto&` will be useful only if your (member) function `foo` returns a l-value reference - `T& foo()` - and you want to avoid a copy while having non-const access.

Note that the expression on the right part of the equal operator can be more complicated than just a call to a function like `foo`.
Anything that could assign `a_secret_variable` could belong there, like `auto&& a_secret_variable =  std::pair(2, "bob");`.

Now that the compiler produced the anonymous variable, how do we obtain `x` and `y` from it? This will depend on the type of expression on the right.
There are three cases: one for array types, one for simple types and one for types that act like std::tuple.
The two first ones are pretty straightforward, while the later one requires a bit more explanations.

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

As you can see, `x` and `y` do not really exist as variables. They don't even have their own storage! Rather, they should be seen as special identifiers ; what the standard call "the names of lvalues that refer to some elements". In this scenario, `x` is a special identifier that refers to `a_secret_variable[0]`. And `y` is a special identifier that refers to `a_secret_variable[1]`.
Since `a_secret_variable` is a l-value reference to `an_array`, mutating `a_secret_variable` is equivalent to mutating `an_array`. Therefore, this snippet will print `42,42`.

Note that the number of special identifiers must match the size of your array! Your compiler will yield an error otherwise.

### Simple types: 

What I call simple types are types whose non-static members are publicly available. Typically a plain old C-like `struct` would fit well into that category. 
In the standard, this case happens only if the type is not already in the category "arrays" or "tuple-like types".

If your type falls into that "simple types" category, the end-result will be very similar to arrays. The difference is that the special identifiers will refer to the non-static members of your type. The special identifiers are referring each members of your type from up to down.

So if we have such code:

```c++
struct A {
    int a;
    int b;
};

A foo() {
    return {1337, 1337};
}

const auto& [x, y] = foo();

std::cout << x << "," << y; // Prints 1337, 1337
```

Let's observe what such a simple example becomes:

```c++
struct A {
    int a;
    int b;
};

A foo() {
    return {1337, 1337};
}

const auto& a_secret_variable = foo();

std::cout << a_secret_variable.a << "," << a_secret_variable.b;
```

As you can see, `a` is the first member of `A`. `x` being also first in the identifier list will refer to `a`.
Note that the number of special identifiers must also match the number of members available in your type!

There is a subtle catch here though. What would `decltype(x)` yield as type (what the standard calls referenced type)? One would assume that this would be strictly the same as `decltype(a_secret_variable.a)` which is equivalent to `int`. The standard made a nice plot-twist here and `decltype(x)` will, in rough terms, have a type equivalent to `decltype(a_secret_variable.a)` **plus** the `const` or `volatile` qualifiers attached to `a_secret_variable`. In our case `a_secret_variable` is `const`, which result in `decltype(x)` being equivalent to `const decltype(a_secret_variable.a)` or in a simpler form `const int`.
C++ is like a box of chocolates... you never know what you're gonna get!

So why did the standard went into creating such "special identifiers" and not simply have proper variables which are references?
If you do so, you have multiple issues here, like:
- How would you handle bit fields? There is not such a thing as reference to bit fields.
- Imagine that you were to capture those variables in a lambda `[=](){}`. What should happen here? Shall this copy the entire `a_secret_variable` or just the members of it?
- ...
For these reasons, the standard had to treat those identifiers in a special way.

### Tuple-like types:

The last kind of types you can bind are tuple-like types. In layman's terms, these types are similar to [std::tuple](https://en.cppreference.com/w/cpp/utility/tuple) in the sense that you can access their members/values using `std::get` or a member function `get` on them. These types do not give a direct access to their members/values but still want to be part of the cool club of structured bindings. Ultimately, this led the standard to use type traits to describe how to access these members. 

#### Example with std::tuple:

Let's start with a simple case that we will decompose in few steps:

```c++
std::tuple my_fancy_tuple(43, std::string("fiction"));
auto& [x, y] = my_fancy_tuple;

y = "factory";

std::cout << x << "," << y; // Prints 43,factory.
```

As always, your compiler will first introduce an anonymous variable:

```c++
std::tuple my_fancy_tuple(43, std::string("fiction"));
auto& a_secret_variable = my_fancy_tuple;
```

As a sanity check, your compiler will check that your special identifiers like `x` or `y` are enough to cover all the values that your tuple-like type holds.
To do so, it will do a "compile-time call" equivalent to `std​::​tuple_­size_v<std::remove_reference_t<decltype(a_secret_variable)>>​`. [std::tuple_size](https://en.cppreference.com/w/cpp/utility/tuple/tuple_size) is already defined for `std::tuple` and will return `2` in our example. Since we have two special identifiers and the size of the tuple is two, no members/values are left behind and the compiler allows us to move to the next step.

To be able to use special identifiers referring to values/members of `a_secret_variable`, the compiler need to extract those with some calls to `std::get` or a member function of your type named `get`. It would be quite slow to repeat this extraction repeatedly, therefore the compiler will introduce a **new set of anonymous variables** to store the result of those calls.
The standard also provides a second customisation point by letting the creator of the tuple-like class decided which type these variables will have.
This customisation point is called [std::tuple_element](https://en.cppreference.com/w/cpp/utility/tuple/tuple_element).
Here is what this will look like in code:

```c++
std::tuple my_fancy_tuple(43, std::string("fiction"));
auto& a_secret_variable = my_fancy_tuple;
std::tuple_element_t<0, std::remove_reference_t<decltype(a_secret_variable)>>& secret_x = std::get<0>(my_fancy_tuple);
//                   ^ The type of the member with index 0                     ^ anonymous         ^ Gets the value of member 0.
std::tuple_element_t<1, std::remove_reference_t<decltype(a_secret_variable)>>& secret_y = std::get<1>(my_fancy_tuple);
```

Given [std::tuple_element](https://en.cppreference.com/w/cpp/utility/tuple/tuple_element) specialisation for `std::tuple`, this results in:
```c++
std::tuple my_fancy_tuple(43, std::string("fiction"));
auto& a_secret_variable = my_fancy_tuple;
int& secret_x = std::get<0>(my_fancy_tuple);
std::string& secret_y = std::get<1>(my_fancy_tuple);
```

Note that the variables are defacto references ; more precisely l-value references in this case. This is to avoid any unnecessary copies of your data.
So what if `get` had returned anything else than l-value reference? The compiler would adapt itself and generate variables which are r-value references "`&&`" with the all the benefit you have from those: it extends the lifetime of temporaries and permits mutability of those.

Afterwards, the compiler proceeds by associating to these new variables our special identifiers `x` and `y`. Once again, these special identifiers simply refer to `secret_x` and `secret_y` but are not proper variables. This leads us to this weird code as an output where `y` would spawn out of nowhere but pretends to be `secret_y`:

```c++
std::tuple my_fancy_tuple(43, std::string("fiction"));
auto& a_secret_variable = my_fancy_tuple;
int& secret_x = std::get<0>(my_fancy_tuple);
std::string& secret_y = std::get<1>(my_fancy_tuple);

y = "factory"; // y refers to secret_y and therefore mutate the variable that secret_y is bound to.
```

To further add to this complicated situation, the reference type of `y` (the result of `decltype(y)`) is also receiving its own treatment. 
You would expect it to be same as `secret_y` which is `std::string&`, but the compiler is assigning the type resulting of `std::tuple_element` instead.
In our case, `std::tuple_element` gave for the member at index 1 the type `std::string`, so `decltype(y)` will return `std::string`.
While slightly awkward, this gave us some types for `x` and `y` that would be similar to if we were accessing to the real members of the tuple directly!  

#### Playing with a custom type:

As you observed, if a type has a specialisation for `std::tuple_element` and `std::tuple_size` and has a `std::get` overload or a `get` member function, then it can be morphed into some structured bindings. So let's write a very dumb type with two members we want to expose this way:

```c++
struct A {
    A(int x, std::string y) : x_(x), y_(std::move(y)) {}

    template <std::size_t I>
    //                    ^ The index of the member you want to get.
    auto& get() {
        // Dispatch to the right member using if constexpr.
        if constexpr (I == 0) {
            return x_;
        } else {
            return y_;
        }
    }

    template <std::size_t I> 
    const auto& get() const {
    //                 ^ A const overload.
        if constexpr (I == 0) {
            return x_;
        } else {
            return y_;
        }
    }

private:
    int x_;
    std::string y_;
};

namespace std {
    template<>
    struct tuple_size<A> : std::integral_constant<std::size_t, 2> {};
    //                ^          A always has 2 members        ^

    template<>
    struct tuple_element<0, A> {
    //                   ^ The member at index 0 has type int.
        using type = int;
    };

    template<>
    struct tuple_element<1, A> {
    // The other one has type std::string.
        using type = std::string;
    };
}
```

As you can see, you don't need a diploma in rocket-science to have your types support structured bindings.
A couple of lines gives enough clues to your compiler to be able to generate the needed boilerplate behind the scene.
In that respect, the standard was quite well designed!

There are still two things I would like to focus your attention on.

##### Handling const:

What happen if we create a structured binding with `const auto&` on our type? Such as:

```c++
A a{1, "yo"};
const auto& [x, y] = a;
```

If you followed carefully the steps on `std::tuple`, you would notice that this will call `std::tuple_element` and `std::tuple_size` with `const A` as a parameter.
As you can see in my code, I did not specialise those two type-traits for `const A`. Yet, this will work as it should!
It turns out that the committee was friendly enough to supply a partial specialisation for any `const T` out there.
By default, these standard provided specialisations will recursively call your own specialisation with `T` while adding `const` where they should.
That's neat!

##### A very odd get:

The last interesting tidbit is the following: what if we decided that our `get` return `x_` and `y_` by value? How would that work?

```c++
struct A {
    // ...

    template <std::size_t I> 
    auto get() const {
    // ^ by value
        if constexpr (I == 0) {
            return x_;
        } else {
            return y_;
        }
    }

    // ...
};

A a{1, "yo"};
const auto& [x, y] = a;
```

As I explained earlier, the standard is actually ready for that extremely hairy situation.
Here the results from `get` would be captured by some r-value references such as:

```c++
int&& secret_x = secret_a.get<0>(); 
std::string&& secret_y = secret_a.get<1>();
```

The temporaries resulting from those hidden calls to `get` would live until the end of their scope.
I am not quite sure if this a genius move from the committee or if this came as by-product of C++'s complexity as I see no point in allowing such weird construction...
With these horrifying thoughts, I let you reach the conclusion of this post!

## Conclusion:

I promised a dumbed-down explanation of structured bindings but ended up writing substantially more than what the standard says.
If you have to remember anything from this post, here are the key-points you should focus on:

- The qualifiers (const, auto, &...) are applied to the entire variable behind your structured bindings and not the identifiers.
- The rest of the boilerplate behind the scene does mostly what you would expect. The only caveat comes for `decltype(an_identifier)` where it gets hairy. 
- You can bring the power of structured bindings to your types quite easily with few type traits. 