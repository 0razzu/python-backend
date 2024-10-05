from enum import Enum, auto


class RepositoryErrorCode(Enum):
    NOT_FOUND = auto()


class RepositoryException(Exception):
    def __init__(self, code: RepositoryErrorCode, field: str | None = None):
        self.code = code
        self.field = field
