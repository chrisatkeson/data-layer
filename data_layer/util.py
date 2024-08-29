from datetime import datetime


def parse(value_type: type, value: any):
    """
    Parse a value to a value type.
    :param value_type: the type that the value should be parsed to.
    :param value: the value to parse.
    :return: the value parsed to the value type.
    """
    if value is None:
        return None
    if isinstance(value, value_type):
        return value
    if isinstance(value, list):
        return [parse(value_type, v) for v in value]
    elif isinstance(value, value_type):
        return value
    elif value_type is datetime and isinstance(value, str):
        return datetime.fromisoformat(value)
    return value_type(value)


def serialize(value: any):
    """
    Serialize a value.
    :param value: any value to serialize.
    :return: the serialized value.
    """
    if value is None:
        return None
    if isinstance(value, list):
        return [serialize(v) for v in value]
    elif isinstance(value, datetime):
        return value.isoformat()
    return value

