from typing import Any, Awaitable, Callable
from urllib.parse import parse_qs

from hw_1.error.error_mapping import error_code_2_http_error
from hw_1.error.http_errors import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_405_METHOD_NOT_ALLOWED
from hw_1.error.server_errors import ServerException
from hw_1.math_service import handle_factorial, handle_fibonacci, handle_mean
from hw_1.network import send_json, send_error, load_json


async def app(
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    if scope['type'] not in ['http', 'https']:
        return

    method = scope['method']
    path = scope['path']
    query_params = parse_qs(scope['query_string'])

    try:
        if path == '/factorial':
            if method != 'GET':
                await send_error(send, HTTP_405_METHOD_NOT_ALLOWED)
                return

            response = handle_factorial(query_params)
            await send_json(send, response)

        elif path.startswith('/fibonacci') and len(path.split('/')) == 3:
            if method != 'GET':
                await send_error(send, HTTP_405_METHOD_NOT_ALLOWED)
                return

            response = handle_fibonacci(path.split('/')[2])
            await send_json(send, response)

        elif path == '/mean':
            if method != 'GET':
                await send_error(send, HTTP_405_METHOD_NOT_ALLOWED)
                return

            body = await load_json(receive)
            response = handle_mean(body)
            await send_json(send, response)

        else:
            await send_error(send, HTTP_404_NOT_FOUND)

    except ServerException as e:
        http_error = error_code_2_http_error(e.code)

        body = {'error': e.code.value}
        if e.field:
            body['field'] = e.field

        await send_error(send, http_error, body)

    except Exception:
        await send_error(send, HTTP_500_INTERNAL_SERVER_ERROR)
