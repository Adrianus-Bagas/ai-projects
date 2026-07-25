from fastapi import APIRouter, Depends

from app.dependencies.auth import get_auth_service
from app.dependencies.current_user import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from database.models import User
from shared.responses import ApiResponse
from shared.errors import AppException

from http import HTTPStatus

from auth.constants import (
    AuthErrorCode,
    INVALID_CREDENTIALS_MESSAGE,
)

router = APIRouter()

@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = await auth_service.login(
        email=request.email,
        password=request.password,
    )
    if token is None:
        raise AppException(
            status_code=HTTPStatus.UNAUTHORIZED,
            message=INVALID_CREDENTIALS_MESSAGE,
            error_code=AuthErrorCode.INVALID_CREDENTIALS,
        )
        
    login_data = LoginResponse(
        access_token=token,
        token_type="bearer",
    )

    return ApiResponse[LoginResponse](
        success=True,
        message="Login successful",
        data=login_data,
    )

@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }