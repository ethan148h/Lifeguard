# stub for thrift.lib.python.types.pyx

import enum


class FieldQualifier(enum.Enum):
    Unqualified: FieldQualifier = ...
    Optional: FieldQualifier = ...
    Terse: FieldQualifier = ...


class StructMeta(type):
    @staticmethod
    def isset(struct):
        return struct.__fbthrift_isset()


class UnionMeta(type):
    no_effects()


class TypeInfoBase:
    no_effects()


class EnumTypeInfo(TypeInfoBase):
    no_effects()


class StructTypeInfo(TypeInfoBase):
    no_effects()


class AdaptedTypeInfo(TypeInfoBase):
    no_effects()


class StructOrUnion:
    no_effects()


class Container:
    no_effects()


class List(Container):
    no_effects()
    def __init__(self, val_info, values):
        no_effects()


class Set(Container):
    no_effects()
    def __init__(self, val_info, values):
        no_effects()


class Map(Container):
    def __init__(self, key_info, val_info, values):
        no_effects()


class Struct:
    """
    Base class for all thrift structs
    """

    def __fbthrift_isset(self):
        raise TypeError(f"{type(self)} does not have concept of isset")

    def _fbthrift_fill_spec(self):
        self._fbthrift_spec = [
            (field.id, field.qualifier, field.name, field.py_name, field.type_info, field.default_value, field.adapter_info, field.is_primitive, field.idl_type)
            for field in self.__thrift_struct__.fields
        ]


class FieldInfo:
    no_effects()
    def __init__(self, id, qualifier, name, py_name, type_info, default_value, adapter_info, is_primitive, idl_type = -1):
        no_effects()


def fill_specs(*specs):
    no_effects()


class SetTypeFactory:
    no_effects()

class MapTypeInfo:
    no_effects()

class MapTypeFactory:
    no_effects()


class ListTypeInfo(TypeInfoBase):
    no_effects()

class SetTypeInfo:
    no_effects()

class ListTypeFactory:
    no_effects()
