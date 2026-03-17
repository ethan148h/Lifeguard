from contextlib import contextmanager
from typing import Any, Iterator, List, Optional, Tuple, Union

from nodeapi.py.cpp_ext.ligen.py_bindings.transaction_token import (
    TransactionToken as PyTransactionToken,
)

# These are the identifiers that we are currently importing in the current
# CythonWrappers.pyi file. Here, we're just Any'ing them out so that we can get *some*
# typechecking in the short term rather than Any'ing this entire module
PyQueryType = Any
_cShard = Any
ShardSuffix = Any
UShard = Any
Node = Any
schema = Any
PyChangesetRef = Any
PyEdgeMetadata = Any
PyFieldEdgeSetData = Any
PyMutationView = Any
debug_query = Any
entry_point = Any
explain_optimized_query = Any
explain_original_query = Any
explain_verbose_optimized_query = Any
explain_verbose_original_query = Any
explain_optimized_query_execution = Any
explain_verbose_optimized_query_execution = Any
explain_normalized_optimized_query_execution = Any
fci_variants_gateway = Any
PyNodeQLExpression = Any
NodeQLExpression = Any
NodeQLExpressionFactory = Any
slog_profile = Any
SchemaHub = Any
SchemaParser = Any
PyViewerContext = Any
evaluate_write_policy_ipp_validation = Any

class PyExtensionDependency:
    @staticmethod
    def initialize(
        pyQueryResult: object,
        pyChangesetResult: object,
        pyExceptionModule: object,
        pyCreateFuture: object,
        pyExecAsyncFunc: object,
        pyIndigoSaveStack: object,
        pyGetStackTrace: object,
    ) -> None: no_effects()
    @staticmethod
    def get_node_schema(projectId: int, schemaId: int) -> schema.NodeSchema: ...
    @staticmethod
    def get_edge_schema(projectId: int, schemaId: int) -> schema.EdgeSchema: ...
    @staticmethod
    def get_pattern_schema(projectId: int, schemaId: int) -> schema.PatternSchema: ...
    @staticmethod
    def get_abstract_edge_schema(
        projectId: int, patternId: int, abstractEdgeName: bytes, idx: int = ...
    ) -> schema.AbstractEdgeSchema: ...
    @staticmethod
    def set_all_schemas(
        projectId: int,
        projectSchema: bytes,
        patternSchemas: List[Tuple[int, bytes]],
        nodeSchemas: List[Tuple[int, bytes]],
        edgeSchemas: List[Tuple[int, bytes]],
        indexSchemas: List[Tuple[int, bytes]],
    ) -> None: ...

class NodeQLCursor:
    @staticmethod
    def create_start() -> "NodeQLCursor": ...
    @staticmethod
    def create_end() -> "NodeQLCursor": ...
    @staticmethod
    def loads_permissive(
        serial: Optional[Union[str, "NodeQLCursor"]],
    ) -> Optional["NodeQLCursor"]: ...
    def is_forward_finished(self) -> bool: ...
    def is_backward_finished(self) -> bool: ...
    @staticmethod
    def loads(serial: str) -> "NodeQLCursor": ...
    def dumps(self) -> str: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def create_next_DONOTUSE(time: int, id2: int) -> "NodeQLCursor": ...
    def get_time_DONOTUSE(self) -> int: ...
    def get_id2_DONOTUSE(self) -> int: ...

class PyShard(_cShard):
    def __init__(self, schema: schema.NodeSchema, shard_input: object) -> None: ...

class NodeAPIUserNotes:
    @classmethod
    @contextmanager
    def shallow_copy_guard_DO_NOT_USE(
        cls, notes: List[Tuple[bytes, bytes]]
    ) -> Iterator[None]: ...
    @classmethod
    def get(cls, key: bytes) -> Optional[str]: ...

class NodeAPITaoHashoutRingOverride:
    @classmethod
    @contextmanager
    def shallow_copy_guard_DO_NOT_USE(cls, ring: int) -> Iterator[None]: ...
    @classmethod
    def get(cls) -> Optional[int]: ...
