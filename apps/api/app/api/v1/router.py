from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.audit_log import router as audit_log_router


router = APIRouter()

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    user_router,
    prefix="/users",
    tags=["User"],
)

router.include_router(
    audit_log_router,
    prefix="/audit_logs",
    tags=["Audit Logs"],
)