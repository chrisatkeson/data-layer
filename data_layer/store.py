from abc import ABC, abstractmethod
from data_layer.filter import Filter
from data_layer.entity import Entity
from elasticsearch import Elasticsearch, NotFoundError
from data_layer.exceptions import EntityNotFoundError
from typing import Type


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


class ElasticStore(Store):
    def __init__(self, entity: Type[Entity], client: Elasticsearch, index: str):
        super().__init__(entity=entity)
        self.client = client
        self.index = index

    def get(self, key: str) -> Entity:
        try:
            doc = self.client.get(index=self.index, id=key)
        except NotFoundError:
            raise EntityNotFoundError.for_key(key=key)
        return self.entity.from_es(data=doc['_source'])

    def create(self, entity: Entity, key: str):
        self.client.index(index=self.index, id=key, body=entity.to_es(), refresh=True)

    def update(self, entity: Entity, key: str):
        self.client.index(index=self.index, id=key, body=entity.to_es(), refresh=True)

    def delete(self, key: str):
        self.client.delete(index=self.index, id=key, refresh=True)

    def read(self, filters: list[Filter]) -> list[Entity]:
        es_query = {
            "query": {
                "bool": {
                    "filter": [f.to_elasticsearch() for f in filters]
                }
            }
        }
        results = self.client.search(index=self.index, body=es_query)
        hits = results['hits']['hits']
        return [self.entity.from_dict(data=hit['_source']) for hit in hits]
