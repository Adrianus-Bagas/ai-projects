from enum import StrEnum


class SharedErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    HTTP_ERROR = "HTTP_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    CANNOT_CHANGE_OWN_ROLE = "CANNOT_CHANGE_OWN_ROLE"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    NOT_IN_ORGANIZATION = "NOT_IN_ORGANIZATION"


VALIDATION_ERROR_MESSAGE = "Request validation failed"
INTERNAL_SERVER_ERROR_MESSAGE = "An unexpected error occurred"
USER_NOT_FOUND_ERROR_MESSAGE = "User not found"
CANNOT_CHANGE_OWN_ROLE_ERROR_MESSAGE = "You cannot change your own role"
RESOURCE_CONFLICT_MESSAGE = (
    "The resource was modified by another request. "
    "Please refresh the data and try again."
)
NOT_IN_ORGANIZATION = "You are not in this organization."