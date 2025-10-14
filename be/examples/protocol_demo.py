"""
Demonstration of how Protocols enforce type safety.
"""
from src.protocols.hrid_protocol import HRIDGeneratorProtocol
from src.protocols.repository_protocol import DocumentRepositoryProtocol
from src.services.document_service import DocumentService


# ✅ VALID: This class satisfies HRIDGeneratorProtocol
class ValidGenerator:
    def generate_id(self) -> str:
        return "valid-id"


# ❌ INVALID: Missing generate_id method
class InvalidGenerator1:
    def create_id(self) -> str:  # Wrong method name!
        return "invalid"


# ❌ INVALID: Wrong return type
class InvalidGenerator2:
    def generate_id(self) -> int:  # Should return str!
        return 123


# ❌ INVALID: Wrong signature (takes parameter)
class InvalidGenerator3:
    def generate_id(self, count: int) -> str:  # Extra parameter!
        return "invalid"


# ✅ VALID: Can pass a valid generator to DocumentService
def test_valid():
    valid_gen = ValidGenerator()
    # This would need a valid repository too, but demonstrates the point
    # service = DocumentService(valid_gen, valid_repo)


# ❌ INVALID: Type checker will complain about these
def test_invalid():
    # Each of these will show a type error in your IDE/mypy
    
    # Error: InvalidGenerator1 doesn't have generate_id method
    # service1 = DocumentService(InvalidGenerator1(), mock_repo)
    
    # Error: InvalidGenerator2.generate_id returns int, not str
    # service2 = DocumentService(InvalidGenerator2(), mock_repo)
    
    # Error: InvalidGenerator3.generate_id has wrong signature
    # service3 = DocumentService(InvalidGenerator3(), mock_repo)
    pass


# ✅ VALID: HRIDService satisfies the protocol (structural typing)
from src.services.hrid_service import HRIDService

def test_real_service():
    """HRIDService automatically satisfies HRIDGeneratorProtocol"""
    hrid_service = HRIDService()
    
    # Type checker verifies this is valid because HRIDService
    # has a generate_id() -> str method
    gen: HRIDGeneratorProtocol = hrid_service  # ✅ Works!

