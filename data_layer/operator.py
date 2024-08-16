from enum import Enum


class Operator(str, Enum):
    IS = 'is'
    IS_NOT = 'is_not'
    IN = 'is_in'
    NOT_IN = 'is_not_in'
    GT = 'gt'
    LT = 'lt'
    EXISTS = 'exists'
    DOES_NOT_EXIST = 'does_not_exist'
    OR = 'or'
