from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, UTC
from bson import ObjectId
from src.settings import settings


class Document(BaseModel):
    """
    Document model for MongoDB storage.
    Represents a text document with both internal ID and human-readable shareable ID.
    """
    
    # MongoDB ObjectId (internal)
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    
    share_id: str = Field(..., description="Human-readable ID for sharing and public access")

    content: str = Field(default="", max_length=settings.max_content_length)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    view_count: int = Field(default=0, ge=0)
    last_accessed: Optional[datetime] = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        # Use share_id as the primary identifier for API responses
        populate_by_name = True
    
    def update_timestamps(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now(UTC)
    
    def increment_view_count(self):
        """Increment view count and update last accessed"""
        self.view_count += 1
        self.last_accessed = datetime.now(UTC)
