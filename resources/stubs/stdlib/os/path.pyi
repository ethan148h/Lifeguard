# lifeguard: This is a copy of posixpath.pyi, not os/path.pyi, since the
# latter uses `from posixpath import *` which we do not handle yet.

import sys
from _typeshed import AnyOrLiteralStr, BytesPath, FileDescriptorOrPath, StrOrBytesPath, StrPath
from collections.abc import Iterable
from genericpath import (
    ALLOW_MISSING as ALLOW_MISSING,
    _AllowMissingType,
    commonprefix as commonprefix,
    exists as exists,
    getatime as getatime,
    getctime as getctime,
    getmtime as getmtime,
    getsize as getsize,
    isdir as isdir,
    isfile as isfile,
    samefile as samefile,
    sameopenfile as sameopenfile,
    samestat as samestat,
)

if sys.version_info >= (3, 13):
    from genericpath import isdevdrive as isdevdrive
from os import PathLike
from typing import AnyStr, overload
from typing_extensions import LiteralString

__all__ = [
    "normcase",
    "isabs",
    "join",
    "splitdrive",
    "split",
    "splitext",
    "basename",
    "dirname",
    "commonprefix",
    "getsize",
    "getmtime",
    "getatime",
    "getctime",
    "islink",
    "exists",
    "lexists",
    "isdir",
    "isfile",
    "ismount",
    "expanduser",
    "expandvars",
    "normpath",
    "abspath",
    "samefile",
    "sameopenfile",
    "samestat",
    "curdir",
    "pardir",
    "sep",
    "pathsep",
    "defpath",
    "altsep",
    "extsep",
    "devnull",
    "realpath",
    "supports_unicode_filenames",
    "relpath",
    "commonpath",
]
__all__ += ["ALLOW_MISSING"]
if sys.version_info >= (3, 12):
    __all__ += ["isjunction", "splitroot"]
if sys.version_info >= (3, 13):
    __all__ += ["isdevdrive"]

supports_unicode_filenames: bool
# aliases (also in os)
curdir: LiteralString
pardir: LiteralString
sep: LiteralString
altsep: LiteralString | None
extsep: LiteralString
pathsep: LiteralString
defpath: LiteralString
devnull: LiteralString

# Overloads are necessary to work around python/mypy#17952 & python/mypy#11880
@overload
def abspath(path: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def abspath(path: AnyStr) -> AnyStr: ...
@overload
def basename(p: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def basename(p: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def dirname(p: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def dirname(p: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def expanduser(path: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def expanduser(path: AnyStr) -> AnyStr: ...
@overload
def expandvars(path: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def expandvars(path: AnyStr) -> AnyStr: ...
@overload
def normcase(s: PathLike[AnyStr]) -> AnyStr: no_effects()
@overload
def normcase(s: AnyOrLiteralStr) -> AnyOrLiteralStr: ...
@overload
def normpath(path: PathLike[AnyStr]) -> AnyStr:
    """Normalize path, eliminating double slashes, etc."""
    no_effects()
@overload
def normpath(path: AnyOrLiteralStr) -> AnyOrLiteralStr:
    """Normalize path, eliminating double slashes, etc."""
    ...
@overload
def commonpath(paths: Iterable[LiteralString]) -> LiteralString: no_effects()
@overload
def commonpath(paths: Iterable[StrPath]) -> str: ...
@overload
def commonpath(paths: Iterable[BytesPath]) -> bytes: ...

# First parameter is not actually pos-only,
# but must be defined as pos-only in the stub or cross-platform code doesn't type-check,
# as the parameter name is different in ntpath.join()
@overload
def join(a: LiteralString, /, *paths: LiteralString) -> LiteralString: no_effects()
@overload
def join(a: StrPath, /, *paths: StrPath) -> str: ...
@overload
def join(a: BytesPath, /, *paths: BytesPath) -> bytes: ...
@overload
def realpath(filename: PathLike[AnyStr], *, strict: bool | _AllowMissingType = False) -> AnyStr: no_effects()
@overload
def realpath(filename: AnyStr, *, strict: bool | _AllowMissingType = False) -> AnyStr: ...
@overload
def relpath(path: LiteralString, start: LiteralString | None = None) -> LiteralString: no_effects()
@overload
def relpath(path: BytesPath, start: BytesPath | None = None) -> bytes: ...
@overload
def relpath(path: StrPath, start: StrPath | None = None) -> str: ...
@overload
def split(p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: no_effects()
@overload
def split(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
@overload
def splitdrive(p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: no_effects()
@overload
def splitdrive(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
@overload
def splitext(p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr]: no_effects()
@overload
def splitext(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr]: ...
def isabs(s: StrOrBytesPath) -> bool: no_effects()
def islink(path: FileDescriptorOrPath) -> bool: no_effects()
def ismount(path: FileDescriptorOrPath) -> bool: no_effects()
def lexists(path: FileDescriptorOrPath) -> bool: no_effects()

if sys.version_info >= (3, 12):
    def isjunction(path: StrOrBytesPath) -> bool: no_effects()
    @overload
    def splitroot(p: AnyOrLiteralStr) -> tuple[AnyOrLiteralStr, AnyOrLiteralStr, AnyOrLiteralStr]: no_effects()
    @overload
    def splitroot(p: PathLike[AnyStr]) -> tuple[AnyStr, AnyStr, AnyStr]: no_effects()
