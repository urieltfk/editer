from pydantic import BaseModel, Field, field_validator
from beanie import Document as BeanieDocument
from typing import Optional
from datetime import datetime, UTC
from ..services.hrid_service import generate_hrid


class DocumentBase(BaseModel):
    """Base document model with common fields."""
    content: str = Field(..., description="Document content")


class DocumentCreate(DocumentBase):
    """Model for creating a new document."""
    
    @field_validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        if len(v) > 1 * 1024 * 1024:  # 1MB limit
            raise ValueError('Content exceeds maximum length')
        return v.strip()


class DocumentUpdate(BaseModel):
    """Model for updating an existing document."""
    content: str = Field(..., description="Updated document content")
    
    @field_validator('content')
    def validate_content(cls, v):
        if v is not None:
            if len(v) > 1 * 1024 * 1024:  # 1MB limit
                raise ValueError('Content exceeds maximum length')
            return v  # Don't strip, preserve whitespace
        return v


class DocumentResponse(BaseModel):
    """Model for document API responses."""
    id: str = Field(..., description="Internal document ID")
    share_id: str = Field(..., description="Human-readable ID for sharing")
    content: str = Field(..., description="Document content")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Document(BeanieDocument):
    """
    Beanie document model for database operations.
    Represents a text document with shareable ID.
    MongoDB will auto-generate the _id field (ObjectId/UUID).
    """
    
    share_id: str = Field(..., description="Human-readable ID for sharing and public access")
    content: str = Field(default="", description="Document content")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    schema_version: int = Field(default=1, description="Schema version for migrations")
    
    class Settings:
        name = "documents"
        indexes = [
            "share_id",  # Index for fast lookups
        ]
    
    @staticmethod
    def generate_share_id() -> str:
        """Generate a human-readable share ID using HRID service."""
        return generate_hrid()
