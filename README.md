<h1 align=center>abcattrs</h1>

<p align=center>
    <a href=https://github.com/antonagestam/abcattrs/actions?query=workflow%3ACI+branch%3Amain><img src=https://github.com/antonagestam/abcattrs/workflows/CI/badge.svg alt="CI Build Status"></a>
    <a href="https://codecov.io/gh/antonagestam/abcattrs"><img src="https://codecov.io/gh/antonagestam/abcattrs/branch/main/graph/badge.svg?token=QY7CX7C73R"/></a>
</p>

Abstract class attributes for ABCs.

```python
import abc
from abcattrs import abstractattrs, Abstract


@abstractattrs
class A(abc.ABC):
    foo: Abstract[int]


# Abstract subclasses can add more required attributes
@abstractattrs
class B(A, abc.ABC):
    bar: Abstract[str]


class C(B):
    # C must define both of these attributes to not raise an error
    foo = 1
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
