from fastapi import APIRouter
from ..settings import settings
from .documents import router as documents_router

router = APIRouter()

router.include_router(documents_router, prefix="/api/v1", tags=["documents"])

# Health check endpoint
@router.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "editer-api",
        "version": settings.api_version,
        "debug": settings.debug
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