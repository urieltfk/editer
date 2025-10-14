"""
Protocol for document repository to enable dependency injection.
"""

from typing import Protocol, Optional
from datetime import datetime


class DocumentData:
    """Data class for document information."""
    
    def __init__(
        self,
        id: str,
        share_id: str,
        content: str,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.share_id = share_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at


class DocumentRepositoryProtocol(Protocol):
    """Protocol defining the interface for document persistence."""
    
    async def create(self, share_id: str, content: str) -> DocumentData:
        """
        Create a new document in the database.
        
        Args:
            share_id: Human-readable share identifier
            content: Document content
            
        Returns:
            DocumentData: Created document data
        """
        ...
    
    async def find_by_share_id(self, share_id: str) -> Optional[DocumentData]:
        """
        Find a document by its share_id.
        
        Args:
            share_id: Human-readable share identifier
            
        Returns:
            Optional[DocumentData]: Document data if found, None otherwise
        """
        ...
    
    async def update(self, share_id: str, content: str, updated_at: datetime) -> Optional[DocumentData]:
        """
        Update a document's content and timestamp.
        
        Args:
            share_id: Human-readable share identifier
            content: New document content
            updated_at: New timestamp
            
        Returns:
            Optional[DocumentData]: Updated document data if found, None otherwise
        """
        ...

