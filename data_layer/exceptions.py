class EntityNotFoundError(Exception):

    @classmethod
    def for_key(cls, key):
        return cls(f"Entity with key {key} not found.")


class InvalidOperatorError(Exception):

    @classmethod
    def for_operator(cls, operator):
        return cls(f"Invalid operator: {operator}")
