"""
Unit tests for DocumentService layer.
Tests service methods directly with mocked database operations.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, UTC

from src.services.document_service import DocumentService
from src.models.document import Document, DocumentCreate, DocumentUpdate, DocumentResponse


@pytest.mark.asyncio
class TestDocumentServiceCreate:
    """Test DocumentService create_document method."""
    
    async def test_create_document_success(self):
        """Test successful document creation through service."""
        service = DocumentService()
        document_data = DocumentCreate(content="Test content")
        
        mock_doc = MagicMock()
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-hrid-123"
        mock_doc.content = "Test content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.insert = AsyncMock()
        
        with patch('src.services.document_service.Document', return_value=mock_doc):
            with patch('src.services.document_service.generate_hrid', return_value="test-hrid-123"):
                result = await service.create_document(document_data)
                
                assert result.share_id == "test-hrid-123"
                assert result.content == "Test content"
                assert result.created_at is not None
                assert result.updated_at is not None
                mock_doc.insert.assert_called_once()
    
    async def test_create_document_generates_unique_share_id(self):
        """Test that create_document generates a share_id."""
        service = DocumentService()
        document_data = DocumentCreate(content="Test content")
        
        mock_doc = MagicMock()
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "unique-id-456"
        mock_doc.content = "Test content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.insert = AsyncMock()
        
        with patch('src.services.document_service.Document', return_value=mock_doc):
            with patch('src.services.document_service.generate_hrid', return_value="unique-id-456"):
                result = await service.create_document(document_data)
                
                assert result.share_id == "unique-id-456"
    
    async def test_create_document_handles_database_error(self):
        """Test that service handles database errors properly."""
        service = DocumentService()
        document_data = DocumentCreate(content="Test content")
        
        mock_doc = MagicMock()
        mock_doc.insert = AsyncMock(side_effect=Exception("Database connection failed"))
        
        with patch('src.services.document_service.Document', return_value=mock_doc):
            with patch('src.services.document_service.generate_hrid', return_value="test-hrid"):
                with pytest.raises(RuntimeError, match="Failed to create document"):
                    await service.create_document(document_data)
    
    async def test_create_document_calls_insert(self):
        """Test that create_document calls the database insert method."""
        service = DocumentService()
        document_data = DocumentCreate(content="Test content")
        
        mock_doc = MagicMock()
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-hrid"
        mock_doc.content = "Test content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.insert = AsyncMock()
        
        with patch('src.services.document_service.Document', return_value=mock_doc):
            with patch('src.services.document_service.generate_hrid', return_value="test-hrid"):
                await service.create_document(document_data)
                
                assert mock_doc.insert.called


@pytest.mark.asyncio
class TestDocumentServiceGet:
    """Test DocumentService get_document method."""
    
    async def test_get_document_success(self):
        """Test successfully retrieving a document."""
        service = DocumentService()
        
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-share-id"
        mock_doc.content = "Test content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            result = await service.get_document("test-share-id")
            
            assert result is not None
            assert result.share_id == "test-share-id"
            assert result.content == "Test content"
            MockDocument.find_one.assert_called_once()
    
    async def test_get_document_not_found(self):
        """Test retrieving non-existent document returns None."""
        service = DocumentService()
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=None)
            
            result = await service.get_document("nonexistent-id")
            
            assert result is None
    
    async def test_get_document_handles_database_error(self):
        """Test that service handles database errors during retrieval."""
        service = DocumentService()
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(side_effect=Exception("Database query failed"))
            
            with pytest.raises(RuntimeError, match="Failed to retrieve document"):
                await service.get_document("test-id")
    
    async def test_get_document_returns_correct_type(self):
        """Test that get_document returns DocumentResponse type."""
        service = DocumentService()
        
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-id"
        mock_doc.content = "Test"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            result = await service.get_document("test-id")
            
            assert isinstance(result, DocumentResponse)


@pytest.mark.asyncio
class TestDocumentServiceUpdate:
    """Test DocumentService update_document method."""
    
    async def test_update_document_success(self):
        """Test successfully updating a document."""
        service = DocumentService()
        
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-share-id"
        mock_doc.content = "Original content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.save = AsyncMock()
        
        update_data = DocumentUpdate(content="Updated content")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            result = await service.update_document("test-share-id", update_data)
            
            assert result is not None
            assert result.share_id == "test-share-id"
            assert result.content == "Updated content"
            assert mock_doc.save.called
    
    async def test_update_document_not_found(self):
        """Test updating non-existent document returns None."""
        service = DocumentService()
        update_data = DocumentUpdate(content="Updated content")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=None)
            
            result = await service.update_document("nonexistent-id", update_data)
            
            assert result is None
    
    async def test_update_document_handles_database_error(self):
        """Test that service handles database errors during update."""
        service = DocumentService()
        update_data = DocumentUpdate(content="Updated content")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(side_effect=Exception("Database error"))
            
            with pytest.raises(RuntimeError, match="Failed to update document"):
                await service.update_document("test-id", update_data)
    
    async def test_update_document_updates_timestamp(self):
        """Test that update_document updates the updated_at timestamp."""
        service = DocumentService()
        
        original_time = datetime(2024, 1, 1, tzinfo=UTC)
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-id"
        mock_doc.content = "Original"
        mock_doc.created_at = original_time
        mock_doc.updated_at = original_time
        mock_doc.save = AsyncMock()
        
        update_data = DocumentUpdate(content="Updated")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            result = await service.update_document("test-id", update_data)
            
            assert result.updated_at > original_time
            assert result.created_at == original_time
    
    async def test_update_document_calls_save(self):
        """Test that update_document calls the save method."""
        service = DocumentService()
        
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "test-id"
        mock_doc.content = "Original"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.save = AsyncMock()
        
        update_data = DocumentUpdate(content="Updated")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            await service.update_document("test-id", update_data)
            
            mock_doc.save.assert_called_once()
    
    async def test_update_document_preserves_share_id(self):
        """Test that update doesn't change the share_id."""
        service = DocumentService()
        
        mock_doc = MagicMock(spec=Document)
        mock_doc.id = "507f1f77bcf86cd799439011"
        mock_doc.share_id = "original-share-id"
        mock_doc.content = "Original content"
        mock_doc.created_at = datetime.now(UTC)
        mock_doc.updated_at = datetime.now(UTC)
        mock_doc.save = AsyncMock()
        
        update_data = DocumentUpdate(content="Updated content")
        
        with patch('src.services.document_service.Document') as MockDocument:
            MockDocument.find_one = AsyncMock(return_value=mock_doc)
            
            result = await service.update_document("original-share-id", update_data)
            
            assert result.share_id == "original-share-id"


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
    
    async def test_concurrent_creates_dont_conflict(self):
        """Test that concurrent document creates work independently."""
        service = DocumentService()
        
        def create_mock_doc(share_id, content):
            mock_doc = MagicMock()
            mock_doc.id = "507f1f77bcf86cd799439011"
            mock_doc.share_id = share_id
            mock_doc.content = content
            mock_doc.created_at = datetime.now(UTC)
            mock_doc.updated_at = datetime.now(UTC)
            mock_doc.insert = AsyncMock()
            return mock_doc
        
        mock_docs = [
            create_mock_doc("id-1", "Doc 1"),
            create_mock_doc("id-2", "Doc 2"),
            create_mock_doc("id-3", "Doc 3")
        ]
        
        with patch('src.services.document_service.Document', side_effect=mock_docs):
            with patch('src.services.document_service.generate_hrid') as mock_hrid:
                mock_hrid.side_effect = ["id-1", "id-2", "id-3"]
                
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


import asyncio

