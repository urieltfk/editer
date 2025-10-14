"""
HRID Service - Singleton for generating human-readable IDs across the application.
"""

import logging
from typing import Optional
from hrid import HRID
from src.protocols.hrid_protocol import HRIDGeneratorProtocol
from uuid import uuid4

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
            seed = str(uuid4())
            self._hrid = HRID(seed=seed)
            logger.info(f"HRID service initialized with seed: {seed[:10]}...")
        except Exception as e:
            logger.error(f"Failed to initialize HRID service: {e}")
            raise RuntimeError(f"HRID initialization failed: {e}")
    
    def generate_id(self) -> str:
        """
        Generate a new human-readable ID.
        
        Returns:
            str: A URL-safe human-readable ID (e.g., "abc123def")
        """
        try:
            if self._hrid is None:
                self._initialize_hrid()
            
            hrid_value = self._hrid.generate()
            url_safe_hrid = hrid_value.replace(' ', '-')
            logger.debug(f"Generated HRID: {url_safe_hrid}")
            return url_safe_hrid
            
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


# Global HRID service instance
hrid_service = HRIDService()

def generate_hrid() -> str:
    """
    Convenience function to generate a single HRID.
    
    Returns:
        str: A human-readable ID
    """
    return hrid_service.generate_id()

def get_hrid_generator() -> HRIDGeneratorProtocol:
    """
    Get the HRID generator instance.
    
    Returns:
        HRIDGeneratorProtocol: HRID generator service
    """
    return hrid_service