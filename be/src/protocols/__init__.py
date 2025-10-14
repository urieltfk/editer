"""
Protocol interfaces for dependency injection.
"""

from .hrid_protocol import HRIDGeneratorProtocol
from .repository_protocol import DocumentRepositoryProtocol

__all__ = ["HRIDGeneratorProtocol", "DocumentRepositoryProtocol"]

