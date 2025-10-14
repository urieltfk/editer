"""
Mock HRID generator for testing.
"""

from typing import List


class MockHRIDGenerator:
    """Mock implementation of HRIDGeneratorProtocol for testing."""
    
    def __init__(self, fixed_ids: List[str] = None):
        """
        Initialize mock HRID generator.
        
        Args:
            fixed_ids: Optional list of IDs to return in sequence. 
                      If not provided, generates predictable IDs.
        """
        self.fixed_ids = fixed_ids or []
        self.call_count = 0
        self.generated_ids: List[str] = []
    
    def generate_id(self) -> str:
        """
        Generate a mock HRID.
        
        Returns:
            str: A predictable test ID
        """
        if self.fixed_ids and self.call_count < len(self.fixed_ids):
            hrid = self.fixed_ids[self.call_count]
        else:
            hrid = f"test-hrid-{self.call_count}"
        
        self.call_count += 1
        self.generated_ids.append(hrid)
        return hrid
    
    def reset(self):
        """Reset the generator state."""
        self.call_count = 0
        self.generated_ids = []

