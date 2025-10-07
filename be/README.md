# Editer Backend

The backend API for Editer - a minimalistic, easily shareable text editor web application.

## Overview

This is the FastAPI backend for the Editer project, providing RESTful API endpoints for document management, real-time collaboration, and seamless sharing capabilities. Built with Python, FastAPI, Pydantic, and MongoDB.

## Technology Stack

- **FastAPI 0.104.1** - Modern, fast web framework for building APIs
- **Pydantic 2.5.0** - Data validation and serialization using Python type annotations
- **Uvicorn 0.24.0** - ASGI server for running FastAPI applications
- **PyMongo 4.6.0** - MongoDB driver for Python
- **Python 3.11** - Modern Python with improved performance
- **Docker** - Containerized deployment

## Features

- **RESTful API Design** - Clean, intuitive API endpoints
- **Automatic Documentation** - Interactive API docs at `/docs`
- **Type Safety** - Full type hints with Pydantic validation
- **CORS Support** - Configured for frontend integration
- **Health Monitoring** - Health check endpoints
- **Scalable Architecture** - Ready for MongoDB integration

## Project Structure

```
be/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # This file
└── .env                # Environment variables (to be created)
```

## API Endpoints

### Core Endpoints

- `GET /` - API information and welcome message
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Document Management (Placeholder)

- `POST /documents` - Create a new document
- `GET /documents/{document_id}` - Retrieve a document
- `PUT /documents/{document_id}` - Update a document

## Development Setup

### Prerequisites

- **Python 3.11+** - Python runtime
- **pip** - Python package manager
- **Docker** (optional) - For containerized development
- **MongoDB** (for future implementation)

### Installation

1. Navigate to the backend directory:
   ```bash
   cd be
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Development Commands

- **Start development server**: `uvicorn main:app --reload`
- **Start with custom host/port**: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- **Run directly**: `python main.py`

### Docker Development

- **Build Docker image**: `docker build -t editer-backend .`
- **Run container**: `docker run -d --rm -p 8000:8000 editer-backend`
- **Run with environment file**: `docker run -d --rm -p 8000:8000 --env-file .env editer-backend`

## Environment Configuration

Create a `.env` file in the backend directory:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=editer

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Data Models

### DocumentCreate
```python
{
    "title": "string (optional)",
    "content": "string"
}
```

### DocumentUpdate
```python
{
    "title": "string (optional)",
    "content": "string (optional)"
}
```

### DocumentResponse
```python
{
    "id": "string",
    "title": "string",
    "content": "string",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)"
}
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

## Future Implementation

### Planned Features

- **MongoDB Integration** - Document storage and retrieval
- **Real-time Collaboration** - WebSocket support for live editing
- **Document Sharing** - Unique URL generation and access control
- **Version History** - Document versioning and change tracking
- **User Analytics** - Basic usage statistics
- **Rate Limiting** - API protection and abuse prevention

### Database Schema (Planned)

```javascript
// Documents Collection
{
  _id: ObjectId,
  title: String,
  content: String,
  share_id: String (unique),
  created_at: Date,
  updated_at: Date,
  last_accessed: Date,
  is_public: Boolean
}
```

## Development Notes

- All endpoints currently return placeholder data
- MongoDB integration is planned for the next phase
- CORS is configured for local development
- Health check endpoint for monitoring
- Automatic API documentation generation
- Type-safe request/response models with Pydantic

## Integration with Frontend

This backend is designed to work with the React frontend located in the `../fe/` directory. The frontend will consume these API endpoints for:

- Creating and editing documents
- Real-time collaboration features
- Document sharing functionality
- User interface updates

## Production Considerations

- Environment variable management
- Database connection pooling
- Error handling and logging
- Security headers and validation
- Performance monitoring
- Container orchestration
