from fastapi import APIRouter

from .routers import healthcheck_router
from .routers import simplification_router
from .routers import analysis_router

router = APIRouter()

router.include_router(healthcheck_router.router, prefix='/healthcheck', tags=['health-check'])
router.include_router(simplification_router.router, prefix='/simplify', tags=['simplify'])
router.include_router(analysis_router.router, prefix='/analyze', tags=['analyze'])
