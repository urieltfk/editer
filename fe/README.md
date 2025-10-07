# Editer Frontend

The frontend application for Editer - a minimalistic, easily shareable text editor web application.

## Overview

This is the React + TypeScript frontend for the Editer project, built using Vite for fast development and optimized builds. The application provides a clean, distraction-free text editing interface that can be easily shared without authentication.

## Technology Stack

- **React 18.3.1** - Modern React with hooks and concurrent features
- **TypeScript 5.2.2** - Type-safe JavaScript development
- **Vite 5.3.4** - Fast build tool and development server
- **React Router 6.25.1** - Client-side routing
- **ESLint** - Code linting and quality assurance
- **pnpm** - Fast, disk space efficient package manager

## Project Structure

```
fe/
├── public/                 # Static assets
│   └── vite.svg          # Vite logo
├── src/
│   ├── assets/           # Static assets (images, fonts, etc.)
│   │   └── react.svg     # React logo
│   ├── lib/              # Reusable code assets
│   │   └── hooks/        # Custom React hooks
│   │       └── useAlert.tsx
│   ├── pages/            # Application pages
│   │   ├── App.tsx       # Main app component
│   │   ├── App.css       # App styles
│   │   ├── About.tsx     # About page
│   │   └── ErrorPage.tsx # Error handling page
│   ├── routes/           # Routing configuration
│   │   └── routes.tsx    # Route definitions
│   ├── main.tsx          # Application entry point
│   ├── index.css         # Global styles
│   └── vite-env.d.ts     # Vite type definitions
├── Dockerfile            # Docker configuration
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
├── pnpm-lock.yaml        # Lock file for reproducible installs
└── README.md             # This file
```

## Architecture

The project follows atomic design principles with a clear separation of concerns:

- **Atoms**: Smallest reusable components
- **Molecules**: Groups of atoms that form functional units
- **Organisms**: Complex UI components made of molecules
- **Pages**: Complete page layouts
- **Templates**: Reusable page structures

## Development Setup

### Prerequisites

- **Node.js 18+** - JavaScript runtime
- **pnpm** - Package manager (install with `npm install -g pnpm`)
- **Docker** (optional) - For containerized development

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd fe
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

### Development Commands

- **Start development server**: `pnpm run dev`
- **Build for production**: `pnpm run build`
- **Preview production build**: `pnpm run preview`
- **Run linting**: `pnpm run lint`

### Docker Development

- **Build Docker image**: `docker build -t editer-frontend .`
- **Run container**: `docker run -d --rm -p 8000:8000 editer-frontend`

## Key Features

- **TypeScript Integration**: Full type safety throughout the application
- **Hot Module Replacement**: Instant updates during development
- **Optimized Builds**: Production builds are optimized for performance
- **ESLint Configuration**: Enforced code quality standards
- **React Router**: Client-side navigation with error boundaries
- **Atomic Design**: Scalable component architecture

## Routing

The application uses React Router v6 with the following routes:

- `/` - Main application (App component)
- `/about` - About page
- Error boundaries handle routing errors gracefully

## Development Notes

- The project uses path aliases (`@/`) for cleaner imports
- ESLint is configured with React-specific rules
- TypeScript strict mode is enabled
- The build process includes type checking before compilation

## Integration with Backend

This frontend is designed to work with the FastAPI backend located in the `../be/` directory. The backend provides:

- RESTful API endpoints
- Real-time collaboration features
- Document storage and retrieval
- Shareable document URLs

## Future Enhancements

- Real-time text synchronization
- Collaborative editing features
- Document sharing functionality
- Mobile-responsive design improvements
- Progressive Web App (PWA) capabilities