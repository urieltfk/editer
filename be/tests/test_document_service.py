"""
Unit tests for DocumentService layer with dependency injection.
Tests service methods with injected mock dependencies.
"""
import pytest
import asyncio
from datetime import datetime, UTC

from src.models.request_response import DocumentCreate, DocumentUpdate, DocumentResponse
from tests.fixtures import MockHRIDGenerator, MockDocumentRepository


@pytest.mark.asyncio
class TestDocumentServiceCreate:
    """Test DocumentService create_document method."""
    
    async def test_create_document_success(self, document_service, mock_hrid_generator, mock_document_repository):
        """Test successful document creation through service."""
        document_data = DocumentCreate(content="Test content")
        
        result = await document_service.create_document(document_data)
        
        assert result.share_id == "test-hrid-0"
        assert result.content == "Test content"
        assert result.created_at is not None
        assert result.updated_at is not None
        assert mock_document_repository.create_called
        assert mock_hrid_generator.call_count == 1
    
    async def test_create_document_generates_unique_share_id(self, document_service, mock_hrid_generator):
        """Test that create_document generates a share_id."""
        document_data = DocumentCreate(content="Test content")
        
        result = await document_service.create_document(document_data)
        
        assert result.share_id == "test-hrid-0"
        assert len(mock_hrid_generator.generated_ids) == 1
    
    async def test_create_document_handles_database_error(self, document_service, mock_document_repository):
        """Test that service handles database errors properly."""
        document_data = DocumentCreate(content="Test content")
        mock_document_repository.should_raise_on_create = True
        
        with pytest.raises(RuntimeError, match="Failed to create document"):
            await document_service.create_document(document_data)
    
    async def test_create_document_calls_repository(self, document_service, mock_document_repository):
        """Test that create_document calls the repository create method."""
        document_data = DocumentCreate(content="Test content")
        
        await document_service.create_document(document_data)
        
        assert mock_document_repository.create_called
        assert "test-hrid-0" in mock_document_repository.documents


@pytest.mark.asyncio
class TestDocumentServiceGet:
    """Test DocumentService get_document method."""
    
    async def test_get_document_success(self, document_service, mock_document_repository):
        """Test successfully retrieving a document."""
        document_data = DocumentCreate(content="Test content")
        created = await document_service.create_document(document_data)
        
        result = await document_service.get_document(created.share_id)
        
        assert result is not None
        assert result.share_id == created.share_id
        assert result.content == "Test content"
        assert mock_document_repository.find_called
    
    async def test_get_document_not_found(self, document_service):
        """Test retrieving non-existent document returns None."""
        result = await document_service.get_document("nonexistent-id")
        
        assert result is None
    
    async def test_get_document_handles_database_error(self, document_service, mock_document_repository):
        """Test that service handles database errors during retrieval."""
        mock_document_repository.should_raise_on_find = True
        
        with pytest.raises(RuntimeError, match="Failed to retrieve document"):
            await document_service.get_document("test-id")
    
    async def test_get_document_returns_correct_type(self, document_service):
        """Test that get_document returns DocumentResponse type."""
        document_data = DocumentCreate(content="Test content")
        created = await document_service.create_document(document_data)
        
        result = await document_service.get_document(created.share_id)
        
        assert isinstance(result, DocumentResponse)


@pytest.mark.asyncio
class TestDocumentServiceUpdate:
    """Test DocumentService update_document method."""
    
    async def test_update_document_success(self, document_service, mock_document_repository):
        """Test successfully updating a document."""
        document_data = DocumentCreate(content="Original content")
        created = await document_service.create_document(document_data)
        
        update_data = DocumentUpdate(content="Updated content")
        result = await document_service.update_document(created.share_id, update_data)
        
        assert result is not None
        assert result.share_id == created.share_id
        assert result.content == "Updated content"
        assert mock_document_repository.update_called
    
    async def test_update_document_not_found(self, document_service):
        """Test updating non-existent document returns None."""
        update_data = DocumentUpdate(content="Updated content")
        
        result = await document_service.update_document("nonexistent-id", update_data)
        
        assert result is None
    
    async def test_update_document_handles_database_error(self, document_service, mock_document_repository):
        """Test that service handles database errors during update."""
        mock_document_repository.should_raise_on_update = True
        
        update_data = DocumentUpdate(content="Updated content")
        
        with pytest.raises(RuntimeError, match="Failed to update document"):
            await document_service.update_document("test-id", update_data)
    
    async def test_update_document_updates_timestamp(self, document_service):
        """Test that update_document updates the updated_at timestamp."""
        document_data = DocumentCreate(content="Original content")
        created = await document_service.create_document(document_data)
        original_time = created.updated_at
        
        await asyncio.sleep(0.01)
        
        update_data = DocumentUpdate(content="Updated content")
        result = await document_service.update_document(created.share_id, update_data)
        
        assert result.updated_at > original_time
        assert result.created_at == created.created_at
    
    async def test_update_document_calls_repository(self, document_service, mock_document_repository):
        """Test that update_document calls the repository update method."""
        document_data = DocumentCreate(content="Original content")
        created = await document_service.create_document(document_data)
        
        update_data = DocumentUpdate(content="Updated content")
        await document_service.update_document(created.share_id, update_data)
        
        assert mock_document_repository.update_called
    
    async def test_update_document_preserves_share_id(self, document_service):
        """Test that update doesn't change the share_id."""
        document_data = DocumentCreate(content="Original content")
        created = await document_service.create_document(document_data)
        
        update_data = DocumentUpdate(content="Updated content")
        result = await document_service.update_document(created.share_id, update_data)
        
        assert result.share_id == created.share_id


@pytest.mark.asyncio
class TestDocumentServiceEdgeCases:
    """Test edge cases and error handling."""
    
    async def test_service_handles_none_content_gracefully(self):
        """Test service handles unexpected None values."""
        with pytest.raises(ValueError):
            DocumentCreate(content=None)
    
    async def test_service_rejects_invalid_content_type(self):
        """Test service rejects non-string content."""
        with pytest.raises((ValueError, TypeError)):
            DocumentCreate(content=12345)
    
    async def test_concurrent_creates_dont_conflict(self, mock_hrid_generator, mock_document_repository):
        """Test that concurrent document creates work independently."""
        from src.services.document_service import DocumentService
        
        mock_hrid_generator.fixed_ids = ["id-1", "id-2", "id-3"]
        service = DocumentService(mock_hrid_generator, mock_document_repository)
        
        doc1 = DocumentCreate(content="Doc 1")
        doc2 = DocumentCreate(content="Doc 2")
        doc3 = DocumentCreate(content="Doc 3")
        
        results = await asyncio.gather(
            service.create_document(doc1),
            service.create_document(doc2),
            service.create_document(doc3)
        )
        
        share_ids = [r.share_id for r in results]
        assert len(set(share_ids)) == 3
        assert "id-1" in share_ids
        assert "id-2" in share_ids
        assert "id-3" in share_ids
