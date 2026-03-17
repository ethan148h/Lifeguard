import _ast
import _sitebuiltins
import _typeshed
import sys
import types
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import (
    AnnotationForm,
    ConvertibleToFloat,
    ConvertibleToInt,
    FileDescriptorOrPath,
    OpenBinaryMode,
    OpenBinaryModeReading,
    OpenBinaryModeUpdating,
    OpenBinaryModeWriting,
    OpenTextMode,
    ReadableBuffer,
    SupportsAdd,
    SupportsAiter,
    SupportsAnext,
    SupportsDivMod,
    SupportsFlush,
    SupportsIter,
    SupportsKeysAndGetItem,
    SupportsLenAndGetItem,
    SupportsNext,
    SupportsRAdd,
    SupportsRDivMod,
    SupportsRichComparison,
    SupportsRichComparisonT,
    SupportsWrite,
)
from collections.abc import Awaitable, Callable, Iterable, Iterator, MutableSet, Reversible, Set as AbstractSet, Sized
from io import BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper
from os import PathLike
from types import CellType, CodeType, GenericAlias, TracebackType

# mypy crashes if any of {ByteString, Sequence, MutableSequence, Mapping, MutableMapping}
# are imported from collections.abc in builtins.pyi
from typing import (  # noqa: Y022,UP035
    IO,
    Any,
    BinaryIO,
    ClassVar,
    Generic,
    Mapping,
    MutableMapping,
    MutableSequence,
    Protocol,
    Sequence,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsIndex,
    TypeVar,
    final,
    overload,
    type_check_only,
)

# we can't import `Literal` from typing or mypy crashes: see #11247
from typing_extensions import (  # noqa: Y023
    Concatenate,
    Literal,
    LiteralString,
    ParamSpec,
    Self,
    TypeAlias,
    TypeGuard,
    TypeIs,
    TypeVarTuple,
    deprecated,
)

if sys.version_info >= (3, 14):
    from _typeshed import AnnotateFunc

