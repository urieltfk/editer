"""
Document service for handling document operations.
"""

import logging
from typing import Optional
from datetime import datetime, UTC
from ..models.request_response import DocumentCreate, DocumentUpdate, DocumentResponse
from ..protocols.hrid_protocol import HRIDGeneratorProtocol
from ..protocols.repository_protocol import DocumentRepositoryProtocol
from ..repositories.document_repository import get_document_repository
from ..services.hrid_service import get_hrid_generator

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document operations with dependency injection."""
    
    def __init__(
        self,
        hrid_generator: HRIDGeneratorProtocol,
        document_repository: DocumentRepositoryProtocol
    ):
        """
        Initialize the document service with its dependencies.
        
        Args:
            hrid_generator: Service for generating human-readable IDs
            document_repository: Repository for document persistence
        """
        self.hrid_generator = hrid_generator
        self.document_repository = document_repository
    
    async def create_document(self, document_data: DocumentCreate) -> DocumentResponse:
        """Create a new document."""
        try:
            share_id = self.hrid_generator.generate_id()
            
            doc_data = await self.document_repository.create(
                share_id=share_id,
                content=document_data.content
            )
            
            return DocumentResponse(
                id=doc_data.id,
                share_id=doc_data.share_id,
                content=doc_data.content,
                created_at=doc_data.created_at,
                updated_at=doc_data.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creating document: {e}")
            raise RuntimeError(f"Failed to create document: {e}")
    
    async def get_document(self, share_id: str) -> Optional[DocumentResponse]:
        """Get a document by share_id."""
        try:
            doc_data = await self.document_repository.find_by_share_id(share_id)
            
            if not doc_data:
                return None
            
            return DocumentResponse(
                id=doc_data.id,
                share_id=doc_data.share_id,
                content=doc_data.content,
                created_at=doc_data.created_at,
                updated_at=doc_data.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            raise RuntimeError(f"Failed to retrieve document: {e}")
    
    async def update_document(self, share_id: str, document_data: DocumentUpdate) -> Optional[DocumentResponse]:
        """Update a document by share_id."""
        try:
            updated_at = datetime.now(UTC)
            
            doc_data = await self.document_repository.update(
                share_id=share_id,
                content=document_data.content,
                updated_at=updated_at
            )
            
            if not doc_data:
                return None
            
            return DocumentResponse(
                id=doc_data.id,
                share_id=doc_data.share_id,
                content=doc_data.content,
                created_at=doc_data.created_at,
                updated_at=doc_data.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise RuntimeError(f"Failed to update document: {e}")

def get_document_service() -> DocumentService:
    """
    Get a DocumentService instance with injected dependencies.
    This function is used with FastAPI's Depends() for automatic dependency injection.
    
    Returns:
        DocumentService: Configured document service instance
    """
    hrid_generator = get_hrid_generator()
    document_repository = get_document_repository()
    
    return DocumentService(
        hrid_generator=hrid_generator,
        document_repository=document_repository
    )

