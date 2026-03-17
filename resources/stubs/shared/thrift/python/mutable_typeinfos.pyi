from enum import IntEnum

from thrift.python.types import TypeInfoBase

class FieldQualifier(IntEnum):
    Unqualified = 1
    Optional = 2
    Terse = 3


class MutableStructTypeInfo(TypeInfoBase):
    def __init__(self, mutable_struct_class):
        no_effects()

    def to_internal_data(self, value):
        no_effects()

    def to_python_value(self, struct_list):
        no_effects()

    def to_container_value(self, value):
        no_effects()

    def same_as(self, other):
        no_effects()

class MutableListTypeInfo:
    no_effects()

class MutableMapTypeInfo:
    no_effects()

class MutableSetTypeInfo:
    no_effects()
