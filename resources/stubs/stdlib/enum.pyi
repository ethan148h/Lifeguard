import _typeshed
import sys
import types
from _typeshed import SupportsKeysAndGetItem, Unused
from builtins import property as _builtins_property
from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Any, Final, Generic, Literal, TypeVar, overload
from typing_extensions import disjoint_base, Self, TypeAlias


__all__ = ["EnumMeta", "Enum", "IntEnum", "Flag", "IntFlag", "auto", "unique"]

if sys.version_info >= (3, 11):
    __all__ += [
        "CONFORM",
        "CONTINUOUS",
        "EJECT",
        "EnumCheck",
        "EnumType",
        "FlagBoundary",
        "KEEP",
        "NAMED_FLAGS",
        "ReprEnum",
        "STRICT",
        "StrEnum",
        "UNIQUE",
        "global_enum",
        "global_enum_repr",
        "global_flag_repr",
        "global_str",
        "member",
        "nonmember",
        "property",
        "verify",
        "pickle_by_enum_name",
        "pickle_by_global_name",
    ]

if sys.version_info >= (3, 13):
    __all__ += ["EnumDict"]

_EnumMemberT = TypeVar("_EnumMemberT")
_EnumerationT = TypeVar("_EnumerationT", bound=type[Enum])

# The following all work:
# >>> from enum import Enum
# >>> from string import ascii_lowercase
# >>> Enum('Foo', names='RED YELLOW GREEN')
# <enum 'Foo'>
# >>> Enum('Foo', names=[('RED', 1), ('YELLOW, 2)])
# <enum 'Foo'>
# >>> Enum('Foo', names=((x for x in (ascii_lowercase[i], i)) for i in range(5)))
# <enum 'Foo'>
# >>> Enum('Foo', names={'RED': 1, 'YELLOW': 2})
# <enum 'Foo'>
_EnumNames: TypeAlias = (
    str | Iterable[str] | Iterable[Iterable[str | Any]] | Mapping[str, Any]
)
_Signature: TypeAlias = Any  # TODO: Unable to import Signature from inspect module

if sys.version_info >= (3, 11):
    class nonmember(Generic[_EnumMemberT]):
        value: _EnumMemberT
        def __init__(self, value: _EnumMemberT) -> None: no_effects()

    class member(Generic[_EnumMemberT]):
        value: _EnumMemberT
        def __init__(self, value: _EnumMemberT) -> None: no_effects()

class _EnumDict(dict[str, Any]):
    if sys.version_info >= (3, 13):
        def __init__(self, cls_name: str | None = None) -> None: no_effects()
    else:
        def __init__(self) -> None: no_effects()

    def __setitem__(self, key: str, value: Any) -> None: ...
    if sys.version_info >= (3, 11):
        # See comment above `typing.MutableMapping.update`
        # for why overloads are preferable to a Union here
        #
        # Unlike with MutableMapping.update(), the first argument is required,
        # hence the type: ignore
        @overload  # type: ignore[override]
        def update(
            self, members: SupportsKeysAndGetItem[str, Any], **more_members: Any
        ) -> None: mutation()
        @overload
        def update(
            self, members: Iterable[tuple[str, Any]], **more_members: Any
        ) -> None: mutation()
    if sys.version_info >= (3, 13):
        @property
        def member_names(self) -> list[str]: no_effects()

if sys.version_info >= (3, 13):
    EnumDict = _EnumDict

