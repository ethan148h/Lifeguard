import sys
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import SupportsItems, SupportsKeysAndGetItem, SupportsRichComparison, SupportsRichComparisonT
from types import GenericAlias
from typing import Any, ClassVar, Generic, NoReturn, SupportsIndex, TypeVar, final, overload, type_check_only
from typing_extensions import Self, disjoint_base

if sys.version_info >= (3, 10):
    from collections.abc import (
        Callable,
        ItemsView,
        Iterable,
        Iterator,
        KeysView,
        Mapping,
        MutableMapping,
        MutableSequence,
        Sequence,
        ValuesView,
    )
else:
    from _collections_abc import *

__all__ = ["ChainMap", "Counter", "OrderedDict", "UserDict", "UserList", "UserString", "defaultdict", "deque", "namedtuple"]

_S = TypeVar("_S")
_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

# namedtuple is special-cased in the type checker; the initializer is ignored.
def namedtuple(
    typename: str,
    field_names: str | Iterable[str],
    *,
    rename: bool = False,
    module: str | None = None,
    defaults: Iterable[Any] | None = None,
) -> type[tuple[Any, ...]]: dunder("__iter__")

class UserDict(MutableMapping[_KT, _VT]):
    data: dict[_KT, _VT]
    # __init__ should be kept roughly in line with `dict.__init__`, which has the same semantics
    @overload
    def __init__(self, dict: None = None, /) -> None: dunder("__iter__")
    @overload
    def __init__(
        self: UserDict[str, _VT], dict: None = None, /, **kwargs: _VT  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    ) -> None: ...
    @overload
    def __init__(self, dict: SupportsKeysAndGetItem[_KT, _VT], /) -> None: ...
    @overload
    def __init__(
        self: UserDict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        dict: SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[tuple[_KT, _VT]], /) -> None: ...
    @overload
    def __init__(
        self: UserDict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        iterable: Iterable[tuple[str, _VT]],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self: UserDict[str, str], iterable: Iterable[list[str]], /) -> None: ...
    @overload
    def __init__(self: UserDict[bytes, bytes], iterable: Iterable[list[bytes]], /) -> None: ...
    def __len__(self) -> int: no_effects()
    def __getitem__(self, key: _KT) -> _VT: no_effects()
    def __setitem__(self, key: _KT, item: _VT) -> None: mutation()
    def __delitem__(self, key: _KT) -> None: mutation()
    def __iter__(self) -> Iterator[_KT]: no_effects()
    def __contains__(self, key: object) -> bool: no_effects()
    def copy(self) -> Self: no_effects()
    def __copy__(self) -> Self: no_effects()

    # `UserDict.fromkeys` has the same semantics as `dict.fromkeys`, so should be kept in line with `dict.fromkeys`.
    # TODO: Much like `dict.fromkeys`, the true signature of `UserDict.fromkeys` is inexpressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> UserDict[_T, Any | None]: dunder("__iter__")
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> UserDict[_T, _S]: ...
    @overload
    def __or__(self, other: UserDict[_KT, _VT] | dict[_KT, _VT]) -> Self: no_effects()
    @overload
    def __or__(self, other: UserDict[_T1, _T2] | dict[_T1, _T2]) -> UserDict[_KT | _T1, _VT | _T2]: ...
    @overload
    def __ror__(self, other: UserDict[_KT, _VT] | dict[_KT, _VT]) -> Self: no_effects()
    @overload
    def __ror__(self, other: UserDict[_T1, _T2] | dict[_T1, _T2]) -> UserDict[_KT | _T1, _VT | _T2]: ...
    # UserDict.__ior__ should be kept roughly in line with MutableMapping.update()
    @overload  # type: ignore[misc]
    def __ior__(self, other: SupportsKeysAndGetItem[_KT, _VT]) -> Self:
        mutation()
        dunder("__iter__")
    @overload
    def __ior__(self, other: Iterable[tuple[_KT, _VT]]) -> Self: ...
    if sys.version_info >= (3, 12):
        @overload
        def get(self, key: _KT, default: None = None) -> _VT | None: no_effects()
        @overload
        def get(self, key: _KT, default: _VT) -> _VT: ...
        @overload
        def get(self, key: _KT, default: _T) -> _VT | _T: ...

