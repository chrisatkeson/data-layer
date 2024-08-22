class EntityNotFoundError(Exception):

    @classmethod
    def for_key(cls, key):
        return cls(f"Entity with key {key} not found.")
