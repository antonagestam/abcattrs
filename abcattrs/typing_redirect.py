import sys

if sys.version_info < (3, 10):
    from typing_extensions import Annotated
    from typing_extensions import get_type_hints
else:
    from typing import Annotated
    from typing import get_type_hints


from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Dict
from typing import Final
from typing import ForwardRef
from typing import Iterable
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin

__all__ = [
    "Annotated",
    "Any",
    "Callable",
    "ClassVar",
    "Dict",
    "Final",
    "ForwardRef",
    "Iterable",
    "Tuple",
    "Type",
    "TypeVar",
    "Union",
    "get_args",
    "get_origin",
    "get_type_hints",
]
