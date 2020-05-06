#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from types import FunctionType, WrapperDescriptorType
from typing import *
import numbers
from operator import index
from itertools import islice, chain


def metadec(dec: FunctionType) -> Callable[[FunctionType], FunctionType]:
    def newdec(func: FunctionType) -> FunctionType:
        # print("metadec.newdec\t", dec, func)
        newfunc = dec(func)
        newfunc.__name__ = func.__name__
        newfunc.__qualname__ = func.__qualname__
        return newfunc

    newdec.__name__ = dec.__name__
    newdec.__qualname__ = dec.__qualname__
    return newdec


def default_eval(car: Object, cdr: Object) -> Object:
    # print("default_eval\t", car, cdr)
    if cdr is None:
        return car
    else:
        return Cons(car, cdr())


@metadec
def eval_dec(func: FunctionType) -> Callable[[Object, Object], Object]:
    def eval_(car: Object, cdr: Object) -> Object:
        # print("eval_dec.eval_\t", func, car, cdr)
        if cdr is None:
            return func(car)
        else:
            return func(car)(cdr)

    return eval_


class Object:
    def __init__(self, call: FunctionType = default_eval,
                 for_eval: bool = True):
        self.call = call
        self.for_eval = for_eval

    def __repr__(self):
        return (
            f"<{type(self).__name__} with call={self.call},"
            + f" for_eval={self.for_eval}>"
        )

    def __eq__(self, other):
        return self.call == other.call and not self.for_eval ^ other.for_eval

    def __bool__(self):
        return True

    def __call__(self, cdr: Optional[Object] = None):
        if self.for_eval:
            # print("Object.__call__\t", self, cdr, self.call)
            return self.call(self, cdr)
        else:
            self.for_eval = True
            return self

    def __add__(self, other):
        # print("Object.__add__\t", self, other)
        return self()+other

    def __radd__(self, other):
        # # # print("__radd__\t", self, self(), other)
        return self()+other


def cons_eval(car: Cons, cdr: Optional[Cons]) -> Object:
    # # print("cons_eval\t", car, car.car, car.cdr)
    no_cdr = car.car(car.cdr)
    if isinstance(cdr, type(None)):
        return no_cdr
    elif car == no_cdr:
        return Cons(car, cdr())
    else:
        return no_cdr(cdr)


class Cons(Object):
    def __init__(self, car: Object, cdr: Object, for_eval: bool = True):
        self.car = car
        self.cdr = cdr
        super().__init__(cons_eval, for_eval)

    def __repr__(self):
        return (
            f"Cons({repr(self.car)}, {repr(self.cdr)}, for_eval={self.for_eval})"
        )

    def __str__(self):
        if self.is_list():
            if self.for_eval:
                return "("+" ".join(map(str, self))+")"
            else:
                return "'("+" ".join(map(str, self))+")"
        else:
            if self.for_eval:
                return "(cons "+str(self.car)+" "+str(self.cdr)+")"
            else:
                return "'(cons "+str(self.car)+" "+str(self.cdr)+")"

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.car == other.car
            and self.cdr == other.cdr
        )

    def __ne__(self, other):
        return self.car != other.car or self.cdr != other.cdr

    def __len__(self):
        i = 0
        while True:
            try:
                self[i]
            except IndexError:
                break
            finally:
                i += 1
        return i-1

    def __getitem__(self, key):
        key = self.offset_max(key)
        try:
            if isinstance(key, slice):
                return list_(*islice(self, key.start, key.stop, key.step))
            else:
                key = index(key)
                return next(islice(self, key, key+1))
        except StopIteration:
            raise IndexError

    def __setitem__(self, key, value):
        key = int(key)
        if key == 0:
            self.car = value
        else:
            if isinstance(self.cdr, (Atom, EmptyList)):
                self.cdr = value
            else:
                self.cdr[key-1] = value

    def __iter__(self):
        if isinstance(self.cdr, Atom):
            return iter(self.split())
        else:
            return chain(iter([self.car]), iter(self.cdr))

    def split(self) -> tuple:
        """Return the whole cdr instead of just self[1]"""
        return self.car, self.cdr

    def is_list(self) -> bool:
        if isinstance(self.cdr, Cons):
            return self.cdr.is_list()
        else:
            return isinstance(self.cdr, EmptyList)

    def offset_max(self, key: Union[numbers.Integral, slice]):
        if isinstance(key, numbers.Integral):
            if key < 0:
                return len(self)+key
            else:
                return key
        elif isinstance(key, slice):
            return slice(
                self.offset_max(key.start),
                self.offset_max(key.stop),
                key.step
            )
        else:
            return key

    def replace(self, obj: Object, to: Object) -> None:
        if self.car == obj:
            self.car = to
        elif isinstance(self.car, Cons):
            self.car.replace(obj, to)
        if self.cdr == obj:
            self.cdr = to
        elif isinstance(self.cdr, Cons):
            self.cdr.replace(obj, to)

    @property
    def for_eval(self):
        # # print("for_eval\t", self.car, self.cdr)
        return self.car.for_eval  #  and self.cdr.for_eval

    @for_eval.setter
    def for_eval(self, value):
        # # print("for_eval.setter\t", repr(self), value)
        self.car.for_eval = value
        self.cdr.for_eval = value


class Atom(Object):
    pass


def empty_eval(car, cdr):
    return car if isinstance(cdr, (EmptyList, type(None))) else Cons(car, cdr)


