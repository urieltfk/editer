"""
Basic tests that don't require database connections.
"""
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.services.document_service import get_document_service
from tests.fixtures import MockHRIDGenerator, MockDocumentRepository
from src.services.document_service import DocumentService


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
    
    def test_create_document_success(self):
        """Test creating a new document successfully."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["abc123def"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
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
        finally:
            app.dependency_overrides.clear()
    
    def test_get_document_success(self):
        """Test retrieving a document successfully."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["abc123def"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                doc_data = {"content": "This is a test document"}
                client.post("/api/v1/documents", json=doc_data)
                
                response = client.get("/api/v1/documents/abc123def")
                
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert data["share_id"] == "abc123def"
                assert data["content"] == "This is a test document"
        finally:
            app.dependency_overrides.clear()
    
    def test_get_nonexistent_document(self):
        """Test retrieving a document that doesn't exist."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                response = client.get("/api/v1/documents/nonexistent123")
                
                assert response.status_code == status.HTTP_404_NOT_FOUND
                data = response.json()
                assert "not found" in data["detail"].lower()
        finally:
            app.dependency_overrides.clear()
    
    def test_update_document_success(self):
        """Test updating a document successfully."""
        mock_hrid_gen = MockHRIDGenerator(fixed_ids=["abc123def"])
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                doc_data = {"content": "Original content"}
                client.post("/api/v1/documents", json=doc_data)
                
                update_data = {"content": "This is updated content"}
                response = client.put("/api/v1/documents/abc123def", json=update_data)
                
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert data["share_id"] == "abc123def"
                assert data["content"] == "This is updated content"
        finally:
            app.dependency_overrides.clear()
    
    def test_update_nonexistent_document(self):
        """Test updating a document that doesn't exist."""
        mock_hrid_gen = MockHRIDGenerator()
        mock_repo = MockDocumentRepository()
        mock_service = DocumentService(mock_hrid_gen, mock_repo)
        
        app.dependency_overrides[get_document_service] = lambda: mock_service
        
        try:
            with TestClient(app) as client:
                update_data = {"content": "This is updated content"}
                response = client.put("/api/v1/documents/nonexistent123", json=update_data)
                
                assert response.status_code == status.HTTP_404_NOT_FOUND
                data = response.json()
                assert "not found" in data["detail"].lower()
        finally:
            app.dependency_overrides.clear()
    
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
