"""
HRID Service - Singleton for generating human-readable IDs across the application.
"""

import logging
from typing import Optional
from hrid import HRID
from ..settings import settings

logger = logging.getLogger(__name__)


class HRIDService:
    """
    Singleton service for generating human-readable IDs using HRID.
    Uses a consistent seed from environment configuration.
    """
    
    _instance: Optional['HRIDService'] = None
    _hrid: Optional[HRID] = None
    
    def __new__(cls) -> 'HRIDService':
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize HRID with seed from settings."""
        if not hasattr(self, '_initialized'):
            self._initialize_hrid()
            self._initialized = True
    
    def _initialize_hrid(self) -> None:
        """Initialize HRID with the configured seed."""
        try:
            self._hrid = HRID(seed=settings.hrid_seed)
            logger.info(f"HRID service initialized with seed: {settings.hrid_seed[:10]}...")
        except Exception as e:
            logger.error(f"Failed to initialize HRID service: {e}")
            raise RuntimeError(f"HRID initialization failed: {e}")
    
    def generate_id(self) -> str:
        """
        Generate a new human-readable ID.
        
        Returns:
            str: A human-readable ID (e.g., "abc123def")
        """
        try:
            if self._hrid is None:
                self._initialize_hrid()
            
            hrid_value = self._hrid.generate()
            logger.debug(f"Generated HRID: {hrid_value}")
            return hrid_value
            
        except Exception as e:
            logger.error(f"Failed to generate HRID: {e}")
            raise RuntimeError(f"HRID generation failed: {e}")
    
    def generate_multiple(self, count: int) -> list[str]:
        """
        Generate multiple human-readable IDs.
        
        Args:
            count: Number of IDs to generate
            
        Returns:
            list[str]: List of human-readable IDs
        """
        try:
            if self._hrid is None:
                self._initialize_hrid()
            
            ids = []
            for _ in range(count):
                ids.append(self._hrid.generate())
            
            logger.debug(f"Generated {count} HRIDs")
            return ids
            
        except Exception as e:
            logger.error(f"Failed to generate multiple HRIDs: {e}")
            raise RuntimeError(f"HRID generation failed: {e}")
    
    def get_seed(self) -> str:
        """Get the current HRID seed."""
        return settings.hrid_seed
    
    def reset_seed(self, new_seed: str) -> None:
        """
        Reset HRID with a new seed.
        Note: This will change the ID generation pattern.
        
        Args:
            new_seed: New seed for HRID generation
        """
        try:
            self._hrid = HRID(seed=new_seed)
            logger.info(f"HRID seed reset to: {new_seed[:10]}...")
        except Exception as e:
            logger.error(f"Failed to reset HRID seed: {e}")
            raise RuntimeError(f"HRID seed reset failed: {e}")


# Global HRID service instance
hrid_service = HRIDService()


def get_hrid_service() -> HRIDService:
    """
    Get the global HRID service instance.
    
    Returns:
        HRIDService: The singleton HRID service instance
    """
    return hrid_service


def generate_hrid() -> str:
    """
    Convenience function to generate a single HRID.
    
    Returns:
        str: A human-readable ID
    """
    return hrid_service.generate_id()
