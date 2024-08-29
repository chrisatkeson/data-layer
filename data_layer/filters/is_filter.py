from data_layer.entity import Entity
from data_layer.filters.filter import Filter
from data_layer.operator import Operator


class IsFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.IS, field=field, value=value)

        if field is None:
            raise Exception("Is filter missing field.")
        if value is None:
            raise Exception("Is filter missing 'value'.")
        if not isinstance(value, field.type):
            raise Exception(f"Value {value} is not of type {field.type}")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_keyword_field or self.field_metadata.es_field_name or self.field.name
        return {
            "term": {
                field_name: self.value
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value == self.value

    def __repr__(self):
        return f"{self.field.name} is {self.value}"