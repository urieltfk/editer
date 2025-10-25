# GitHub Actions CI/CD

This directory contains GitHub Actions workflows for the Editer project.

## Workflows

### CI Workflow (`ci.yml`)

The main CI workflow that runs on:
- Push to `main` and `develop` branches
- Pull requests to `main` and `develop` branches  
- Manual trigger via `workflow_dispatch`

#### Jobs

1. **Docker Build** (`docker-build`)
   - Builds the backend Docker image
   - Verifies the image can start and respond to health checks
   - Runs independently for faster feedback

2. **Backend Tests** (`backend-tests`)
   - Depends on successful Docker build
   - Sets up Python 3.11 environment
   - Installs dependencies with caching
   - Spins up MongoDB 7.0 service
   - Runs the full pytest test suite
   - Tests Docker container integration with MongoDB

#### Environment Variables

The workflow sets up the following environment variables for testing:
- `MONGODB_URL`: mongodb://localhost:27017
- `DATABASE_NAME`: test_editer  
- `DEBUG`: False
- `HRID_SEED`: test-seed-for-testing-123
- `API_HOST`: 0.0.0.0
- `API_PORT`: 8000

#### Features

- **Caching**: Pip dependencies are cached for faster builds
- **Health Checks**: MongoDB service includes health checks
- **Parallel Execution**: Docker build and tests run in parallel where possible
- **Comprehensive Testing**: Tests both direct Python execution and Docker container execution
- **Error Handling**: Proper timeout and error handling for all steps

## Usage

The workflow will automatically run when you:
1. Push code to `main` or `develop` branches
2. Create a pull request to `main` or `develop` branches
3. Manually trigger it from the GitHub Actions tab

## Monitoring

Check the workflow status in the GitHub Actions tab of your repository. The workflow provides detailed logs for each step, making it easy to debug any issues.

