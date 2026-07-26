from http import HTTPStatus

from shared.errors.constants import SharedErrorCode


def map_http_error_code(status_code: int) -> SharedErrorCode:
    if status_code == HTTPStatus.NOT_FOUND:
        return SharedErrorCode.NOT_FOUND

    if status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        return SharedErrorCode.METHOD_NOT_ALLOWED

    return SharedErrorCode.HTTP_ERROR