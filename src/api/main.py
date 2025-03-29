from fastapi import APIRouter

from src.api.routes.general.general import router as general_router
from src.api.routes.profile.profile import router as profile_router
from src.api.routes.client.client import router as client_router
from src.api.routes.staff.staff import router as staff_router
from src.api.routes.specialist.specialist import router as specialist_router

router = APIRouter()

router.include_router(general_router)
router.include_router(profile_router)
router.include_router(client_router)
router.include_router(staff_router)
router.include_router(specialist_router)
