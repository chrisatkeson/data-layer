from abc import ABC, abstractmethod
from dataclasses import Field

from data_layer.entity import Entity, MetaData
from data_layer.operator import Operator


class Filter(ABC):
    def __init__(self, field, operator: Operator, value: any):
        self.field = field
        self.operator = operator
        self.value = value

        if field and not isinstance(field, Field):
            raise Exception("field must be a dataclass Field.")

    @abstractmethod
    def evaluate(self, entity: Entity) -> bool:
        pass

    @abstractmethod
    def to_elasticsearch(self):
        pass

    @property
    def field_metadata(self):
        if self.field:
            return MetaData(**self.field.metadata)
        return None