class UserList(MutableSequence[_T]):
    data: list[_T]
    @overload
    def __init__(self, initlist: None = None) -> None: dunder("__iter__")
    @overload
    def __init__(self, initlist: Iterable[_T]) -> None: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]
    def __lt__(self, other: list[_T] | UserList[_T]) -> bool: no_effects()
    def __le__(self, other: list[_T] | UserList[_T]) -> bool: no_effects()
    def __gt__(self, other: list[_T] | UserList[_T]) -> bool: no_effects()
    def __ge__(self, other: list[_T] | UserList[_T]) -> bool: no_effects()
    def __eq__(self, other: object) -> bool: no_effects()
    def __contains__(self, item: object) -> bool: no_effects()
    def __len__(self) -> int: no_effects()
    @overload
    def __getitem__(self, i: SupportsIndex) -> _T: no_effects()
    @overload
    def __getitem__(self, i: slice) -> Self: ...
    @overload
    def __setitem__(self, i: SupportsIndex, item: _T) -> None:
        mutation()
        dunder("__iter__")
    @overload
    def __setitem__(self, i: slice, item: Iterable[_T]) -> None: ...
    def __delitem__(self, i: SupportsIndex | slice) -> None: mutation()
    def __add__(self, other: Iterable[_T]) -> Self: dunder("__iter__")
    def __radd__(self, other: Iterable[_T]) -> Self: dunder("__iter__")
    def __iadd__(self, other: Iterable[_T]) -> Self:
        mutation()
        dunder("__iter__")
    def __mul__(self, n: int) -> Self: no_effects()
    def __rmul__(self, n: int) -> Self: no_effects()
    def __imul__(self, n: int) -> Self: mutation()
    def append(self, item: _T) -> None: mutation()
    def insert(self, i: int, item: _T) -> None: mutation()
    def pop(self, i: int = -1) -> _T: mutation()
    def remove(self, item: _T) -> None: mutation()
    def copy(self) -> Self: no_effects()
    def __copy__(self) -> Self: no_effects()
    def count(self, item: _T) -> int: no_effects()
    # The runtime signature is "item, *args", and the arguments are then passed
    # to `list.index`. In order to give more precise types, we pretend that the
    # `item` argument is positional-only.
    def index(self, item: _T, start: SupportsIndex = 0, stop: SupportsIndex = sys.maxsize, /) -> int: no_effects()
    # All arguments are passed to `list.sort` at runtime, so the signature should be kept in line with `list.sort`.
    @overload
    def sort(self: UserList[SupportsRichComparisonT], *, key: None = None, reverse: bool = False) -> None: mutation()
    @overload
    def sort(self, *, key: Callable[[_T], SupportsRichComparison], reverse: bool = False) -> None: ...
    def extend(self, other: Iterable[_T]) -> None:
        mutation()
        dunder("__iter__")

