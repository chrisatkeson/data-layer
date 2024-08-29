from data_layer.filters import *
from data_layer.operator import Operator
from data_layer import Entity
from data_layer.util import parse
from data_layer.exceptions import InvalidOperatorError


class FilterFactory:
    _filter_map = {
        Operator.IS: IsFilter,
        Operator.IS_NOT: IsNotFilter,
        Operator.IN: IsOneOfFilter,
        Operator.NOT_IN: IsNotOneOfFilter,
        Operator.GT: GreaterThanFilter,
        Operator.LT: LessThanFilter,
        Operator.EXISTS: ExistsFilter,
        Operator.DOES_NOT_EXIST: DoesNotExistFilter,
        Operator.OR: OrFilter,
    }

    @staticmethod
    def filter_from_dict(filter_dict: dict[str, any], entity: type(Entity)) -> Filter:
        """
        Create a filter from a dictionary.
        :param filter_dict: the dictionary representation of a filter: {"operator": str, "field": str, "value": any}
        :param entity: the entity class.  Needed to validate the field.
        :return: an instance of a Filter.
        """
        try:
            operator = Operator(filter_dict.get("operator"))
        except ValueError:
            raise InvalidOperatorError(filter_dict.get("operator"))

        filter_class = FilterFactory._filter_map.get(operator)

        if not filter_class:
            raise ValueError(f"Unsupported operator: {operator}")

        field = filter_dict.get("field")
        if field:
            if not hasattr(entity, field):
                raise ValueError(f"Entity {entity.__class__.__name__} does not have field {field}")
            field = getattr(entity, field)

        value = filter_dict.get("value")

        if field:
            value = parse(value_type=field.type, value=value)

        if operator == Operator.OR:
            filters = filter_dict.get("filters", [])
            filters = [FilterFactory.filter_from_dict(filter_dict=f, entity=entity) for f in filters]
            return filter_class(filters=filters)

        if operator in [Operator.EXISTS, Operator.DOES_NOT_EXIST]:
            return filter_class(field=field)

        return filter_class(field=field, value=value)
