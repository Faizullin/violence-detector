from fastapi import APIRouter

from app.api.routes import (
    violence_detection
)

api_router = APIRouter()
# api_router.include_router(user_face_id_auth.router, tags=["user_face_id/auth"])
# api_router.include_router(user_face_id_register.router, tags=["user_face_id/register"])
api_router.include_router(violence_detection.router, tags=["violence_detection"])
