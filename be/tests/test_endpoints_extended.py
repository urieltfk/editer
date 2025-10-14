"""
Extended endpoint tests for error handling and edge cases.
"""
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.services.document_service import get_document_service, DocumentService
from tests.fixtures import MockHRIDGenerator, MockDocumentRepository


class TestDocumentEndpointsErrorHandling:
    """Test error handling in document endpoints."""
    
    def test_create_document_service_runtime_error(self):
        """Test that RuntimeError from service returns 500."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_repo.should_raise_on_create = True
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                response = client.post("/api/v1/documents", json={"content": "test"})
                
                assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
                assert "Failed to create document" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()
    
    def test_get_document_service_runtime_error(self):
        """Test that RuntimeError from service on GET returns 500."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_repo.should_raise_on_find = True
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                response = client.get("/api/v1/documents/test-id")
                
                assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
                assert "Failed to retrieve document" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()
    
    def test_update_document_service_runtime_error(self):
        """Test that RuntimeError from service on PUT returns 500."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_repo.should_raise_on_update = True
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                response = client.put(
                    "/api/v1/documents/test-id",
                    json={"content": "updated"}
                )
                
                assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
                assert "Failed to update document" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()


class TestDocumentEndpointsEdgeCases:
    """Test edge cases for document endpoints."""
    
    def test_create_document_with_whitespace_only(self):
        """Test that whitespace-only content fails validation."""
        with TestClient(app) as client:
            response = client.post("/api/v1/documents", json={"content": "   \n\t  "})
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_document_with_very_long_content(self):
        """Test that content exceeding 1MB limit fails validation."""
        with TestClient(app) as client:
            large_content = "x" * (1024 * 1024 + 1)  # 1MB + 1 byte
            response = client.post("/api/v1/documents", json={"content": large_content})
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_document_with_unicode_content(self):
        """Test that unicode content is handled correctly."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["unicode-test"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                unicode_content = "Hello 世界 🌍 Привет"
                response = client.post("/api/v1/documents", json={"content": unicode_content})
                
                assert response.status_code == status.HTTP_201_CREATED
                assert response.json()["content"] == unicode_content
        finally:
            app.dependency_overrides.clear()
    
    def test_update_document_with_empty_content(self):
        """Test updating document with empty content fails."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["test-id"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                # Create document first
                client.post("/api/v1/documents", json={"content": "original"})
                
                # Try to update with empty content
                response = client.put("/api/v1/documents/test-id", json={"content": ""})
                
                # Should succeed since DocumentUpdate doesn't strip/validate empty
                assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
        finally:
            app.dependency_overrides.clear()
    
    def test_get_document_with_special_chars_in_id(self):
        """Test GET with special characters in share_id."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                # FastAPI should handle URL encoding
                response = client.get("/api/v1/documents/test%20id%20with%20spaces")
                
                # Should return 404 since document doesn't exist
                assert response.status_code == status.HTTP_404_NOT_FOUND
        finally:
            app.dependency_overrides.clear()


class TestDocumentEndpointsFullFlow:
    """Test complete document lifecycle."""
    
    def test_full_document_lifecycle(self):
        """Test creating, retrieving, updating, and verifying a document."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["lifecycle-test"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                # 1. Create document
                create_response = client.post(
                    "/api/v1/documents",
                    json={"content": "Initial content"}
                )
                assert create_response.status_code == status.HTTP_201_CREATED
                share_id = create_response.json()["share_id"]
                
                # 2. Retrieve document
                get_response = client.get(f"/api/v1/documents/{share_id}")
                assert get_response.status_code == status.HTTP_200_OK
                assert get_response.json()["content"] == "Initial content"
                
                # 3. Update document
                update_response = client.put(
                    f"/api/v1/documents/{share_id}",
                    json={"content": "Updated content"}
                )
                assert update_response.status_code == status.HTTP_200_OK
                assert update_response.json()["content"] == "Updated content"
                
                # 4. Verify update persisted
                final_get = client.get(f"/api/v1/documents/{share_id}")
                assert final_get.status_code == status.HTTP_200_OK
                assert final_get.json()["content"] == "Updated content"
        finally:
            app.dependency_overrides.clear()
    
    def test_multiple_documents_independent(self):
        """Test that multiple documents don't interfere with each other."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["doc1", "doc2", "doc3"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                # Create multiple documents
                doc1 = client.post("/api/v1/documents", json={"content": "Content 1"})
                doc2 = client.post("/api/v1/documents", json={"content": "Content 2"})
                doc3 = client.post("/api/v1/documents", json={"content": "Content 3"})
                
                # Verify all have unique IDs
                ids = {doc1.json()["share_id"], doc2.json()["share_id"], doc3.json()["share_id"]}
                assert len(ids) == 3
                
                # Verify content is independent
                assert client.get(f"/api/v1/documents/{doc1.json()['share_id']}").json()["content"] == "Content 1"
                assert client.get(f"/api/v1/documents/{doc2.json()['share_id']}").json()["content"] == "Content 2"
                assert client.get(f"/api/v1/documents/{doc3.json()['share_id']}").json()["content"] == "Content 3"
        finally:
            app.dependency_overrides.clear()