class UserString(Sequence[UserString]):
    data: str
    def __init__(self, seq: object) -> None: no_effects()
    def __int__(self) -> int: no_effects()
    def __float__(self) -> float: no_effects()
    def __complex__(self) -> complex: no_effects()
    def __getnewargs__(self) -> tuple[str]: no_effects()
    def __lt__(self, string: str | UserString) -> bool: no_effects()
    def __le__(self, string: str | UserString) -> bool: no_effects()
    def __gt__(self, string: str | UserString) -> bool: no_effects()
    def __ge__(self, string: str | UserString) -> bool: no_effects()
    def __eq__(self, string: object) -> bool: no_effects()
    def __hash__(self) -> int: no_effects()
    def __contains__(self, char: object) -> bool: no_effects()
    def __len__(self) -> int: no_effects()
    def __getitem__(self, index: SupportsIndex | slice) -> Self: no_effects()
    def __iter__(self) -> Iterator[Self]: no_effects()
    def __reversed__(self) -> Iterator[Self]: no_effects()
    def __add__(self, other: object) -> Self: no_effects()
    def __radd__(self, other: object) -> Self: no_effects()
    def __mul__(self, n: int) -> Self: no_effects()
    def __rmul__(self, n: int) -> Self: no_effects()
    def __mod__(self, args: Any) -> Self: no_effects()
    def __rmod__(self, template: object) -> Self: no_effects()
    def capitalize(self) -> Self: no_effects()
    def casefold(self) -> Self: no_effects()
    def center(self, width: int, *args: Any) -> Self: no_effects()
    def count(self, sub: str | UserString, start: int = 0, end: int = sys.maxsize) -> int: no_effects()
    def encode(self: UserString, encoding: str | None = "utf-8", errors: str | None = "strict") -> bytes: no_effects()
    def endswith(self, suffix: str | tuple[str, ...], start: int | None = 0, end: int | None = sys.maxsize) -> bool: no_effects()
    def expandtabs(self, tabsize: int = 8) -> Self: no_effects()
    def find(self, sub: str | UserString, start: int = 0, end: int = sys.maxsize) -> int: no_effects()
    def format(self, *args: Any, **kwds: Any) -> str: no_effects()
    def format_map(self, mapping: Mapping[str, Any]) -> str: no_effects()
    def index(self, sub: str, start: int = 0, end: int = sys.maxsize) -> int: no_effects()
    def isalpha(self) -> bool: no_effects()
    def isalnum(self) -> bool: no_effects()
    def isdecimal(self) -> bool: no_effects()
    def isdigit(self) -> bool: no_effects()
    def isidentifier(self) -> bool: no_effects()
    def islower(self) -> bool: no_effects()
    def isnumeric(self) -> bool: no_effects()
    def isprintable(self) -> bool: no_effects()
    def isspace(self) -> bool: no_effects()
    def istitle(self) -> bool: no_effects()
    def isupper(self) -> bool: no_effects()
    def isascii(self) -> bool: no_effects()
    def join(self, seq: Iterable[str]) -> str: dunder("__iter__")
    def ljust(self, width: int, *args: Any) -> Self: no_effects()
    def lower(self) -> Self: no_effects()
    def lstrip(self, chars: str | None = None) -> Self: no_effects()
    maketrans = str.maketrans
    def partition(self, sep: str) -> tuple[str, str, str]: no_effects()
    def removeprefix(self, prefix: str | UserString, /) -> Self: no_effects()
    def removesuffix(self, suffix: str | UserString, /) -> Self: no_effects()
    def replace(self, old: str | UserString, new: str | UserString, maxsplit: int = -1) -> Self: no_effects()
    def rfind(self, sub: str | UserString, start: int = 0, end: int = sys.maxsize) -> int: no_effects()
    def rindex(self, sub: str | UserString, start: int = 0, end: int = sys.maxsize) -> int: no_effects()
    def rjust(self, width: int, *args: Any) -> Self: no_effects()
    def rpartition(self, sep: str) -> tuple[str, str, str]: no_effects()
    def rstrip(self, chars: str | None = None) -> Self: no_effects()
    def split(self, sep: str | None = None, maxsplit: int = -1) -> list[str]: no_effects()
    def rsplit(self, sep: str | None = None, maxsplit: int = -1) -> list[str]: no_effects()
    def splitlines(self, keepends: bool = False) -> list[str]: no_effects()
    def startswith(self, prefix: str | tuple[str, ...], start: int | None = 0, end: int | None = sys.maxsize) -> bool: no_effects()
    def strip(self, chars: str | None = None) -> Self: no_effects()
    def swapcase(self) -> Self: no_effects()
    def title(self) -> Self: no_effects()
    def translate(self, *args: Any) -> Self: no_effects()
    def upper(self) -> Self: no_effects()
    def zfill(self, width: int) -> Self: no_effects()

