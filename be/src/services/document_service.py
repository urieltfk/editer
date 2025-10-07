"""
Document service for handling document operations.
"""

import logging
from typing import Optional
from ..models.document import Document, DocumentCreate, DocumentUpdate, DocumentResponse
from ..services.hrid_service import generate_hrid

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document operations."""
    
    async def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        """Create a new document."""
        try:
            # Generate unique share_id
            share_id = generate_hrid()
            
            # Create document
            document = Document(
                share_id=share_id,
                content=document_data.content
            )
            
            # Save to database
            await document.insert()
            
            # Return response
            return DocumentResponse(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            raise RuntimeError(f"Failed to create document: {e}")
    
    async def get_document(self, share_id: str) -> Optional[DocumentResponse]:
        """Get a document by share_id."""
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
            logger.error(f"Error retrieving document: {e}")
            raise RuntimeError(f"Failed to retrieve document: {e}")
    
    async def update_document(self, share_id: str, document_data: DocumentUpdate) -> Optional[DocumentResponse]:
        """Update a document by share_id."""
        try:
            document = await Document.find_one(Document.share_id == share_id)
            
            if not document:
                return None
            
            # Update content and timestamp
            from datetime import datetime, UTC
            document.content = document_data.content
            document.updated_at = datetime.now(UTC)
            
            # Save changes
            await document.save()
            
            return DocumentResponse(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise RuntimeError(f"Failed to update document: {e}")


# Global service instance
document_service = DocumentService()
