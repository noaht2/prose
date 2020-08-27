#!/usr/bin/env python3

from typing import Dict, List, Any, Union, List, Optional
from types import FunctionType, BuiltinFunctionType
from operator import *
from copy import deepcopy

Value = Dict[str, Any]
Operator = Dict[str, Union[str, FunctionType]]
Integer = Dict[str, Union[int, str]]
Keyword = Var = Dict[str, str]
ProseList = Dict[str, Union[List[Value], str]]
ArgList = List[Value]
ScopeDict = Dict[str, Value]


def def_(args: ArgList) -> ProseList:
    """Define a variable.

    >>> print(write(evaluate(read(["def", "x", "1"]))))
    1
    >>> print(write(evaluate(read("x"))))
    1
    """
    variables[args[0]["underlying"]] = evaluate(args[1])
    return evaluate(args[0])


def del_(args: ArgList) -> ProseList:
    del variables[args[0]["underlying"]]
    return read([])


def let1(args: ArgList) -> Value:
    # print([write(arg) for arg in args])
    var, value, result = args
    if value_is_list(var):
        # print(var == read("app"))
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


#def let(args: ArgList) -> Value:
#    pairs, result = args
#    if len(args[0]["underlying"]) > 1:
#        var, value = pairs["underlying"][:2]
#        return let1([var, value, let([quote(pairs["underlying"][2:]), result])])


def change_scope(code: Value, scope: ScopeDict) -> Value:
    if value_is_list(code) and len(code["underlying"]) > 0:
        return {**quote([change_scope(value, scope) for value in code["underlying"]]),
                **{"scope": scope}}
    else:
        return {**code, **{"scope": scope}}


def lambda_(args: ArgList) -> Operator:
    global variables
    param = args[0]
    body = args[1]
    tempvars = deepcopy(variables)
    # print(args)
    # print("variables" in globals().keys())
    # print(param["display"], variables.keys())
    def abstraction(args: ArgList) -> Value:
        # print(variables == variablesL)
        # print("let1", write(param), write(args[0]), write(body))
        # print([arg["display"] for arg in args], "\t", tempvars.keys())
        return evaluate(change_scope(quote([read("let1"), param, args[0], body]), tempvars))
    return {"underlying": abstraction,
            "display": ["lambda", write(param), write(body)],
            "scope": variables}


def quote(args: ArgList) -> ProseList:
    # print(args)
    return {"underlying": args,
            "display": [write(arg) for arg in args],
            "scope": {}}


def evaluate_expression(args: ArgList):
    return evaluate(args[0])


def list_fn(args: ArgList) -> ProseList:
    return quote([evaluate(arg) for arg in args])


def if_(args: ArgList):
    if evaluate(args["underlying"][0]):
        return evaluate(args["underlying"][1])["underlying"]
    else:
        return evaluate(args["underlying"][2])["underlying"]


def first(args: ArgList) -> Value:
    return args[0]["underlying"][0]


def rest(args: ArgList) -> Value:
    if len(args) > 1:
        return args[0]["underlying"][1:]
    else:
        return read([])


# def add(args: ArgList) -> Integer:
#     for i in range(len(args)):
#         args[i] = evaluate(args[i])
#     n = sum(element["underlying"] for element in args)
#     return {"underlying": n,
#             "display": str(n)}


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


def arith_op(symbol: str, func: BuiltinFunctionType, ) -> None:
    def compute(args: ArgList) -> Value:
        args = [evaluate(arg) for arg in args]
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


def entry_is_int(entry: str) -> bool:
    try:
        return type(eval(entry)) is int
    except Exception:
        return False


def entry_is_str(entry: str) -> bool:
    try:
        return type(eval(entry)) is str
    except Exception:
        return False


#def entry_is_var(entry: str) -> bool:
#    return entry.startswith("-")


def read(entry: Union[list, str]) -> Value:
    if isinstance(entry, list):
        if len(entry) > 0:
            # print([read(element) for element in entry])
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


def evaluate(value: Value) -> Any:
    if value_is_list(value):
        if len(value["underlying"]) > 0:
            # print(value)
            value["underlying"][0] = evaluate(value["underlying"][0])
            return value["underlying"][0]["underlying"](value["underlying"][1:])
        else:
            return value
    elif value_is_int(value) or value_is_str(value):
        return value
    else:
        # print(value)
        if value["underlying"] in value["scope"]:
            return value["scope"][value["underlying"]]
        else:
            # print(value, value_is_var()
            return variables[value["underlying"]]


def write(value: Value) -> Union[list, str]:
    # print(value)
    return value["display"]


if __name__ == "__main__":
    from sys import argv, stdin
    if len(argv) == 1:
        program = stdin.read()
    elif len(argv) == 2:
        with open(argv[1]) as f:
            program = f.read()
    elif len(argv) == 3:
        with open(argv[2]) as f:
            program = "\n".join(f.read().split("\n")[1:])
    # print(program)
    print(write(evaluate(read(eval(program)))))
