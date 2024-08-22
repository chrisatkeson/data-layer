from dataclasses import dataclass, field, asdict
from data_layer import Entity, MetaData
from datetime import datetime


@dataclass
class TestEntity(Entity):
    key: str
    count: int
    name: str = field(metadata=asdict(MetaData(es_keyword_field="name.keyword")), default=None)
    timestamp: datetime = field(metadata=asdict(MetaData(es_field_name="@timestamp")), default=None)


test_entities = [
    TestEntity(key="1", count=1, name="test 1", timestamp=datetime(year=2023, month=1, day=1)),
    TestEntity(key="2", count=2, name="test 2", timestamp=datetime(year=2023, month=2, day=1)),
    TestEntity(key="3", count=2, name="test 3", timestamp=datetime(year=2024, month=1, day=1)),
    TestEntity(key="4", count=4, name="test 4", timestamp=datetime(year=2024, month=2, day=1)),
    TestEntity(key="5", count=5, name="test 5", timestamp=datetime(year=2024, month=3, day=1))
]
