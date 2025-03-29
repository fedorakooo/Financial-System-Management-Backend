from fastapi import APIRouter

from src.api.routes.staff.banks.bank import router as bank_router
from src.api.routes.staff.users.user import router as user_router
from src.api.routes.staff.accounts.account import router as account_router
from src.api.routes.staff.enterprises.enterprise import router as enterprise_router

router = APIRouter(prefix="/staff", tags=["Staff"])

router.include_router(bank_router)
router.include_router(user_router)
router.include_router(account_router)
router.include_router(enterprise_router)

