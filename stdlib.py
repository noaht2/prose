#!/usr/bin/env python3
from core import *
from operator import *
from itertools import chain, islice, repeat
from functools import reduce
from typing import *

@Macro
def bind(car: Macro, cdr: Cons) -> Symbol:
    """Bind a symbol to a value and return the symbol.

    >>> bind(list_(Symbol('x'), Number(1)))
    Symbol('x', Number(1.0), for_eval=True)
    """

    symbol, value = cdr[:2]
    symbol.value = value
    return symbol

@Macro
@eval_default_macro_dec
def lambda_(cons: Cons) -> Callable[[Cons], Object]:
    """Create a function.

    >>> lambda_(
        list_(list_(Symbol('x')), list_(ADD, Symbol('x'), Number(1.0)))
    )(list_(Number(2.0)))
    Number(3.0)
    """

    params, value = cons[:2]

    @Function
    def func(cons: Cons) -> Object:
        param_iter = iter(params)
        for arg in cons:
            next(param_iter).value = arg
        return value()

    return func


# @Macro
# @eval_default_macro_dec
# def defun(cons: Cons):
#     # print("defun\t", cons)
#     name, params, value = cons[:3]
#     for i, param in enumerate(params):
#         if hasattr(param, "value"):
#             params[i] = Symbol(f"{repr(name)}_({repr(param)})", param.value)
#         else:
#             params[i] = Symbol(f"{repr(name)}_({repr(param)})")
#         value.replace(param, params[i])
#     return bind(list_(name, lambda_(list_(params, value))))


@Macro
def macro(car: Macro, cdr: Cons) -> Callable[[Cons], Object]:
    """A macro to create macro.

    Has not been tested.
    """
    params, value = cdr[0], cdr[1]
    print("macro\t", car, cdr)

    @Macro
    def user_macro(car: Macro, cdr: Cons) -> Object:
        param_iter = iter(params)
        for arg in cdr:
            next(param_iter).value = arg
        return value

    return user_macro


@Macro
def map_(car: Macro, cdr: Cons) -> Cons:
    """Map a function to a list."""

    # print(car, cdr)
    func = cdr[0]
    args = cdr[1:]
    args = args()
    return list_(*map(func, map(list_, args)))


@Macro
def if_(car: Macro, cdr: Cons) -> Object:
    """Choose between two values based on a condition.

    >>> if_(list_(Truth(), Number(1), Number(2)))
    Number(1.0)
    """
    # print("if_\t", repr(cdr))
    condition, if_value, else_value = cdr[:3]
    return if_value() if condition() else else_value()


@metadec
def unary_dec(func: Callable) -> Callable[[Cons], Object]:
    def unary_func(cons: Cons) -> Object:
        return Cons(func(cons.car), cons.cdr)

    return unary_func


@metadec
def binary_dec(func: Callable) -> Callable[[Cons], Object]:
    def binary_func(cons: Cons) -> Object:
        # print("binary_func\t", func, cons)
        if cons.for_eval:
            return reduce(func, cons)
        else:
            return cons

    return binary_func


@metadec
def ternary_dec(func: Callable) -> Callable[[Cons], Object]:
    def ternary_func(cons: Cons) -> Object:
        return func(*cons[:3])

    return ternary_func


@metadec
def boolean_dec(func: Callable) -> Callable[[Cons], Boolean]:
    def boolean_func(cons: Cons) -> Boolean:
        return boolean(func(cons))

    return boolean_func


@metadec
def number_dec(func: Callable) -> Callable[[Cons], Number]:
    def number_func(cons: Cons) -> Number:
        return Number(func(cons))

    return number_func


@metadec
def iterable_dec(func: Callable) -> Callable[[Cons], Cons]:
    def iterable_func(cons: Cons) -> Cons:
        return list_(*func(cons))

    return iterable_func


