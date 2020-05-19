#!/usr/bin/env python3

"""The core low-level features of Prose"""

from __future__ import annotations

__all__ = [
    "metadec", "Object", "Cons", "Atom", "EmptyList", "String", "Number",
    "Truth", "boolean", "Symbol", "Function", "eval_default_macro_dec",
    "Macro", "list_", "Boolean", "NIL", "EmptyList"
]

from copy import deepcopy

from types import FunctionType, WrapperDescriptorType, MethodType
from typing import *
import numbers
from operator import index
from itertools import islice, chain


def metadec(dec: FunctionType) -> Callable[[FunctionType], FunctionType]:
    """A decorator that should be applied to all decorators.

    Define a new decorator that does not change the name of the function
    it acts on.
    """

    def newdec(func: FunctionType) -> FunctionType:
        # print("metadec.newdec\t", dec, func)
        newfunc = dec(func)
        newfunc.__name__ = func.__name__
        newfunc.__qualname__ = func.__qualname__
        return newfunc

    newdec.__name__ = dec.__name__
    newdec.__qualname__ = dec.__qualname__

    # newdec.__annotations__ = dec.__annotations__
    # newdec.__defaults__ = dec.__defaults__
    newdec.__doc__ = dec.__doc__
    return newdec


def default_eval(car: Object, cdr: Object) -> Object:
    """Evaluation for ``Object``"""
    # print("default_eval\t", car, cdr)
    if cdr is None:
        return car
    else:
        return Cons(car, cdr())


class Object:
    """The base Prose object.

    Instance variables:
    ``call``
        A function that is indirectly called by the ``__call__`` method.
        It must take two arguments:
        - ``self``
        - ``cdr``
    ``for_eval``
        If evaluation is attempted, ``self`` is returned and ``self.for_eval``
        is set to ``False``.
    """
    def __init__(self, call: Callable = default_eval,
                 for_eval: bool = True):
        self.call = MethodType(call, self)
        self.for_eval = for_eval

    def __repr__(self):
        return (
            f"<{type(self).__name__} with call={self.call},"
            + f" for_eval={self.for_eval}>"
        )

    def __eq__(self, other):
        return self.call == other.call and self.for_eval == other.for_eval

    def __bool__(self):
        return True

    def __call__(self, cdr: Optional[Object] = None):
        if self.for_eval:
            # print("Object.__call__\t", self, cdr, self.call)
            return self.call(cdr)
        else:
            self.for_eval = True
            return self


def cons_eval(car: Cons, cdr: Optional[Cons]) -> Object:
    """Evaluation for ``Cons``"""
    # print("cons_eval\t", car, car.car, car.cdr)
    no_cdr = car.car(car.cdr)
    if isinstance(cdr, type(None)):
        return no_cdr
    else:
        return no_cdr(cdr)


