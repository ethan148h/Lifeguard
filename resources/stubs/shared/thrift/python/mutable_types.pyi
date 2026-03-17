# Loosely based on fbcode/thrift/lib/python/mutable_types.pyi
# and fbcode/thrift/lib/python/mutable_types.pyx

import copy
import typing

from enum import IntEnum

from thrift.python.exceptions import Error
from thrift.python.mutable_typeinfos import FieldQualifier
from thrift.python.mutable_exceptions import MutableGeneratedError
from thrift.python.types import (
    AdaptedTypeInfo,
    TypeInfoBase,
)



class ThriftIdlType(IntEnum):
    Void = 0
    Bool = 1
    Byte = 2
    I16 = 3
    I32 = 4
    I64 = 5
    Float = 6
    Double = 7
    String = 8
    Binary = 9
    Enum = 10
    Struct = 11
    Union = 12
    Exception = 13
    List = 14
    Set = 15
    Map = 16


class _ThriftListWrapper:
    def __init__(self, list_data):
        self._list_data = list_data

def to_thrift_list(list_data):
    return _ThriftListWrapper(list_data)


class _ThriftSetWrapper:
    def __init__(self, set_data):
        self._set_data = set_data

def to_thrift_set(set_data):
    return _ThriftSetWrapper(set_data)


class _ThriftMapWrapper:
    def __init__(self, map_data):
        self._map_data = map_data

def to_thrift_map(map_data):
    return _ThriftMapWrapper(map_data)


class _ThriftContainerWrapper:
    def __init__(self, container_data):
        self._container_data = container_data


def fill_specs(*structured_thrift_classes):
    no_effects()

def _resetFieldToStandardDefault(structOrError, field_index):
    structOrError._fbthrift_reset_field_to_standard_default(field_index)


class _MutableStructField:
    __slots__ = ('_field_index', '_is_optional')

    def __init__(self, field_id, is_optional):
        self._field_index = field_id
        self._is_optional = is_optional

    def __get__(self, obj, objtype):
        if obj is None:
            return None

        return obj._fbthrift_get_field_value(self._field_index)

    def __set__(self, obj, value):
        if obj is None:
            return

        if value is None and self._is_optional:
            _resetFieldToStandardDefault(obj, self._field_index)
            return

        obj._fbthrift_set_field_value(self._field_index, value)


def is_cacheable_non_primitive(idl_type):
    return idl_type in (ThriftIdlType.String, ThriftIdlType.Struct)


def is_container(idl_type):
    return idl_type in (ThriftIdlType.List, ThriftIdlType.Set, ThriftIdlType.Map)


class _MutableStructCachedField:
    __slots__ = ('_field_index', '_is_optional')

    def __init__(self, field_id, is_optional):
        self._field_index = field_id
        self._is_optional = is_optional

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return obj._fbthrift_get_cached_field_value(self._field_index)

    def __set__(self, obj, value):
        if obj is None:
            return

        if value is None and self._is_optional:
            # reseting optional field to default is setting it to `None`
            _resetFieldToStandardDefault(obj, self._field_index)
            obj._fbthrift_field_cache[self._field_index] = None
            return

        obj._fbthrift_set_field_value(self._field_index, value)
        obj._fbthrift_field_cache[self._field_index] = None


def set_mutable_struct_field(struct_list, index, value):
    setMutableStructIsset(struct_list, index, True)
    struct_list[index + 1] = value


# Base class for mutable structs and mutable unions
class MutableStructOrUnion:
    def fbthrift_reset(self):
        raise NotImplementedError("Not implemented on base MutableStructOrUnion class")

    def _fbthrift_serialize(self, proto):
        raise NotImplementedError("Not implemented on base MutableStructOrUnion class")

    def _fbthrift_deserialize(self, buf, proto):
        raise NotImplementedError("Not implemented on base MutableStructOrUnion class")

    def _fbthrift_get_field_value(self, index):
        raise NotImplementedError("Not implemented on base MutableStructOrUnion class")


class MutableStructMeta(type):
    def _fbthrift_fill_spec(cls):
        pass

    def _fbthrift_store_field_values(cls):
        pass

    def __iter__(cls):
        while False:
            yield


class MutableStruct(MutableStructOrUnion, metaclass=MutableStructMeta):
    def fbthrift_reset(self):
        pass

    def _fbthrift_reset_struct_field_state(self, kwargs):
        pass

    def __call__(self, **kwargs):
        pass

    def _fbthrift_set_field_value(self, index, value):
        pass


class MutableStructInfo:
    def __init__(self, name, fields):
        pass

    def fill(self):
        pass

    def _initialize_default_values(self):
        pass


class _MutableUnionFieldDescriptor:
    def __init__(self, field_info):
        pass

    def __get__(self, union_instance, unused_union_class):
        pass

    def __set__(self, union_instance, field_python_value):
        pass


class MutableUnionMeta(type):
    def _fbthrift_fill_spec(cls):
        pass


class MutableUnion(MutableStructOrUnion, metaclass=MutableUnionMeta):
    def fbthrift_reset(self):
        pass

    def _fbthrift_set_mutable_union_value(self, field_id, field_python_value):
        pass

    def _fbthrift_convert_field_python_value_to_internal_data(
        self, field_id, field_python_value
    ):
        pass

    def _fbthrift_update_current_field_attributes(self):
        pass

    def _fbthrift_get_current_field_python_value(self, current_field_enum_value):
        pass

    def _fbthrift_get_field_value(self, field_id):
        pass


def _isset(struct):
    pass


class _fbthrift_MutableResponseStreamResult(MutableStruct):
    pass
