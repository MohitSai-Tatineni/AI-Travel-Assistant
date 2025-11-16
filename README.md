# AI_Trip_Planner

## Docker Deploy

1. Copy required secrets (API keys, etc.) into `.env`. Both services load that file automatically.
2. Build the service-specific images and start the FastAPI backend (port `8000`) plus the Streamlit frontend (port `8501`):
   ```bash
   docker compose up --build
   ```
3. Visit `http://localhost:8501` for the UI. The frontend talks to the backend through the internal Docker network, so no further configuration is required.
4. When finished, stop the stack:
   ```bash
   docker compose down
   ```

### Build & run services individually

```bash
# Backend API
docker build -f Dockerfile.backend -t ai-trip-planner-backend .
docker run --env-file .env -p 8000:8000 ai-trip-planner-backend

# Frontend UI
docker build -f Dockerfile.frontend -t ai-trip-planner-frontend .
docker run --env-file .env -e BACKEND_URL=http://localhost:8000 -p 8501:8501 ai-trip-planner-frontend
```
