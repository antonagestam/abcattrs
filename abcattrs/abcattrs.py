import abc
from functools import partial
from functools import wraps
from typing import Annotated
from typing import Any
from typing import Callable
from typing import Final
from typing import Iterable
from typing import TypeVar
from typing import get_args

from .type_hints import extract_annotated
from .type_hints import get_resolvable_type_hints

_abstract_marker: Final = object()
_O = TypeVar("_O")
Abstract = Annotated[_O, _abstract_marker]


def get_abstract_attributes(cls: type) -> Iterable[tuple[str, type]]:
    for var, hint in get_resolvable_type_hints(cls).items():
        annotated = extract_annotated(hint)
        if not annotated:
            continue
        # Checking for both the abstract marker and the type alias itself allows both
        # a concise way using e.g. `var: Abstract[int]` as well as a verbose way that
        # allows combining the qualifier with other annotated types and qualifiers, e.g.
        # `var: Annotated[int, Abstract, Other]`.
        if {_abstract_marker, Abstract} & set(get_args(annotated)):
            yield var, annotated


C = TypeVar("C")


def abstractattrs(cls: C) -> C:
    attributes = get_abstract_attributes(cls)  # type: ignore[arg-type]

    # Save metadata about the abstract attributes on the decorated class. By merging
    # with any already defined attributes we support multiple decorations and
    # inheritance.
    cls.__abstract_attributes__ = frozenset(  # type: ignore[attr-defined]
        {var for var, _ in attributes} | getattr(cls, "__abstract_attributes__", set())
    )

    # Add an __init_subclass__ method to the base class. If it already defines one, we
    # wrap it inside a function that will first check the subclasses' class attributes
    # and then call the already existing method.
    cls.__init_subclass__ = (  # type: ignore[assignment]
        classmethod(  # type: ignore[assignment]
            wraps(cls.__init_subclass__)(
                partial(
                    _init_subclass,
                    existing_init_subclass=(
                        cls.__init_subclass__.__func__  # type: ignore[attr-defined]
                    ),
                )
            )
        )
        if "__init_subclass__" in cls.__dict__
        else classmethod(_init_subclass)
    )

    return cls


class UndefinedAbstractAttribute(TypeError):
    ...


def check_abstract_class_attributes(cls: type) -> None:
    """Check that a class defines inherited abstract attributes."""
    if abc.ABC in cls.__bases__:
        return

    for attr in getattr(cls, "__abstract_attributes__", ()):
        if not hasattr(cls, attr):
            raise UndefinedAbstractAttribute(
                f"Concrete class {cls.__qualname__!r} must define abstract "
                f"class attribute {attr!r}."
            )


def _init_subclass(
    cls: type,
    existing_init_subclass: Callable[..., None] | None = None,
    *args: Any,
    **kwargs: Any,
) -> None:
    """
    __init_subclass__ implementation added to classes decorated with @abstractattrs.
    """
    super(cls).__init_subclass__()  # type: ignore[misc]
    check_abstract_class_attributes(cls)
    if existing_init_subclass is not None:
        existing_init_subclass(cls, *args, **kwargs)
