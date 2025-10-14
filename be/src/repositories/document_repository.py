"""
Document repository implementation for database operations.
Separates data access logic from business logic.
"""

import logging
from typing import Optional
from datetime import datetime
from ..models.document import Document
from ..protocols.repository_protocol import DocumentData, DocumentRepositoryProtocol

logger = logging.getLogger(__name__)


class DocumentRepository:
    """Repository for document persistence using Beanie ODM."""
    
    async def create(self, share_id: str, content: str) -> DocumentData:
        """
        Create a new document in the database.
        
        Args:
            share_id: Human-readable share identifier
            content: Document content
            
        Returns:
            DocumentData: Created document data
            
        Raises:
            RuntimeError: If database operation fails
        """
        try:
            document = Document(
                share_id=share_id,
                content=content
            )
            await document.insert()
            
            return DocumentData(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
        except Exception as e:
            logger.error(f"Failed to create document in database: {e}")
            raise RuntimeError(f"Database create operation failed: {e}")
    
    async def find_by_share_id(self, share_id: str) -> Optional[DocumentData]:
        """
        Find a document by its share_id.
        
        Args:
            share_id: Human-readable share identifier
            
        Returns:
            Optional[DocumentData]: Document data if found, None otherwise
            
        Raises:
            RuntimeError: If database operation fails
        """
        try:
            document = await Document.find_one(Document.share_id == share_id)
            
            if not document:
                return None
            
            return DocumentData(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
        except Exception as e:
            logger.error(f"Failed to find document in database: {e}")
            raise RuntimeError(f"Database find operation failed: {e}")
    
    async def update(self, share_id: str, content: str, updated_at: datetime) -> Optional[DocumentData]:
        """
        Update a document's content and timestamp.
        
        Args:
            share_id: Human-readable share identifier
            content: New document content
            updated_at: New timestamp
            
        Returns:
            Optional[DocumentData]: Updated document data if found, None otherwise
            
        Raises:
            RuntimeError: If database operation fails
        """
        try:
            document = await Document.find_one(Document.share_id == share_id)
            
            if not document:
                return None
            
            document.content = content
            document.updated_at = updated_at
            await document.save()
            
            return DocumentData(
                id=str(document.id),
                share_id=document.share_id,
                content=document.content,
                created_at=document.created_at,
                updated_at=document.updated_at
            )
        except Exception as e:
            logger.error(f"Failed to update document in database: {e}")
            raise RuntimeError(f"Database update operation failed: {e}")

def get_document_repository() -> DocumentRepositoryProtocol:
    """
    Get the document repository instance.
    
    Returns:
        DocumentRepositoryProtocol: Document repository for database operations
    """
    return DocumentRepository()