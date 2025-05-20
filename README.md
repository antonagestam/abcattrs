<h1 align=center>abcattrs</h1>

<p align=center>
    <a href=https://github.com/antonagestam/abcattrs/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/antonagestam/abcattrs/actions/workflows/ci.yaml/badge.svg?branch=main alt="CI Build Status"></a>
    <a href="https://codecov.io/gh/antonagestam/abcattrs"><img src="https://codecov.io/gh/antonagestam/abcattrs/branch/main/graph/badge.svg?token=QY7CX7C73R"/></a>
    <br>
    <a href=https://pypi.org/project/abcattrs/><img src=https://img.shields.io/pypi/v/abcattrs.svg?color=informational&label=PyPI alt="PyPI Package"></a>
    <a href=https://pypi.org/project/abcattrs/><img src=https://img.shields.io/pypi/pyversions/abcattrs.svg?color=informational&label=Python alt="Python versions"></a>
</p>

Abstract class attributes for ABCs.

### Examples

```python
import abc
from abcattrs import abstractattrs, Abstract


@abstractattrs
class A(abc.ABC):
    foo: Abstract[int]


# Abstract subclasses can add more required attributes.
class B(A, abc.ABC):
    bar: Abstract[str]


class C(B):
    # C must assign values to both of these attributes to not raise an error.
    foo = 1
    bar = "str"


# This raises an error.
class MissingBar(B):
    foo = 1


# This raises an error.
class MissingFoo(B):
    bar = "str"
```

The `Abstract` qualifier can be combined with other PEP 593 annotations.

```python
from typing import Annotated
import abc
from abcattrs import abstractattrs, Abstract


@abstractattrs
class A(abc.ABC):
    # Combine with other annotations
    bar: Annotated[str, Abstract, "other info"]
```
