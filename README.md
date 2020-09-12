# My Programming Language: Prose

Prose is a programming language I’m working on implemented in Python.
It is a dialect of Lisp.

## Basics

The fundamental data structure of Prose is the list. A list is written like this: `(a b c)`.
Code is also in lists – instead of `1+2`, you write `(+ 1 2)`.

Functions are not a core feature.
Instead, operators act on the code passed to them directly.

## Example

This:
```lisp
(list
 (def lambda2fn1 (lambda app (lambda arg (app (eval arg)))))
 ((lambda2fn1 (lambda x (+ x 1))) (+ 1 1))
 (def add2 (lambda2fn1 (lambda n (lambda m (+ m (* 2 n))))))
 (add2 (+ 1 1) (+ 1 1)))
```
Evaluates to:
```lisp
((lambda app (lambda arg (app (eval arg)))) 3 (lambda arg (app (eval arg))) 6)
```

## TODO
 - More tests
 - A complete standard library inspired by Scheme’s (another Lisp dialect)
 - Documentation
 - Making all values be stored as lists
 - A REPL
 - Better scope semantics
