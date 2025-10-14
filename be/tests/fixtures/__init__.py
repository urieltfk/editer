"""
Test fixtures and mock implementations for dependency injection.
"""

from .mock_hrid_generator import MockHRIDGenerator
from .mock_document_repository import MockDocumentRepository

__all__ = ["MockHRIDGenerator", "MockDocumentRepository"]

