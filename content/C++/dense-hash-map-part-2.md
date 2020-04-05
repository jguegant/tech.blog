
### Conclusion:

- If you are inserting a new pair into an **associative container** consider using `try_emplace` first.
- If you cannot use **C++17**, prefer to use `emplace` over `insert`.
- If you are cannot use **C++11**, I feel sorry for you!
- You can borrow my `lazy_convert_construct` if you are dealing with smart pointers and `try_emplace`, to get a blazzing fast insertion.

A special thanks to my colleague Yo Anes with whom I had a lot of fun discussing this specific topic.