# Structurally: Iterable[T], Reversible[T], Container[T] where T is the enum itself
class EnumMeta(type):
    if sys.version_info >= (3, 11):
        def __new__(
            metacls: type[_typeshed.Self],
            cls: str,
            bases: tuple[type, ...],
            classdict: _EnumDict,
            *,
            boundary: FlagBoundary | None = None,
            _simple: bool = False,
            **kwds: Any,
        ) -> _typeshed.Self: no_effects()
    else:
        def __new__(
            metacls: type[_typeshed.Self],
            cls: str,
            bases: tuple[type, ...],
            classdict: _EnumDict,
            **kwds: Any,
        ) -> _typeshed.Self: no_effects()

    @classmethod
    def __prepare__(
        metacls, cls: str, bases: tuple[type, ...], **kwds: Any
    ) -> _EnumDict: no_effects()  # type: ignore[override]
    def __iter__(self: type[_EnumMemberT]) -> Iterator[_EnumMemberT]: no_effects()
    def __reversed__(self: type[_EnumMemberT]) -> Iterator[_EnumMemberT]: no_effects()
    if sys.version_info >= (3, 12):
        def __contains__(self: type[Any], value: object) -> bool: no_effects()
    elif sys.version_info >= (3, 11):
        def __contains__(self: type[Any], member: object) -> bool: no_effects()
    elif sys.version_info >= (3, 10):
        def __contains__(self: type[Any], obj: object) -> bool: no_effects()
    else:
        def __contains__(self: type[Any], member: object) -> bool: no_effects()

    def __getitem__(self: type[_EnumMemberT], name: str) -> _EnumMemberT: no_effects()
    @_builtins_property
    def __members__(
        self: type[_EnumMemberT],
    ) -> types.MappingProxyType[str, _EnumMemberT]:
        """
        Returns a mapping of member name->value.

        This mapping lists all enum members, including aliases. Note that this
        is a read-only view of the internal mapping.
        """
        ...
    def __len__(self) -> int: no_effects()
    def __bool__(self) -> Literal[True]: no_effects()
    def __dir__(self) -> list[str]: no_effects()

    # Overload 1: Value lookup on an already existing enum class (simple case)
    @overload
    def __call__(
        cls: type[_EnumMemberT], value: Any, names: None = None
    ) -> _EnumMemberT: no_effects()

    # Overload 2: Functional API for constructing new enum classes.
    if sys.version_info >= (3, 11):
        @overload
        def __call__(
            cls,
            value: str,
            names: _EnumNames,
            *,
            module: str | None = None,
            qualname: str | None = None,
            type: type | None = None,
            start: int = 1,
            boundary: FlagBoundary | None = None,
        ) -> type[Enum]: no_effects()
    else:
        @overload
        def __call__(
            cls,
            value: str,
            names: _EnumNames,
            *,
            module: str | None = None,
            qualname: str | None = None,
            type: type | None = None,
            start: int = 1,
        ) -> type[Enum]: no_effects()

    # Overload 3 (py312+ only): Value lookup on an already existing enum class (complex case)
    #
    # >>> class Foo(enum.Enum):
    # ...     X = 1, 2, 3
    # >>> Foo(1, 2, 3)
    # <Foo.X: (1, 2, 3)>
    #
    if sys.version_info >= (3, 12):
        @overload
        def __call__(
            cls: type[_EnumMemberT], value: Any, *values: Any
        ) -> _EnumMemberT: no_effects()
    if sys.version_info >= (3, 14):
        @property
        def __signature__(cls) -> _Signature: no_effects()

    _member_names_: list[str]  # undocumented
    _member_map_: dict[str, Enum]  # undocumented
    _value2member_map_: dict[Any, Enum]  # undocumented

if sys.version_info >= (3, 11):
    # In 3.11 `EnumMeta` metaclass is renamed to `EnumType`, but old name also exists.
    EnumType = EnumMeta

    class property(types.DynamicClassAttribute):
        def __set_name__(self, ownerclass: type[Enum], name: str) -> None: ...
        name: str
        clsname: str
        member: Enum | None

    _magic_enum_attr = property
else:
    _magic_enum_attr = types.DynamicClassAttribute

class Enum(metaclass=EnumMeta):
    @_magic_enum_attr
    def name(self) -> str: no_effects()
    @_magic_enum_attr
    def value(self) -> Any: no_effects()
    _name_: str
    _value_: Any
    _ignore_: str | list[str]
    _order_: str
    __order__: str
    @classmethod
    def _missing_(cls, value: object) -> Any: no_effects()
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any: no_effects()
    # It's not true that `__new__` will accept any argument type,
    # so ideally we'd use `Any` to indicate that the argument type is inexpressible.
    # However, using `Any` causes too many false-positives for those using mypy's `--disallow-any-expr`
    # (see #7752, #2539, mypy/#5788),
    # and in practice using `object` here has the same effect as using `Any`.
    def __new__(cls, value: object) -> Self: no_effects()
    def __dir__(self) -> list[str]: no_effects()
    def __hash__(self) -> int: no_effects()
    def __format__(self, format_spec: str) -> str: no_effects()
    def __reduce_ex__(self, proto: Unused) -> tuple[Any, ...]: no_effects()
    if sys.version_info >= (3, 11):
        def __copy__(self) -> Self: no_effects()
        def __deepcopy__(self, memo: Any) -> Self: no_effects()
    if sys.version_info >= (3, 12) and sys.version_info < (3, 14):
        @classmethod
        def __signature__(cls) -> str: no_effects()
    if sys.version_info >= (3, 13):
        # Value may be any type, even in special enums. Enabling Enum parsing from
        # multiple value types
        def _add_value_alias_(self, value: Any) -> None: mutation()
        def _add_alias_(self, name: str) -> None: mutation()

if sys.version_info >= (3, 11):
    class ReprEnum(Enum): ...

if sys.version_info >= (3, 12):
    class IntEnum(int, ReprEnum):
        _value_: int
        @_magic_enum_attr
        def value(self) -> int: no_effects()
        def __new__(cls, value: int) -> Self: no_effects()

else:
    if sys.version_info >= (3, 11):
        _IntEnumBase = ReprEnum
    else:
        _IntEnumBase = Enum

    @disjoint_base
    class IntEnum(int, _IntEnumBase):
        _value_: int
        @_magic_enum_attr
        def value(self) -> int: no_effects()
        def __new__(cls, value: int) -> Self: no_effects()

def unique(enumeration: _EnumerationT) -> _EnumerationT: no_effects()

_auto_null: Any

