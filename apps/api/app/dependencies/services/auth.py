from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.config import Settings, get_settings
from fastapi import Depends
from app.dependencies.repositories import get_user_repository

def get_auth_service(user_repository: UserRepository = Depends(get_user_repository), settings: Settings = Depends(get_settings)) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        jwt_secret_key=settings.JWT_SECRET_KEY,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )