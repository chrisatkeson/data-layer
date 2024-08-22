from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class MetaData:
    es_field_name: str = None
    es_keyword_field: str = None


class EntityMeta(ABCMeta):
    def __getattribute__(cls, name):
        if name == '__dataclass_fields__':
            return super().__getattribute__(name)
        elif hasattr(cls, '__dataclass_fields__') and name in cls.__dataclass_fields__:
            return cls.__dataclass_fields__[name]
        return super().__getattribute__(name)


@dataclass
class Entity(ABC, metaclass=EntityMeta):

    @staticmethod
    def parse(field_type, value: any):
        if value is None:
            return None
        elif isinstance(value, field_type):
            return value
        elif field_type is datetime and isinstance(value, str):
            return datetime.fromisoformat(value)
        return field_type(value)

    def to_dict(self):
        """
        Convert the entity to a dict.
        """
        data = {}
        for field in fields(self):
            data[field.name] = getattr(self, field.name)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """
        Convert the data from a dict to an entity.
        """
        params = {}
        for field in fields(cls):
            field_value = data.get(field.name)
            params[field.name] = cls.parse(field_type=field.type, value=field_value)
        return cls(**params)

    def to_es(self) -> dict:
        """
        Convert the entity to a dict suitable for elasticsearch.
        """
        data = {}
        for field in fields(self):
            metadata = MetaData(**field.metadata)
            field_name = metadata.es_field_name or field.name
            data[field_name] = getattr(self, field.name)
        return data

    @classmethod
    def from_es(cls, data: dict) -> "Entity":
        """
        Convert the data from an elasticsearch hit to an entity.
        :param data: the source data from elasticsearch
        :return: an instance of the Entity class
        """
        params = {}
        for field in fields(cls):
            metadata = MetaData(**field.metadata)
            field_name = metadata.es_field_name or field.name
            field_value = data.get(field_name)
            params[field.name] = cls.parse(field_type=field.type, value=field_value)
        return cls(**params)
