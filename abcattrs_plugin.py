from __future__ import annotations

from typing import Callable
from typing import Final
from typing import TypeAlias
from typing import TypeVar

from mypy.nodes import MDEF
from mypy.nodes import Block
from mypy.nodes import ClassDef
from mypy.nodes import Context
from mypy.nodes import SymbolTable
from mypy.nodes import TypeInfo
from mypy.nodes import Var
from mypy.plugin import AnalyzeTypeContext
from mypy.plugin import ClassDefContext
from mypy.plugin import Plugin
from mypy.types import Instance

abc_fullname: Final = "abc.ABC"
abstract_fullname: Final = "abcattrs.abcattrs.Abstract"


def is_abstract(info: TypeInfo) -> bool:
    return any(base.type.fullname == abc_fullname for base in info.bases)


def has_abstract_ancestor(info: TypeInfo) -> bool:
    return any(base.fullname == abc_fullname for base in info.mro)


def mark_abstract_class_attrs(context: ClassDefContext) -> None:
    if is_abstract(context.cls.info):
        return
    if not has_abstract_ancestor(context.cls.info):
        return

    print(f"checking {context.cls.fullname}")

    # for base in context.cls.info.bases:
    #     print(base)
    assignments = set()
    abstract_definitions = set()
    for base in context.cls.info.mro:
        for name, defn in base.names.items():
            # Filter for class member definitions only.
            if defn.kind != MDEF or defn.node is None or not isinstance(defn.node, Var):
                continue
            if defn.node.has_explicit_value:
                assignments.add(defn.node.name)
                print(f"{base.fullname} assigns {defn.node.name}")

            if defn.node.type is None:
                continue

            if not isinstance(defn.node.type, Instance):
                continue

            namespace = defn.node.type.type.metadata.get("abcattrs", {})
            if namespace.get("is_abstract", False):
                print(f"{base.fullname} defines {defn.node.name}")
                abstract_definitions.add(defn.node.name)

    if missing_assignments := abstract_definitions - assignments:
        failing_context = Context()
        failing_context.set_line(
            target=context.cls.line,
            column=context.cls.column,
            end_line=context.cls.end_line,
            end_column=context.cls.end_column,
        )
        for missing_name in missing_assignments:
            context.api.fail(
                (
                    f"Concrete class {context.cls.name!r} is missing a value for "
                    f"abstract attribute {missing_name!r}."
                ),
                failing_context,
            )


# def create_type_info(name: str, bases: list[Instance]) -> TypeInfo:
#     classdef = ClassDef(name, Block([]))
#     classdef.fullname = "abcattrs.sentinel"
#     new_typeinfo = TypeInfo(SymbolTable(), classdef, "abcattrs")
#     new_typeinfo.bases = bases
#     new_typeinfo.metadata = {"abcattrs": "was here!"}
#     # calculate_mro(new_typeinfo)
#     # new_typeinfo.calculate_metaclass_type()
#     classdef.info = new_typeinfo
#     return new_typeinfo


def type_analyze(context: AnalyzeTypeContext) -> None:
    inner_type = context.api.anal_type(context.type.args[0])
    assert isinstance(inner_type, Instance)
    # FIXME: Need to create a unique typeinfo here?
    inner_type.type.metadata.setdefault("abcattrs", {"is_abstract": True})
    return inner_type


T = TypeVar("T")
CB: TypeAlias = Callable[[T], None] | None


class ABCAttrsPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> CB[AnalyzeTypeContext]:
        if fullname == abstract_fullname:
            return type_analyze

    def get_base_class_hook(self, fullname: str) -> CB[ClassDefContext]:
        return mark_abstract_class_attrs


def plugin(_version: str) -> type[ABCAttrsPlugin]:
    return ABCAttrsPlugin
