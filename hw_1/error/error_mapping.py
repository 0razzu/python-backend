from hw_1.error.http_errors import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from hw_1.error.server_errors import ServerErrorCode, FIELD_ERROR_CODES, VAL_ERROR_CODES


def error_code_2_http_error(code: ServerErrorCode):
    if code in FIELD_ERROR_CODES:
        return HTTP_422_UNPROCESSABLE_ENTITY
    if code in VAL_ERROR_CODES:
        return HTTP_400_BAD_REQUEST

    return HTTP_500_INTERNAL_SERVER_ERROR
