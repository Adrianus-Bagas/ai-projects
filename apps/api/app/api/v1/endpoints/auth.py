from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import get_auth_service
from app.dependencies.current_user import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from database.models import User

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = await auth_service.login(
        email=request.email,
        password=request.password,
    )
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return LoginResponse(
        access_token=token, 
        token_type="bearer"
    )

@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }