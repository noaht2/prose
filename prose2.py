#!/usr/bin/env python3

from typing import Dict, List, Any, Union, List, Optional, Callable
from types import FunctionType, BuiltinFunctionType
from operator import *
from copy import deepcopy
from random import random

Entry = Union[str, list]
Value = Dict[str, Any]
Operator = Dict[str, Union[str, FunctionType]]
Integer = Dict[str, Union[int, str]]
Keyword = Var = Dict[str, str]
ProseList = Dict[str, Union[List[Value], str]]
ArgList = List[Value]
ScopeDict = Dict[str, Value]


def def_(args: ArgList) -> ProseList:
    """Define a variable.

    >>> write(evaluate(read(["def", "x", "1"])))
    "1"
    >>> print(write(evaluate(read("x"))))
    "1"
    """
    variables[args[0]["underlying"]] = evaluate(args[1])
    return evaluate(args[0])


def del_(args: ArgList) -> ProseList:
    """Remove a variables from `variables`."""
    del variables[args[0]["underlying"]]
    return read([])


def let1(args: ArgList) -> Value:
    var, value, result = args
    if value_is_list(var):
        # `var` is code that is evaluated to a variable
        return let1([evaluate(var), value, result])
    elif var["underlying"] in variables:
        old = variables[var["underlying"]]
        variables[var["underlying"]] = evaluate(value)
        result = evaluate(result)
        variables[var["underlying"]] = old
    else:
        variables[var["underlying"]] = evaluate(value)
        result = evaluate(result)
        del variables[var["underlying"]]
    return result


def change_scope(code: Value, scope: ScopeDict) -> Value:
    # Used for closures
    if value_is_list(code) and len(code["underlying"]) > 0:
        return {**quote([change_scope(value,
                                      scope) for value in code["underlying"]]),
                **{"scope": scope}}
    else:
        return {**code, **{"scope": scope}}


def lambda_(args: ArgList) -> Operator:
    global variables
    param, body = args
    tempvars = deepcopy(variables)
    def abstraction(args: ArgList) -> Value:
        if len(args) == 1:
            return evaluate(change_scope(quote([read("let1"),
                                                param,
                                                args[0],
                                                body]),
                                         tempvars))
        else:
            return evaluate(change_scope(quote([abstraction(args[:-1]),
                                                args[-1]]),
                                         tempvars))
    return {"underlying": abstraction,
            "display": ["lambda", write(param), write(body)],
            "scope": tempvars}


def quote(args: ArgList) -> ProseList:
    """Returns a `ProseList` of the arguments.

    (Without evaluating them first.)
    """
    return {"underlying": args,
            "display": [write(arg) for arg in args],
            "scope": {}}


def evaluate_expression(args: ArgList):
    return evaluate(args[0])


def list_fn(args: ArgList) -> ProseList:
    return quote([evaluate(arg) for arg in args])


def if_(args: ArgList):
    if evaluate(args["underlying"][0]):
        return evaluate(args["underlying"][1])
    else:
        return evaluate(args["underlying"][2])


def first(args: ArgList) -> Value:
    return evaluate(args[0])["underlying"][0]


def rest(args: ArgList) -> Value:
    """Returns the second item in a list onwards."""
    if len(args[0]) > 1:
        return args[0]["underlying"][1:]
    else:
        return read([])


def println(args: ArgList) -> List:
    for i in range(len(args)):
        args[i] = evaluate(args[i])
    for element in args:
        print(evaluate(element)["display"])
    return read([])


