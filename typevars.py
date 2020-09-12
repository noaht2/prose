#!/usr/bin/env python3

from typing import Dict, List, Any, Union, Tuple, Optional, Callable
from types import FunctionType

__all__ = ["Entry", "Value", "Operator", "Integer", "Keyword", "ProseList",
           "ArgList", "ScopeDict"]

Entry = Union[str, tuple]
Value = Dict[str, Any]
Operator = Dict[str, Union[str, FunctionType]]
Integer = Dict[str, Union[int, str]]
Keyword = Var = Dict[str, str]
ProseList = Dict[str, Union[List[Value], str]]
ArgList = Tuple[Value]
ScopeDict = Dict[str, Value]
