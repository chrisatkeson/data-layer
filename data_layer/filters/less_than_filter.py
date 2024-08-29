from datetime import datetime

from data_layer.entity import Entity
from data_layer.filters.filter import Filter
from data_layer.operator import Operator


class LessThanFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.LT, field=field, value=value)

        if field is None:
            raise Exception("Greater Than filter missing field.")
        if value is None:
            raise Exception("Greater Than filter missing 'value'.")
        if field.type not in [int, float, datetime]:
            raise Exception(f"Field {field.name} is not a numeric field")
        if not isinstance(value, field.type):
            raise Exception(f"Value {value} is not of type {field.type}")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_field_name or self.field.name
        return {
            "range": {
                field_name: {
                    "lt": self.value
                }
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        if value is None:
            return False
        return value < self.value

    def __repr__(self):
        return f"{self.field.name} is less than {self.value}"