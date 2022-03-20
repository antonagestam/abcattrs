import abc

from abcattrs import Abstract


class A(abc.ABC):
    foo: Abstract[int]


# Should error
class B(A):
    irrelevant = True
    undefined: bool
