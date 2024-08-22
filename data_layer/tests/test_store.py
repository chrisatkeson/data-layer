import pytest

from data_layer.exceptions import EntityNotFoundError
from data_layer.tests.data import TestEntity


@pytest.mark.parametrize("store", ['dict_store', 'es_store'])
def test_crud(store, request):
    """
    Test create, get, update, read, and delete operations.
    """
    store = request.getfixturevalue(store)
    entity = TestEntity(key="1", count=1)
    store.create(entity=entity, key="1")
    assert store.get(key="1") == entity

    entity.count = 2
    store.update(entity=entity, key="1")
    assert store.get(key="1") == entity

    assert store.read(filters=[]) == [entity]

    store.delete(key="1")
    with pytest.raises(EntityNotFoundError):
        store.get(key="1")