@disjoint_base
class deque(MutableSequence[_T]):
    @property
    def maxlen(self) -> int | None: no_effects()
    @overload
    def __init__(self, *, maxlen: int | None = None) -> None: dunder("__iter__")
    @overload
    def __init__(self, iterable: Iterable[_T], maxlen: int | None = None) -> None: ...
    def append(self, x: _T, /) -> None: mutation()
    def appendleft(self, x: _T, /) -> None: mutation()
    def copy(self) -> Self: no_effects()
    def count(self, x: _T, /) -> int: no_effects()
    def extend(self, iterable: Iterable[_T], /) -> None:
        mutation()
        dunder("__iter__")
    def extendleft(self, iterable: Iterable[_T], /) -> None:
        mutation()
        dunder("__iter__")
    def insert(self, i: int, x: _T, /) -> None: mutation()
    def index(self, x: _T, start: int = 0, stop: int = ..., /) -> int: no_effects()
    def pop(self) -> _T: mutation()  # type: ignore[override]
    def popleft(self) -> _T: mutation()
    def remove(self, value: _T, /) -> None: mutation()
    def rotate(self, n: int = 1, /) -> None: mutation()
    def __copy__(self) -> Self: no_effects()
    def __len__(self) -> int: no_effects()
    __hash__: ClassVar[None]  # type: ignore[assignment]
    # These methods of deque don't take slices, unlike MutableSequence, hence the type: ignores
    def __getitem__(self, key: SupportsIndex, /) -> _T: no_effects()  # type: ignore[override]
    def __setitem__(self, key: SupportsIndex, value: _T, /) -> None: mutation()  # type: ignore[override]
    def __delitem__(self, key: SupportsIndex, /) -> None: mutation()  # type: ignore[override]
    def __contains__(self, key: object, /) -> bool: no_effects()
    def __reduce__(self) -> tuple[type[Self], tuple[()], None, Iterator[_T]]: no_effects()
    def __iadd__(self, value: Iterable[_T], /) -> Self:
        mutation()
        dunder("__iter__")
    def __add__(self, value: Self, /) -> Self: no_effects()
    def __mul__(self, value: int, /) -> Self: no_effects()
    def __imul__(self, value: int, /) -> Self: mutation()
    def __lt__(self, value: deque[_T], /) -> bool: no_effects()
    def __le__(self, value: deque[_T], /) -> bool: no_effects()
    def __gt__(self, value: deque[_T], /) -> bool: no_effects()
    def __ge__(self, value: deque[_T], /) -> bool: no_effects()
    def __eq__(self, value: object, /) -> bool: no_effects()
    def __class_getitem__(cls, item: Any, /) -> GenericAlias: no_effects()

class Counter(dict[_T, int], Generic[_T]):
    @overload
    def __init__(self, iterable: None = None, /) -> None: dunder("__iter__")
    @overload
    def __init__(self: Counter[str], iterable: None = None, /, **kwargs: int) -> None: ...
    @overload
    def __init__(self, mapping: SupportsKeysAndGetItem[_T, int], /) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[_T], /) -> None: ...
    def copy(self) -> Self: no_effects()
    def elements(self) -> Iterator[_T]: no_effects()
    def most_common(self, n: int | None = None) -> list[tuple[_T, int]]: no_effects()
    @classmethod
    def fromkeys(cls, iterable: Any, v: int | None = None) -> NoReturn: dunder("__iter__")  # type: ignore[override]
    @overload
    def subtract(self, iterable: None = None, /) -> None:
        mutation()
        dunder("__iter__")
    @overload
    def subtract(self, mapping: Mapping[_T, int], /) -> None: ...
    @overload
    def subtract(self, iterable: Iterable[_T], /) -> None: ...
    # Unlike dict.update(), use Mapping instead of SupportsKeysAndGetItem for the first overload
    # (source code does an `isinstance(other, Mapping)` check)
    #
    # The second overload is also deliberately different to dict.update()
    # (if it were `Iterable[_T] | Iterable[tuple[_T, int]]`,
    # the tuples would be added as keys, breaking type safety)
    @overload  # type: ignore[override]
    def update(self, m: Mapping[_T, int], /, **kwargs: int) -> None:
        mutation()
        dunder("__iter__")
    @overload
    def update(self, iterable: Iterable[_T], /, **kwargs: int) -> None: ...
    @overload
    def update(self, iterable: None = None, /, **kwargs: int) -> None: ...
    def __missing__(self, key: _T) -> int: no_effects()
    def __delitem__(self, elem: object) -> None: no_effects()
    if sys.version_info >= (3, 10):
        def __eq__(self, other: object) -> bool: no_effects()
        def __ne__(self, other: object) -> bool: no_effects()

    def __add__(self, other: Counter[_S]) -> Counter[_T | _S]: no_effects()
    def __sub__(self, other: Counter[_T]) -> Counter[_T]: no_effects()
    def __and__(self, other: Counter[_T]) -> Counter[_T]: no_effects()
    def __or__(self, other: Counter[_S]) -> Counter[_T | _S]: no_effects()  # type: ignore[override]
    def __pos__(self) -> Counter[_T]: no_effects()
    def __neg__(self) -> Counter[_T]: no_effects()
    # several type: ignores because __iadd__ is supposedly incompatible with __add__, etc.
    def __iadd__(self, other: SupportsItems[_T, int]) -> Self: mutation()  # type: ignore[misc]
    def __isub__(self, other: SupportsItems[_T, int]) -> Self: mutation()
    def __iand__(self, other: SupportsItems[_T, int]) -> Self: mutation()
    def __ior__(self, other: SupportsItems[_T, int]) -> Self: mutation()  # type: ignore[override,misc]
    if sys.version_info >= (3, 10):
        def total(self) -> int: no_effects()
        def __le__(self, other: Counter[Any]) -> bool: no_effects()
        def __lt__(self, other: Counter[Any]) -> bool: no_effects()
        def __ge__(self, other: Counter[Any]) -> bool: no_effects()
        def __gt__(self, other: Counter[Any]) -> bool: no_effects()

