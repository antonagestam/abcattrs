import abc
from typing import Annotated
from typing import Any
from typing import ClassVar
from unittest import mock

import pytest

from abcattrs import Abstract
from abcattrs import UndefinedAbstractAttribute
from abcattrs import abstractattrs
from abcattrs import check_abstract_class_attributes


def test_base_class_saves_attributes() -> None:
    @abstractattrs
    class A(abc.ABC):
        bar: int
        foo: Abstract[int]

    assert not {"foo"} ^ A.__abstract_attributes__  # type: ignore[attr-defined]


def test_abstract_subclass_adds_to_attributes() -> None:
    @abstractattrs
    class A(abc.ABC):
        foo: Abstract[int]

    @abstractattrs
    class B(A, abc.ABC):
        bar: Abstract[str]

    assert not {"foo", "bar"} ^ B.__abstract_attributes__  # type: ignore[attr-defined]


def test_subclassing_without_defining_raises() -> None:
    @abstractattrs
    class A(abc.ABC):
        foo: Abstract[int]

    with pytest.raises(
        UndefinedAbstractAttribute,
        match=r"^Concrete class 'B' must define abstract class attribute 'foo'\.$",
    ):
        type("B", (A,), {})


def test_can_combine_qualifier_with_class_var() -> None:
    @abstractattrs
    class A(abc.ABC):
        foo: ClassVar[Abstract[int]]

    with pytest.raises(
        UndefinedAbstractAttribute,
        match=r"^Concrete class 'B' must define abstract class attribute 'foo'\.$",
    ):
        type("B", (A,), {})

    assert not {"foo"} ^ A.__abstract_attributes__  # type: ignore[attr-defined]


def test_can_combine_qualifier_with_annotated() -> None:
    other_annotation = object()

    @abstractattrs
    class A(abc.ABC):
        foo: Annotated[int, Abstract, other_annotation]

    assert not {"foo"} ^ A.__abstract_attributes__  # type: ignore[attr-defined]


def test_concrete_multiple_subclass_raises_for_all_missing_attributes() -> None:
    @abstractattrs
    class A(abc.ABC):
        foo: Abstract[int]

    @abstractattrs
    class B(A, abc.ABC):
        bar: Abstract[str]

    valid_a = {"foo": 1}
    valid_b = {"bar": "str"}

    with pytest.raises(
        UndefinedAbstractAttribute,
        match=r"^Concrete class 'C' must define abstract class attribute 'bar'\.",
    ):
        type("C", (B,), valid_a)

    with pytest.raises(
        UndefinedAbstractAttribute,
        match=r"^Concrete class 'D' must define abstract class attribute 'foo'\.$",
    ):
        type("D", (B,), valid_b)

    type("E", (B,), valid_a | valid_b)


def test_can_check_class_without_abstract_class_attributes() -> None:
    check_abstract_class_attributes(type("A", (), {}))


def test_existing_init_subclass_method_is_wrapped() -> None:
    init_subclass = mock.MagicMock()

    @abstractattrs
    class A(abc.ABC):
        def __init_subclass__(cls, class_arg: str, **kwargs: Any) -> None:
            init_subclass(cls, class_arg=class_arg, **kwargs)

        attr: Abstract[int]

    with pytest.raises(UndefinedAbstractAttribute):
        type("B", (A,), {}, class_arg="doot")

    init_subclass.assert_not_called()
    init_subclass.reset_mock()

    class C(A, class_arg="intact"):
        attr = 1

    init_subclass.assert_called_once_with(C, class_arg="intact")


def test_can_decorate_class_with_self_reference() -> None:
    @abstractattrs
    class A(abc.ABC):
        recursive: Abstract["A"]  # noqa: F821


def test_can_decorate_class_with_forward_reference() -> None:
    @abstractattrs
    class A(abc.ABC):
        forward: Abstract["B"]  # noqa: F821

    class B:
        ...

    class C(A):
        forward = B()
