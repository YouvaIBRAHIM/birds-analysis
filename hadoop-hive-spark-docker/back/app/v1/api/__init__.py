from fastapi import APIRouter
from app.v1.api.users.users_controller import router as user_router
from app.v1.api.stats.stats_controller import router as stats_router

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(user_router)
router.include_router(stats_router)

