from fastapi import APIRouter, Depends

from app.dependencies.services.auth import get_auth_service
from app.dependencies.current_user import get_current_active_user
from app.dependencies.require_roles import require_roles
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.responses.user import UserResponse
from app.services.auth import AuthService
from database.models.user import User, UserRole
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
async def get_current_user_profile(
    current_user: User = Depends(
        get_current_active_user,
    ),
) -> ApiResponse[UserResponse]:
    return ApiResponse(
        success=True,
        message="Get current user success",
        data=current_user,
    )

@router.get("/admin-only")
async def admin_only(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
):
    return {
        "message": "Admin access granted",
        "email": current_user.email,
        "role": current_user.role,
    }

@router.get("/authenticated")
async def authenticated(
    current_user: User = Depends(
        require_roles(
            UserRole.USER,
            UserRole.ADMIN,
        ),
    ),
):
    return {
        "message": "Authenticated access granted",
        "email": current_user.email,
        "role": current_user.role,
    }