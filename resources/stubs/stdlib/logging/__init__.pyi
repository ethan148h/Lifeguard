import sys
import threading
from _typeshed import StrPath, SupportsWrite
from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from io import TextIOWrapper
from re import Pattern
from string import Template
from time import struct_time
from types import FrameType, GenericAlias, TracebackType
from typing import Any, ClassVar, Final, Generic, Literal, Protocol, TextIO, TypeVar, overload, type_check_only
from typing_extensions import Self, TypeAlias, deprecated

__all__ = [
    "BASIC_FORMAT",
    "BufferingFormatter",
    "CRITICAL",
    "DEBUG",
    "ERROR",
    "FATAL",
    "FileHandler",
    "Filter",
    "Formatter",
    "Handler",
    "INFO",
    "LogRecord",
    "Logger",
    "LoggerAdapter",
    "NOTSET",
    "NullHandler",
    "StreamHandler",
    "WARN",
    "WARNING",
    "addLevelName",
    "basicConfig",
    "captureWarnings",
    "critical",
    "debug",
    "disable",
    "error",
    "exception",
    "fatal",
    "getLevelName",
    "getLogger",
    "getLoggerClass",
    "info",
    "log",
    "makeLogRecord",
    "setLoggerClass",
    "shutdown",
    "warning",
    "getLogRecordFactory",
    "setLogRecordFactory",
    "lastResort",
    "raiseExceptions",
    "warn",
]

if sys.version_info >= (3, 11):
    __all__ += ["getLevelNamesMapping"]
if sys.version_info >= (3, 12):
    __all__ += ["getHandlerByName", "getHandlerNames"]

_SysExcInfoType: TypeAlias = tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
_ExcInfoType: TypeAlias = None | bool | _SysExcInfoType | BaseException
_ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]
_Level: TypeAlias = int | str
_FormatStyle: TypeAlias = Literal["%", "{", "$"]

if sys.version_info >= (3, 12):
    @type_check_only
    class _SupportsFilter(Protocol):
        def filter(self, record: LogRecord, /) -> bool | LogRecord:
            no_effects()

    _FilterType: TypeAlias = Filter | Callable[[LogRecord], bool | LogRecord] | _SupportsFilter
else:
    @type_check_only
    class _SupportsFilter(Protocol):
        def filter(self, record: LogRecord, /) -> bool:
            no_effects()

    _FilterType: TypeAlias = Filter | Callable[[LogRecord], bool] | _SupportsFilter

raiseExceptions: bool
logThreads: bool
logMultiprocessing: bool
logProcesses: bool
_srcfile: str | None

def currentframe() -> FrameType:
    no_effects()

_levelToName: dict[int, str]
_nameToLevel: dict[str, int]

class Filterer:
    filters: list[_FilterType]
    def addFilter(self, filter: _FilterType) -> None:
        no_effects()
    def removeFilter(self, filter: _FilterType) -> None:
        no_effects()
    if sys.version_info >= (3, 12):
        def filter(self, record: LogRecord) -> bool | LogRecord:
            no_effects()
    else:
        def filter(self, record: LogRecord) -> bool:
            no_effects()

class Manager:  # undocumented
    root: RootLogger
    disable: int
    emittedNoHandlerWarning: bool
    loggerDict: dict[str, Logger | PlaceHolder]
    loggerClass: type[Logger] | None
    logRecordFactory: Callable[..., LogRecord] | None
    def __init__(self, rootnode: RootLogger) -> None:
        no_effects()

    def getLogger(self, name: str) -> Logger:
        no_effects()

    def setLoggerClass(self, klass: type[Logger]) -> None:
        no_effects()

    def setLogRecordFactory(self, factory: Callable[..., LogRecord]) -> None:
        no_effects()

class Logger(Filterer):
    name: str  # undocumented
    level: int  # undocumented
    parent: Logger | None  # undocumented
    propagate: bool
    handlers: list[Handler]  # undocumented
    disabled: bool  # undocumented
    root: ClassVar[RootLogger]  # undocumented
    manager: Manager  # undocumented
    def __init__(self, name: str, level: _Level = 0) -> None:
        no_effects()
    def setLevel(self, level: _Level) -> None:
        no_effects()
    def isEnabledFor(self, level: int) -> bool:
        no_effects()
    def getEffectiveLevel(self) -> int:
        no_effects()
    def getChild(self, suffix: str) -> Self:  # see python/typing#980
        no_effects()
    if sys.version_info >= (3, 12):
        def getChildren(self) -> set[Logger]:
            no_effects()

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def info(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def warning(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    @deprecated("Deprecated since Python 3.3. Use `Logger.warning()` instead.")
    def warn(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def error(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def exception(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = True,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def critical(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        no_effects()
    def _log(
        self,
        level: int,
        msg: object,
        args: _ArgsType,
        exc_info: _ExcInfoType | None = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:  # undocumented
        no_effects()
    fatal = critical
    def addHandler(self, hdlr: Handler) -> None:
        no_effects()

    def removeHandler(self, hdlr: Handler) -> None: ...
    def findCaller(self, stack_info: bool = False, stacklevel: int = 1) -> tuple[str, int, str, str | None]: ...
    def handle(self, record: LogRecord) -> None: ...
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: _ArgsType,
        exc_info: _SysExcInfoType | None,
        func: str | None = None,
        extra: Mapping[str, object] | None = None,
        sinfo: str | None = None,
    ) -> LogRecord: ...
    def hasHandlers(self) -> bool:
        no_effects()
    def callHandlers(self, record: LogRecord) -> None: ...  # undocumented

CRITICAL: Final = 50
FATAL: Final = CRITICAL
ERROR: Final = 40
WARNING: Final = 30
WARN: Final = WARNING
INFO: Final = 20
DEBUG: Final = 10
NOTSET: Final = 0

class Handler(Filterer):
    level: int  # undocumented
    formatter: Formatter | None  # undocumented
    lock: threading.Lock | None  # undocumented
    name: str | None  # undocumented
    def __init__(self, level: _Level = 0) -> None: ...
    def get_name(self) -> str: ...  # undocumented
    def set_name(self, name: str) -> None: ...  # undocumented
    def createLock(self) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def setLevel(self, level: _Level) -> None: 
        no_effects()

    def setFormatter(self, fmt: Formatter | None) -> None: 
        no_effects()

    def flush(self) -> None: ...
    def close(self) -> None: ...
    def handle(self, record: LogRecord) -> bool: ...
    def handleError(self, record: LogRecord) -> None: ...
    def format(self, record: LogRecord) -> str: ...
    def emit(self, record: LogRecord) -> None: ...

if sys.version_info >= (3, 12):
    def getHandlerByName(name: str) -> Handler | None:
        no_effects()
    def getHandlerNames() -> frozenset[str]:
        no_effects()

class Formatter:
    converter: Callable[[float | None], struct_time]
    _fmt: str | None  # undocumented
    datefmt: str | None  # undocumented
    _style: PercentStyle  # undocumented
    default_time_format: str
    default_msec_format: str | None

    if sys.version_info >= (3, 10):
        def __init__(
            self,
            fmt: str | None = None,
            datefmt: str | None = None,
            style: _FormatStyle = "%",
            validate: bool = True,
            *,
            defaults: Mapping[str, Any] | None = None,
        ) -> None: 
            no_effects()
    else:
        def __init__(
            self, fmt: str | None = None, datefmt: str | None = None, style: _FormatStyle = "%", validate: bool = True
        ) -> None: 
            no_effects()

    def format(self, record: LogRecord) -> str:
        no_effects()
    def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
        no_effects()
    def formatException(self, ei: _SysExcInfoType) -> str:
        no_effects()
    def formatMessage(self, record: LogRecord) -> str:  # undocumented
        no_effects()
    def formatStack(self, stack_info: str) -> str:
        no_effects()
    def usesTime(self) -> bool:  # undocumented
        no_effects()

class BufferingFormatter:
    linefmt: Formatter
    def __init__(self, linefmt: Formatter | None = None) -> None: ...
    def formatHeader(self, records: Sequence[LogRecord]) -> str: ...
    def formatFooter(self, records: Sequence[LogRecord]) -> str: ...
    def format(self, records: Sequence[LogRecord]) -> str: ...

class Filter:
    name: str  # undocumented
    nlen: int  # undocumented
    def __init__(self, name: str = "") -> None: ...
    if sys.version_info >= (3, 12):
        def filter(self, record: LogRecord) -> bool | LogRecord:
            no_effects()
    else:
        def filter(self, record: LogRecord) -> bool:
            no_effects()

class LogRecord:
    # args can be set to None by logging.handlers.QueueHandler
    # (see https://bugs.python.org/issue44473)
    args: _ArgsType | None
    asctime: str
    created: float
    exc_info: _SysExcInfoType | None
    exc_text: str | None
    filename: str
    funcName: str
    levelname: str
    levelno: int
    lineno: int
    module: str
    msecs: float
    # Only created when logging.Formatter.format is called. See #6132.
    message: str
    msg: str | Any  # The runtime accepts any object, but will be a str in 99% of cases
    name: str
    pathname: str
    process: int | None
    processName: str | None
    relativeCreated: float
    stack_info: str | None
    thread: int | None
    threadName: str | None
    if sys.version_info >= (3, 12):
        taskName: str | None

    def __init__(
        self,
        name: str,
        level: int,
        pathname: str,
        lineno: int,
        msg: object,
        args: _ArgsType | None,
        exc_info: _SysExcInfoType | None,
        func: str | None = None,
        sinfo: str | None = None,
    ) -> None:
        no_effects()

    def getMessage(self) -> str:
        no_effects()

    # Allows setting contextual information on LogRecord objects as per the docs, see #7833
    def __setattr__(self, name: str, value: Any, /) -> None:
        no_effects()


_L = TypeVar("_L", bound=Logger | LoggerAdapter[Any])

class LoggerAdapter(Generic[_L]):
    logger: _L
    manager: Manager  # undocumented

    if sys.version_info >= (3, 13):
        def __init__(self, logger: _L, extra: Mapping[str, object] | None = None, merge_extra: bool = False) -> None:
            no_effects()
    elif sys.version_info >= (3, 10):
        def __init__(self, logger: _L, extra: Mapping[str, object] | None = None) -> None:
            no_effects()
    else:
        def __init__(self, logger: _L, extra: Mapping[str, object]) -> None:
            no_effects()

    if sys.version_info >= (3, 10):
        extra: Mapping[str, object] | None
    else:
        extra: Mapping[str, object]

    if sys.version_info >= (3, 13):
        merge_extra: bool

    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> tuple[Any, MutableMapping[str, Any]]: 
        no_effects()
    def debug(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        no_effects()
    def info(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        no_effects()
    def warning(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None: 
        no_effects()
    @deprecated("Deprecated since Python 3.3. Use `LoggerAdapter.warning()` instead.")
    def warn(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None: 
        no_effects()
    def error(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None: 
        no_effects()
    def exception(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = True,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        no_effects()
    def critical(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None: 
        no_effects()
    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
        **kwargs: object,
    ) -> None:
        no_effects()
    def isEnabledFor(self, level: int) -> bool:
        no_effects()
    def getEffectiveLevel(self) -> int:
        no_effects()
    def setLevel(self, level: _Level) -> None:
        no_effects()
    def hasHandlers(self) -> bool: 
        no_effects()
    if sys.version_info >= (3, 11):
        def _log(
            self,
            level: int,
            msg: object,
            args: _ArgsType,
            *,
            exc_info: _ExcInfoType | None = None,
            extra: Mapping[str, object] | None = None,
            stack_info: bool = False,
        ) -> None:  # undocumented
            no_effects()
    else:
        def _log(
            self,
            level: int,
            msg: object,
            args: _ArgsType,
            exc_info: _ExcInfoType | None = None,
            extra: Mapping[str, object] | None = None,
            stack_info: bool = False,
        ) -> None:  # undocumented
            no_effects()

    @property
    def name(self) -> str:  # undocumented
        no_effects()
    if sys.version_info >= (3, 11):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

def getLogger(name: str | None = None) -> Logger: 
    no_effects()

def getLoggerClass() -> type[Logger]: 
    no_effects()

def getLogRecordFactory() -> Callable[..., LogRecord]:
    no_effects()

def debug(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def info(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def warning(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
@deprecated("Deprecated since Python 3.3. Use `warning()` instead.")
def warn(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def error(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def critical(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def exception(
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = True,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()
def log(
    level: int,
    msg: object,
    *args: object,
    exc_info: _ExcInfoType = None,
    stack_info: bool = False,
    stacklevel: int = 1,
    extra: Mapping[str, object] | None = None,
) -> None:
    no_effects()

fatal = critical

def disable(level: int = 50) -> None: 
    no_effects()
def addLevelName(level: int, levelName: str) -> None:
    no_effects()
@overload
def getLevelName(level: int) -> str: no_effects()
@overload
@deprecated("The str -> int case is considered a mistake.")
def getLevelName(level: str) -> Any: ...

if sys.version_info >= (3, 11):
    def getLevelNamesMapping() -> dict[str, int]:
        no_effects()

def makeLogRecord(dict: Mapping[str, object]) -> LogRecord:
    no_effects()
def basicConfig(
    *,
    filename: StrPath | None = ...,
    filemode: str = ...,
    format: str = ...,
    datefmt: str | None = ...,
    style: _FormatStyle = ...,
    level: _Level | None = ...,
    stream: SupportsWrite[str] | None = ...,
    handlers: Iterable[Handler] | None = ...,
    force: bool | None = ...,
    encoding: str | None = ...,
    errors: str | None = ...,
) -> None:
    no_effects()
def shutdown(handlerList: Sequence[Any] = ...) -> None:  # handlerList is undocumented
    no_effects()
def setLoggerClass(klass: type[Logger]) -> None: 
    no_effects()
def captureWarnings(capture: bool) -> None: 
    no_effects()
def setLogRecordFactory(factory: Callable[..., LogRecord]) -> None: 
    no_effects()

lastResort: Handler | None

_StreamT = TypeVar("_StreamT", bound=SupportsWrite[str])

class StreamHandler(Handler, Generic[_StreamT]):
    stream: _StreamT  # undocumented
    terminator: str
    @overload
    def __init__(self: StreamHandler[TextIO], stream: None = None) -> None: no_effects()
    @overload
    def __init__(self: StreamHandler[_StreamT], stream: _StreamT) -> None: ...  # pyright: ignore[reportInvalidTypeVarUse]  #11780
    def setStream(self, stream: _StreamT) -> _StreamT | None: 
        no_effects()
    if sys.version_info >= (3, 11):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias: ...

class FileHandler(StreamHandler[TextIOWrapper]):
    baseFilename: str  # undocumented
    mode: str  # undocumented
    encoding: str | None  # undocumented
    delay: bool  # undocumented
    errors: str | None  # undocumented
    def __init__(
        self, filename: StrPath, mode: str = "a", encoding: str | None = None, delay: bool = False, errors: str | None = None
    ) -> None:
        no_effects()
    def _open(self) -> TextIOWrapper:  # undocumented
        no_effects()

class NullHandler(Handler):
    no_effects()

class PlaceHolder:  # undocumented
    loggerMap: dict[Logger, None]
    def __init__(self, alogger: Logger) -> None:
        no_effects()
    def append(self, alogger: Logger) -> None: 
        no_effects()

# Below aren't in module docs but still visible

class RootLogger(Logger):
    def __init__(self, level: int) -> None:
        no_effects()

root: RootLogger

class PercentStyle:  # undocumented
    default_format: str
    asctime_format: str
    asctime_search: str
    validation_pattern: Pattern[str]
    _fmt: str
    if sys.version_info >= (3, 10):
        def __init__(self, fmt: str, *, defaults: Mapping[str, Any] | None = None) -> None: ...
    else:
        def __init__(self, fmt: str) -> None: ...

    def usesTime(self) -> bool: ...
    def validate(self) -> None: ...
    def format(self, record: Any) -> str: ...

class StrFormatStyle(PercentStyle):  # undocumented
    fmt_spec: Pattern[str]
    field_spec: Pattern[str]

class StringTemplateStyle(PercentStyle):  # undocumented
    _tpl: Template

_STYLES: Final[dict[str, tuple[PercentStyle, str]]]

BASIC_FORMAT: Final = "%(levelname)s:%(name)s:%(message)s"