class Cons(Object):
    """The most common data type: the cons cell (a pair of values)

    A cons cell is a list if its ``cdr`` is a list. The cons cell not part a
    ``Cons`` object is the empty list (``EmptyList``), which is an instance of
    ``EmptyList``.

    Instance variables:
    ``car``
        The first item in the pair
    ``cdr``
        The second item in the pair

    Methods:
    ``split``
        Return the car and cdr as a tuple.
    ``is_list``
        Return whether the cons cell is a list.
    ``offset_max``
        Convert negative indices to positive.
    ``replace``
        Replace an item in the cons cell.
    """

    def __init__(self, car: Object, cdr: Object, for_eval: bool = True):
        self.car = car
        self.cdr = cdr
        super().__init__(cons_eval, for_eval)

    def __repr__(self):
        return (
            f"Cons({repr(self.car)}, {repr(self.cdr)}"
            + f", for_eval={self.for_eval})"
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
        # print((Atom, type(EmptyList)))
        if key == 0:
            self.car = value
        elif isinstance(self.cdr, (Atom, type(EmptyList))):
            self.cdr = value
        else:
            self.cdr[key-1] = value

    def __iter__(self):
        if isinstance(self.cdr, Atom):
            return iter(self.split())
        else:
            return chain(iter([self.car]), iter(self.cdr))

    def split(self) -> tuple:
        """Return the car and cdr as a tuple.

        Return the whole cdr instead of just ``self[1]``.
        """
        return self.car, self.cdr

    def is_list(self) -> bool:
        """Return whether the cons cell is a list."""
        if isinstance(self.cdr, Cons):
            return self.cdr.is_list()
        else:
            return isinstance(self.cdr, type(EmptyList))

    def offset_max(self, key: Union[numbers.Integral, slice]):
        """Convert negative indices to positive."""
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
        """Replace ``obj`` with ``to``.

        If ``self.car`` or ``self.cdr`` are equal to ``obj``, they are
        replaced by ``to``.  Otherwise, if ``self.car`` or ``self.cdr``
        are cons cells, ``replace`` is tried recursively on them with
        the same arguments.
        """
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
        # print("for_eval\t", self.car, self.cdr)
        return self.car.for_eval  #  and self.cdr.for_eval

    @for_eval.setter
    def for_eval(self, value):
        # print("for_eval.setter\t", repr(self), value)
        self.car.for_eval = value
        self.cdr.for_eval = value


class Atom(Object):
    """The base class for non-``Cons`` objects.

    The empty list is an atom but ``EmptyList`` is not a subclass of
    ``Atom``.  For more information, see ``EmptyList``.
    """


def empty_eval(car, cdr):
    return car if isinstance(
        cdr, (type(EmptyList), type(None))
    ) else Cons(car, cdr)


def singleton(cls: type) -> object:
    return cls()

@singleton
class EmptyList(Object):
    """The empty list.

    The empty list is both an atom and a cons cell but because of how I
    have translated the Prose types into Python, ``EmptyList`` is only
    a subclass of ``Object``.

    Do not call this directly; instead use ``EmptyList``.

    Properties:
    ``car``, ``cdr``
        Both are ``self``.  This is for the Prose functions ``car`` and
        ``cdr``.
    """
    def __init__(self):
        super().__init__(empty_eval)

    def __repr__(self):
        return "EmptyList"

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
    """Metaclass for Prose types that are subclasses of Python bultins.

    The class must put a container called ``override`` with the dunder
    methods to override in the class body.  For each of the methods of
    the first parent, which should be the builtin, with a name in
    ``override``, the method with that name in the new class becomes
    that of the parent decorated by the static method
    ``parent_func_dec``, which returns a function.

    Static method:
    ``parent_func_dec``
        Return a new function that acts as a method, which returns
        ``type(self)`` called with the output of the argument method.
    """
    @staticmethod
    @metadec
    def parent_func_dec(builtin: WrapperDescriptorType) -> FunctionType:
        """Override builtin dunders.

        Return a new function that acts as a method, which returns
        ``type(self)`` called with the output of the argument method.
        """

        def modified_builtin(self, *args):
            result = builtin(self, *args)
            if result is NotImplemented:
                return result
            else:
                return type(self)(result)

        return modified_builtin

    def __new__(cls, name: str, bases: Tuple[type, type], dct: Dict[str, Any]):
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


class Truth(Object, int):
    """The truth value.

    A singleton class.
    """

    def __new__(cls):
        # print("Truth.__new__\t", cls, cls.__bases__)
        if not hasattr(cls, "value"):
            cls.value = super().__new__(cls, 1)
        return cls.value

    def __repr__(self):
        return "Truth()"

    def __str__(self):
        return "#t"

    def __bool__(self):
        return True


def boolean(obj: Object) -> Boolean:
    """Return a Prose boolean from the truth value of a Python object.
    """
    return Truth() if obj else EmptyList

# ......................................................................
class Symbol(Atom):
    """A symbol for a value.

    Symbols in Prose are the equivalent of variables in other languages,
    except they are values that can be manipulated like any other (like
    pointers with names).

    Class variable:
    ``registered``
        A dictionary from the symbolnames to their values.  Symbols are
        really just key, value pairs in this dictionaru with an OOP API.

    Instance variable:
    ``name``

    Property:
    ``value``
    """
    registered: Dict[str, Object] = {}

    def __init__(self, name: str, value: Optional[Object] = None):
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

    def call(self, cdr: Optional[Object]) -> Cons:
        if hasattr(self, "value"):
            return self.value(cdr)
        elif cdr is None:
            return self
        else:
            return Cons(self, cdr)


@metadec
def eval_func_dec(func: FunctionType
                  ) -> Callable[[FunctionType, Object], Object]:
    def eval_func(car: Function, cdr: Object) -> Object:
        # print("eval_func\t", func.__name__, "\t", cdr())
        return func(cdr())()

    return eval_func


@metadec
class Function(Atom):
    """The function type.

    The arguments are evaluated (possibly on each other) before being
    passed to the function.
    """

    def __init__(self, func: FunctionType, for_eval: bool = True):
        """``func`` should act on act on its arguments (not itself)."""
        super().__init__(eval_func_dec(func), for_eval)

    @property
    def __name__(self):
        return self.call.__name__

    @__name__.setter
    def __name__(self, value):
        try:
            self.call.__name__ = value
        except AttributeError:
            pass


@metadec
def eval_default_macro_dec(func: FunctionType) -> Callable[[Macro, Object], Object]:
    def eval_macro(car: Macro, cdr: Object) -> Object:
        # # print("eval_macro\t", func, car, cdr)
        return func(cdr)

    return eval_macro


class Macro(Atom):
    """Macros have their own evaluation rules."""
    def __init__(self, func: FunctionType, for_eval: bool = True):
        """
        ``func`` acts on the cons cell of the macro and its
        arguments.
        """
        super().__init__(func, for_eval)


def list_(*elements: Object, for_eval: bool = True) -> Cons:
    result = Cons(elements[0], EmptyList, for_eval=for_eval)
    for element in elements[1:]:
        result[-1] = Cons(element, EmptyList)
    return result


Boolean = Union[Truth, type(EmptyList)]
NIL = Symbol("nil", EmptyList)

# recurring: Set[str] = set()
