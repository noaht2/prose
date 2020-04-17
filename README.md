# My Programming Language: Prose

Prose is a programming language I’m working on implemented in Python. It is a dialect of Lisp made by someone who hasn’t written any.

## Basics

The fundamental data structure of Prose is the list. A list is written like this: `(a b c)`.

Code is also in lists – instead of `1+2`, you write `(+ 1 2)`. Fizzbuzz from 0 to 100 is written like this:

```lisp
(map (lambda (x) (if (= (% x 15) 0) `fizzbuzz' (if (= (% x 5) 0) `buzz' (if (= (% x 3) 0) `fizz'))))(range 0 10 2))
```

## Current State of Things

Much basic functionality has been implemented. However, the parser is not complete, which means that instead of the above, to write fizzbuzz one currently has to write:

```python
code = ["map", ["lambda", ["x"], ["if", ["=", ["%", "x", "15"], "0"], "`fizzbuzz'", ["if", ["=", ["%", "x", "5"], "0"], "`buzz'", ["if", ["=", ["%", "x", "3"], "0"], "`fizz'", "x"]]]], "range", "0", "101", "1"]
```
