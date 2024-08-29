from typing import Type

from data_layer.entity import Entity
from data_layer.exceptions import EntityNotFoundError
from data_layer.filters import Filter
from data_layer.stores.store import Store


class DictStore(Store):

    def __init__(self, entity: Type[Entity]):
        super().__init__(entity)
        self.data = {}

    def get(self, key: str) -> Entity:
        try:
            return self.data[key]
        except KeyError:
            raise EntityNotFoundError.for_key(key=key)

    def create(self, entity: Entity, key: str):
        self.data[key] = entity

    def update(self, entity: Entity, key: str):
        self.data[key] = entity

    def delete(self, key: str):
        del self.data[key]

    def read(self, filters: list[Filter]) -> list[Entity]:
        return [entity for entity in self.data.values() if all([f.evaluate(entity) for f in filters])]
