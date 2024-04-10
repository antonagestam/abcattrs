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
    from typing import Annotated  # type: ignore[attr-defined]
    from typing import Any  # type: ignore[attr-defined]
    from typing import Callable  # type: ignore[attr-defined]
    from typing import ClassVar  # type: ignore[attr-defined]
    from typing import Dict  # type: ignore[attr-defined]
    from typing import Final  # type: ignore[attr-defined]
    from typing import ForwardRef  # type: ignore[attr-defined]
    from typing import Iterable  # type: ignore[attr-defined]
    from typing import Tuple  # type: ignore[attr-defined]
    from typing import Type  # type: ignore[attr-defined]
    from typing import TypeVar  # type: ignore[attr-defined]
    from typing import Union  # type: ignore[attr-defined]
    from typing import get_args  # type: ignore[attr-defined]
    from typing import get_origin  # type: ignore[attr-defined]
    from typing import get_type_hints  # type: ignore[attr-defined]

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
