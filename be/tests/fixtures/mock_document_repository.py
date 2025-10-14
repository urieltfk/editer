"""
Mock document repository for testing.
"""

from typing import Dict, Optional
from datetime import datetime, UTC
from src.protocols.repository_protocol import DocumentData


class MockDocumentRepository:
    """Mock implementation of DocumentRepositoryProtocol for testing."""
    
    def __init__(self):
        """Initialize mock repository with in-memory storage."""
        self.documents: Dict[str, DocumentData] = {}
        self.create_called = False
        self.find_called = False
        self.update_called = False
        self.should_raise_on_create = False
        self.should_raise_on_find = False
        self.should_raise_on_update = False
    
    async def create(self, share_id: str, content: str) -> DocumentData:
        """
        Mock document creation.
        
        Args:
            share_id: Human-readable share identifier
            content: Document content
            
        Returns:
            DocumentData: Created document data
            
        Raises:
            RuntimeError: If configured to raise errors
        """
        self.create_called = True
        
        if self.should_raise_on_create:
            raise RuntimeError("Mock database error on create")
        
        doc_data = DocumentData(
            id=f"mock-id-{len(self.documents)}",
            share_id=share_id,
            content=content,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        
        self.documents[share_id] = doc_data
        return doc_data
    
    async def find_by_share_id(self, share_id: str) -> Optional[DocumentData]:
        """
        Mock document lookup.
        
        Args:
            share_id: Human-readable share identifier
            
        Returns:
            Optional[DocumentData]: Document data if found, None otherwise
            
        Raises:
            RuntimeError: If configured to raise errors
        """
        self.find_called = True
        
        if self.should_raise_on_find:
            raise RuntimeError("Mock database error on find")
        
        return self.documents.get(share_id)
    
    async def update(self, share_id: str, content: str, updated_at: datetime) -> Optional[DocumentData]:
        """
        Mock document update.
        
        Args:
            share_id: Human-readable share identifier
            content: New document content
            updated_at: New timestamp
            
        Returns:
            Optional[DocumentData]: Updated document data if found, None otherwise
            
        Raises:
            RuntimeError: If configured to raise errors
        """
        self.update_called = True
        
        if self.should_raise_on_update:
            raise RuntimeError("Mock database error on update")
        
        doc_data = self.documents.get(share_id)
        if not doc_data:
            return None
        
        doc_data.content = content
        doc_data.updated_at = updated_at
        return doc_data
    
    def reset(self):
        """Reset the mock repository state."""
        self.documents.clear()
        self.create_called = False
        self.find_called = False
        self.update_called = False
        self.should_raise_on_create = False
        self.should_raise_on_find = False
        self.should_raise_on_update = False

