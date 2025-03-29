from fastapi import APIRouter

from src.api.routes.client.profile.accounts.account import router as account_router

router = APIRouter(prefix="/profile", tags=["Profile"])

router.include_router(account_router)
