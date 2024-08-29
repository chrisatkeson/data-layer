from data_layer.entity import Entity
from data_layer.filters.filter import Filter
from data_layer.operator import Operator


class ExistsFilter(Filter):

    def __init__(self, field):
        super().__init__(operator=Operator.EXISTS, field=field, value=None)

        if field is None:
            raise Exception("Exists filter missing field.")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_field_name or self.field.name
        return {
            "exists": {
                "field": field_name
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value is not None

    def __repr__(self):
        return f"{self.field.name} exists"
