import abc
from typing import Annotated
from unittest import mock

import pytest

from abcattrs import Abstract
from abcattrs import UndefinedAbstractAttribute
from abcattrs import abstractattrs
from abcattrs import check_abstract_class_attributes


def test_base_class_saves_attributes() -> None:
    @abstractattrs
    class A(abc.ABC):
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


def test_can_combine_annotations() -> None:
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

    type("E", (B,), valid_a | valid_b)  # type: ignore[operator]


def test_can_check_class_without_abstract_class_attributes() -> None:
    check_abstract_class_attributes(type("A", (), {}))


def test_existing_init_subclass_method_is_wrapped() -> None:
    init_subclass = mock.MagicMock()

    @abstractattrs
    class A(abc.ABC):
        __init_subclass__ = init_subclass
        attr: Abstract[int]

    with pytest.raises(UndefinedAbstractAttribute):
        type("B", (A,), {})

    init_subclass.assert_not_called()

    class C(A, class_arg="intact"):
        attr = 1

    init_subclass.assert_called_once_with(C, class_arg="intact")
