from enum import Enum


class ServerErrorCode(Enum):
    FIELD_IS_EMPTY = 'Field is empty'
    VAL_IS_EMPTY = 'Value is empty'
    VAL_IS_NEG = 'Value is negative'
    WRONG_TYPE = 'Field type is wrong'


FIELD_ERROR_CODES = {
    ServerErrorCode.FIELD_IS_EMPTY,
    ServerErrorCode.WRONG_TYPE,
}
VAL_ERROR_CODES = {
    ServerErrorCode.VAL_IS_EMPTY,
    ServerErrorCode.VAL_IS_NEG,
}


class ServerException(Exception):
    def __init__(self, code: ServerErrorCode, field: str = None):
        self.code = code
        self.field = field
