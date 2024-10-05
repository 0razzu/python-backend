import math
from typing import AnyStr, Any

from hw_1.error.server_errors import ServerException, ServerErrorCode


def handle_factorial(query_params: dict[AnyStr, list[AnyStr]]) -> dict[str, int]:
    n = query_params.get(b'n', None)

    if not n:
        raise ServerException(ServerErrorCode.FIELD_IS_EMPTY, 'n')

    try:
        n = int(n[0])
    except ValueError:
        raise ServerException(ServerErrorCode.WRONG_TYPE, 'n')

    if n < 0:
        raise ServerException(ServerErrorCode.VAL_IS_NEG, 'n')

    return {'result': math.factorial(n)}


def handle_fibonacci(path_param: AnyStr) -> dict[str, int]:
    if not path_param:
        raise ServerException(ServerErrorCode.FIELD_IS_EMPTY, 'n')

    try:
        n = int(path_param)
    except ValueError:
        raise ServerException(ServerErrorCode.WRONG_TYPE, 'n')

    if n < 0:
        raise ServerException(ServerErrorCode.VAL_IS_NEG, 'n')

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return {'result': a}


def handle_mean(body: Any) -> dict[str, float]:
    if body is None:
        raise ServerException(ServerErrorCode.FIELD_IS_EMPTY, 'body')

    if len(body) == 0:
        raise ServerException(ServerErrorCode.VAL_IS_EMPTY, 'body')

    if not isinstance(body, list) or not all(isinstance(n, float) or isinstance(n, int) for n in body):
        raise ServerException(ServerErrorCode.WRONG_TYPE, 'body')

    return {'result': sum(body) / len(body)}
