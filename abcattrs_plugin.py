from typing import Callable
from typing import Optional
from typing import TypeVar

from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext
from mypy.plugin import Plugin

T = TypeVar("T")
CB = Optional[Callable[[T], None]]

abc_fullname = "abc.ABC"


def is_abstract(info: TypeInfo) -> bool:
    # info.mro vs info.bases
    return any(base.fullname == abc_fullname for base in info.mro)


def has_abstract_ancestor():
    ...


def is_concrete():
    ...


def mark_abstract_class_attrs(context: ClassDefContext) -> None:
    if context.cls.fullname != "prog.B":
        # print(context.cls.base_type_exprs[0])
        # print(f"{context.cls.metaclass=}")
        return

    # for base in context.cls.info.bases:
    #     print(base)
    abstract_attrs = set()
    for base in context.cls.info.mro:
        for name, defn in base.names.items():
            # print(name, )
            print(defn.kind)
            print(defn.)
            # print(defn.node.fullname, defn.type)

    print(context.cls.info.names)

    # print(context.cls.base_type_exprs)
    # print(context.cls.keywords)
    # print(context.cls.info)
    # print(context.cls.info.metadata)
    # print(context.cls.info.names)
    # print(context.cls.info.abstract_attributes)
    # print(context.cls.info.is_abstract)


class ABCAttrsPlugin(Plugin):
    def get_base_class_hook(self, fullname: str) -> "CB[ClassDefContext]":
        sym = self.lookup_fully_qualified(fullname)

        if sym and isinstance(sym.node, TypeInfo) and is_abstract(sym.node):
            return mark_abstract_class_attrs
        return None


def plugin(_version: str):
    return ABCAttrsPlugin
