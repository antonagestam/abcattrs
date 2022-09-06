import abc

from abcattrs import Abstract

# from typing import _GenericAlias
# from typing import _SpecialForm
# from typing import _type_check


# @_SpecialForm
# def Abstract(self, parameters):
#     item = _type_check(parameters, f"{self} accepts only single type.")
#     return _GenericAlias(self, (item,))


class A(abc.ABC):
    foo: Abstract[int]
    bar: Abstract[int]
    other: int


class B(A, abc.ABC):
    baz: Abstract[int]
    bar = 1


# Should error: missing foo, missing baz
class C(B):
    irrelevant = True
    undefined: bool


class Foo:
    ...


class Bar(Foo):
    ...
