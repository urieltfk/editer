"""
Protocol for HRID generation to enable dependency injection.
"""

from typing import Protocol


class HRIDGeneratorProtocol(Protocol):
    """Protocol defining the interface for HRID generation."""
    
    def generate_id(self) -> str:
        """
        Generate a new human-readable ID.
        
        Returns:
            str: A human-readable ID
        """
        ...

