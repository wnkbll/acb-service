from fastapi import APIRouter

from src.api.routes import battaries, devices

router = APIRouter()

router.include_router(battaries.router, tags=["Battaries"], prefix="/battaries")
router.include_router(devices.router, tags=["Devices"], prefix="/devices")

__all__ = [
    "router",
]
