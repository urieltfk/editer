from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from settings import settings

# Initialize FastAPI app with settings
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug
)

# Configure CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class DocumentCreate(BaseModel):
    title: Optional[str] = "Untitled"
    content: str = ""
    
    class Config:
        # Validate title length
        @classmethod
        def validate_title(cls, v):
            if v and len(v) > settings.max_title_length:
                raise ValueError(f"Title must be less than {settings.max_title_length} characters")
            return v
        
        # Validate content length
        @classmethod
        def validate_content(cls, v):
            if len(v) > settings.max_content_length:
                raise ValueError(f"Content must be less than {settings.max_content_length} characters")
            return v

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    
    class Config:
        # Validate title length
        @classmethod
        def validate_title(cls, v):
            if v and len(v) > settings.max_title_length:
                raise ValueError(f"Title must be less than {settings.max_title_length} characters")
            return v
        
        # Validate content length
        @classmethod
        def validate_content(cls, v):
            if v and len(v) > settings.max_content_length:
                raise ValueError(f"Content must be less than {settings.max_content_length} characters")
            return v

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "editer-api",
        "version": settings.api_version,
        "debug": settings.debug
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Editer API",
        "title": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }

# Document endpoints (placeholder for future implementation)
@app.post("/documents", response_model=DocumentResponse)
async def create_document(document: DocumentCreate):
    # TODO: Implement document creation with MongoDB
    return {
        "id": "placeholder-id",
        "title": document.title,
        "content": document.content,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }

@app.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    # TODO: Implement document retrieval from MongoDB
    return {
        "id": document_id,
        "title": "Sample Document",
        "content": "This is a placeholder document",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }

@app.put("/documents/{document_id}", response_model=DocumentResponse)
async def update_document(document_id: str, document: DocumentUpdate):
    # TODO: Implement document update with MongoDB
    return {
        "id": document_id,
        "title": document.title or "Updated Document",
        "content": document.content or "Updated content",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
