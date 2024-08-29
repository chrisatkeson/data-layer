from abc import ABC, abstractmethod
from typing import Type

from data_layer.entity import Entity
from data_layer.filters import Filter


class Store(ABC):

    def __init__(self, entity: Type[Entity]):
        self.entity = entity

    @abstractmethod
    def get(self, key: str) -> Entity:
        pass

    @abstractmethod
    def create(self, entity: Entity, key: str):
        pass

    @abstractmethod
    def update(self, entity: Entity, key: str):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def read(self, filters: list[Filter]) -> list[Entity]:
        pass
