from fastapi import APIRouter

from .registration import router as registration_router
from .authorization import router as authorization_router

router = APIRouter(prefix="/security")

router.include_router(registration_router)
router.include_router(authorization_router)
