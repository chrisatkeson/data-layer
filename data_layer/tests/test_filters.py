import pytest

from data_layer.tests.data import TestEntity
from data_layer import (IsFilter, IsNotFilter, GreaterThanFilter, LessThanFilter, ExistsFilter, DoesNotExistFilter,
                        OrFilter, Filter, IsOneOfFilter, IsNotOneOfFilter)
from data_layer import FilterFactory
from datetime import datetime


@pytest.mark.parametrize("store", ['dict_store', 'es_store'])
@pytest.mark.parametrize("filters, keys", [
    ([], {"1", "2", "3", "4", "5"}),
    ([IsFilter(field=TestEntity.count, value=2)], {"2", "3"}),
    ([IsNotFilter(field=TestEntity.count, value=2)], {"1", "4", "5"}),
    ([IsOneOfFilter(field=TestEntity.count, value=[1, 4])], {"1", "4"}),
    ([IsNotOneOfFilter(field=TestEntity.count, value=[1, 4])], {"2", "3", "5"}),
    ([GreaterThanFilter(field=TestEntity.count, value=3)], {"4", "5"}),
    ([GreaterThanFilter(field=TestEntity.timestamp, value=datetime(year=2024, day=1, month=1))], {"4", "5"}),
    ([LessThanFilter(field=TestEntity.count, value=3)], {"1", "2", "3"}),
    ([ExistsFilter(field=TestEntity.name)], {"1", "2", "3", "4", "5"}),
    ([DoesNotExistFilter(field=TestEntity.name)], set()),
    ([OrFilter(filters=[IsFilter(field=TestEntity.count, value=1),
                        IsFilter(field=TestEntity.count, value=4)])], {"1", "4"}),
])
def test_filters(setup_teardown_test_entities, store: str, filters: list[Filter], keys: set):
    """
    Test the IsFilter class.
    """
    store = setup_teardown_test_entities
    results = store.read(filters=filters)
    assert {entity.key for entity in results} == keys


@pytest.mark.parametrize("store", ['es_store'])
@pytest.mark.parametrize("filters, keys", [
    ([IsFilter(field=TestEntity.name, value="test 3")], {"3"}),
    ([IsNotFilter(field=TestEntity.name, value="test 3")], {"1", "2", "4", "5"}),
    ([IsOneOfFilter(field=TestEntity.name, value=["test 3", "test 4"])], {"3", "4"}),
    ([IsNotOneOfFilter(field=TestEntity.name, value=["test 3", "test 4"])], {"1", "2", "5"}),
])
def test_es_keyword_field(setup_teardown_test_entities, store, filters: list[Filter], keys: set):
    """
    Test the keyword field. In elasticsearch multi fields need to be used to search for a keyword field.
    """
    store = setup_teardown_test_entities
    results = store.read(filters=filters)
    assert {entity.key for entity in results} == keys


@pytest.mark.parametrize("store", ['es_store'])
@pytest.mark.parametrize("filters, keys", [
    ([IsFilter(field=TestEntity.timestamp, value=datetime(year=2024, month=1, day=1))], {"3"}),
    ([IsNotFilter(field=TestEntity.timestamp, value=datetime(year=2024, month=2, day=1))], {"1", "2", "3", "5"}),
    ([IsOneOfFilter(field=TestEntity.timestamp, value=[datetime(year=2024, month=1, day=1)])], {"3"}),
    ([IsNotOneOfFilter(field=TestEntity.timestamp, value=[datetime(year=2024, month=2, day=1)])], {"1", "2", "3", "5"}),
    ([GreaterThanFilter(field=TestEntity.timestamp, value=datetime(year=2024, month=1, day=1))], {"4", "5"}),
    ([LessThanFilter(field=TestEntity.timestamp, value=datetime(year=2024, month=2, day=1))], {"1", "2", "3"}),
    ([ExistsFilter(field=TestEntity.timestamp)], {"1", "2", "3", "4", "5"}),
    ([DoesNotExistFilter(field=TestEntity.timestamp)], set())
])
def test_es_field_name(setup_teardown_test_entities, store, filters: list[Filter], keys: set):
    """
    Test that fields that are indexed with a different name in elasticsearch can be filtered on.
    """
    store = setup_teardown_test_entities
    results = store.read(filters=filters)
    assert {entity.key for entity in results} == keys


@pytest.mark.parametrize("filter_dict, expected_filter", [
    ({"field": "count", "operator": "is", "value": 2}, IsFilter),
    ({"field": "count", "operator": "is_not", "value": 2}, IsNotFilter),
    ({"field": "count", "operator": "is_in", "value": [2, 3]}, IsOneOfFilter),
    ({"field": "count", "operator": "is_not_in", "value": [2, 3]}, IsNotOneOfFilter),
    ({"field": "count", "operator": "gt", "value": 2}, GreaterThanFilter),
    ({"field": "count", "operator": "lt", "value": 2}, LessThanFilter),
    ({"field": "count", "operator": "exists"}, ExistsFilter),
    ({"field": "count", "operator": "does_not_exist"}, DoesNotExistFilter),
    ({"operator": "or", "filters": [{"field": "count", "operator": "is", "value": 2},
                                    {"field": "count", "operator": "is", "value": 3}]}, OrFilter)
])
def test_from_dict_to_dict(filter_dict: dict, expected_filter: type(Filter)):
    """
    Test the filter factory, which creates an instance of a filter from a dict representation.  Also verify that
    a filter can be converted back to a dict representation.
    """
    data_filter = FilterFactory.filter_from_dict(filter_dict=filter_dict, entity=TestEntity)
    assert isinstance(data_filter, expected_filter)
    assert data_filter.to_dict() == filter_dict



