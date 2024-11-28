from ._version import __version__
from ._version import __version_tuple__
from .abcattrs import Abstract
from .abcattrs import UndefinedAbstractAttribute
from .abcattrs import abstractattrs
from .abcattrs import check_abstract_class_attributes

__all__ = (
    "__version__",
    "__version_tuple__",
    "Abstract",
    "UndefinedAbstractAttribute",
    "abstractattrs",
    "check_abstract_class_attributes",
)
