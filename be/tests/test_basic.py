"""
Basic tests that don't require database connections.
"""
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns healthy status."""
        with TestClient(app) as client:
            response = client.get("/health")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == "healthy"
            assert data["service"] == "editer-api"
            assert "version" in data


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns welcome message."""
        with TestClient(app) as client:
            response = client.get("/")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "message" in data
            assert "Welcome to Editer API" in data["message"]
            assert "docs" in data
            assert "health" in data


class TestDocumentEndpoints:
    """Test document CRUD endpoints with mocked database."""
    
    @patch('src.services.document_service.document_service.create_document')
    def test_create_document_success(self, mock_create):
        """Test creating a new document successfully."""
        # Import the DocumentResponse model
        from src.models.document import DocumentResponse
        from datetime import datetime, UTC
        
        # Mock the service response with proper DocumentResponse object
        mock_response = DocumentResponse(
            id="test_id_123",
            share_id="abc123def",
            content="This is a test document",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            schema_version=1
        )
        mock_create.return_value = mock_response
        
        with TestClient(app) as client:
            document_data = {
                "content": "This is a test document"
            }
            
            response = client.post("/api/v1/documents", json=document_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["share_id"] == "abc123def"
            assert data["content"] == "This is a test document"
            assert "created_at" in data
            assert "updated_at" in data
    
    @patch('src.services.document_service.document_service.get_document')
    def test_get_document_success(self, mock_get):
        """Test retrieving a document successfully."""
        # Import the DocumentResponse model
        from src.models.document import DocumentResponse
        from datetime import datetime, UTC
        
        # Mock the service response with proper DocumentResponse object
        mock_response = DocumentResponse(
            id="test_id_123",
            share_id="abc123def",
            content="This is a test document",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            schema_version=1
        )
        mock_get.return_value = mock_response
        
        with TestClient(app) as client:
            response = client.get("/api/v1/documents/abc123def")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["share_id"] == "abc123def"
            assert data["content"] == "This is a test document"
    
    @patch('src.services.document_service.document_service.get_document')
    def test_get_nonexistent_document(self, mock_get):
        """Test retrieving a document that doesn't exist."""
        # Mock the service to return None (not found)
        mock_get.return_value = None
        
        with TestClient(app) as client:
            response = client.get("/api/v1/documents/nonexistent123")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "not found" in data["detail"].lower()
    
    @patch('src.services.document_service.document_service.update_document')
    def test_update_document_success(self, mock_update):
        """Test updating a document successfully."""
        # Import the DocumentResponse model
        from src.models.document import DocumentResponse
        from datetime import datetime, UTC
        
        # Mock the service response with proper DocumentResponse object
        mock_response = DocumentResponse(
            id="test_id_123",
            share_id="abc123def",
            content="This is updated content",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            schema_version=1
        )
        mock_update.return_value = mock_response
        
        with TestClient(app) as client:
            update_data = {
                "content": "This is updated content"
            }
            
            response = client.put(
                "/api/v1/documents/abc123def",
                json=update_data
            )
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["share_id"] == "abc123def"
            assert data["content"] == "This is updated content"
    
    @patch('src.services.document_service.document_service.update_document')
    def test_update_nonexistent_document(self, mock_update):
        """Test updating a document that doesn't exist."""
        # Mock the service to return None (not found)
        mock_update.return_value = None
        
        with TestClient(app) as client:
            update_data = {
                "content": "This is updated content"
            }
            
            response = client.put(
                "/api/v1/documents/nonexistent123",
                json=update_data
            )
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "not found" in data["detail"].lower()
    
    def test_create_document_empty_content(self):
        """Test creating a document with empty content fails."""
        with TestClient(app) as client:
            document_data = {
                "content": ""
            }
            
            response = client.post("/api/v1/documents", json=document_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_document_missing_content(self):
        """Test creating a document without content fails."""
        with TestClient(app) as client:
            document_data = {}
            
            response = client.post("/api/v1/documents", json=document_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
