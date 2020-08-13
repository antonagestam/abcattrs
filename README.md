# abcattrs

Abstract class attributes for ABCs.


```python
import abc
from abcattrs import abstractattrs, Abstract


@abstractattrs
class A:
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
