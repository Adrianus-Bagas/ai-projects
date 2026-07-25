from enum import StrEnum


class AuthErrorCode(StrEnum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"


INVALID_CREDENTIALS_MESSAGE = "Invalid email or password"