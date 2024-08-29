from data_layer.entity import Entity
from data_layer.filters.filter import Filter
from data_layer.operator import Operator


class OrFilter(Filter):

    def __init__(self, filters: list[Filter]):
        super().__init__(operator=Operator.OR, field=None, value=None)

        if filters is None:
            raise Exception("Or filter missing filters.")
        if not isinstance(filters, list):
            raise Exception("Or filter 'filters' must be a list.")
        for f in filters:
            if not isinstance(f, Filter):
                raise Exception(f"Value {f} is not of type Filter")

        self.filters = filters

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        return {
            "bool": {
                "should": [f.to_elasticsearch() for f in self.filters]
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        return any([f.evaluate(entity) for f in self.filters])

    def __repr__(self):
        return f"{' OR '.join([str(f) for f in self.filters])}"