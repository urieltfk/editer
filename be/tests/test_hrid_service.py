"""
Unit tests for HRID Service.
Tests human-readable ID generation functionality.
"""
import pytest
from unittest.mock import patch

from src.services.hrid_service import HRIDService, generate_hrid, get_hrid_generator


class TestHRIDServiceInitialization:
    """Test HRID service initialization and singleton behavior."""
    
    def test_hrid_service_is_singleton(self):
        """Test that HRIDService follows singleton pattern."""
        service1 = HRIDService()
        service2 = HRIDService()
        
        assert service1 is service2
    
    def test_hrid_service_initializes_with_seed(self):
        """Test that HRID service initializes with configured seed."""
        service = HRIDService()
        
        assert service._hrid is not None
    
    def test_get_hrid_service_returns_singleton(self):
        """Test that get_hrid_generator returns the global instance."""
        service1 = get_hrid_generator()
        service2 = get_hrid_generator()
        
        assert service1 is service2
    
    def test_hrid_service_initialization_only_once(self):
        """Test that HRID service is initialized only once."""
        service = HRIDService()
        
        assert hasattr(service, '_initialized')
        assert service._initialized is True


class TestHRIDGeneration:
    """Test HRID generation methods."""
    
    def test_generate_id_returns_string(self):
        """Test that generate_id returns a string."""
        service = HRIDService()
        
        hrid = service.generate_id()
        
        assert isinstance(hrid, str)
        assert len(hrid) > 0
    
    def test_generate_id_returns_unique_ids(self):
        """Test that generate_id produces unique IDs."""
        service = HRIDService()
        
        ids = [service.generate_id() for _ in range(100)]
        
        assert len(set(ids)) == 100
    
    def test_generate_hrid_convenience_function(self):
        """Test the convenience function generate_hrid."""
        hrid = generate_hrid()
        
        assert isinstance(hrid, str)
        assert len(hrid) > 0
    
    def test_generate_multiple_returns_list(self):
        """Test that generate_multiple returns a list of IDs."""
        service = HRIDService()
        
        hrids = service.generate_multiple(5)
        
        assert isinstance(hrids, list)
        assert len(hrids) == 5
        assert all(isinstance(h, str) for h in hrids)
    
    def test_generate_multiple_returns_unique_ids(self):
        """Test that generate_multiple produces unique IDs."""
        service = HRIDService()
        
        hrids = service.generate_multiple(50)
        
        assert len(set(hrids)) == 50
    
    def test_generate_multiple_with_zero_count(self):
        """Test generating zero IDs returns empty list."""
        service = HRIDService()
        
        hrids = service.generate_multiple(0)
        
        assert isinstance(hrids, list)
        assert len(hrids) == 0
    
    def test_generate_multiple_with_one_count(self):
        """Test generating single ID with generate_multiple."""
        service = HRIDService()
        
        hrids = service.generate_multiple(1)
        
        assert len(hrids) == 1
        assert isinstance(hrids[0], str)
    
    def test_generated_ids_are_human_readable(self):
        """Test that generated IDs follow human-readable format."""
        service = HRIDService()
        
        hrids = [service.generate_id() for _ in range(10)]
        
        for hrid in hrids:
            assert len(hrid) > 3
            assert hrid.isalnum() or '-' in hrid


class TestHRIDServiceErrorHandling:
    """Test error handling in HRID service."""
    
    def test_generate_id_handles_hrid_library_error(self):
        """Test that service handles errors from HRID library."""
        service = HRIDService()
        
        with patch.object(service._hrid, 'generate') as mock_generate:
            mock_generate.side_effect = Exception("HRID generation failed")
            
            with pytest.raises(RuntimeError, match="HRID generation failed"):
                service.generate_id()
    
    def test_generate_id_reinitializes_if_hrid_is_none(self):
        """Test that generate_id reinitializes if _hrid becomes None."""
        service = HRIDService()
        original_hrid = service._hrid
        
        service._hrid = None
        
        hrid = service.generate_id()
        
        assert service._hrid is not None
        assert isinstance(hrid, str)
        assert len(hrid) > 0


class TestHRIDServiceIntegration:
    """Integration tests for HRID service with document creation."""
    
    def test_hrid_format_is_url_safe(self):
        """Test that generated HRIDs are URL-safe."""
        service = HRIDService()
        
        hrids = [service.generate_id() for _ in range(20)]
        
        for hrid in hrids:
            assert ' ' not in hrid
            assert '\n' not in hrid
            assert '\t' not in hrid
    
    def test_hrid_collision_rate_is_low(self):
        """Test that HRID collision rate is acceptably low."""
        service = HRIDService()
        
        num_ids = 1000
        hrids = [service.generate_id() for _ in range(num_ids)]
        unique_hrids = set(hrids)
        
        assert len(unique_hrids) == num_ids
    
    def test_hrid_consistency_across_calls(self):
        """Test that multiple calls to generate_id work consistently."""
        service = HRIDService()
        
        for _ in range(100):
            hrid = service.generate_id()
            assert isinstance(hrid, str)
            assert len(hrid) > 0
    
    def test_generate_hrid_function_uses_global_service(self):
        """Test that generate_hrid function uses the global service instance."""
        with patch('src.services.hrid_service.hrid_service') as mock_service:
            mock_service.generate_id.return_value = "mocked-hrid"
            
            result = generate_hrid()
            
            assert result == "mocked-hrid"
            mock_service.generate_id.assert_called_once()