_T = TypeVar("_T")
_I = TypeVar("_I", default=int)
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_R_co = TypeVar("_R_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_S = TypeVar("_S")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_SupportsNextT_co = TypeVar("_SupportsNextT_co", bound=SupportsNext[Any], covariant=True)
_SupportsAnextT_co = TypeVar("_SupportsAnextT_co", bound=SupportsAnext[Any], covariant=True)
_AwaitableT = TypeVar("_AwaitableT", bound=Awaitable[Any])
_AwaitableT_co = TypeVar("_AwaitableT_co", bound=Awaitable[Any], covariant=True)
_P = ParamSpec("_P")

# Type variables for slice
_StartT_co = TypeVar("_StartT_co", covariant=True, default=Any)  # slice -> slice[Any, Any, Any]
_StopT_co = TypeVar("_StopT_co", covariant=True, default=_StartT_co)  #  slice[A] -> slice[A, A, A]
# NOTE: step could differ from start and stop, (e.g. datetime/timedelta)l
#   the default (start|stop) is chosen to cater to the most common case of int/index slices.
# FIXME: https://github.com/python/typing/issues/213 (replace step=start|stop with step=start&stop)
_StepT_co = TypeVar("_StepT_co", covariant=True, default=_StartT_co | _StopT_co)  #  slice[A,B] -> slice[A, B, A|B]

class object:
    __doc__: str | None
    __dict__: dict[str, Any]
    __module__: str
    __annotations__: dict[str, Any]
    @property
    def __class__(self) -> type[Self]: no_effects()
    @__class__.setter
    def __class__(self, type: type[Self], /) -> None: no_effects()
    def __init__(self) -> None: no_effects()
    def __new__(cls) -> Self: no_effects()
    # N.B. `object.__setattr__` and `object.__delattr__` are heavily special-cased by type checkers.
    # Overriding them in subclasses has different semantics, even if the override has an identical signature.
    def __setattr__(self, name: str, value: Any, /) -> None: mutation()
    def __delattr__(self, name: str, /) -> None: mutation()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __str__(self) -> str: no_effects()  # noqa: Y029
    def __repr__(self) -> str: no_effects()  # noqa: Y029
    def __hash__(self) -> int: no_effects()
    def __format__(self, format_spec: str, /) -> str: no_effects()
    def __getattribute__(self, name: str, /) -> Any: no_effects()
    def __sizeof__(self) -> int: no_effects()
    # return type of pickle methods is rather hard to express in the current type system
    # see #6661 and https://docs.python.org/3/library/pickle.html#object.__reduce__
    def __reduce__(self) -> str | tuple[Any, ...]: no_effects()
    def __reduce_ex__(self, protocol: SupportsIndex, /) -> str | tuple[Any, ...]: no_effects()
    if sys.version_info >= (3, 11):
        def __getstate__(self) -> object: no_effects()

    def __dir__(self) -> Iterable[str]: no_effects()
    def __init_subclass__(cls) -> None: no_effects()
    @classmethod
    def __subclasshook__(cls, subclass: type, /) -> bool: no_effects()

class staticmethod(Generic[_P, _R_co]):
    @property
    def __func__(self) -> Callable[_P, _R_co]: no_effects()
    @property
    def __isabstractmethod__(self) -> bool: no_effects()
    def __init__(self, f: Callable[_P, _R_co], /) -> None: no_effects()
    @overload
    def __get__(self, instance: None, owner: type, /) -> Callable[_P, _R_co]: no_effects()
    @overload
    def __get__(self, instance: _T, owner: type[_T] | None = None, /) -> Callable[_P, _R_co]: ...
    if sys.version_info >= (3, 10):
        __name__: str
        __qualname__: str
        @property
        def __wrapped__(self) -> Callable[_P, _R_co]: no_effects()
        def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R_co: no_effects()
    if sys.version_info >= (3, 14):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()
        __annotate__: AnnotateFunc | None

class classmethod(Generic[_T, _P, _R_co]):
    @property
    def __func__(self) -> Callable[Concatenate[type[_T], _P], _R_co]: no_effects()
    @property
    def __isabstractmethod__(self) -> bool: no_effects()
    def __init__(self, f: Callable[Concatenate[type[_T], _P], _R_co], /) -> None: no_effects()
    @overload
    def __get__(self, instance: _T, owner: type[_T] | None = None, /) -> Callable[_P, _R_co]: no_effects()
    @overload
    def __get__(self, instance: None, owner: type[_T], /) -> Callable[_P, _R_co]: ...
    if sys.version_info >= (3, 10):
        __name__: str
        __qualname__: str
        @property
        def __wrapped__(self) -> Callable[Concatenate[type[_T], _P], _R_co]: no_effects()
    if sys.version_info >= (3, 14):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()
        __annotate__: AnnotateFunc | None

class type:
    # object.__base__ is None. Otherwise, it would be a type.
    @property
    def __base__(self) -> type | None: no_effects()
    __bases__: tuple[type, ...]
    @property
    def __basicsize__(self) -> int: no_effects()
    @property
    def __dict__(self) -> types.MappingProxyType[str, Any]: no_effects()  # type: ignore[override]
    @property
    def __dictoffset__(self) -> int: no_effects()
    @property
    def __flags__(self) -> int: no_effects()
    @property
    def __itemsize__(self) -> int: no_effects()
    __module__: str
    @property
    def __mro__(self) -> tuple[type, ...]: no_effects()
    __name__: str
    __qualname__: str
    @property
    def __text_signature__(self) -> str | None: no_effects()
    @property
    def __weakrefoffset__(self) -> int: no_effects()
    @overload
    def __init__(self, o: object, /) -> None: no_effects()
    @overload
    def __init__(self, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any) -> None: ...
    @overload
    def __new__(cls, o: object, /) -> type: no_effects()
    @overload
    def __new__(
        cls: type[_typeshed.Self], name: str, bases: tuple[type, ...], namespace: dict[str, Any], /, **kwds: Any
    ) -> _typeshed.Self: ...
    def __call__(self, *args: Any, **kwds: Any) -> Any: no_effects()
    def __subclasses__(self: _typeshed.Self) -> list[_typeshed.Self]: no_effects()
    # Note: the documentation doesn't specify what the return type is, the standard
    # implementation seems to be returning a list.
    def mro(self) -> list[type]: no_effects()
    def __instancecheck__(self, instance: Any, /) -> bool: no_effects()
    def __subclasscheck__(self, subclass: type, /) -> bool: no_effects()
    @classmethod
    def __prepare__(metacls, name: str, bases: tuple[type, ...], /, **kwds: Any) -> MutableMapping[str, object]: no_effects()
    if sys.version_info >= (3, 10):
        def __or__(self, value: Any, /) -> types.UnionType: no_effects()
        def __ror__(self, value: Any, /) -> types.UnionType: no_effects()
    if sys.version_info >= (3, 12):
        __type_params__: tuple[TypeVar | ParamSpec | TypeVarTuple, ...]
    __annotations__: dict[str, AnnotationForm]
    if sys.version_info >= (3, 14):
        __annotate__: AnnotateFunc | None

class super:
    @overload
    def __init__(self, t: Any, obj: Any, /) -> None: no_effects()
    @overload
    def __init__(self, t: Any, /) -> None: ...
    @overload
    def __init__(self) -> None: ...

_PositiveInteger: TypeAlias = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
_NegativeInteger: TypeAlias = Literal[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20]
_LiteralInteger = _PositiveInteger | _NegativeInteger | Literal[0]  # noqa: Y026  # TODO: Use TypeAlias once mypy bugs are fixed

class int:
    @overload
    def __new__(cls, x: ConvertibleToInt = ..., /) -> Self:
        dunder("__int__")
        dunder("__index__")
    @overload
    def __new__(cls, x: str | bytes | bytearray, /, base: SupportsIndex) -> Self: ...
    def as_integer_ratio(self) -> tuple[int, Literal[1]]: no_effects()
    @property
    def real(self) -> int: no_effects()
    @property
    def imag(self) -> Literal[0]: no_effects()
    @property
    def numerator(self) -> int: no_effects()
    @property
    def denominator(self) -> Literal[1]: no_effects()
    def conjugate(self) -> int: no_effects()
    def bit_length(self) -> int: no_effects()
    if sys.version_info >= (3, 10):
        def bit_count(self) -> int: no_effects()

    if sys.version_info >= (3, 11):
        def to_bytes(
            self, length: SupportsIndex = 1, byteorder: Literal["little", "big"] = "big", *, signed: bool = False
        ) -> bytes: no_effects()
        @classmethod
        def from_bytes(
            cls,
            bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
            byteorder: Literal["little", "big"] = "big",
            *,
            signed: bool = False,
        ) -> Self: no_effects()
    else:
        def to_bytes(self, length: SupportsIndex, byteorder: Literal["little", "big"], *, signed: bool = False) -> bytes: no_effects()
        @classmethod
        def from_bytes(
            cls,
            bytes: Iterable[SupportsIndex] | SupportsBytes | ReadableBuffer,
            byteorder: Literal["little", "big"],
            *,
            signed: bool = False,
        ) -> Self: no_effects()

    if sys.version_info >= (3, 12):
        def is_integer(self) -> Literal[True]: no_effects()

    def __add__(self, value: int, /) -> int: no_effects()
    def __sub__(self, value: int, /) -> int: no_effects()
    def __mul__(self, value: int, /) -> int: no_effects()
    def __floordiv__(self, value: int, /) -> int: no_effects()
    def __truediv__(self, value: int, /) -> float: no_effects()
    def __mod__(self, value: int, /) -> int: no_effects()
    def __divmod__(self, value: int, /) -> tuple[int, int]: no_effects()
    def __radd__(self, value: int, /) -> int: no_effects()
    def __rsub__(self, value: int, /) -> int: no_effects()
    def __rmul__(self, value: int, /) -> int: no_effects()
    def __rfloordiv__(self, value: int, /) -> int: no_effects()
    def __rtruediv__(self, value: int, /) -> float: no_effects()
    def __rmod__(self, value: int, /) -> int: no_effects()
    def __rdivmod__(self, value: int, /) -> tuple[int, int]: no_effects()
    @overload
    def __pow__(self, x: Literal[0], /) -> Literal[1]: no_effects()
    @overload
    def __pow__(self, value: Literal[0], mod: None, /) -> Literal[1]: ...
    @overload
    def __pow__(self, value: _PositiveInteger, mod: None = None, /) -> int: ...
    @overload
    def __pow__(self, value: _NegativeInteger, mod: None = None, /) -> float: ...
    # positive __value -> int; negative __value -> float
    # return type must be Any as `int | float` causes too many false-positive errors
    @overload
    def __pow__(self, value: int, mod: None = None, /) -> Any: ...
    @overload
    def __pow__(self, value: int, mod: int, /) -> int: ...
    def __rpow__(self, value: int, mod: int | None = None, /) -> Any: no_effects()
    def __and__(self, value: int, /) -> int: no_effects()
    def __or__(self, value: int, /) -> int: no_effects()
    def __xor__(self, value: int, /) -> int: no_effects()
    def __lshift__(self, value: int, /) -> int: no_effects()
    def __rshift__(self, value: int, /) -> int: no_effects()
    def __rand__(self, value: int, /) -> int: no_effects()
    def __ror__(self, value: int, /) -> int: no_effects()
    def __rxor__(self, value: int, /) -> int: no_effects()
    def __rlshift__(self, value: int, /) -> int: no_effects()
    def __rrshift__(self, value: int, /) -> int: no_effects()
    def __neg__(self) -> int: no_effects()
    def __pos__(self) -> int: no_effects()
    def __invert__(self) -> int: no_effects()
    def __trunc__(self) -> int: no_effects()
    def __ceil__(self) -> int: no_effects()
    def __floor__(self) -> int: no_effects()
    if sys.version_info >= (3, 14):
        def __round__(self, ndigits: SupportsIndex | None = None, /) -> int: no_effects()
    else:
        def __round__(self, ndigits: SupportsIndex = ..., /) -> int: no_effects()

    def __getnewargs__(self) -> tuple[int]: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __lt__(self, value: int, /) -> bool: no_effects()
    def __le__(self, value: int, /) -> bool: no_effects()
    def __gt__(self, value: int, /) -> bool: no_effects()
    def __ge__(self, value: int, /) -> bool: no_effects()
    def __float__(self) -> float: no_effects()
    def __int__(self) -> int: no_effects()
    def __abs__(self) -> int: no_effects()
    def __hash__(self) -> int: no_effects()
    def __bool__(self) -> bool: no_effects()
    def __index__(self) -> int: no_effects()

class float:
    def __new__(cls, x: ConvertibleToFloat = ..., /) -> Self: dunder("__float__")
    def as_integer_ratio(self) -> tuple[int, int]: no_effects()
    def hex(self) -> str: no_effects()
    def is_integer(self) -> bool: no_effects()
    @classmethod
    def fromhex(cls, string: str, /) -> Self: no_effects()
    @property
    def real(self) -> float: no_effects()
    @property
    def imag(self) -> float: no_effects()
    def conjugate(self) -> float: no_effects()
    def __add__(self, value: float, /) -> float: no_effects()
    def __sub__(self, value: float, /) -> float: no_effects()
    def __mul__(self, value: float, /) -> float: no_effects()
    def __floordiv__(self, value: float, /) -> float: no_effects()
    def __truediv__(self, value: float, /) -> float: no_effects()
    def __mod__(self, value: float, /) -> float: no_effects()
    def __divmod__(self, value: float, /) -> tuple[float, float]: no_effects()
    @overload
    def __pow__(self, value: int, mod: None = None, /) -> float: no_effects()
    # positive __value -> float; negative __value -> complex
    # return type must be Any as `float | complex` causes too many false-positive errors
    @overload
    def __pow__(self, value: float, mod: None = None, /) -> Any: ...
    def __radd__(self, value: float, /) -> float: no_effects()
    def __rsub__(self, value: float, /) -> float: no_effects()
    def __rmul__(self, value: float, /) -> float: no_effects()
    def __rfloordiv__(self, value: float, /) -> float: no_effects()
    def __rtruediv__(self, value: float, /) -> float: no_effects()
    def __rmod__(self, value: float, /) -> float: no_effects()
    def __rdivmod__(self, value: float, /) -> tuple[float, float]: no_effects()
    @overload
    def __rpow__(self, value: _PositiveInteger, mod: None = None, /) -> float: no_effects()
    @overload
    def __rpow__(self, value: _NegativeInteger, mod: None = None, /) -> complex: ...
    # Returning `complex` for the general case gives too many false-positive errors.
    @overload
    def __rpow__(self, value: float, mod: None = None, /) -> Any: ...
    def __getnewargs__(self) -> tuple[float]: no_effects()
    def __trunc__(self) -> int: no_effects()
    def __ceil__(self) -> int: no_effects()
    def __floor__(self) -> int: no_effects()
    @overload
    def __round__(self, ndigits: None = None, /) -> int: no_effects()
    @overload
    def __round__(self, ndigits: SupportsIndex, /) -> float: ...
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __lt__(self, value: float, /) -> bool: no_effects()
    def __le__(self, value: float, /) -> bool: no_effects()
    def __gt__(self, value: float, /) -> bool: no_effects()
    def __ge__(self, value: float, /) -> bool: no_effects()
    def __neg__(self) -> float: no_effects()
    def __pos__(self) -> float: no_effects()
    def __int__(self) -> int: no_effects()
    def __float__(self) -> float: no_effects()
    def __abs__(self) -> float: no_effects()
    def __hash__(self) -> int: no_effects()
    def __bool__(self) -> bool: no_effects()
    if sys.version_info >= (3, 14):
        @classmethod
        def from_number(cls, number: float | SupportsIndex | SupportsFloat, /) -> Self: no_effects()

class complex:
    # Python doesn't currently accept SupportsComplex for the second argument
    @overload
    def __new__(
        cls,
        real: complex | SupportsComplex | SupportsFloat | SupportsIndex = ...,
        imag: complex | SupportsFloat | SupportsIndex = ...,
    ) -> Self: 
        dunder("__complex__")
        dunder("__float__")
        dunder("__index__")
    @overload
    def __new__(cls, real: str | SupportsComplex | SupportsFloat | SupportsIndex | complex) -> Self: ...
    @property
    def real(self) -> float: no_effects()
    @property
    def imag(self) -> float: no_effects()
    def conjugate(self) -> complex: no_effects()
    def __add__(self, value: complex, /) -> complex: no_effects()
    def __sub__(self, value: complex, /) -> complex: no_effects()
    def __mul__(self, value: complex, /) -> complex: no_effects()
    def __pow__(self, value: complex, mod: None = None, /) -> complex: no_effects()
    def __truediv__(self, value: complex, /) -> complex: no_effects()
    def __radd__(self, value: complex, /) -> complex: no_effects()
    def __rsub__(self, value: complex, /) -> complex: no_effects()
    def __rmul__(self, value: complex, /) -> complex: no_effects()
    def __rpow__(self, value: complex, mod: None = None, /) -> complex: no_effects()
    def __rtruediv__(self, value: complex, /) -> complex: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __neg__(self) -> complex: no_effects()
    def __pos__(self) -> complex: no_effects()
    def __abs__(self) -> float: no_effects()
    def __hash__(self) -> int: no_effects()
    def __bool__(self) -> bool: no_effects()
    if sys.version_info >= (3, 11):
        def __complex__(self) -> complex: no_effects()
    if sys.version_info >= (3, 14):
        @classmethod
        def from_number(cls, number: complex | SupportsComplex | SupportsFloat | SupportsIndex, /) -> Self: no_effects()

class _FormatMapMapping(Protocol):
    def __getitem__(self, key: str, /) -> Any: no_effects()

class _TranslateTable(Protocol):
    def __getitem__(self, key: int, /) -> str | int | None: no_effects()

class str(Sequence[str]):
    @overload
    def __new__(cls, object: object = ...) -> Self:
        dunder("__str__")
        dunder("__repr__")
    @overload
    def __new__(cls, object: ReadableBuffer, encoding: str = ..., errors: str = ...) -> Self: ...
    @overload
    def capitalize(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def capitalize(self) -> str: ...  # type: ignore[misc]
    @overload
    def casefold(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def casefold(self) -> str: ...  # type: ignore[misc]
    @overload
    def center(self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /) -> LiteralString: no_effects()
    @overload
    def center(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    def count(self, sub: str, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /) -> int: no_effects()
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes: no_effects()
    def endswith(
        self, suffix: str | tuple[str, ...], start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> bool: no_effects()
    @overload
    def expandtabs(self: LiteralString, tabsize: SupportsIndex = 8) -> LiteralString: no_effects()
    @overload
    def expandtabs(self, tabsize: SupportsIndex = 8) -> str: ...  # type: ignore[misc]
    def find(self, sub: str, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /) -> int: no_effects()
    @overload
    def format(self: LiteralString, *args: LiteralString, **kwargs: LiteralString) -> LiteralString: no_effects()
    @overload
    def format(self, *args: object, **kwargs: object) -> str: ...
    def format_map(self, mapping: _FormatMapMapping, /) -> str: no_effects()
    def index(self, sub: str, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /) -> int: no_effects()
    def isalnum(self) -> bool: no_effects()
    def isalpha(self) -> bool: no_effects()
    def isascii(self) -> bool: no_effects()
    def isdecimal(self) -> bool: no_effects()
    def isdigit(self) -> bool: no_effects()
    def isidentifier(self) -> bool: no_effects()
    def islower(self) -> bool: no_effects()
    def isnumeric(self) -> bool: no_effects()
    def isprintable(self) -> bool: no_effects()
    def isspace(self) -> bool: no_effects()
    def istitle(self) -> bool: no_effects()
    def isupper(self) -> bool: no_effects()
    @overload
    def join(self: LiteralString, iterable: Iterable[LiteralString], /) -> LiteralString: no_effects()
    @overload
    def join(self, iterable: Iterable[str], /) -> str: ...  # type: ignore[misc]
    @overload
    def ljust(self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /) -> LiteralString: no_effects()
    @overload
    def ljust(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    @overload
    def lower(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def lower(self) -> str: ...  # type: ignore[misc]
    @overload
    def lstrip(self: LiteralString, chars: LiteralString | None = None, /) -> LiteralString: no_effects()
    @overload
    def lstrip(self, chars: str | None = None, /) -> str: ...  # type: ignore[misc]
    @overload
    def partition(self: LiteralString, sep: LiteralString, /) -> tuple[LiteralString, LiteralString, LiteralString]: no_effects()
    @overload
    def partition(self, sep: str, /) -> tuple[str, str, str]: ...  # type: ignore[misc]
    if sys.version_info >= (3, 13):
        @overload
        def replace(
            self: LiteralString, old: LiteralString, new: LiteralString, /, count: SupportsIndex = -1
        ) -> LiteralString: no_effects()
        @overload
        def replace(self, old: str, new: str, /, count: SupportsIndex = -1) -> str: ...  # type: ignore[misc]
    else:
        @overload
        def replace(
            self: LiteralString, old: LiteralString, new: LiteralString, count: SupportsIndex = -1, /
        ) -> LiteralString: no_effects()
        @overload
        def replace(self, old: str, new: str, count: SupportsIndex = -1, /) -> str: ...  # type: ignore[misc]

    @overload
    def removeprefix(self: LiteralString, prefix: LiteralString, /) -> LiteralString: no_effects()
    @overload
    def removeprefix(self, prefix: str, /) -> str: ...  # type: ignore[misc]
    @overload
    def removesuffix(self: LiteralString, suffix: LiteralString, /) -> LiteralString: no_effects()
    @overload
    def removesuffix(self, suffix: str, /) -> str: ...  # type: ignore[misc]
    def rfind(self, sub: str, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /) -> int: no_effects()
    def rindex(self, sub: str, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /) -> int: no_effects()
    @overload
    def rjust(self: LiteralString, width: SupportsIndex, fillchar: LiteralString = " ", /) -> LiteralString: no_effects()
    @overload
    def rjust(self, width: SupportsIndex, fillchar: str = " ", /) -> str: ...  # type: ignore[misc]
    @overload
    def rpartition(self: LiteralString, sep: LiteralString, /) -> tuple[LiteralString, LiteralString, LiteralString]: no_effects()
    @overload
    def rpartition(self, sep: str, /) -> tuple[str, str, str]: ...  # type: ignore[misc]
    @overload
    def rsplit(self: LiteralString, sep: LiteralString | None = None, maxsplit: SupportsIndex = -1) -> list[LiteralString]: no_effects()
    @overload
    def rsplit(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[str]: ...  # type: ignore[misc]
    @overload
    def rstrip(self: LiteralString, chars: LiteralString | None = None, /) -> LiteralString: no_effects()
    @overload
    def rstrip(self, chars: str | None = None, /) -> str: ...  # type: ignore[misc]
    @overload
    def split(self: LiteralString, sep: LiteralString | None = None, maxsplit: SupportsIndex = -1) -> list[LiteralString]: no_effects()
    @overload
    def split(self, sep: str | None = None, maxsplit: SupportsIndex = -1) -> list[str]: ...  # type: ignore[misc]
    @overload
    def splitlines(self: LiteralString, keepends: bool = False) -> list[LiteralString]: no_effects()
    @overload
    def splitlines(self, keepends: bool = False) -> list[str]: ...  # type: ignore[misc]
    def startswith(
        self, prefix: str | tuple[str, ...], start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> bool: no_effects()
    @overload
    def strip(self: LiteralString, chars: LiteralString | None = None, /) -> LiteralString: no_effects()
    @overload
    def strip(self, chars: str | None = None, /) -> str: ...  # type: ignore[misc]
    @overload
    def swapcase(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def swapcase(self) -> str: ...  # type: ignore[misc]
    @overload
    def title(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def title(self) -> str: ...  # type: ignore[misc]
    def translate(self, table: _TranslateTable, /) -> str: no_effects()
    @overload
    def upper(self: LiteralString) -> LiteralString: no_effects()
    @overload
    def upper(self) -> str: ...  # type: ignore[misc]
    @overload
    def zfill(self: LiteralString, width: SupportsIndex, /) -> LiteralString: no_effects()
    @overload
    def zfill(self, width: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    @staticmethod
    @overload
    def maketrans(x: dict[int, _T] | dict[str, _T] | dict[str | int, _T], /) -> dict[int, _T]: no_effects()
    @staticmethod
    @overload
    def maketrans(x: str, y: str, /) -> dict[int, int]: ...
    @staticmethod
    @overload
    def maketrans(x: str, y: str, z: str, /) -> dict[int, int | None]: ...
    @overload
    def __add__(self: LiteralString, value: LiteralString, /) -> LiteralString: no_effects()
    @overload
    def __add__(self, value: str, /) -> str: ...  # type: ignore[misc]
    # Incompatible with Sequence.__contains__
    def __contains__(self, key: str, /) -> bool: no_effects()  # type: ignore[override]
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ge__(self, value: str, /) -> bool: no_effects()
    @overload
    def __getitem__(self: LiteralString, key: SupportsIndex | slice, /) -> LiteralString: no_effects()
    @overload
    def __getitem__(self, key: SupportsIndex | slice, /) -> str: ...  # type: ignore[misc]
    def __gt__(self, value: str, /) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    @overload
    def __iter__(self: LiteralString) -> Iterator[LiteralString]: no_effects()
    @overload
    def __iter__(self) -> Iterator[str]: ...  # type: ignore[misc]
    def __le__(self, value: str, /) -> bool: no_effects()
    def __len__(self) -> int: no_effects()
    def __lt__(self, value: str, /) -> bool: no_effects()
    @overload
    def __mod__(self: LiteralString, value: LiteralString | tuple[LiteralString, ...], /) -> LiteralString: no_effects()
    @overload
    def __mod__(self, value: Any, /) -> str: ...
    @overload
    def __mul__(self: LiteralString, value: SupportsIndex, /) -> LiteralString: no_effects()
    @overload
    def __mul__(self, value: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    def __ne__(self, value: object, /) -> bool: no_effects()
    @overload
    def __rmul__(self: LiteralString, value: SupportsIndex, /) -> LiteralString: no_effects()
    @overload
    def __rmul__(self, value: SupportsIndex, /) -> str: ...  # type: ignore[misc]
    def __getnewargs__(self) -> tuple[str]: no_effects()

class bytes(Sequence[int]):
    @overload
    def __new__(cls, o: Iterable[SupportsIndex] | SupportsIndex | SupportsBytes | ReadableBuffer, /) -> Self: dunder("__bytes__")
    @overload
    def __new__(cls, string: str, /, encoding: str, errors: str = ...) -> Self: ...
    @overload
    def __new__(cls) -> Self: ...
    def capitalize(self) -> bytes: no_effects()
    def center(self, width: SupportsIndex, fillchar: bytes = b" ", /) -> bytes: no_effects()
    def count(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def decode(self, encoding: str = "utf-8", errors: str = "strict") -> str: no_effects()
    def endswith(
        self,
        suffix: ReadableBuffer | tuple[ReadableBuffer, ...],
        start: SupportsIndex | None = ...,
        end: SupportsIndex | None = ...,
        /,
    ) -> bool: no_effects()
    def expandtabs(self, tabsize: SupportsIndex = 8) -> bytes: no_effects()
    def find(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def hex(self, sep: str | bytes = ..., bytes_per_sep: SupportsIndex = ...) -> str: no_effects()
    def index(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def isalnum(self) -> bool: no_effects()
    def isalpha(self) -> bool: no_effects()
    def isascii(self) -> bool: no_effects()
    def isdigit(self) -> bool: no_effects()
    def islower(self) -> bool: no_effects()
    def isspace(self) -> bool: no_effects()
    def istitle(self) -> bool: no_effects()
    def isupper(self) -> bool: no_effects()
    def join(self, iterable_of_bytes: Iterable[ReadableBuffer], /) -> bytes: no_effects()
    def ljust(self, width: SupportsIndex, fillchar: bytes | bytearray = b" ", /) -> bytes: no_effects()
    def lower(self) -> bytes: no_effects()
    def lstrip(self, bytes: ReadableBuffer | None = None, /) -> bytes: no_effects()
    def partition(self, sep: ReadableBuffer, /) -> tuple[bytes, bytes, bytes]: no_effects()
    def replace(self, old: ReadableBuffer, new: ReadableBuffer, count: SupportsIndex = -1, /) -> bytes: no_effects()
    def removeprefix(self, prefix: ReadableBuffer, /) -> bytes: no_effects()
    def removesuffix(self, suffix: ReadableBuffer, /) -> bytes: no_effects()
    def rfind(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def rindex(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def rjust(self, width: SupportsIndex, fillchar: bytes | bytearray = b" ", /) -> bytes: no_effects()
    def rpartition(self, sep: ReadableBuffer, /) -> tuple[bytes, bytes, bytes]: no_effects()
    def rsplit(self, sep: ReadableBuffer | None = None, maxsplit: SupportsIndex = -1) -> list[bytes]: no_effects()
    def rstrip(self, bytes: ReadableBuffer | None = None, /) -> bytes: no_effects()
    def split(self, sep: ReadableBuffer | None = None, maxsplit: SupportsIndex = -1) -> list[bytes]: no_effects()
    def splitlines(self, keepends: bool = False) -> list[bytes]: no_effects()
    def startswith(
        self,
        prefix: ReadableBuffer | tuple[ReadableBuffer, ...],
        start: SupportsIndex | None = ...,
        end: SupportsIndex | None = ...,
        /,
    ) -> bool: no_effects()
    def strip(self, bytes: ReadableBuffer | None = None, /) -> bytes: no_effects()
    def swapcase(self) -> bytes: no_effects()
    def title(self) -> bytes: no_effects()
    def translate(self, table: ReadableBuffer | None, /, delete: ReadableBuffer = b"") -> bytes: no_effects()
    def upper(self) -> bytes: no_effects()
    def zfill(self, width: SupportsIndex, /) -> bytes: no_effects()
    @classmethod
    def fromhex(cls, string: str, /) -> Self: no_effects()
    @staticmethod
    def maketrans(frm: ReadableBuffer, to: ReadableBuffer, /) -> bytes: no_effects()
    def __len__(self) -> int: no_effects()
    def __iter__(self) -> Iterator[int]: no_effects()
    def __hash__(self) -> int: no_effects()
    @overload
    def __getitem__(self, key: SupportsIndex, /) -> int: no_effects()
    @overload
    def __getitem__(self, key: slice, /) -> bytes: ...
    def __add__(self, value: ReadableBuffer, /) -> bytes: no_effects()
    def __mul__(self, value: SupportsIndex, /) -> bytes: no_effects()
    def __rmul__(self, value: SupportsIndex, /) -> bytes: no_effects()
    def __mod__(self, value: Any, /) -> bytes: no_effects()
    # Incompatible with Sequence.__contains__
    def __contains__(self, key: SupportsIndex | ReadableBuffer, /) -> bool: no_effects()  # type: ignore[override]
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __lt__(self, value: bytes, /) -> bool: no_effects()
    def __le__(self, value: bytes, /) -> bool: no_effects()
    def __gt__(self, value: bytes, /) -> bool: no_effects()
    def __ge__(self, value: bytes, /) -> bool: no_effects()
    def __getnewargs__(self) -> tuple[bytes]: no_effects()
    if sys.version_info >= (3, 11):
        def __bytes__(self) -> bytes: no_effects()

    def __buffer__(self, flags: int, /) -> memoryview: no_effects()

class bytearray(MutableSequence[int]):
    @overload
    def __init__(self) -> None: dunder("__iter__")
    @overload
    def __init__(self, ints: Iterable[SupportsIndex] | SupportsIndex | ReadableBuffer, /) -> None: ...
    @overload
    def __init__(self, string: str, /, encoding: str, errors: str = ...) -> None: ...
    def append(self, item: SupportsIndex, /) -> None: no_effects()
    def capitalize(self) -> bytearray: no_effects()
    def center(self, width: SupportsIndex, fillchar: bytes = b" ", /) -> bytearray: no_effects()
    def count(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def copy(self) -> bytearray: no_effects()
    def decode(self, encoding: str = "utf-8", errors: str = "strict") -> str: no_effects()
    def endswith(
        self,
        suffix: ReadableBuffer | tuple[ReadableBuffer, ...],
        start: SupportsIndex | None = ...,
        end: SupportsIndex | None = ...,
        /,
    ) -> bool: no_effects()
    def expandtabs(self, tabsize: SupportsIndex = 8) -> bytearray: no_effects()
    def extend(self, iterable_of_ints: Iterable[SupportsIndex], /) -> None: mutation()
    def find(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def hex(self, sep: str | bytes = ..., bytes_per_sep: SupportsIndex = ...) -> str: no_effects()
    def index(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def insert(self, index: SupportsIndex, item: SupportsIndex, /) -> None: mutation()
    def isalnum(self) -> bool: no_effects()
    def isalpha(self) -> bool: no_effects()
    def isascii(self) -> bool: no_effects()
    def isdigit(self) -> bool: no_effects()
    def islower(self) -> bool: no_effects()
    def isspace(self) -> bool: no_effects()
    def istitle(self) -> bool: no_effects()
    def isupper(self) -> bool: no_effects()
    def join(self, iterable_of_bytes: Iterable[ReadableBuffer], /) -> bytearray: no_effects()
    def ljust(self, width: SupportsIndex, fillchar: bytes | bytearray = b" ", /) -> bytearray: no_effects()
    def lower(self) -> bytearray: no_effects()
    def lstrip(self, bytes: ReadableBuffer | None = None, /) -> bytearray: no_effects()
    def partition(self, sep: ReadableBuffer, /) -> tuple[bytearray, bytearray, bytearray]: no_effects()
    def pop(self, index: int = -1, /) -> int: mutation()
    def remove(self, value: int, /) -> None: mutation()
    def removeprefix(self, prefix: ReadableBuffer, /) -> bytearray: no_effects()
    def removesuffix(self, suffix: ReadableBuffer, /) -> bytearray: no_effects()
    def replace(self, old: ReadableBuffer, new: ReadableBuffer, count: SupportsIndex = -1, /) -> bytearray: no_effects()
    def rfind(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def rindex(
        self, sub: ReadableBuffer | SupportsIndex, start: SupportsIndex | None = ..., end: SupportsIndex | None = ..., /
    ) -> int: no_effects()
    def rjust(self, width: SupportsIndex, fillchar: bytes | bytearray = b" ", /) -> bytearray: no_effects()
    def rpartition(self, sep: ReadableBuffer, /) -> tuple[bytearray, bytearray, bytearray]: no_effects()
    def rsplit(self, sep: ReadableBuffer | None = None, maxsplit: SupportsIndex = -1) -> list[bytearray]: no_effects()
    def rstrip(self, bytes: ReadableBuffer | None = None, /) -> bytearray: no_effects()
    def split(self, sep: ReadableBuffer | None = None, maxsplit: SupportsIndex = -1) -> list[bytearray]: no_effects()
    def splitlines(self, keepends: bool = False) -> list[bytearray]: no_effects()
    def startswith(
        self,
        prefix: ReadableBuffer | tuple[ReadableBuffer, ...],
        start: SupportsIndex | None = ...,
        end: SupportsIndex | None = ...,
        /,
    ) -> bool: no_effects()
    def strip(self, bytes: ReadableBuffer | None = None, /) -> bytearray: no_effects()
    def swapcase(self) -> bytearray: no_effects()
    def title(self) -> bytearray: no_effects()
    def translate(self, table: ReadableBuffer | None, /, delete: bytes = b"") -> bytearray: no_effects()
    def upper(self) -> bytearray: no_effects()
    def zfill(self, width: SupportsIndex, /) -> bytearray: no_effects()
    @classmethod
    def fromhex(cls, string: str, /) -> Self: no_effects()
    @staticmethod
    def maketrans(frm: ReadableBuffer, to: ReadableBuffer, /) -> bytes: no_effects()
    def __len__(self) -> int: no_effects()
    def __iter__(self) -> Iterator[int]: no_effects()
    __hash__: ClassVar[None]  # type: ignore[assignment]
    @overload
    def __getitem__(self, key: SupportsIndex, /) -> int: no_effects()
    @overload
    def __getitem__(self, key: slice, /) -> bytearray: ...
    @overload
    def __setitem__(self, key: SupportsIndex, value: SupportsIndex, /) -> None: no_effects()
    @overload
    def __setitem__(self, key: slice, value: Iterable[SupportsIndex] | bytes, /) -> None: ...
    def __delitem__(self, key: SupportsIndex | slice, /) -> None: no_effects()
    def __add__(self, value: ReadableBuffer, /) -> bytearray: no_effects()
    # The superclass wants us to accept Iterable[int], but that fails at runtime.
    def __iadd__(self, value: ReadableBuffer, /) -> Self: no_effects()  # type: ignore[override]
    def __mul__(self, value: SupportsIndex, /) -> bytearray: no_effects()
    def __rmul__(self, value: SupportsIndex, /) -> bytearray: no_effects()
    def __imul__(self, value: SupportsIndex, /) -> Self: no_effects()
    def __mod__(self, value: Any, /) -> bytes: no_effects()
    # Incompatible with Sequence.__contains__
    def __contains__(self, key: SupportsIndex | ReadableBuffer, /) -> bool: no_effects()  # type: ignore[override]
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __ne__(self, value: object, /) -> bool: no_effects()
    def __lt__(self, value: ReadableBuffer, /) -> bool: no_effects()
    def __le__(self, value: ReadableBuffer, /) -> bool: no_effects()
    def __gt__(self, value: ReadableBuffer, /) -> bool: no_effects()
    def __ge__(self, value: ReadableBuffer, /) -> bool: no_effects()
    def __alloc__(self) -> int: no_effects()
    def __buffer__(self, flags: int, /) -> memoryview: no_effects()
    def __release_buffer__(self, buffer: memoryview, /) -> None: no_effects()
    if sys.version_info >= (3, 14):
        def resize(self, size: int, /) -> None: no_effects()

_IntegerFormats: TypeAlias = Literal[
    "b", "B", "@b", "@B", "h", "H", "@h", "@H", "i", "I", "@i", "@I", "l", "L", "@l", "@L", "q", "Q", "@q", "@Q", "P", "@P"
]

@final
class memoryview(Sequence[_I]):
    @property
    def format(self) -> str: no_effects()
    @property
    def itemsize(self) -> int: no_effects()
    @property
    def shape(self) -> tuple[int, ...] | None: no_effects()
    @property
    def strides(self) -> tuple[int, ...] | None: no_effects()
    @property
    def suboffsets(self) -> tuple[int, ...] | None: no_effects()
    @property
    def readonly(self) -> bool: no_effects()
    @property
    def ndim(self) -> int: no_effects()
    @property
    def obj(self) -> ReadableBuffer: no_effects()
    @property
    def c_contiguous(self) -> bool: no_effects()
    @property
    def f_contiguous(self) -> bool: no_effects()
    @property
    def contiguous(self) -> bool: no_effects()
    @property
    def nbytes(self) -> int: no_effects()
    def __new__(cls, obj: ReadableBuffer) -> Self: dunder("__buffer__")
    def __enter__(self) -> Self: no_effects()
    def __exit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: PYI036 # This is the module declaring BaseException
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
        /,
    ) -> None: no_effects()
    @overload
    def cast(self, format: Literal["c", "@c"], shape: list[int] | tuple[int, ...] = ...) -> memoryview[bytes]: no_effects()
    @overload
    def cast(self, format: Literal["f", "@f", "d", "@d"], shape: list[int] | tuple[int, ...] = ...) -> memoryview[float]: ...
    @overload
    def cast(self, format: Literal["?"], shape: list[int] | tuple[int, ...] = ...) -> memoryview[bool]: ...
    @overload
    def cast(self, format: _IntegerFormats, shape: list[int] | tuple[int, ...] = ...) -> memoryview: ...
    @overload
    def __getitem__(self, key: SupportsIndex | tuple[SupportsIndex, ...], /) -> _I: no_effects()
    @overload
    def __getitem__(self, key: slice, /) -> memoryview[_I]: ...
    def __contains__(self, x: object, /) -> bool: no_effects()
    def __iter__(self) -> Iterator[_I]: no_effects()
    def __len__(self) -> int: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    @overload
    def __setitem__(self, key: slice, value: ReadableBuffer, /) -> None: no_effects()
    @overload
    def __setitem__(self, key: SupportsIndex | tuple[SupportsIndex, ...], value: _I, /) -> None: ...
    if sys.version_info >= (3, 10):
        def tobytes(self, order: Literal["C", "F", "A"] | None = "C") -> bytes: no_effects()
    else:
        def tobytes(self, order: Literal["C", "F", "A"] | None = None) -> bytes: no_effects()

    def tolist(self) -> list[int]: no_effects()
    def toreadonly(self) -> memoryview: no_effects()
    def release(self) -> None: no_effects()
    def hex(self, sep: str | bytes = ..., bytes_per_sep: SupportsIndex = ...) -> str: no_effects()
    def __buffer__(self, flags: int, /) -> memoryview: no_effects()
    def __release_buffer__(self, buffer: memoryview, /) -> None: no_effects()

    # These are inherited from the Sequence ABC, but don't actually exist on memoryview.
    # See https://github.com/python/cpython/issues/125420
    index: ClassVar[None]  # type: ignore[assignment]
    count: ClassVar[None]  # type: ignore[assignment]
    if sys.version_info >= (3, 14):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

@final
class bool(int):
    def __new__(cls, o: object = ..., /) -> Self: dunder("__bool__")
    # The following overloads could be represented more elegantly with a TypeVar("_B", bool, int),
    # however mypy has a bug regarding TypeVar constraints (https://github.com/python/mypy/issues/11880).
    @overload
    def __and__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __and__(self, value: int, /) -> int: ...
    @overload
    def __or__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __or__(self, value: int, /) -> int: ...
    @overload
    def __xor__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __xor__(self, value: int, /) -> int: ...
    @overload
    def __rand__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __rand__(self, value: int, /) -> int: ...
    @overload
    def __ror__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __ror__(self, value: int, /) -> int: ...
    @overload
    def __rxor__(self, value: bool, /) -> bool: no_effects()
    @overload
    def __rxor__(self, value: int, /) -> int: ...
    def __getnewargs__(self) -> tuple[int]: no_effects()
    @deprecated("Will throw an error in Python 3.16. Use `not` for logical negation of bools instead.")
    def __invert__(self) -> int: no_effects()

@final
class slice(Generic[_StartT_co, _StopT_co, _StepT_co]):
    @property
    def start(self) -> _StartT_co: no_effects()
    @property
    def step(self) -> _StepT_co: no_effects()
    @property
    def stop(self) -> _StopT_co: no_effects()
    # Note: __new__ overloads map `None` to `Any`, since users expect slice(x, None)
    #  to be compatible with slice(None, x).
    # generic slice --------------------------------------------------------------------
    @overload
    def __new__(cls, start: None, stop: None = None, step: None = None, /) -> slice[Any, Any, Any]: no_effects()
    # unary overloads ------------------------------------------------------------------
    @overload
    def __new__(cls, stop: _T2, /) -> slice[Any, _T2, Any]: ...
    # binary overloads -----------------------------------------------------------------
    @overload
    def __new__(cls, start: _T1, stop: None, step: None = None, /) -> slice[_T1, Any, Any]: ...
    @overload
    def __new__(cls, start: None, stop: _T2, step: None = None, /) -> slice[Any, _T2, Any]: ...
    @overload
    def __new__(cls, start: _T1, stop: _T2, step: None = None, /) -> slice[_T1, _T2, Any]: ...
    # ternary overloads ----------------------------------------------------------------
    @overload
    def __new__(cls, start: None, stop: None, step: _T3, /) -> slice[Any, Any, _T3]: ...
    @overload
    def __new__(cls, start: _T1, stop: None, step: _T3, /) -> slice[_T1, Any, _T3]: ...
    @overload
    def __new__(cls, start: None, stop: _T2, step: _T3, /) -> slice[Any, _T2, _T3]: ...
    @overload
    def __new__(cls, start: _T1, stop: _T2, step: _T3, /) -> slice[_T1, _T2, _T3]: ...
    def __eq__(self, value: object, /) -> bool: no_effects()
    if sys.version_info >= (3, 12):
        def __hash__(self) -> int: no_effects()
    else:
        __hash__: ClassVar[None]  # type: ignore[assignment]

    def indices(self, len: SupportsIndex, /) -> tuple[int, int, int]: no_effects()

class tuple(Sequence[_T_co]):
    def __new__(cls, iterable: Iterable[_T_co] = ..., /) -> Self: dunder("__iter__")
    def __len__(self) -> int: no_effects()
    def __contains__(self, key: object, /) -> bool: no_effects()
    @overload
    def __getitem__(self, key: SupportsIndex, /) -> _T_co: no_effects()
    @overload
    def __getitem__(self, key: slice, /) -> tuple[_T_co, ...]: ...
    def __iter__(self) -> Iterator[_T_co]: no_effects()
    def __lt__(self, value: tuple[_T_co, ...], /) -> bool: no_effects()
    def __le__(self, value: tuple[_T_co, ...], /) -> bool: no_effects()
    def __gt__(self, value: tuple[_T_co, ...], /) -> bool: no_effects()
    def __ge__(self, value: tuple[_T_co, ...], /) -> bool: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    @overload
    def __add__(self, value: tuple[_T_co, ...], /) -> tuple[_T_co, ...]: no_effects()
    @overload
    def __add__(self, value: tuple[_T, ...], /) -> tuple[_T_co | _T, ...]: ...
    def __mul__(self, value: SupportsIndex, /) -> tuple[_T_co, ...]: no_effects()
    def __rmul__(self, value: SupportsIndex, /) -> tuple[_T_co, ...]: no_effects()
    def count(self, value: Any, /) -> int: no_effects()
    def index(self, value: Any, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize, /) -> int: no_effects()
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

# Doesn't exist at runtime, but deleting this breaks mypy and pyright. See:
# https://github.com/python/typeshed/issues/7580
# https://github.com/python/mypy/issues/8240
# Obsolete, use types.FunctionType instead.
@final
@type_check_only
class function:
    # Make sure this class definition stays roughly in line with `types.FunctionType`
    @property
    def __closure__(self) -> tuple[CellType, ...] | None: no_effects()
    __code__: CodeType
    __defaults__: tuple[Any, ...] | None
    __dict__: dict[str, Any]
    @property
    def __globals__(self) -> dict[str, Any]: no_effects()
    __name__: str
    __qualname__: str
    __annotations__: dict[str, AnnotationForm]
    if sys.version_info >= (3, 14):
        __annotate__: AnnotateFunc | None
    __kwdefaults__: dict[str, Any] | None
    if sys.version_info >= (3, 10):
        @property
        def __builtins__(self) -> dict[str, Any]: no_effects()
    if sys.version_info >= (3, 12):
        __type_params__: tuple[TypeVar | ParamSpec | TypeVarTuple, ...]

    __module__: str
    if sys.version_info >= (3, 13):
        def __new__(
            cls,
            code: CodeType,
            globals: dict[str, Any],
            name: str | None = None,
            argdefs: tuple[object, ...] | None = None,
            closure: tuple[CellType, ...] | None = None,
            kwdefaults: dict[str, object] | None = None,
        ) -> Self: no_effects()
    else:
        def __new__(
            cls,
            code: CodeType,
            globals: dict[str, Any],
            name: str | None = None,
            argdefs: tuple[object, ...] | None = None,
            closure: tuple[CellType, ...] | None = None,
        ) -> Self: no_effects()

    # mypy uses `builtins.function.__get__` to represent methods, properties, and getset_descriptors so we type the return as Any.
    def __get__(self, instance: object, owner: type | None = None, /) -> Any: no_effects()

class list(MutableSequence[_T]):
    @overload
    def __init__(self) -> None: dunder("__iter__")
    @overload
    def __init__(self, iterable: Iterable[_T], /) -> None: ...
    def copy(self) -> list[_T]: no_effects()
    def append(self, object: _T, /) -> None: mutation()
    def extend(self, iterable: Iterable[_T], /) -> None: mutation()
    def pop(self, index: SupportsIndex = -1, /) -> _T: mutation()
    # Signature of `list.index` should be kept in line with `collections.UserList.index()`
    # and multiprocessing.managers.ListProxy.index()
    def index(self, value: _T, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize, /) -> int: no_effects()
    def count(self, value: _T, /) -> int: no_effects()
    def insert(self, index: SupportsIndex, object: _T, /) -> None: mutation()
    def remove(self, value: _T, /) -> None: mutation()
    # Signature of `list.sort` should be kept inline with `collections.UserList.sort()`
    # and multiprocessing.managers.ListProxy.sort()
    #
    # Use list[SupportsRichComparisonT] for the first overload rather than [SupportsRichComparison]
    # to work around invariance
    @overload
    def sort(self: list[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: mutation()
    @overload
    def sort(self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False) -> None: ...
    def __len__(self) -> int: no_effects()
    def __iter__(self) -> Iterator[_T]: no_effects()
    __hash__: ClassVar[None]  # type: ignore[assignment]
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> _T: no_effects()
    @overload
    def __getitem__(self, s: slice, /) -> list[_T]: ...
    @overload
    def __setitem__(self, key: SupportsIndex, value: _T, /) -> None: mutation()
    @overload
    def __setitem__(self, key: slice, value: Iterable[_T], /) -> None: ...
    def __delitem__(self, key: SupportsIndex | slice, /) -> None: mutation()
    # Overloading looks unnecessary, but is needed to work around complex mypy problems
    @overload
    def __add__(self, value: list[_T], /) -> list[_T]: no_effects()
    @overload
    def __add__(self, value: list[_S], /) -> list[_S | _T]: ...
    def __iadd__(self, value: Iterable[_T], /) -> Self: no_effects()  # type: ignore[misc]
    def __mul__(self, value: SupportsIndex, /) -> list[_T]: no_effects()
    def __rmul__(self, value: SupportsIndex, /) -> list[_T]: no_effects()
    def __imul__(self, value: SupportsIndex, /) -> Self: no_effects()
    def __contains__(self, key: object, /) -> bool: no_effects()
    def __reversed__(self) -> Iterator[_T]: no_effects()
    def __gt__(self, value: list[_T], /) -> bool: no_effects()
    def __ge__(self, value: list[_T], /) -> bool: no_effects()
    def __lt__(self, value: list[_T], /) -> bool: no_effects()
    def __le__(self, value: list[_T], /) -> bool: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

class dict(MutableMapping[_KT, _VT]):
    # __init__ should be kept roughly in line with `collections.UserDict.__init__`, which has similar semantics
    # Also multiprocessing.managers.SyncManager.dict()
    @overload
    def __init__(self) -> None:
        dunder("__iter__")
        dunder("__getitem__")
    @overload
    def __init__(self: dict[str, _VT], **kwargs: _VT) -> None: ...  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    @overload
    def __init__(self, map: SupportsKeysAndGetItem[_KT, _VT], /) -> None: ...
    @overload
    def __init__(
        self: dict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        map: SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[tuple[_KT, _VT]], /) -> None: ...
    @overload
    def __init__(
        self: dict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        iterable: Iterable[tuple[str, _VT]],
        /,
        **kwargs: _VT,
    ) -> None: ...
    # Next two overloads are for dict(string.split(sep) for string in iterable)
    # Cannot be Iterable[Sequence[_T]] or otherwise dict(["foo", "bar", "baz"]) is not an error
    @overload
    def __init__(self: dict[str, str], iterable: Iterable[list[str]], /) -> None: ...
    @overload
    def __init__(self: dict[bytes, bytes], iterable: Iterable[list[bytes]], /) -> None: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: dunder("__iter__")
    def copy(self) -> dict[_KT, _VT]: no_effects()
    def keys(self) -> dict_keys[_KT, _VT]: no_effects()
    def values(self) -> dict_values[_KT, _VT]: no_effects()
    def items(self) -> dict_items[_KT, _VT]: no_effects()
    # Signature of `dict.fromkeys` should be kept identical to
    # `fromkeys` methods of `OrderedDict`/`ChainMap`/`UserDict` in `collections`
    # TODO: the true signature of `dict.fromkeys` is not expressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: None = None, /) -> dict[_T, Any | None]: no_effects()
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> dict[_T, _S]: ...
    # Positional-only in dict, but not in MutableMapping
    @overload  # type: ignore[override]
    def get(self, key: _KT, default: None = None, /) -> _VT | None: no_effects()
    @overload
    def get(self, key: _KT, default: _VT, /) -> _VT: ...
    @overload
    def get(self, key: _KT, default: _T, /) -> _VT | _T: ...
    @overload
    def pop(self, key: _KT, /) -> _VT: mutation()
    @overload
    def pop(self, key: _KT, default: _VT, /) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T, /) -> _VT | _T: ...
    def __len__(self) -> int: no_effects()
    def __getitem__(self, key: _KT, /) -> _VT: no_effects()
    def __setitem__(self, key: _KT, value: _VT, /) -> None: mutation()
    def __delitem__(self, key: _KT, /) -> None: mutation()
    def __iter__(self) -> Iterator[_KT]: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __reversed__(self) -> Iterator[_KT]: no_effects()
    __hash__: ClassVar[None]  # type: ignore[assignment]
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()
    @overload
    def __or__(self, value: dict[_KT, _VT], /) -> dict[_KT, _VT]: no_effects()
    @overload
    def __or__(self, value: dict[_T1, _T2], /) -> dict[_KT | _T1, _VT | _T2]: ...
    @overload
    def __ror__(self, value: dict[_KT, _VT], /) -> dict[_KT, _VT]: no_effects()
    @overload
    def __ror__(self, value: dict[_T1, _T2], /) -> dict[_KT | _T1, _VT | _T2]: ...
    # dict.__ior__ should be kept roughly in line with MutableMapping.update()
    @overload  # type: ignore[misc]
    def __ior__(self, value: SupportsKeysAndGetItem[_KT, _VT], /) -> Self: no_effects()
    @overload
    def __ior__(self, value: Iterable[tuple[_KT, _VT]], /) -> Self: ...
    def update(self, other: dict[_KT, _VT], /) -> None: mutation()

class set(MutableSet[_T]):
    @overload
    def __init__(self) -> None: dunder("__iter__")
    @overload
    def __init__(self, iterable: Iterable[_T], /) -> None: ...
    def add(self, element: _T, /) -> None: mutation()
    def copy(self) -> set[_T]: no_effects()
    def difference(self, *s: Iterable[Any]) -> set[_T]: no_effects()
    def difference_update(self, *s: Iterable[Any]) -> None: no_effects()
    def discard(self, element: _T, /) -> None: no_effects()
    def intersection(self, *s: Iterable[Any]) -> set[_T]: no_effects()
    def intersection_update(self, *s: Iterable[Any]) -> None: no_effects()
    def isdisjoint(self, s: Iterable[Any], /) -> bool: no_effects()
    def issubset(self, s: Iterable[Any], /) -> bool: no_effects()
    def issuperset(self, s: Iterable[Any], /) -> bool: no_effects()
    def remove(self, element: _T, /) -> None: mutation()
    def symmetric_difference(self, s: Iterable[_T], /) -> set[_T]: no_effects()
    def symmetric_difference_update(self, s: Iterable[_T], /) -> None: no_effects()
    def union(self, *s: Iterable[_S]) -> set[_T | _S]: no_effects()
    def update(self, *s: Iterable[_T]) -> None: mutation()
    def __len__(self) -> int: no_effects()
    def __contains__(self, o: object, /) -> bool: no_effects()
    def __iter__(self) -> Iterator[_T]: no_effects()
    def __and__(self, value: AbstractSet[object], /) -> set[_T]: no_effects()
    def __iand__(self, value: AbstractSet[object], /) -> Self: no_effects()
    def __or__(self, value: AbstractSet[_S], /) -> set[_T | _S]: no_effects()
    def __ior__(self, value: AbstractSet[_T], /) -> Self: no_effects()  # type: ignore[override,misc]
    def __sub__(self, value: AbstractSet[_T | None], /) -> set[_T]: no_effects()
    def __isub__(self, value: AbstractSet[object], /) -> Self: no_effects()
    def __xor__(self, value: AbstractSet[_S], /) -> set[_T | _S]: no_effects()
    def __ixor__(self, value: AbstractSet[_T], /) -> Self: no_effects()  # type: ignore[override,misc]
    def __le__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __lt__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __ge__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __gt__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    __hash__: ClassVar[None]  # type: ignore[assignment]
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

class frozenset(AbstractSet[_T_co]):
    @overload
    def __new__(cls) -> Self: no_effects()
    @overload
    def __new__(cls, iterable: Iterable[_T_co], /) -> Self: ...
    def copy(self) -> frozenset[_T_co]: no_effects()
    def difference(self, *s: Iterable[object]) -> frozenset[_T_co]: no_effects()
    def intersection(self, *s: Iterable[object]) -> frozenset[_T_co]: no_effects()
    def isdisjoint(self, s: Iterable[_T_co], /) -> bool: no_effects()
    def issubset(self, s: Iterable[object], /) -> bool: no_effects()
    def issuperset(self, s: Iterable[object], /) -> bool: no_effects()
    def symmetric_difference(self, s: Iterable[_T_co], /) -> frozenset[_T_co]: no_effects()
    def union(self, *s: Iterable[_S]) -> frozenset[_T_co | _S]: no_effects()
    def __len__(self) -> int: no_effects()
    def __contains__(self, o: object, /) -> bool: no_effects()
    def __iter__(self) -> Iterator[_T_co]: no_effects()
    def __and__(self, value: AbstractSet[_T_co], /) -> frozenset[_T_co]: no_effects()
    def __or__(self, value: AbstractSet[_S], /) -> frozenset[_T_co | _S]: no_effects()
    def __sub__(self, value: AbstractSet[_T_co], /) -> frozenset[_T_co]: no_effects()
    def __xor__(self, value: AbstractSet[_S], /) -> frozenset[_T_co | _S]: no_effects()
    def __le__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __lt__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __ge__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __gt__(self, value: AbstractSet[object], /) -> bool: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

class enumerate(Generic[_T]):
    def __new__(cls, iterable: Iterable[_T], start: int = 0) -> Self: no_effects()
    def __iter__(self) -> Self: no_effects()
    def __next__(self) -> tuple[int, _T]: no_effects()
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

@final
class range(Sequence[int]):
    @property
    def start(self) -> int: no_effects()
    @property
    def stop(self) -> int: no_effects()
    @property
    def step(self) -> int: no_effects()
    @overload
    def __new__(cls, stop: SupportsIndex, /) -> Self: dunder("__index__")
    @overload
    def __new__(cls, start: SupportsIndex, stop: SupportsIndex, step: SupportsIndex = ..., /) -> Self: ...
    def count(self, value: int, /) -> int: no_effects()
    def index(self, value: int, /) -> int: no_effects()  # type: ignore[override]
    def __len__(self) -> int: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    def __contains__(self, key: object, /) -> bool: no_effects()
    def __iter__(self) -> Iterator[int]: no_effects()
    @overload
    def __getitem__(self, key: SupportsIndex, /) -> int: no_effects()
    @overload
    def __getitem__(self, key: slice, /) -> range: ...
    def __reversed__(self) -> Iterator[int]: no_effects()

class property:
    fget: Callable[[Any], Any] | None
    fset: Callable[[Any, Any], None] | None
    fdel: Callable[[Any], None] | None
    __isabstractmethod__: bool
    if sys.version_info >= (3, 13):
        __name__: str

    def __init__(
        self,
        fget: Callable[[Any], Any] | None = ...,
        fset: Callable[[Any, Any], None] | None = ...,
        fdel: Callable[[Any], None] | None = ...,
        doc: str | None = ...,
    ) -> None: no_effects()
    def getter(self, fget: Callable[[Any], Any], /) -> property: no_effects()
    def setter(self, fset: Callable[[Any, Any], None], /) -> property: no_effects()
    def deleter(self, fdel: Callable[[Any], None], /) -> property: no_effects()
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: no_effects()
    @overload
    def __get__(self, instance: Any, owner: type | None = None, /) -> Any: ...
    def __set__(self, instance: Any, value: Any, /) -> None: no_effects()
    def __delete__(self, instance: Any, /) -> None: no_effects()

@final
class _NotImplementedType(Any):
    __call__: None

NotImplemented: _NotImplementedType

def abs(x: SupportsAbs[_T], /) -> _T: dunder("__abs__")
def all(iterable: Iterable[object], /) -> bool: no_effects()
def any(iterable: Iterable[object], /) -> bool: no_effects()
def ascii(obj: object, /) -> str: no_effects()
def bin(number: int | SupportsIndex, /) -> str: dunder("__index__")
def breakpoint(*args: Any, **kws: Any) -> None: unsafe()
def callable(obj: object, /) -> TypeIs[Callable[..., object]]: no_effects()
def chr(i: int | SupportsIndex, /) -> str: no_effects()

if sys.version_info >= (3, 10):
    def aiter(async_iterable: SupportsAiter[_SupportsAnextT_co], /) -> _SupportsAnextT_co: no_effects()

    class _SupportsSynchronousAnext(Protocol[_AwaitableT_co]):
        def __anext__(self) -> _AwaitableT_co: no_effects()

    @overload
    # `anext` is not, in fact, an async function. When default is not provided
    # `anext` is just a passthrough for `obj.__anext__`
    # See discussion in #7491 and pure-Python implementation of `anext` at https://github.com/python/cpython/blob/ea786a882b9ed4261eafabad6011bc7ef3b5bf94/Lib/test/test_asyncgen.py#L52-L80
    def anext(i: _SupportsSynchronousAnext[_AwaitableT], /) -> _AwaitableT: no_effects()
    @overload
    async def anext(i: SupportsAnext[_T], default: _VT, /) -> _T | _VT: no_effects()

# compile() returns a CodeType, unless the flags argument includes PyCF_ONLY_AST (=1024),
# in which case it returns ast.AST. We have overloads for flag 0 (the default) and for
# explicitly passing PyCF_ONLY_AST. We fall back to Any for other values of flags.
@overload
def compile(
    source: str | ReadableBuffer | _ast.Module | _ast.Expression | _ast.Interactive,
    filename: str | ReadableBuffer | PathLike[Any],
    mode: str,
    flags: Literal[0],
    dont_inherit: bool = False,
    optimize: int = -1,
    *,
    _feature_version: int = -1,
) -> CodeType: no_effects()
@overload
def compile(
    source: str | ReadableBuffer | _ast.Module | _ast.Expression | _ast.Interactive,
    filename: str | ReadableBuffer | PathLike[Any],
    mode: str,
    *,
    dont_inherit: bool = False,
    optimize: int = -1,
    _feature_version: int = -1,
) -> CodeType: ...
@overload
def compile(
    source: str | ReadableBuffer | _ast.Module | _ast.Expression | _ast.Interactive,
    filename: str | ReadableBuffer | PathLike[Any],
    mode: str,
    flags: Literal[1024],
    dont_inherit: bool = False,
    optimize: int = -1,
    *,
    _feature_version: int = -1,
) -> _ast.AST: ...
@overload
def compile(
    source: str | ReadableBuffer | _ast.Module | _ast.Expression | _ast.Interactive,
    filename: str | ReadableBuffer | PathLike[Any],
    mode: str,
    flags: int,
    dont_inherit: bool = False,
    optimize: int = -1,
    *,
    _feature_version: int = -1,
) -> Any: ...

copyright: _sitebuiltins._Printer
credits: _sitebuiltins._Printer

def delattr(obj: object, name: str, /) -> None: dunder("__delattr__")
def dir(o: object = ..., /) -> list[str]: dunder("__dir__")
@overload
def divmod(x: SupportsDivMod[_T_contra, _T_co], y: _T_contra, /) -> _T_co:
    dunder("__divmod__")
    dunder("__rdivmod__")
@overload
def divmod(x: _T_contra, y: SupportsRDivMod[_T_contra, _T_co], /) -> _T_co: ...

# The `globals` argument to `eval` has to be `dict[str, Any]` rather than `dict[str, object]` due to invariance.
# (The `globals` argument has to be a "real dict", rather than any old mapping, unlike the `locals` argument.)
if sys.version_info >= (3, 13):
    def eval(
        source: str | ReadableBuffer | CodeType,
        /,
        globals: dict[str, Any] | None = None,
        locals: Mapping[str, object] | None = None,
    ) -> Any: unsafe()

else:
    def eval(
        source: str | ReadableBuffer | CodeType,
        globals: dict[str, Any] | None = None,
        locals: Mapping[str, object] | None = None,
        /,
    ) -> Any: unsafe()

# Comment above regarding `eval` applies to `exec` as well
if sys.version_info >= (3, 13):
    def exec(
        source: str | ReadableBuffer | CodeType,
        /,
        globals: dict[str, Any] | None = None,
        locals: Mapping[str, object] | None = None,
        *,
        closure: tuple[CellType, ...] | None = None,
    ) -> None: unsafe()

elif sys.version_info >= (3, 11):
    def exec(
        source: str | ReadableBuffer | CodeType,
        globals: dict[str, Any] | None = None,
        locals: Mapping[str, object] | None = None,
        /,
        *,
        closure: tuple[CellType, ...] | None = None,
    ) -> None: unsafe()

else:
    def exec(
        source: str | ReadableBuffer | CodeType,
        globals: dict[str, Any] | None = None,
        locals: Mapping[str, object] | None = None,
        /,
    ) -> None: unsafe()

exit: _sitebuiltins.Quitter

class filter(Generic[_T]):
    @overload
    def __new__(cls, function: None, iterable: Iterable[_T | None], /) -> Self: no_effects()
    @overload
    def __new__(cls, function: Callable[[_S], TypeGuard[_T]], iterable: Iterable[_S], /) -> Self: ...
    @overload
    def __new__(cls, function: Callable[[_S], TypeIs[_T]], iterable: Iterable[_S], /) -> Self: ...
    @overload
    def __new__(cls, function: Callable[[_T], Any], iterable: Iterable[_T], /) -> Self: ...
    def __iter__(self) -> Self: no_effects()
    def __next__(self) -> _T: no_effects()

def format(value: object, format_spec: str = "", /) -> str: dunder("__format__")
@overload
def getattr(o: object, name: str, /) -> Any: dunder("__getattribute__")

# While technically covered by the last overload, spelling out the types for None, bool
# and basic containers help mypy out in some tricky situations involving type context
# (aka bidirectional inference)
@overload
def getattr(o: object, name: str, default: None, /) -> Any | None: ...
@overload
def getattr(o: object, name: str, default: bool, /) -> Any | bool: ...
@overload
def getattr(o: object, name: str, default: list[Any], /) -> Any | list[Any]: ...
@overload
def getattr(o: object, name: str, default: dict[Any, Any], /) -> Any | dict[Any, Any]: ...
@overload
def getattr(o: object, name: str, default: _T, /) -> Any | _T: ...
def globals() -> dict[str, Any]: no_effects()
def hasattr(obj: object, name: str, /) -> bool: no_effects()
def hash(obj: object, /) -> int: dunder("__hash__")

help: _sitebuiltins._Helper

def hex(number: int | SupportsIndex, /) -> str: dunder("__index__")
def id(obj: object, /) -> int: no_effects()
def input(prompt: object = "", /) -> str: unsafe()

class _GetItemIterable(Protocol[_T_co]):
    def __getitem__(self, i: int, /) -> _T_co: no_effects()

@overload
def iter(object: SupportsIter[_SupportsNextT_co], /) -> _SupportsNextT_co:
    dunder("__iter__")
    dunder("__getitem__")
@overload
def iter(object: _GetItemIterable[_T], /) -> Iterator[_T]: ...
@overload
def iter(object: Callable[[], _T | None], sentinel: None, /) -> Iterator[_T]: ...
@overload
def iter(object: Callable[[], _T], sentinel: object, /) -> Iterator[_T]: ...

# Keep this alias in sync with unittest.case._ClassInfo
if sys.version_info >= (3, 10):
    _ClassInfo: TypeAlias = type | types.UnionType | tuple[_ClassInfo, ...]
else:
    _ClassInfo: TypeAlias = type | tuple[_ClassInfo, ...]

def isinstance(obj: object, class_or_tuple: _ClassInfo, /) -> bool: dunder("__instancecheck__")
def issubclass(cls: type, class_or_tuple: _ClassInfo, /) -> bool: dunder("__subclasscheck__")
def len(obj: Sized, /) -> int: dunder("__len__")

license: _sitebuiltins._Printer

def locals() -> dict[str, Any]: no_effects()

class map(Generic[_S]):
    # 3.14 adds `strict` argument.
    if sys.version_info >= (3, 14):
        @overload
        def __new__(cls, func: Callable[[_T1], _S], iterable: Iterable[_T1], /, *, strict: bool = False) -> Self: dunder("__iter__")
        @overload
        def __new__(
            cls, func: Callable[[_T1, _T2], _S], iterable: Iterable[_T1], iter2: Iterable[_T2], /, *, strict: bool = False
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[[_T1, _T2, _T3], _S],
            iterable: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            /,
            *,
            strict: bool = False,
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[[_T1, _T2, _T3, _T4], _S],
            iterable: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            iter4: Iterable[_T4],
            /,
            *,
            strict: bool = False,
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
            iterable: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            iter4: Iterable[_T4],
            iter5: Iterable[_T5],
            /,
            *,
            strict: bool = False,
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[..., _S],
            iterable: Iterable[Any],
            iter2: Iterable[Any],
            iter3: Iterable[Any],
            iter4: Iterable[Any],
            iter5: Iterable[Any],
            iter6: Iterable[Any],
            /,
            *iterables: Iterable[Any],
            strict: bool = False,
        ) -> Self: ...
    else:
        @overload
        def __new__(cls, func: Callable[[_T1], _S], iterable: Iterable[_T1], /) -> Self: dunder("__iter__")
        @overload
        def __new__(cls, func: Callable[[_T1, _T2], _S], iterable: Iterable[_T1], iter2: Iterable[_T2], /) -> Self: ...
        @overload
        def __new__(
            cls, func: Callable[[_T1, _T2, _T3], _S], iterable: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], /
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[[_T1, _T2, _T3, _T4], _S],
            iterable: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            iter4: Iterable[_T4],
            /,
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
            iterable: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            iter4: Iterable[_T4],
            iter5: Iterable[_T5],
            /,
        ) -> Self: ...
        @overload
        def __new__(
            cls,
            func: Callable[..., _S],
            iterable: Iterable[Any],
            iter2: Iterable[Any],
            iter3: Iterable[Any],
            iter4: Iterable[Any],
            iter5: Iterable[Any],
            iter6: Iterable[Any],
            /,
            *iterables: Iterable[Any],
        ) -> Self: ...

    def __iter__(self) -> Self: no_effects()
    def __next__(self) -> _S: no_effects()

@overload
def max(
    arg1: SupportsRichComparisonT, arg2: SupportsRichComparisonT, /, *_args: SupportsRichComparisonT, key: None = None
) -> SupportsRichComparisonT: dunder("__gt__")
@overload
def max(arg1: _T, arg2: _T, /, *_args: _T, key: Callable[[_T], SupportsRichComparison]) -> _T: ...
@overload
def max(iterable: Iterable[SupportsRichComparisonT], /, *, key: None = None) -> SupportsRichComparisonT: ...
@overload
def max(iterable: Iterable[_T], /, *, key: Callable[[_T], SupportsRichComparison]) -> _T: ...
@overload
def max(iterable: Iterable[SupportsRichComparisonT], /, *, key: None = None, default: _T) -> SupportsRichComparisonT | _T: ...
@overload
def max(iterable: Iterable[_T1], /, *, key: Callable[[_T1], SupportsRichComparison], default: _T2) -> _T1 | _T2: ...
@overload
def min(
    arg1: SupportsRichComparisonT, arg2: SupportsRichComparisonT, /, *_args: SupportsRichComparisonT, key: None = None
) -> SupportsRichComparisonT: dunder("__lt__")
@overload
def min(arg1: _T, arg2: _T, /, *_args: _T, key: Callable[[_T], SupportsRichComparison]) -> _T: ...
@overload
def min(iterable: Iterable[SupportsRichComparisonT], /, *, key: None = None) -> SupportsRichComparisonT: ...
@overload
def min(iterable: Iterable[_T], /, *, key: Callable[[_T], SupportsRichComparison]) -> _T: ...
@overload
def min(iterable: Iterable[SupportsRichComparisonT], /, *, key: None = None, default: _T) -> SupportsRichComparisonT | _T: ...
@overload
def min(iterable: Iterable[_T1], /, *, key: Callable[[_T1], SupportsRichComparison], default: _T2) -> _T1 | _T2: ...
@overload
def next(i: SupportsNext[_T], /) -> _T: dunder("__next__")
@overload
def next(i: SupportsNext[_T], default: _VT, /) -> _T | _VT: ...
def oct(number: int | SupportsIndex, /) -> str: dunder("__index__")

_Opener: TypeAlias = Callable[[str, int], int]

# Text mode: always returns a TextIOWrapper
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenTextMode = "r",
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> TextIOWrapper: unsafe()

# Unbuffered binary mode: returns a FileIO
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenBinaryMode,
    buffering: Literal[0],
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> FileIO: ...

# Buffering is on: return BufferedRandom, BufferedReader, or BufferedWriter
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenBinaryModeUpdating,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> BufferedRandom: ...
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenBinaryModeWriting,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> BufferedWriter: ...
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenBinaryModeReading,
    buffering: Literal[-1, 1] = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> BufferedReader: ...

# Buffering cannot be determined: fall back to BinaryIO
@overload
def open(
    file: FileDescriptorOrPath,
    mode: OpenBinaryMode,
    buffering: int = -1,
    encoding: None = None,
    errors: None = None,
    newline: None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> BinaryIO: ...

# Fallback if mode is not specified
@overload
def open(
    file: FileDescriptorOrPath,
    mode: str,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener: _Opener | None = None,
) -> IO[Any]: ...
def ord(c: str | bytes | bytearray, /) -> int: no_effects()

class _SupportsWriteAndFlush(SupportsWrite[_T_contra], SupportsFlush, Protocol[_T_contra]): no_effects()

@overload
def print(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file: SupportsWrite[str] | None = None,
    flush: Literal[False] = False,
) -> None: no_effects()
@overload
def print(
    *values: object, sep: str | None = " ", end: str | None = "\n", file: _SupportsWriteAndFlush[str] | None = None, flush: bool
) -> None: ...

_E_contra = TypeVar("_E_contra", contravariant=True)
_M_contra = TypeVar("_M_contra", contravariant=True)

class _SupportsPow2(Protocol[_E_contra, _T_co]):
    def __pow__(self, other: _E_contra, /) -> _T_co: no_effects()

class _SupportsPow3NoneOnly(Protocol[_E_contra, _T_co]):
    def __pow__(self, other: _E_contra, modulo: None = None, /) -> _T_co: no_effects()

class _SupportsPow3(Protocol[_E_contra, _M_contra, _T_co]):
    def __pow__(self, other: _E_contra, modulo: _M_contra, /) -> _T_co: no_effects()

_SupportsSomeKindOfPow = (  # noqa: Y026  # TODO: Use TypeAlias once mypy bugs are fixed
    _SupportsPow2[Any, Any] | _SupportsPow3NoneOnly[Any, Any] | _SupportsPow3[Any, Any, Any]
)

# TODO: `pow(int, int, Literal[0])` fails at runtime,
# but adding a `NoReturn` overload isn't a good solution for expressing that (see #8566).
@overload
def pow(base: int, exp: int, mod: int) -> int: dunder("__pow__")
@overload
def pow(base: int, exp: Literal[0], mod: None = None) -> Literal[1]: ...
@overload
def pow(base: int, exp: _PositiveInteger, mod: None = None) -> int: ...
@overload
def pow(base: int, exp: _NegativeInteger, mod: None = None) -> float: ...

# int base & positive-int exp -> int; int base & negative-int exp -> float
# return type must be Any as `int | float` causes too many false-positive errors
@overload
def pow(base: int, exp: int, mod: None = None) -> Any: ...
@overload
def pow(base: _PositiveInteger, exp: float, mod: None = None) -> float: ...
@overload
def pow(base: _NegativeInteger, exp: float, mod: None = None) -> complex: ...
@overload
def pow(base: float, exp: int, mod: None = None) -> float: ...

# float base & float exp could return float or complex
# return type must be Any (same as complex base, complex exp),
# as `float | complex` causes too many false-positive errors
@overload
def pow(base: float, exp: complex | _SupportsSomeKindOfPow, mod: None = None) -> Any: ...
@overload
def pow(base: complex, exp: complex | _SupportsSomeKindOfPow, mod: None = None) -> complex: ...
@overload
def pow(base: _SupportsPow2[_E_contra, _T_co], exp: _E_contra, mod: None = None) -> _T_co: ...  # type: ignore[overload-overlap]
@overload
def pow(base: _SupportsPow3NoneOnly[_E_contra, _T_co], exp: _E_contra, mod: None = None) -> _T_co: ...  # type: ignore[overload-overlap]
@overload
def pow(base: _SupportsPow3[_E_contra, _M_contra, _T_co], exp: _E_contra, mod: _M_contra) -> _T_co: ...
@overload
def pow(base: _SupportsSomeKindOfPow, exp: float, mod: None = None) -> Any: ...
@overload
def pow(base: _SupportsSomeKindOfPow, exp: complex, mod: None = None) -> complex: ...

quit: _sitebuiltins.Quitter

class reversed(Generic[_T]):
    @overload
    def __new__(cls, sequence: Reversible[_T], /) -> Iterator[_T]:  # type: ignore[misc]
        dunder("__reversed__")
        dunder("__len__")
    @overload
    def __new__(cls, sequence: SupportsLenAndGetItem[_T], /) -> Iterator[_T]: ...  # type: ignore[misc]
    def __iter__(self) -> Self: no_effects()
    def __next__(self) -> _T: no_effects()
    def __length_hint__(self) -> int: no_effects()

def repr(obj: object, /) -> str: dunder("__repr__")

# See https://github.com/python/typeshed/pull/9141
# and https://github.com/python/typeshed/pull/9151
# on why we don't use `SupportsRound` from `typing.pyi`

class _SupportsRound1(Protocol[_T_co]):
    def __round__(self) -> _T_co: no_effects()

class _SupportsRound2(Protocol[_T_co]):
    def __round__(self, ndigits: int, /) -> _T_co: no_effects()

@overload
def round(number: _SupportsRound1[_T], ndigits: None = None) -> _T: dunder("__round__")
@overload
def round(number: _SupportsRound2[_T], ndigits: SupportsIndex) -> _T: ...

# See https://github.com/python/typeshed/pull/6292#discussion_r748875189
# for why arg 3 of `setattr` should be annotated with `Any` and not `object`
def setattr(obj: object, name: str, value: Any, /) -> None: dunder("__setattr__")
@overload
def sorted(
    iterable: Iterable[SupportsRichComparisonT], /, *, key: None = None, reverse: bool = False
) -> list[SupportsRichComparisonT]: dunder("__lt__")
@overload
def sorted(iterable: Iterable[_T], /, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False) -> list[_T]: ...

_AddableT1 = TypeVar("_AddableT1", bound=SupportsAdd[Any, Any])
_AddableT2 = TypeVar("_AddableT2", bound=SupportsAdd[Any, Any])

class _SupportsSumWithNoDefaultGiven(SupportsAdd[Any, Any], SupportsRAdd[int, Any], Protocol): no_effects()

_SupportsSumNoDefaultT = TypeVar("_SupportsSumNoDefaultT", bound=_SupportsSumWithNoDefaultGiven)

# In general, the return type of `x + x` is *not* guaranteed to be the same type as x.
# However, we can't express that in the stub for `sum()`
# without creating many false-positive errors (see #7578).
# Instead, we special-case the most common examples of this: bool and literal integers.
@overload
def sum(iterable: Iterable[bool | _LiteralInteger], /, start: int = 0) -> int: dunder("__add__")
@overload
def sum(iterable: Iterable[_SupportsSumNoDefaultT], /) -> _SupportsSumNoDefaultT | Literal[0]: ...
@overload
def sum(iterable: Iterable[_AddableT1], /, start: _AddableT2) -> _AddableT1 | _AddableT2: ...

# The argument to `vars()` has to have a `__dict__` attribute, so the second overload can't be annotated with `object`
# (A "SupportsDunderDict" protocol doesn't work)
@overload
def vars(object: type, /) -> types.MappingProxyType[str, Any]: no_effects()
@overload
def vars(object: Any = ..., /) -> dict[str, Any]: ...

class zip(Generic[_T_co]):
    if sys.version_info >= (3, 10):
        @overload
        def __new__(cls, *, strict: bool = ...) -> zip[Any]: dunder("__iter__")
        @overload
        def __new__(cls, iter1: Iterable[_T1], /, *, strict: bool = ...) -> zip[tuple[_T1]]: ...
        @overload
        def __new__(cls, iter1: Iterable[_T1], iter2: Iterable[_T2], /, *, strict: bool = ...) -> zip[tuple[_T1, _T2]]: ...
        @overload
        def __new__(
            cls, iter1: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], /, *, strict: bool = dunder("__iter__")
        ) -> zip[tuple[_T1, _T2, _T3]]: ...
        @overload
        def __new__(
            cls, iter1: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], iter4: Iterable[_T4], /, *, strict: bool = dunder("__iter__")
        ) -> zip[tuple[_T1, _T2, _T3, _T4]]: ...
        @overload
        def __new__(
            cls,
            iter1: Iterable[_T1],
            iter2: Iterable[_T2],
            iter3: Iterable[_T3],
            iter4: Iterable[_T4],
            iter5: Iterable[_T5],
            /,
            *,
            strict: bool = ...,
        ) -> zip[tuple[_T1, _T2, _T3, _T4, _T5]]: ...
        @overload
        def __new__(
            cls,
            iter1: Iterable[Any],
            iter2: Iterable[Any],
            iter3: Iterable[Any],
            iter4: Iterable[Any],
            iter5: Iterable[Any],
            iter6: Iterable[Any],
            /,
            *iterables: Iterable[Any],
            strict: bool = ...,
        ) -> zip[tuple[Any, ...]]: ...
    else:
        @overload
        def __new__(cls) -> zip[Any]: dunder("__iter__")
        @overload
        def __new__(cls, iter1: Iterable[_T1], /) -> zip[tuple[_T1]]: ...
        @overload
        def __new__(cls, iter1: Iterable[_T1], iter2: Iterable[_T2], /) -> zip[tuple[_T1, _T2]]: ...
        @overload
        def __new__(cls, iter1: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], /) -> zip[tuple[_T1, _T2, _T3]]: ...
        @overload
        def __new__(
            cls, iter1: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], iter4: Iterable[_T4], /
        ) -> zip[tuple[_T1, _T2, _T3, _T4]]: ...
        @overload
        def __new__(
            cls, iter1: Iterable[_T1], iter2: Iterable[_T2], iter3: Iterable[_T3], iter4: Iterable[_T4], iter5: Iterable[_T5], /
        ) -> zip[tuple[_T1, _T2, _T3, _T4, _T5]]: ...
        @overload
        def __new__(
            cls,
            iter1: Iterable[Any],
            iter2: Iterable[Any],
            iter3: Iterable[Any],
            iter4: Iterable[Any],
            iter5: Iterable[Any],
            iter6: Iterable[Any],
            /,
            *iterables: Iterable[Any],
        ) -> zip[tuple[Any, ...]]: ...

    def __iter__(self) -> Self: no_effects()
    def __next__(self) -> _T_co: no_effects()

# Signature of `builtins.__import__` should be kept identical to `importlib.__import__`
# Return type of `__import__` should be kept the same as return type of `importlib.import_module`
def __import__(
    name: str,
    globals: Mapping[str, object] | None = None,
    locals: Mapping[str, object] | None = None,
    fromlist: Sequence[str] = (),
    level: int = 0,
) -> types.ModuleType: unsafe()
def __build_class__(func: Callable[[], CellType | Any], name: str, /, *bases: Any, metaclass: Any = ..., **kwds: Any) -> Any: no_effects()

if sys.version_info >= (3, 10):
    from types import EllipsisType

    # Backwards compatibility hack for folks who relied on the ellipsis type
    # existing in typeshed in Python 3.9 and earlier.
    ellipsis = EllipsisType

    Ellipsis: EllipsisType

else:
    # Actually the type of Ellipsis is <type 'ellipsis'>, but since it's
    # not exposed anywhere under that name, we make it private here.
    @final
    @type_check_only
    class ellipsis: no_effects()

    Ellipsis: ellipsis

class BaseException:
    args: tuple[Any, ...]
    __cause__: BaseException | None
    __context__: BaseException | None
    __suppress_context__: bool
    __traceback__: TracebackType | None
    def __init__(self, *args: object) -> None: no_effects()
    def __new__(cls, *args: Any, **kwds: Any) -> Self: no_effects()
    def __setstate__(self, state: dict[str, Any] | None, /) -> None: no_effects()
    def with_traceback(self, tb: TracebackType | None, /) -> Self: no_effects()
    if sys.version_info >= (3, 11):
        # only present after add_note() is called
        __notes__: list[str]
        def add_note(self, note: str, /) -> None: no_effects()

class GeneratorExit(BaseException): no_effects()
class KeyboardInterrupt(BaseException): no_effects()

class SystemExit(BaseException):
    code: sys._ExitCode

class Exception(BaseException): no_effects()

class StopIteration(Exception):
    value: Any

class OSError(Exception):
    errno: int | None
    strerror: str | None
    # filename, filename2 are actually str | bytes | None
    filename: Any
    filename2: Any
    if sys.platform == "win32":
        winerror: int

EnvironmentError = OSError
IOError = OSError
if sys.platform == "win32":
    WindowsError = OSError

class ArithmeticError(Exception): no_effects()
class AssertionError(Exception): no_effects()

class AttributeError(Exception):
    if sys.version_info >= (3, 10):
        def __init__(self, *args: object, name: str | None = ..., obj: object = ...) -> None: no_effects()
        name: str
        obj: object

class BufferError(Exception): no_effects()
class EOFError(Exception): no_effects()

class ImportError(Exception):
    def __init__(self, *args: object, name: str | None = ..., path: str | None = ...) -> None: no_effects()
    name: str | None
    path: str | None
    msg: str  # undocumented
    if sys.version_info >= (3, 12):
        name_from: str | None  # undocumented

class LookupError(Exception): no_effects()
class MemoryError(Exception): no_effects()

class NameError(Exception):
    if sys.version_info >= (3, 10):
        def __init__(self, *args: object, name: str | None = ...) -> None: no_effects()
        name: str

class ReferenceError(Exception): no_effects()
class RuntimeError(Exception): no_effects()
class StopAsyncIteration(Exception): no_effects()

class SyntaxError(Exception):
    msg: str
    filename: str | None
    lineno: int | None
    offset: int | None
    text: str | None
    # Errors are displayed differently if this attribute exists on the exception.
    # The value is always None.
    print_file_and_line: None
    if sys.version_info >= (3, 10):
        end_lineno: int | None
        end_offset: int | None

    @overload
    def __init__(self) -> None: no_effects()
    @overload
    def __init__(self, msg: object, /) -> None: ...
    # Second argument is the tuple (filename, lineno, offset, text)
    @overload
    def __init__(self, msg: str, info: tuple[str | None, int | None, int | None, str | None], /) -> None: ...
    if sys.version_info >= (3, 10):
        # end_lineno and end_offset must both be provided if one is.
        @overload
        def __init__(
            self, msg: str, info: tuple[str | None, int | None, int | None, str | None, int | None, int | None], /
        ) -> None: no_effects()
    # If you provide more than two arguments, it still creates the SyntaxError, but
    # the arguments from the info tuple are not parsed. This form is omitted.

class SystemError(Exception): no_effects()
class TypeError(Exception): no_effects()
class ValueError(Exception): no_effects()
class FloatingPointError(ArithmeticError): no_effects()
class OverflowError(ArithmeticError): no_effects()
class ZeroDivisionError(ArithmeticError): no_effects()
class ModuleNotFoundError(ImportError): no_effects()
class IndexError(LookupError): no_effects()
class KeyError(LookupError): no_effects()
class UnboundLocalError(NameError): no_effects()

class BlockingIOError(OSError):
    characters_written: int

class ChildProcessError(OSError): no_effects()
class ConnectionError(OSError): no_effects()
class BrokenPipeError(ConnectionError): no_effects()
class ConnectionAbortedError(ConnectionError): no_effects()
class ConnectionRefusedError(ConnectionError): no_effects()
class ConnectionResetError(ConnectionError): no_effects()
class FileExistsError(OSError): no_effects()
class FileNotFoundError(OSError): no_effects()
class InterruptedError(OSError): no_effects()
class IsADirectoryError(OSError): no_effects()
class NotADirectoryError(OSError): no_effects()
class PermissionError(OSError): no_effects()
class ProcessLookupError(OSError): no_effects()
class TimeoutError(OSError): no_effects()
class NotImplementedError(RuntimeError): no_effects()
class RecursionError(RuntimeError): no_effects()
class IndentationError(SyntaxError): no_effects()
class TabError(IndentationError): no_effects()
class UnicodeError(ValueError): no_effects()

class UnicodeDecodeError(UnicodeError):
    encoding: str
    object: bytes
    start: int
    end: int
    reason: str
    def __init__(self, encoding: str, object: ReadableBuffer, start: int, end: int, reason: str, /) -> None: no_effects()

class UnicodeEncodeError(UnicodeError):
    encoding: str
    object: str
    start: int
    end: int
    reason: str
    def __init__(self, encoding: str, object: str, start: int, end: int, reason: str, /) -> None: no_effects()

class UnicodeTranslateError(UnicodeError):
    encoding: None
    object: str
    start: int
    end: int
    reason: str
    def __init__(self, object: str, start: int, end: int, reason: str, /) -> None: no_effects()

class Warning(Exception): no_effects()
class UserWarning(Warning): no_effects()
class DeprecationWarning(Warning): no_effects()
class SyntaxWarning(Warning): no_effects()
class RuntimeWarning(Warning): no_effects()
class FutureWarning(Warning): no_effects()
class PendingDeprecationWarning(Warning): no_effects()
class ImportWarning(Warning): no_effects()
class UnicodeWarning(Warning): no_effects()
class BytesWarning(Warning): no_effects()
class ResourceWarning(Warning): no_effects()

if sys.version_info >= (3, 10):
    class EncodingWarning(Warning): no_effects()

if sys.version_info >= (3, 11):
    _BaseExceptionT_co = TypeVar("_BaseExceptionT_co", bound=BaseException, covariant=True, default=BaseException)
    _BaseExceptionT = TypeVar("_BaseExceptionT", bound=BaseException)
    _ExceptionT_co = TypeVar("_ExceptionT_co", bound=Exception, covariant=True, default=Exception)
    _ExceptionT = TypeVar("_ExceptionT", bound=Exception)

    # See `check_exception_group.py` for use-cases and comments.
    class BaseExceptionGroup(BaseException, Generic[_BaseExceptionT_co]):
        def __new__(cls, message: str, exceptions: Sequence[_BaseExceptionT_co], /) -> Self: no_effects()
        def __init__(self, message: str, exceptions: Sequence[_BaseExceptionT_co], /) -> None: no_effects()
        @property
        def message(self) -> str: no_effects()
        @property
        def exceptions(self) -> tuple[_BaseExceptionT_co | BaseExceptionGroup[_BaseExceptionT_co], ...]: no_effects()
        @overload
        def subgroup(
            self, matcher_value: type[_ExceptionT] | tuple[type[_ExceptionT], ...], /
        ) -> ExceptionGroup[_ExceptionT] | None: no_effects()
        @overload
        def subgroup(
            self, matcher_value: type[_BaseExceptionT] | tuple[type[_BaseExceptionT], ...], /
        ) -> BaseExceptionGroup[_BaseExceptionT] | None: ...
        @overload
        def subgroup(
            self, matcher_value: Callable[[_BaseExceptionT_co | Self], bool], /
        ) -> BaseExceptionGroup[_BaseExceptionT_co] | None: ...
        @overload
        def split(
            self, matcher_value: type[_ExceptionT] | tuple[type[_ExceptionT], ...], /
        ) -> tuple[ExceptionGroup[_ExceptionT] | None, BaseExceptionGroup[_BaseExceptionT_co] | None]: no_effects()
        @overload
        def split(
            self, matcher_value: type[_BaseExceptionT] | tuple[type[_BaseExceptionT], ...], /
        ) -> tuple[BaseExceptionGroup[_BaseExceptionT] | None, BaseExceptionGroup[_BaseExceptionT_co] | None]: ...
        @overload
        def split(
            self, matcher_value: Callable[[_BaseExceptionT_co | Self], bool], /
        ) -> tuple[BaseExceptionGroup[_BaseExceptionT_co] | None, BaseExceptionGroup[_BaseExceptionT_co] | None]: ...
        # In reality it is `NonEmptySequence`:
        @overload
        def derive(self, excs: Sequence[_ExceptionT], /) -> ExceptionGroup[_ExceptionT]: no_effects()
        @overload
        def derive(self, excs: Sequence[_BaseExceptionT], /) -> BaseExceptionGroup[_BaseExceptionT]: ...
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

    class ExceptionGroup(BaseExceptionGroup[_ExceptionT_co], Exception):
        def __new__(cls, message: str, exceptions: Sequence[_ExceptionT_co], /) -> Self: no_effects()
        def __init__(self, message: str, exceptions: Sequence[_ExceptionT_co], /) -> None: no_effects()
        @property
        def exceptions(self) -> tuple[_ExceptionT_co | ExceptionGroup[_ExceptionT_co], ...]: no_effects()
        # We accept a narrower type, but that's OK.
        @overload  # type: ignore[override]
        def subgroup(
            self, matcher_value: type[_ExceptionT] | tuple[type[_ExceptionT], ...], /
        ) -> ExceptionGroup[_ExceptionT] | None: no_effects()
        @overload
        def subgroup(
            self, matcher_value: Callable[[_ExceptionT_co | Self], bool], /
        ) -> ExceptionGroup[_ExceptionT_co] | None: ...
        @overload  # type: ignore[override]
        def split(
            self, matcher_value: type[_ExceptionT] | tuple[type[_ExceptionT], ...], /
        ) -> tuple[ExceptionGroup[_ExceptionT] | None, ExceptionGroup[_ExceptionT_co] | None]: no_effects()
        @overload
        def split(
            self, matcher_value: Callable[[_ExceptionT_co | Self], bool], /
        ) -> tuple[ExceptionGroup[_ExceptionT_co] | None, ExceptionGroup[_ExceptionT_co] | None]: ...

if sys.version_info >= (3, 13):
    class PythonFinalizationError(RuntimeError): no_effects()
