import auth.jwt as jwt_utils

from datetime import timedelta

from auth.password import verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        jwt_secret_key: str,
        access_token_expire_minutes: int,
    ) -> None:
        self.user_repository = user_repository
        self.jwt_secret_key = jwt_secret_key
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, subject: str) -> str:
        access_token = jwt_utils.create_access_token(
            subject,
            self.jwt_secret_key,
            timedelta(minutes=self.access_token_expire_minutes),
        )
        return access_token

    async def login(self, email: str, password: str) -> str | None:
        user = await self.user_repository.get_by_email(email)
    
        if user is None:
            return None
        if not verify_password(password, user.password_hash):
            return None
        
        access_token = jwt_utils.create_access_token(str(user.id))
        return access_token