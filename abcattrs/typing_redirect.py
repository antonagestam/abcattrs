import sys

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
    from typing_extensions import Any
    from typing_extensions import Callable
    from typing_extensions import ClassVar
    from typing_extensions import Dict
    from typing_extensions import Final
    from typing_extensions import ForwardRef
    from typing_extensions import Iterable
    from typing_extensions import Tuple
    from typing_extensions import Type
    from typing_extensions import TypeVar
    from typing_extensions import Union
    from typing_extensions import get_args
    from typing_extensions import get_origin
    from typing_extensions import get_type_hints
else:
    from typing import Annotated
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
    from typing import get_type_hints

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
