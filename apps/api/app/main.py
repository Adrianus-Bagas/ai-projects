from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()

# Create the ASGI application object that Uvicorn imports as `app.main:app`.
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
# Permit the browser-based web application to call this API from another origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Keep every API endpoint below the versioned prefix configured for this deployment.
app.include_router(api_router, prefix=settings.API_PREFIX)