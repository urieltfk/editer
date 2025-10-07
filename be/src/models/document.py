from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, UTC


class Document(BaseModel):
    """
    Document model for API responses.
    Represents a text document with shareable ID.
    """
    
    id: Optional[str] = Field(default=None, description="Document ID")
    share_id: str = Field(..., description="Human-readable ID for sharing and public access")
    content: str = Field(default="", description="Document content")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