# The pure-Python implementations of the "views" classes
# These are exposed at runtime in `collections/__init__.py`
class _OrderedDictKeysView(KeysView[_KT_co]):
    def __reversed__(self) -> Iterator[_KT_co]: no_effects()

class _OrderedDictItemsView(ItemsView[_KT_co, _VT_co]):
    def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: no_effects()

class _OrderedDictValuesView(ValuesView[_VT_co]):
    def __reversed__(self) -> Iterator[_VT_co]: no_effects()

# The C implementations of the "views" classes
# (At runtime, these are called `odict_keys`, `odict_items` and `odict_values`,
# but they are not exposed anywhere)
# pyright doesn't have a specific error code for subclassing error!
@final
@type_check_only
class _odict_keys(dict_keys[_KT_co, _VT_co]):  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
    def __reversed__(self) -> Iterator[_KT_co]: no_effects()

@final
@type_check_only
class _odict_items(dict_items[_KT_co, _VT_co]):  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
    def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: no_effects()

@final
@type_check_only
class _odict_values(dict_values[_KT_co, _VT_co]):  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
    def __reversed__(self) -> Iterator[_VT_co]: no_effects()

@disjoint_base
class OrderedDict(dict[_KT, _VT]):
    def popitem(self, last: bool = True) -> tuple[_KT, _VT]: mutation()
    def move_to_end(self, key: _KT, last: bool = True) -> None: mutation()
    def copy(self) -> Self: mutation()
    def __reversed__(self) -> Iterator[_KT]: no_effects()
    def keys(self) -> _odict_keys[_KT, _VT]: no_effects()
    def items(self) -> _odict_items[_KT, _VT]: no_effects()
    def values(self) -> _odict_values[_KT, _VT]: no_effects()
    # The signature of OrderedDict.fromkeys should be kept in line with `dict.fromkeys`, modulo positional-only differences.
    # Like dict.fromkeys, its true signature is not expressible in the current type system.
    # See #3800 & https://github.com/python/typing/issues/548#issuecomment-683336963.
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: None = None) -> OrderedDict[_T, Any | None]: dunder("__iter__")
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S) -> OrderedDict[_T, _S]: ...
    # Keep OrderedDict.setdefault in line with MutableMapping.setdefault, modulo positional-only differences.
    @overload
    def setdefault(self: OrderedDict[_KT, _T | None], key: _KT, default: None = None) -> _T | None: mutation()
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    # Same as dict.pop, but accepts keyword arguments
    @overload
    def pop(self, key: _KT) -> _VT: mutation()
    @overload
    def pop(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T) -> _VT | _T: ...
    def __eq__(self, value: object, /) -> bool: no_effects()
    @overload
    def __or__(self, value: dict[_KT, _VT], /) -> Self: no_effects()
    @overload
    def __or__(self, value: dict[_T1, _T2], /) -> OrderedDict[_KT | _T1, _VT | _T2]: ...
    @overload
    def __ror__(self, value: dict[_KT, _VT], /) -> Self: no_effects()
    @overload
    def __ror__(self, value: dict[_T1, _T2], /) -> OrderedDict[_KT | _T1, _VT | _T2]: ...  # type: ignore[misc]

