from typing import Optional
from datetime import datetime, UTC
import logging

from ..models.document import Document, DocumentCreate, DocumentUpdate, DocumentResponse
from .hrid_service import hrid_service

logger = logging.getLogger(__name__)


class DocumentService:
    """Service class for document operations using Beanie ODM."""
    
    async def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        """Create a new document with auto-generated share_id using HRID service."""
        try:
            share_id = hrid_service.generate_id()
            logger.debug(f"Generated share_id: {share_id}")
            
            document = Document(
                share_id=share_id,
                content=document_data.content
            )
            
            saved_document = await document.save()
            logger.info(f"Document created with share_id: {share_id}")
            
            return DocumentResponse(
                id=str(saved_document.id),
                share_id=saved_document.share_id,
                content=saved_document.content,
                created_at=saved_document.created_at,
                updated_at=saved_document.updated_at
            )
            
        except Exception as e:
            logger.error(f"Unexpected error creating document: {e}")
            raise RuntimeError("Failed to create document")
    
    async def get_document(self, share_id: str) -> Optional[DocumentResponse]:
        """Retrieve a document by share_id."""
        try:
            document = await Document.find_one(Document.share_id == share_id)
            
            if not document:
                return None
            
            return DocumentResponse(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
            
        except Exception as e:
            logger.error(f"Unexpected error retrieving document: {e}")
            raise RuntimeError("Failed to retrieve document")
    
    async def update_document(self, share_id: str, update_data: DocumentUpdate) -> Optional[DocumentResponse]:
        """Update a document by share_id."""
        try:
            document = await Document.find_one(Document.share_id == share_id)
            
            if not document:
                return None
            
            if update_data.content is not None:
                document.content = update_data.content
            
            document.updated_at = datetime.now(UTC)
            await document.save()
            
            return DocumentResponse(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
            
        except Exception as e:
            logger.error(f"Unexpected error updating document: {e}")
            raise RuntimeError("Failed to update document")


# Global service instance
document_service = DocumentService()
