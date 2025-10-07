# Editer

A minimalistic, easily shareable, non-authentication-required text editor web application.

## Overview

Editer is a web application designed to provide a simple, distraction-free text editing experience that can be easily shared without requiring user authentication. The focus is on simplicity, speed, and seamless collaboration.

## Features

- **No Authentication Required**: Start editing immediately without signing up
- **Easy Sharing**: Share your documents with simple URLs
- **Minimalistic Interface**: Clean, distraction-free editing experience
- **Real-time Collaboration**: Multiple users can edit simultaneously
- **Cross-platform**: Works on desktop and mobile devices

## Technology Stack

### Frontend
- **React** with **TypeScript** for type-safe, component-based UI
- Modern build tools and development environment
- Responsive design for all device sizes

### Backend
- **Python** with **FastAPI** for high-performance API development
- **Pydantic** for data validation and serialization
- **MongoDB** for flexible document storage
- RESTful API design with automatic OpenAPI documentation

## Project Structure

```
editer/
├── fe/                 # Frontend React application
├── be/                 # Backend FastAPI application
├── README.md           # Project documentation
└── .gitignore         # Git ignore rules
```

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Node.js 18+** (for frontend development)
- **Python 3.11+** (for backend development)
- **MongoDB** (for data storage)

### Quick Start with Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd editer
   ```

2. **Run the entire application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MongoDB: localhost:27017

### Development Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Manual Development Setup

If you prefer to run services individually:

#### Backend Setup
```bash
cd be
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd fe
pnpm install
pnpm run dev
```

#### MongoDB Setup
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or install MongoDB locally
# Follow MongoDB installation guide for your OS
```

## Development Status

🚧 **Currently in development** - Building project structure and core functionality.

## Contributing

This project is in active development. More contribution guidelines will be added as the project matures.

## License

*License information will be added as the project develops.*