@disjoint_base
class defaultdict(dict[_KT, _VT]):
    default_factory: Callable[[], _VT] | None
    @overload
    def __init__(self) -> None: dunder("__iter__")
    @overload
    def __init__(self: defaultdict[str, _VT], **kwargs: _VT) -> None: ...  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    @overload
    def __init__(self, default_factory: Callable[[], _VT] | None, /) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        default_factory: Callable[[], _VT] | None,
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self, default_factory: Callable[[], _VT] | None, map: SupportsKeysAndGetItem[_KT, _VT], /) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        default_factory: Callable[[], _VT] | None,
        map: SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def __init__(self, default_factory: Callable[[], _VT] | None, iterable: Iterable[tuple[_KT, _VT]], /) -> None: ...
    @overload
    def __init__(
        self: defaultdict[str, _VT],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        default_factory: Callable[[], _VT] | None,
        iterable: Iterable[tuple[str, _VT]],
        /,
        **kwargs: _VT,
    ) -> None: ...
    def __missing__(self, key: _KT, /) -> _VT: no_effects()
    def __copy__(self) -> Self: no_effects()
    def copy(self) -> Self: no_effects()
    @overload
    def __or__(self, value: dict[_KT, _VT], /) -> Self: no_effects()
    @overload
    def __or__(self, value: dict[_T1, _T2], /) -> defaultdict[_KT | _T1, _VT | _T2]: ...
    @overload
    def __ror__(self, value: dict[_KT, _VT], /) -> Self: no_effects()
    @overload
    def __ror__(self, value: dict[_T1, _T2], /) -> defaultdict[_KT | _T1, _VT | _T2]: ...  # type: ignore[misc]

class ChainMap(MutableMapping[_KT, _VT]):
    maps: list[MutableMapping[_KT, _VT]]
    def __init__(self, *maps: MutableMapping[_KT, _VT]) -> None: no_effects()
    def new_child(self, m: MutableMapping[_KT, _VT] | None = None) -> Self: no_effects()
    @property
    def parents(self) -> Self: no_effects()
    def __setitem__(self, key: _KT, value: _VT) -> None: mutation()
    def __delitem__(self, key: _KT) -> None: mutation()
    def __getitem__(self, key: _KT) -> _VT: no_effects()
    def __iter__(self) -> Iterator[_KT]: no_effects()
    def __len__(self) -> int: no_effects()
    def __contains__(self, key: object) -> bool: no_effects()
    @overload
    def get(self, key: _KT, default: None = None) -> _VT | None: no_effects()
    @overload
    def get(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def get(self, key: _KT, default: _T) -> _VT | _T: ...
    def __missing__(self, key: _KT) -> _VT: no_effects()  # undocumented
    def __bool__(self) -> bool: no_effects()
    # Keep ChainMap.setdefault in line with MutableMapping.setdefault, modulo positional-only differences.
    @overload
    def setdefault(self: ChainMap[_KT, _T | None], key: _KT, default: None = None) -> _T | None: mutation()
    @overload
    def setdefault(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT) -> _VT: mutation()
    @overload
    def pop(self, key: _KT, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, default: _T) -> _VT | _T: ...
    def copy(self) -> Self: no_effects()
    __copy__ = copy
    # All arguments to `fromkeys` are passed to `dict.fromkeys` at runtime,
    # so the signature should be kept in line with `dict.fromkeys`.
    if sys.version_info >= (3, 13):
        @classmethod
        @overload
        def fromkeys(cls, iterable: Iterable[_T], /) -> ChainMap[_T, Any | None]: dunder("__iter__")
    else:
        @classmethod
        @overload
        def fromkeys(cls, iterable: Iterable[_T]) -> ChainMap[_T, Any | None]: dunder("__iter__")

    @classmethod
    @overload
    # Special-case None: the user probably wants to add non-None values later.
    def fromkeys(cls, iterable: Iterable[_T], value: None, /) -> ChainMap[_T, Any | None]: dunder("__iter__")
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_T], value: _S, /) -> ChainMap[_T, _S]: ...
    @overload
    def __or__(self, other: Mapping[_KT, _VT]) -> Self: no_effects()
    @overload
    def __or__(self, other: Mapping[_T1, _T2]) -> ChainMap[_KT | _T1, _VT | _T2]: ...
    @overload
    def __ror__(self, other: Mapping[_KT, _VT]) -> Self: no_effects()
    @overload
    def __ror__(self, other: Mapping[_T1, _T2]) -> ChainMap[_KT | _T1, _VT | _T2]: ...
    # ChainMap.__ior__ should be kept roughly in line with MutableMapping.update()
    @overload  # type: ignore[misc]
    def __ior__(self, other: SupportsKeysAndGetItem[_KT, _VT]) -> Self:
        mutation()
        dunder("__iter__")
    @overload
    def __ior__(self, other: Iterable[tuple[_KT, _VT]]) -> Self: ...
