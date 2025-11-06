from fastapi import APIRouter

from src.api.routes import batteries, bind, devices

router = APIRouter()

router.include_router(batteries.router, tags=["Battaries"], prefix="/battaries")
router.include_router(devices.router, tags=["Devices"], prefix="/devices")
router.include_router(bind.router, tags=["Bind"], prefix="/bind")

__all__ = [
    "router",
]
