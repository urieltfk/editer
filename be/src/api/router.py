from fastapi import APIRouter
from ..settings import settings
from .documents import router as documents_router
from ..services.database import db_manager

router = APIRouter()

router.include_router(documents_router, prefix="/api/v1", tags=["documents"])

# Health check endpoint
@router.get("/health")
async def health_check():
    # Check database health
    db_healthy = await db_manager.health_check()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy", 
        "service": "editer-api",
        "version": settings.api_version,
        "debug": settings.debug,
        "database": "healthy" if db_healthy else "unhealthy"
    }

# Root endpoint
@router.get("/")
async def root():
    return {
        "message": "Welcome to Editer API",
        "title": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }