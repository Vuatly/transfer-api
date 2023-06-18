from fastapi import APIRouter

from src.api.v1.users import router as users_router
from src.api.v1.coins import router as coins_router

router = APIRouter(prefix="/api/v1")
router.include_router(users_router)
router.include_router(coins_router)
