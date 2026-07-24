from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from auth.jwt import decode_access_token
from app.core.config import Settings, get_settings
from app.repositories.user_repository import UserRepository
from app.dependencies.repositories import get_user_repository


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    settings: Settings = Depends(get_settings),
    user_repository: UserRepository = Depends(get_user_repository)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(
            encoded_token=token,
            secret_key=settings.JWT_SECRET_KEY,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = await user_repository.get_by_id(
        user_id=user_id
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )
    
    return user