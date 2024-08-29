from typing import Type

from elasticsearch import Elasticsearch, NotFoundError

from data_layer.entity import Entity
from data_layer.exceptions import EntityNotFoundError
from data_layer.filters import Filter
from data_layer.stores.store import Store


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
