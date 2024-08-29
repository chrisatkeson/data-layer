# Data Layer

The Data Layer is a set of classes designed to abstract the data layer from the implementation details of how data 
is stored. By decoupling your code from specific technologies like Elasticsearch or MySQL, this layer allows you to:

- Run unit tests without a database.
- Switch out the data store without modifying your code.

The Wave Data Layer is composed of three main classes:

1. [**Entity**](#entity)
2. [**Store**](#store)
3. [**Filter**](#filter)

---

## Entity

The [`Entity`](#entity) class is a dataclass that represents the data you want to store. It defines the schema of your 
data and implements methods to convert the data to and from a dictionary. The `Entity` class is intended to be subclassed, 
with each subclass representing a specific type of data to be stored. Subclasses must be implemented as Python dataclasses.

Example:
```python
from dataclasses import dataclass
from data_layer import Entity

@dataclass
class MyData(Entity):
    key: str
    count: int
    name: str

```

---

## Store

The [`Store`](#store) class is an abstract class that defines the interface for storing and retrieving data. It provides 
methods for basic CRUD operations like create, read, update, and delete. The `Store` class is meant to be subclassed 
based on the technology you choose for data storage.

### Implementations

We currently have two implementations of the `Store` class (update this list as more are added):

- **DictStore**: An in-memory store that uses a dictionary to store data. This is particularly useful for unit testing 
without a database.
  
- **ElasticsearchStore**: A store that utilizes Elasticsearch for data storage, ideal for live environments interacting 
with an Elasticsearch cluster.

---

## Filter

The [`Filter`](#filter) class offers a flexible language for filtering and querying data. It's used to build queries 
within the `read` method of the `Store`. Filters are defined on fields within the `Entity` class and can be combined 
to create complex queries.

We currently have several implementations of the `Filter` class (update this list as more are added):

- **IsFilter**: A filter that checks if a field is equal to a specific value.
- **IsNotFilter**: A filter that checks if a field is not equal to a specific value.
- **IsOneOfFilter**: A filter that checks if a field is equal to one of a list of values.
- **IsNotOneOfFilter**: A filter that checks if a field is not equal to any value in a list.
- **GreaterThanFilter**: A filter that checks if a field is greater than a specific value.
- **LessThanFilter**: A filter that checks if a field is less than a specific value.
- **ExistsFilter**: A filter that checks if a field is not None.
- **DoesNotExistFilter**: A filter that checks if a field is None.
- **OrFilter**: A filter that combines multiple filters with an OR operation.

Filters also have a `to_dict` method that returns a dictionary representation of the filter, and a factory method
filter_from_dict that creates a filter from a dictionary.  This is useful for serializing and deserializing filters for
interfacing with other systems.

Example:
```python
from data_layer import FilterFactory, Entity, DictStore
from dataclasses import dataclass

@dataclass
class MyData(Entity):
    count: int

store = DictStore(entity=MyData)
store.create(MyData(count=2), key="1")
filter_dict = {"field": "count", "operator": "is", "value": 2}
filter_instance = FilterFactory.filter_from_dict(filter_dict=filter_dict, entity=MyData)
assert len(store.read(filters=[filter_instance])) == 1
assert filter_instance.to_dict() == filter_dict

```


---
# Basic Use Case
```python
from dataclasses import dataclass
from data_layer import Entity, DictStore, IsFilter

# Define a new dataclass that inherits from Entity
@dataclass
class MyData(Entity):
    key: str
    count: int
    name: str

if __name__ == "__main__":
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

```