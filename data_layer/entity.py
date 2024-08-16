from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass


class EntityMeta(ABCMeta):
    def __getattribute__(cls, name):
        if name == '__dataclass_fields__':
            return super().__getattribute__(name)
        elif hasattr(cls, '__dataclass_fields__') and name in cls.__dataclass_fields__:
            return cls.__dataclass_fields__[name]
        return super().__getattribute__(name)


@dataclass
class Entity(ABC, metaclass=EntityMeta):

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "Entity":
        pass

    @abstractmethod
    def to_dict(self):
        pass
