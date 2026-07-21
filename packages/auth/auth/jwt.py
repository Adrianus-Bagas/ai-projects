from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

JWT_ALGORITHM = "HS256"

def create_access_token(
    subject: str,
    secret_key: str,
    expires_delta: timedelta,
) -> str:
    expires_at = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm=JWT_ALGORITHM,
    )

    return token

def decode_access_token(
    encoded_token: str,
    secret_key: str,
) -> dict[str, Any]:
    decoded_token = jwt.decode(
        encoded_token,
        secret_key,
        algorithms=[JWT_ALGORITHM],
    )

    return decoded_token