class EmptyList(Object):
    # Should be Cons and Atom but cannot due to MRO.
    def __init__(self):
        super().__init__(empty_eval)

    def __repr__(self):
        return "EmptyList()"

    def __str__(self):
        return "()"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __ne__(self, other):
        return not isinstance(other, type(self))

    def __bool__(self):
        return False

    def __getitem__(self, key):
        return self

    def __iter__(self):
        return iter([])

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    @property
    def cons(self):
        return self

    @property
    def cdr(self):
        return self



class BuiltinWrapper(type):
    @staticmethod
    def parent_func_dec(builtin: WrapperDescriptorType) -> FunctionType:
        def modified_builtin(self, *args):
            result = builtin(self, *args)
            if result is NotImplemented:
                return result
            else:
                return type(self)(result)

        return modified_builtin

    def __new__(cls, name, bases, dct):
        Builtin = deepcopy(bases[0])

        class BuiltinChild(Builtin):
            pass

        for attr in dir(bases[0]):
            if attr in dct["override"]:
                setattr(
                    BuiltinChild,
                    attr,
                    cls.parent_func_dec(getattr(bases[0], attr))
                )
        return super().__new__(cls, name, (BuiltinChild,)+bases[1:], dct)


class String(str, Atom, metaclass=BuiltinWrapper):
    override = ["__add__", "__mul__", "__rmul__"]

    def __new__(cls, obj):
        return super().__new__(cls, obj)

    def __init__(self, obj):
        Atom.__init__(self)
        str.__init__(self)

    def __repr__(self):
        return "String("+super().__repr__()+")"

    def __str__(self):
        return '`'+super().__str__()+"'"

    def __bool__(self):
        return True

    def __getitem__(self, key):
        return super().__getitem__(int(key))


class Number(float, Atom, metaclass=BuiltinWrapper):
    override = [
        "__abs__", "__add__", "__floordiv__", "__mod__", "__mul__", "__neg__",
        "__pos__", "__pow__", "__rmul__", "__rpow__", "__rsub__",
        "__rtruediv__", "__sub__"
    ]

    def __new__(cls, obj):
        # print("Number.__new__\t", cls, obj)
        return super().__new__(cls, obj)

    def __init__(self, obj):
        Atom.__init__(self)
        float.__init__(self)

    def __repr__(self):
        return "Number("+super().__repr__()+")"

    def __bool__(self):
        return True


class Truth(object, Number):
    override: List[str] = []

    def __new__(cls):
        if not hasattr(cls, "value"):
            cls.value = super().__new__(cls, 1)
        return cls.value

    def __init__(self):
        Number.__init__(self, self)

    def __repr__(self):
        return "Truth()"

    def __str__(self):
        return "#t"


def boolean(obj: Object) -> Boolean:
    return Truth() if obj else NIL_VALUE


class Symbol(Atom):
    registered: Dict[str, Object] = {}

    def __init__(self, name: str, value: Optional[Object] = None):
        super().__init__(symbol_eval)
        self.name = name
        self.value = value
        # print("Symbol.__init__\t", self, name, value)

    def __repr__(self):
        if self.name in type(self).registered:
            return (
                f"Symbol({repr(self.name)}, {repr(self.value)})"  # +", for_eval="
                # + str(self.for_eval)+")"
            )
        else:
            return "Symbol("+repr(self.name)+")"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and (
                (not hasattr(self, "value") and not hasattr(other, "value"))
                or self.value == other.value
            )
        )

    def __ne__(self, other):
        return (
            not isinstance(other, type(self))
            or self.name != other.name
            or self.value != other.value
        )

    def __iter__(self):
        return iter(self.value)

    @property
    def value(self):
        # print("Symbol.value\t", self.name, type(self).registered[self.name])
        try:
            return type(self).registered[self.name]
        except KeyError:
            raise AttributeError

    @value.setter
    def value(self, value):
        # print("Symbol.value.setter\t", self, value)
        if value is not None:
            type(self).registered[self.name] = value

    @value.deleter
    def value(self):
        try:
            del type(self).registered[self.name]
        except KeyError:
            pass

    @property
    def for_eval(self):
        return hasattr(self, "value")

    @for_eval.setter
    def for_eval(self, value):
        pass


def symbol_eval(car: Symbol, cdr: Optional[Object]) -> Cons:
    if hasattr(car, "value"):
        return car.value(cdr)
    elif cdr is None:
        return car
    else:
        return Cons(car, cdr)


@metadec
def eval_func_dec(func: FunctionType
                  ) -> Callable[[FunctionType, Object], Object]:
    def eval_func(car: Function, cdr: Object) -> Object:
        # print("eval_func\t", func.__name__, "\t", cdr())
        return func(cdr())()

    return eval_func


@metadec
class Function(Atom):
    def __init__(self, func: FunctionType, for_eval: bool = True):
        super().__init__(eval_func_dec(func), for_eval)

    @property
    def __name__(self):
        return self.call.__name__

    @__name__.setter
    def __name__(self, value):
        self.call.__name__ = value


@metadec
def eval_default_macro_dec(func: FunctionType
                  ) -> Callable[[Macro, Object], Object]:
    def eval_macro(car: Macro, cdr: Object) -> Object:
        # # print("eval_macro\t", func, car, cdr)
        return func(cdr)

    return eval_macro


class Macro(Atom):
    def __init__(self, func: FunctionType, for_eval: bool = True):
        super().__init__(func, for_eval)


def list_(*elements: Object, for_eval: bool = True) -> Cons:
    result = Cons(elements[0], NIL_VALUE, for_eval=for_eval)
    for element in elements[1:]:
        result[-1] = Cons(element, NIL_VALUE)
    return result


Boolean = Union[Truth, EmptyList]
NIL = Symbol("nil", EmptyList())
NIL_VALUE = NIL()

# recurring: Set[str] = set()
