# InferESG Development Instructions

InferESG is an ESG (Environment, Societal and Governance) analysis tool built with React frontend, Python FastAPI backend, Neo4j graph database, and Redis cache. The application helps analyze ESG-related documents and data to identify potential greenwashing.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Quick Start Commands

Copy environment configuration:
```bash
cp .env.example .env
```

**Recommended approach - Docker Compose (full stack):**
```bash
docker compose build  # NEVER CANCEL: Takes 3-4 minutes. Set timeout to 10+ minutes.
docker compose up      # NEVER CANCEL: Startup takes 2-3 minutes for all services.
```

**Alternative - Local development:**
```bash
# Frontend (from ./frontend directory)
npm install           # Takes ~26 seconds. Set timeout to 2+ minutes.
npm start            # Runs on http://localhost:8650

# Backend (from ./backend directory) 
pip install -r requirements.txt  # Takes ~45 seconds. Set timeout to 2+ minutes.
uvicorn src.api:app --port 8250  # Runs on http://localhost:8250
```

## Core Development Workflow

### Environment Setup
1. **ALWAYS** copy `.env.example` to `.env` before starting
2. Configure API keys in `.env` (MISTRAL_KEY, OPENAI_KEY) for LLM functionality
3. Use default values for local development ports and database connections

### Build & Test Commands - CRITICAL TIMEOUTS

**Frontend Commands (run from `./frontend`):**
```bash
npm install                    # ~26 seconds - NEVER CANCEL, timeout: 120s
npm run build                  # ~6 seconds - timeout: 60s  
npm run lint                   # ~2 seconds - timeout: 30s
npm run lint:fix              # Auto-fixes linting issues
npx prettier . --check        # Check code formatting
npm start                      # Development server on port 8650
```

**Backend Commands (run from `./backend`):**
```bash
pip install -r requirements.txt   # ~45 seconds - NEVER CANCEL, timeout: 120s
ruff check                        # ~0.02 seconds - timeout: 30s
ruff format                       # Formats 40+ files automatically
pytest --ignore=tests/BDD -v     # ~4.4 seconds, 144 tests - timeout: 60s
uvicorn src.api:app --port 8250   # Development server on port 8250
```

**Docker Commands:**
```bash
# Individual component builds (for debugging)
docker build -t inferesg/frontend ./frontend           # ~9 seconds - timeout: 300s
docker build -t inferesg/redis ./redis                 # ~0.3 seconds
docker build -t inferesg/data ./data                   # ~0.3 seconds

# Backend requires SSL workaround in sandboxed environments:
docker build --build-arg PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org" -t inferesg/backend ./backend  # ~40 seconds - timeout: 1800s

# Full stack
docker compose build      # NEVER CANCEL: 3-4 minutes total - timeout: 600s
docker compose up         # NEVER CANCEL: 2-3 minutes startup - timeout: 300s
docker compose down       # Clean shutdown
```

## Validation & Testing

### Pre-commit Validation
**ALWAYS run these before committing changes:**
```bash
# Frontend validation
cd frontend
npm run lint && npx prettier . --check

# Backend validation  
cd backend
ruff check && ruff format --check
pytest --ignore=tests/BDD -v
```

### Manual Application Testing
After making changes, **ALWAYS** test functionality:

1. **Start the application** (Docker Compose recommended)
2. **Verify services are healthy:**
   - Frontend: http://localhost:8650 (should load UI)
   - Backend: http://localhost:8250/health (should return JSON)
   - Neo4j: http://localhost:7474 (database browser)
   - Redis: Port 6379 (cache service)

3. **Test basic functionality:**
   - Type "healthcheck" in the frontend UI to verify backend connectivity
   - Verify file upload functionality works
   - Test basic chat/query features

### Common Validation Scenarios
- **After frontend changes**: Build and start frontend, verify UI loads and functions
- **After backend changes**: Run tests, start backend, verify /health endpoint responds
- **After Docker changes**: Build and run full stack, verify all services start properly
- **After dependency changes**: Clean install/rebuild, run full test suite

## Known Issues & Workarounds

### Docker Build SSL Issues
In sandboxed environments, backend Docker build may fail with SSL certificate errors:
**Workaround**: Use trusted hosts flag:
```bash
docker build --build-arg PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org" -t inferesg/backend ./backend
```

### Neo4j Healthcheck Timing
Docker Compose may take 2-3 minutes for Neo4j to become healthy and backend/frontend to start.
**Solution**: Wait patiently, do not cancel. Check status with `docker compose ps`.

### Code Formatting Required
Backend code requires formatting before CI passes:
```bash
cd backend
ruff format  # Automatically formats ~40 files
```

### Environment Variables
Some .env variables are optional but generate warnings:
- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_STORAGE_CONTAINER_NAME` 
- `AZURE_INITIAL_DATA_FILENAME`
- `AGENT_CLASS_MODEL`

These warnings are safe to ignore for local development.

## Project Structure & Key Files

### Frontend (`./frontend`)
- **Technology**: React 18, TypeScript, Webpack 5
- **Key files**: `src/`, `package.json`, `webpack.config.js`
- **Linting**: ESLint + Prettier configuration
- **Port**: 8650

### Backend (`./backend`) 
- **Technology**: Python 3.12, FastAPI, agents/supervisors pattern
- **Key directories**: `src/agents/`, `src/directors/`, `src/utils/`
- **Testing**: pytest with 144 tests
- **Linting**: Ruff (configured in `ruff.toml`)
- **Port**: 8250

### Database & Cache
- **Neo4j**: Graph database on port 7474 (HTTP), 7687 (Bolt)
- **Redis**: Cache service on port 6379
- **Docker**: Full stack orchestration in `compose.yml`

## GitHub Actions CI/CD

The repository includes automated workflows:
- **Frontend linting**: ESLint and Prettier checks
- **Backend linting**: Ruff format and style checks  
- **Backend testing**: pytest with coverage
- **Type checking**: Backend type validation

**All CI checks must pass before merging.**

## Troubleshooting

### Build Failures
1. **Frontend npm install fails**: Clear node_modules, retry with longer timeout
2. **Backend pip install fails**: Check Python version (requires 3.12), use virtual environment
3. **Docker build fails**: Use SSL workarounds, check Docker daemon status
4. **Tests fail**: Run `ruff format` first, check for missing dependencies

### Runtime Issues
1. **Frontend won't start**: Check if port 8650 is available, verify npm install completed
2. **Backend won't start**: Verify database connection, check .env configuration
3. **Database connection fails**: Ensure Neo4j is running, check port 7687 accessibility
4. **Services not healthy**: Wait for healthchecks, verify inter-service networking

### Development Tips
- **Use Docker Compose** for full stack development to avoid service dependency issues
- **Run tests frequently** during development to catch issues early
- **Format code before committing** to avoid CI failures
- **Check logs** in Docker Compose output for detailed error information
- **Test locally** before pushing to verify changes work in full environment

## Dependencies & Versions

- **Node.js**: Version 21 (frontend)
- **Python**: Version 3.12 (backend)
- **Neo4j**: Latest community edition
- **Redis**: Latest with modules (search, timeseries, JSON)
- **Docker**: Latest version with Compose V2

**Critical reminder**: NEVER CANCEL long-running build commands. Builds may take several minutes. Always use appropriate timeouts and wait for completion.