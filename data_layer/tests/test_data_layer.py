from dataclasses import dataclass
from data_layer import Entity, DictStore, IsFilter


@dataclass
class MyData(Entity):
    key: str
    count: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        return cls(**data)

    def to_dict(self):
        return self.__dict__


def test_dict_store():
    # Create a new DictStore
    store = DictStore(entity=MyData)

    # Create a new entity object
    my_data = MyData(count=1, name="test", key="123")

    # Create the entity in the store
    store.create(my_data, key=my_data.key)

    # Define filters. Note that the dataclass field can be accessed as an attribute.
    filters = [IsFilter(field=MyData.count, value=1)]

    # Read the entity from the store
    hits = store.read(filters=filters)
    assert len(hits) == 1

    # Update the entity in the store
    my_data.count = 2
    store.update(my_data, key=my_data.key)

    # Now our filters shouldn't get any hits.
    hits = store.read(filters=filters)
    assert len(hits) == 0

    # Delete the entity from the store
    store.delete(key=my_data.key)