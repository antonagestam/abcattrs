from typing import Annotated
from typing import ClassVar
from typing import Final
from typing import ForwardRef
from typing import get_args
from typing import get_origin
from typing import get_type_hints

max_iterations: Final = 10_000


class MaxIterations(RuntimeError):
    ...


def get_name_error_name(error: NameError) -> str:
    return str(error).split("'", 2)[1]


def get_resolvable_type_hints(cls: type) -> dict[str, type]:
    """
    Repeatedly attempt to resolve the type hints of the given class, handling the
    NameErrors produced by unresolvable names by inserting sentinel typing.ForwardRef
    objects.
    """
    local_ns = {cls.__name__: cls}

    for _ in range(max_iterations):
        try:
            return get_type_hints(cls, include_extras=True, localns=local_ns)
        except NameError as exception:
            name = get_name_error_name(exception)
            local_ns[name] = ForwardRef(name)  # type: ignore[assignment]
    else:  # pragma: no cover
        raise MaxIterations(
            f"Exceeded {max_iterations} iterations trying to resolve type hints of "
            f"{cls.__module__}.{cls.__qualname__}."
        )


def extract_annotated(hint: type) -> type | None:
    # Unwrap ClassVar[T] -> T.
    if get_origin(hint) is ClassVar:
        try:
            (hint,) = get_args(hint)
        # Wrong-argument ClassVars are very hard to produce at runtime, so pragma is
        # reasonable here.
        except ValueError:  # pragma: no cover
            return None

    if not get_origin(hint) is Annotated:
        return None

    return hint