@Function
@iterable_dec
@ternary_dec
def range_(start: Number, stop: Number, step: Number) -> Iterable[Number]:
    """Do the equivalent of Python ``range``.

    >>> range_(list_(Number(1), Number(11), Number(1)))
    Cons(Number(1.0), Cons(Number(2.0), Cons(Number(3.0), Cons(Number(4.0),
    Cons(Number(5.0), Cons(Number(6.0), Cons(Number(7.0), Cons(Number(8.0),
    Cons(Number(9.0), Cons(Number(10.0), EmptyList(), for_eval=True),
    for_eval=True), for_eval=True), for_eval=True), for_eval=True),
    for_eval=True), for_eval=True), for_eval=True), for_eval=True),
    for_eval=True)
    """

    return map(Number, range(int(start), int(stop), int(step)))


@Function
def car(cons: Cons) -> Object:
    """Return the car of ``cons``.

    >>> car(Cons(Number(1.0), Number(2.0)))
    Number(1.0)
    """

    return cons.car


@Function
def cdr(cons: Cons) -> Object:
    """Return the cdr of ``cons``.

    >>> cdr(Cons(Number(1.0), Number(2.0)))
    Number(2.0)
    """

    return cons.cdr


LIST = Symbol("list", Function(list_))
BIND = Symbol("bind", bind)
LAMBDA = Symbol("lambda", lambda_)
LAMBDA_UNICODE = Symbol("λ", lambda_)
MACRO = Symbol("macro", macro)
# DEFUN = Symbol("defun", defun)
IF = Symbol("if", if_)
CAR = Symbol("car", car)
CDR = Symbol("cdr", cdr)

MAP = Symbol("map", map_)
RANGE = Symbol("range", range_)

ABS = Symbol("abs", Function(unary_dec(abs)))
ADD = Symbol("+", Function(binary_dec(add)))
CONTAINS = Symbol("contains", Function(binary_dec(contains)))
CONTAINS_UNICODE = Symbol("∋", Function(binary_dec(contains)))
COUNTOF = Symbol("countOf", Function(binary_dec(countOf)))
EQ = Symbol("=", Function(boolean_dec(binary_dec(eq))))
FLOORDIV = Symbol("//", Function(binary_dec(floordiv)))
GE = Symbol(">=", Function(binary_dec(ge)))
GE_UNICODE = Symbol("≥", Function(boolean_dec(binary_dec(ge))))
GETITEM = Symbol("getitem", Function(binary_dec(getitem)))
GT = Symbol(">", Function(binary_dec(gt)))
INDEXOF = Symbol("index", Function(number_dec(binary_dec(indexOf))))
IS = Symbol("is", Function(boolean_dec(binary_dec(is_))))
IS_UNICODE = Symbol("≡", Function(boolean_dec(binary_dec(is_))))
LE = Symbol("<=", Function(boolean_dec(binary_dec(le))))
LE_UNICODE = Symbol("≤", Function(boolean_dec(binary_dec(le))))
LT = Symbol("<", Function(boolean_dec(binary_dec(lt))))
MOD = Symbol("%", Function(binary_dec(mod)))
MUL = Symbol("*", Function(binary_dec(mul)))
MUL_UNICODE1 = Symbol("×", Function(binary_dec(mul)))
MUL_UNICODE2 = Symbol("⋅", Function(binary_dec(mul)))
NOT = Symbol("!", Function(boolean_dec(unary_dec(not_))))
NOT_UNICODE = Symbol("¬", Function(boolean_dec(unary_dec(not_))))
POW = Symbol("**", Function(binary_dec(pow)))
SUB = Symbol("-", Function(binary_dec(sub)))
SUB_UNICODE = Symbol("−", Function(binary_dec(sub)))
TRUEDIV = Symbol("/", Function(binary_dec(truediv)))
TRUEDIV_UNICODE1 = Symbol("÷", Function(binary_dec(truediv)))
TRUEDIV_UNICODE2 = Symbol("∕", Function(binary_dec(truediv)))
TRUTH = Symbol("?", Function(boolean_dec(binary_dec(truth))))


def prep(*args) -> Cons:
    return list_(*map(Number, args))

if __name__ == "__main__":
    from doctest import testmod
    testmod()
