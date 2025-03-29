from fastapi import APIRouter

from src.api.routes.client.profile.profile import router as profile_router

router = APIRouter(prefix="", tags=["Client"])

router.include_router(profile_router)
