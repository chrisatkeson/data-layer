from abc import ABC, abstractmethod
from data_layer.entity import Entity, MetaData
from data_layer.operator import Operator
from dataclasses import Field
from datetime import datetime


class Filter(ABC):
    def __init__(self, field, operator: Operator, value: any):
        self.field = field
        self.operator = operator
        self.value = value

        if field and not isinstance(field, Field):
            raise Exception("field must be a dataclass Field.")

    @abstractmethod
    def evaluate(self, entity: Entity) -> bool:
        pass

    @abstractmethod
    def to_elasticsearch(self):
        pass

    @property
    def field_metadata(self):
        if self.field:
            return MetaData(**self.field.metadata)
        return None


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


class IsNotFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.IS_NOT, field=field, value=value)

        if field is None:
            raise Exception("Is Not filter missing field.")
        if value is None:
            raise Exception("Is Not filter missing 'value'.")
        if not isinstance(value, field.type):
            raise Exception(f"Value {value} is not of type {field.type}")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_keyword_field or self.field_metadata.es_field_name or self.field.name
        return {
            "bool": {
                "must_not": {
                    "term": {
                        field_name: self.value
                    }
                }
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value != self.value

    def __repr__(self):
        return f"{self.field.name} is not {self.value}"


class IsOneOfFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.IN, field=field, value=value)

        if field is None:
            raise Exception("Is One Of filter missing field.")
        if value is None:
            raise Exception("Is One Of filter missing 'value'.")
        if not isinstance(value, list):
            raise Exception("Is One Of filter 'value' must be a list.")
        for val in value:
            if not isinstance(val, field.type):
                raise Exception(f"Value {val} is not of type {field.type}")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_keyword_field or self.field_metadata.es_field_name or self.field.name
        return {
            "terms": {
                field_name: self.value
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value in self.value

    def __repr__(self):
        return f"{self.field.name} is one of {self.value}"


class IsNotOneOfFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.NOT_IN, field=field, value=value)

        if field is None:
            raise Exception("Is Not One Of filter missing field.")
        if value is None:
            raise Exception("Is Not One Of filter missing 'value'.")
        if not isinstance(value, list):
            raise Exception("Is Not One Of filter 'value' must be a list.")
        for val in value:
            if not isinstance(val, field.type):
                raise Exception(f"Value {val} is not of type {field.type}")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_keyword_field or self.field_metadata.es_field_name or self.field.name
        return {
            "bool": {
                "must_not": {
                    "terms": {
                        field_name: self.value
                    }
                }
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value not in self.value

    def __repr__(self):
        return f"{self.field.name} is not one of {self.value}"


class GreaterThanFilter(Filter):

    def __init__(self, field, value: any):
        super().__init__(operator=Operator.GT, field=field, value=value)

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
                    "gt": self.value
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
        return value > self.value

    def __repr__(self):
        return f"{self.field.name} is greater than {self.value}"


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


class DoesNotExistFilter(Filter):

    def __init__(self, field):
        super().__init__(operator=Operator.DOES_NOT_EXIST, field=field, value=None)

        if field is None:
            raise Exception("Does Not Exist filter missing field.")

    def to_elasticsearch(self) -> dict:
        """
        Create term elasticsearch filter
        :return: dict term filter
        """
        field_name = self.field_metadata.es_field_name or self.field.name
        return {
            "bool": {
                "must_not": {
                    "exists": {
                        "field": field_name
                    }
                }
            }
        }

    def evaluate(self, entity: Entity) -> bool:
        """
        Evaluate a filter on a value.  Return True or False depending on the evaluation of the filter.
        :return: True if the filter evaluates to True on the value and False otherwise.
        """
        value = getattr(entity, self.field.name, None)
        return value is None

    def __repr__(self):
        return f"{self.field.name} does not exist"


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
