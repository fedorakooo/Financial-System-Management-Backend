from fastapi import APIRouter

from src.api.routes.general.registration.registration import router as registration_router
from src.api.routes.general.login.login import router as login_router
from src.api.routes.general.banks.bank import router as bank_router

router = APIRouter(prefix="", tags=["General"])

router.include_router(registration_router)
router.include_router(login_router)
router.include_router(bank_router)
