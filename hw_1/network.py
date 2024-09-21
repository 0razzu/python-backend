import json
from typing import Callable, Any, Awaitable

from hw_1.error.http_errors import HTTPError
from hw_1.error.server_errors import ServerException, ServerErrorCode


async def send_json(
        send: Callable[[dict[str, Any]], Awaitable[None]],
        body: dict[str, Any],
        status: int = 200,
) -> None:
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [
            [b'content-type', b'application/json'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(body).encode('utf-8'),
    })


async def send_error(
        send: Callable[[dict[str, Any]], Awaitable[None]],
        error: HTTPError,
        body: dict[str, Any] = {},
) -> None:
    await send({
        'type': 'http.response.start',
        'status': error.code,
        'headers': [
            [b'content-type', b'application/json'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(body).encode('utf-8'),
    })


async def _load_body(receive: Callable[[], Awaitable[dict[str, Any]]]) -> bytes:
    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def load_json(receive: Callable[[], Awaitable[dict[str, Any]]]) -> Any:
    body = await _load_body(receive)
    try:
        body = json.loads(body or 'null')
    except json.JSONDecodeError:
        raise ServerException(ServerErrorCode.WRONG_TYPE, 'body')

    return body
