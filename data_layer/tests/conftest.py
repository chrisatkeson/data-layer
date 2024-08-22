from elasticsearch import Elasticsearch
from data_layer import ElasticStore, DictStore
from data_layer.tests.data import TestEntity, test_entities
import pytest

es_client = Elasticsearch(['http://localhost:9201'])


@pytest.fixture
def es_store():
    """Fixture that provides an ElasticStore object for the test entity."""
    return ElasticStore(entity=TestEntity, client=es_client, index="test_index")


@pytest.fixture
def dict_store():
    """Fixture that provides a DictStore object for the test entity."""
    return DictStore(entity=TestEntity)


def setup_test_entity():
    """Helper function to set up a test entity in Elasticsearch."""
    index = "test_index"
    es_client.indices.delete(index=index, ignore=[400, 404])
    mapping = {
        "mappings": {
            "properties": {
                "key": {"type": "keyword"},
                "count": {"type": "integer"},
                "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "@timestamp": {"type": "date"}
            }
        }
    }
    es_client.indices.create(index=index, body=mapping)


@pytest.fixture
def setup_teardown_test_entities(request, store):
    """Helper function to set up and tear down test entities in the store."""
    store_fixture_name = store
    store = request.getfixturevalue(store_fixture_name)
    for entity in test_entities:
        store.create(entity=entity, key=entity.key)
    yield store
    for entity in test_entities:
        store.delete(key=entity.key)


@pytest.fixture(scope="session", autouse=True)
def es_setup():
    """Fixture sets up elasticsearch for using the test entity."""
    setup_test_entity()
