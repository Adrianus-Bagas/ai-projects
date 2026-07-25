from shared.errors import AppException


try:
    raise AppException(
        status_code=401,
        message="Invalid email or password",
        error_code="INVALID_CREDENTIALS",
    )
except AppException as exc:
    print(exc.status_code)
    print(exc.message)
    print(exc.error_code)
    print(str(exc))