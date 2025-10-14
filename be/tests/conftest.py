"""
Pytest configuration and shared fixtures.
"""
import os
import pytest

os.environ["DEBUG"] = "False"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
os.environ["DATABASE_NAME"] = "test_editer"
os.environ["HRID_SEED"] = "test-seed-for-testing-123"

from tests.fixtures import MockHRIDGenerator, MockDocumentRepository
from src.services.document_service import DocumentService


@pytest.fixture
def mock_hrid_generator():
    """Fixture providing a mock HRID generator."""
    return MockHRIDGenerator()


@pytest.fixture
def mock_document_repository():
    """Fixture providing a mock document repository."""
    return MockDocumentRepository()


@pytest.fixture
def document_service(mock_hrid_generator, mock_document_repository):
    """Fixture providing a DocumentService with injected mocks."""
    return DocumentService(
        hrid_generator=mock_hrid_generator,
        document_repository=mock_document_repository
    )
