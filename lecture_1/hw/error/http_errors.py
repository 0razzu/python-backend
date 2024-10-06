class HTTPError:
    def __init__(self, code, message):
        self.code = code
        self.message = message


HTTP_400_BAD_REQUEST = HTTPError(400, 'Bad Request')
HTTP_404_NOT_FOUND = HTTPError(404, 'Not Found')
HTTP_405_METHOD_NOT_ALLOWED = HTTPError(405, 'Method Not Allowed')
HTTP_422_UNPROCESSABLE_ENTITY = HTTPError(422, 'Unprocessable Entity')
HTTP_500_INTERNAL_SERVER_ERROR = HTTPError(500, 'Internal Server Error')