class Flag(Enum):
    _name_: str | None  # type: ignore[assignment]
    _value_: int
    @_magic_enum_attr
    def name(self) -> str | None: no_effects()  # type: ignore[override]
    @_magic_enum_attr
    def value(self) -> int: no_effects()
    def __contains__(self, other: Self) -> bool: no_effects()
    def __bool__(self) -> bool: no_effects()
    def __or__(self, other: Self) -> Self: no_effects()
    def __and__(self, other: Self) -> Self: no_effects()
    def __xor__(self, other: Self) -> Self: no_effects()
    def __invert__(self) -> Self: no_effects()
    if sys.version_info >= (3, 11):
        def __iter__(self) -> Iterator[Self]: no_effects()
        def __len__(self) -> int: no_effects()
        __ror__ = __or__
        __rand__ = __and__
        __rxor__ = __xor__

if sys.version_info >= (3, 11):
    class StrEnum(str, ReprEnum):
        def __new__(cls, value: str) -> Self: no_effects()
        _value_: str
        @_magic_enum_attr
        def value(self) -> str: no_effects()
        @staticmethod
        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[str]
        ) -> str: no_effects()

    class EnumCheck(StrEnum):
        CONTINUOUS = "no skipped integer values"
        NAMED_FLAGS = "multi-flag aliases may not contain unnamed flags"
        UNIQUE = "one name per value"

    CONTINUOUS: Final = EnumCheck.CONTINUOUS
    NAMED_FLAGS: Final = EnumCheck.NAMED_FLAGS
    UNIQUE: Final = EnumCheck.UNIQUE

    class verify:
        def __init__(self, *checks: EnumCheck) -> None: no_effects()
        def __call__(self, enumeration: _EnumerationT) -> _EnumerationT: ...

    class FlagBoundary(StrEnum):
        STRICT = "strict"
        CONFORM = "conform"
        EJECT = "eject"
        KEEP = "keep"

    STRICT: Final = FlagBoundary.STRICT
    CONFORM: Final = FlagBoundary.CONFORM
    EJECT: Final = FlagBoundary.EJECT
    KEEP: Final = FlagBoundary.KEEP

    def global_str(self: Enum) -> str: no_effects()
    def global_enum(cls: _EnumerationT, update_str: bool = False) -> _EnumerationT: no_effects()
    def global_enum_repr(self: Enum) -> str: no_effects()
    def global_flag_repr(self: Flag) -> str: no_effects()

if sys.version_info >= (3, 12):
    # The body of the class is the same, but the base classes are different.
    class IntFlag(int, ReprEnum, Flag, boundary=KEEP):  # type: ignore[misc]  # complaints about incompatible bases
        def __new__(cls, value: int) -> Self: no_effects()
        def __or__(self, other: int) -> Self: no_effects()
        def __and__(self, other: int) -> Self: no_effects()
        def __xor__(self, other: int) -> Self: no_effects()
        def __invert__(self) -> Self: no_effects()
        __ror__ = __or__
        __rand__ = __and__
        __rxor__ = __xor__

elif sys.version_info >= (3, 11):
    # The body of the class is the same, but the base classes are different.
    @disjoint_base
    class IntFlag(int, ReprEnum, Flag, boundary=KEEP):  # type: ignore[misc]  # complaints about incompatible bases
        def __new__(cls, value: int) -> Self: no_effects()
        def __or__(self, other: int) -> Self: no_effects()
        def __and__(self, other: int) -> Self: no_effects()
        def __xor__(self, other: int) -> Self: no_effects()
        def __invert__(self) -> Self: no_effects()
        __ror__ = __or__
        __rand__ = __and__
        __rxor__ = __xor__

else:
    @disjoint_base
    class IntFlag(int, Flag):  # type: ignore[misc]  # complaints about incompatible bases
        def __new__(cls, value: int) -> Self: no_effects()
        def __or__(self, other: int) -> Self: no_effects()
        def __and__(self, other: int) -> Self: no_effects()
        def __xor__(self, other: int) -> Self: no_effects()
        def __invert__(self) -> Self: no_effects()
        __ror__ = __or__
        __rand__ = __and__
        __rxor__ = __xor__

class auto:
    _value_: Any
    @_magic_enum_attr
    def value(self) -> Any: no_effects()
    def __new__(cls) -> Self:
        no_effects()

    # These don't exist, but auto is basically immediately replaced with
    # either an int or a str depending on the type of the enum. StrEnum's auto
    # shouldn't have these, but they're needed for int versions of auto (mostly the __or__).
    # Ideally type checkers would special case auto enough to handle this,
    # but until then this is a slightly inaccurate helping hand.
    def __or__(self, other: int | Self) -> Self:
        """Return self|value."""
        no_effects()
    def __and__(self, other: int | Self) -> Self: no_effects()
    def __xor__(self, other: int | Self) -> Self: no_effects()
    __ror__ = __or__
    __rand__ = __and__
    __rxor__ = __xor__

if sys.version_info >= (3, 11):
    def pickle_by_global_name(self: Enum, proto: int) -> str: no_effects()
    def pickle_by_enum_name(
        self: _EnumMemberT, proto: int
    ) -> tuple[Callable[..., Any], tuple[type[_EnumMemberT], str]]: no_effects()