variables: ScopeDict = {"def":
                        {"underlying": def_,
                         "display": "def",
                         "scope": {}},
                        "lambda":
                        {"underlying": lambda_,
                         "display": "lambda",
                         "scope": {}},
                        "'":
                        {"underlying": quote,
                         "display": "'",
                         "scope": {}},
                        "eval":
                        {"underlying": evaluate_expression,
                         "display": "eval",
                         "scope": {}},
                        "let1":
                        {"underlying": let1,
                         "display": "let1",
                         "scope": {}},
                        "list":
                        {"underlying": list_fn,
                         "display": "list",
                         "scope": {}},
                        "if":
                        {"underlying": if_,
                         "display": "if",
                         "scope": {}},
                        "first":
                        {"underlying": first,
                         "display": "first",
                         "scope": {}},
                        "rest":
                        {"underlying": rest,
                         "display": "rest",
                         "scope": {}},
                        "+":
                        {"underlying": add,
                         "display": "+",
                         "scope": {}},
                        "println":
                        {"underlying": println,
                         "display": "println",
                        "scope": {}},
                        "true":
                        {"underlying": True,
                         "display": "true",
                         "scope": {}}}


def arith_op(symbol: str, func: BuiltinFunctionType) -> None:
    def compute(args: ArgList) -> Value:
        args = [evaluate(evaluate(arg)) for arg in args]
        current = args[0]["underlying"]
        for n in args[1:]:
            current = func(current, n["underlying"])
        return {"underlying": current,
                "display": str(current)}
    variables[symbol] = {"underlying": compute,
                         "display": symbol,
                         "scope": {}}


arith_op("+", add)
arith_op(r"/", floordiv)
arith_op("%", mod)
arith_op("*", mul)
arith_op("**", pow)
arith_op("-", sub)


def comparison(symbol: str, func: BuiltinFunctionType) -> None:
    def compare(args: ArgList) -> Value:
        args = [evaluate(arg) for arg in args]
        return read("true") if func(args[0], args[1]) else read([])
    variables[symbol] = {"underlying": compare,
                         "display": symbol,
                         "scope": {}}


comparison("<", lt)
comparison("<=", le)
comparison("==", eq)
comparison("!=", ne)
comparison(">=", ge)
comparison(">", gt)


def entry_is_int(entry: Entry) -> bool:
    try:
        return type(eval(entry)) is int
    except Exception:
        return False


def entry_is_str(entry: Entry) -> bool:
    try:
        return type(eval(entry)) is str
    except Exception:
        return False


def read(entry: Union[list, str]) -> Value:
    if isinstance(entry, list):
        if len(entry) > 0:
            return quote([read(element) for element in entry])
        else:
            return {"underlying": [],
                    "display": [],
                    "scope": {}}
    else:
        if entry_is_int(entry):
            return {"underlying": int(entry),
                    "display": str(int(entry)),
                    "scope": {}}
        elif entry_is_str(entry):
            return {"underlying": entry[1:-1],
                    "display": entry,
                    "scope": {}}
        else:
            # `entry` is a `var`
            return {"underlying": entry,
                    "display": entry,
                    "scope": {}}


def value_is_list(value: Value) -> bool:
    return type(value["underlying"]) is list


def value_is_int(value: Value) -> bool:
    return entry_is_int(write(value))


def value_is_str(value: Value) -> bool:
    try:
        return type(eval(value["display"])) is str
    except Exception:
        return False


def value_is_operator(value: Value):
    return isinstance(value["underlying"], Callable)


def value_is_atom(value: Value):
    return (value_is_int(value)
            or value_is_str(value)
            or value_is_operator(value))


def evaluate(value: Value) -> Any:
    if value_is_list(value):
        if len(value["underlying"]) > 0:
            value["underlying"][0] = evaluate(value["underlying"][0])
            # Evaluate operator
            return value["underlying"][0]["underlying"](value["underlying"][1:])
        else:
            return value
    elif value_is_atom(value):
        return value
    elif value["underlying"] in value["scope"]:  # var
        return value["scope"][value["underlying"]]
    else:
        return variables[value["display"]]


def write(value: Value) -> Entry:
    return value["display"]


if __name__ == "__main__":
    from sys import argv, stdin, stdout
    if len(argv) == 1:
        program = stdin.read()
    elif len(argv) == 2:
        with open(argv[1]) as f:
            program = f.read()
    elif len(argv) == 3:
        with open(argv[2]) as f:
            program = "\n".join(f.read().split("\n")[1:])
    print(write(evaluate(read(eval(program)))))
