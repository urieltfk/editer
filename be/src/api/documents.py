from fastapi import APIRouter, HTTPException, status, Depends
import logging

from ..models.document import DocumentCreate, DocumentUpdate, DocumentResponse
from ..services.document_service import DocumentService
from src.services.document_service import get_document_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document: DocumentCreate,
    document_service: DocumentService = Depends(get_document_service)
):
    """Create a new document with auto-generated share_id."""
    try:
        result = await document_service.create_document(document)
        logger.info(f"Document created with share_id: {result.share_id}")
        return result
    except ValueError as e:
        logger.warning(f"Validation error creating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(f"Service error creating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create document"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/documents/{share_id}", response_model=DocumentResponse)
async def get_document(
    share_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """Retrieve a document by share_id."""
    try:
        result = await document_service.get_document(share_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with share_id '{share_id}' not found"
            )
        logger.info(f"Document retrieved: {share_id}")
        return result
    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"Service error retrieving document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve document"
        )
    except Exception as e:
        logger.error(f"Unexpected error retrieving document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/documents/{share_id}", response_model=DocumentResponse)
async def update_document(
    share_id: str,
    document: DocumentUpdate,
    document_service: DocumentService = Depends(get_document_service)
):
    """Update a document by share_id."""
    try:
        result = await document_service.update_document(share_id, document)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with share_id '{share_id}' not found"
            )
        logger.info(f"Document updated: {share_id}")
        return result
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error updating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        logger.error(f"Service error updating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update document"
        )
    except Exception as e:
        logger.error(f"Unexpected error updating document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )