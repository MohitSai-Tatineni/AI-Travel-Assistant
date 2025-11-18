# AI Trip Planner — Project Overview

This document explains the repository structure, key files, workflows, functionality, and how the pieces work together.

## High-Level Architecture
- **Frontend**: Streamlit app (`app.py`) renders the travel planner UI and calls the backend API.
- **Backend**: FastAPI service (`main.py`) exposes `/query` that runs the agentic planner and returns Markdown itineraries.
- **Agent**: LangGraph-powered orchestration (`agent/agentic_workflow.py`) that routes requests to LLM + tools.
- **Tools**: Weather, place search, calculator, and currency utilities under `tools/` backed by `utils/` service clients.
- **Containerization/Deploy**: Dockerfiles for backend/frontend, `docker-compose.yml` for local, `.github/workflows/aws-deploy.yml` for ECS CI/CD.

## File-by-File Guide

### App / UI
- `app.py` — Streamlit UI: hero layout, prompt input, quick-start buttons, latest itinerary display, and Markdown download. Calls backend via `BACKEND_URL` (env/default `http://localhost:8000`).

### Backend API
- `main.py` — FastAPI app with `POST /query`. Builds the LangGraph (`GraphBuilder`) and returns the final itinerary content.
- `agent/agentic_workflow.py` — Defines `GraphBuilder`: loads LLM, binds tools, compiles a LangGraph (agent node + tool node) and executes.
- `prompt_library/prompt.py` — System prompt instructing the agent to produce two itineraries (tourist + off-beat) with costs, weather, and details.

### Tools (LangChain tool wrappers)
- `tools/weather_info_tool.py` — Gets current and forecast weather via OpenWeatherMap (`OPENWEATHERMAP_API_KEY`).
- `tools/place_search_tool.py` — Attractions/restaurants/activities/transport via Google Places (`GPLACES_API_KEY`) with Tavily fallback (`TAVILY_API_KEY`).
- `tools/calculator_tool.py` — Budget math: totals, daily budget, hotel cost estimation.
- `tools/currency_conversion_tool.py` — Currency conversion via ExchangeRate API (`EXCHANGE_RATE_API_KEY`).

### Utilities / Service Clients
- `utils/model_loader.py` — Loads Groq or OpenAI chat models based on `config/config.yaml` and env keys (`GROQ_API_KEY`/`OPENAI_API_KEY`).
- `utils/config_loader.py` — Reads YAML config.
- `utils/weather_info.py` — HTTP client for OpenWeatherMap.
- `utils/place_info_search.py` — Google Places and Tavily search helpers.
- `utils/currency_converter.py` — ExchangeRate API client.
- `utils/expense_calculator.py` — Arithmetic helpers.
- `utils/save_to_document.py` — Helper to save content to docs (unused in main flow).

### Config / Environment
- `config/config.yaml` — LLM model names for Groq/OpenAI.
- `.env` — API keys (do not commit real secrets).
- `requirements.txt`, `setup.py`, `pyproject.toml` — Python package setup.
- `.dockerignore`, `.gitignore` — Ignore patterns for Docker/Git.

### Docker / Local Dev
- `Dockerfile.backend` — Builds FastAPI service on port 8000.
- `Dockerfile.frontend` — Builds Streamlit UI on port 8501.
- `docker-compose.yml` — Runs both services locally; frontend points to backend service.

### CI/CD
- `.github/workflows/aws-deploy.yml` — On push to `main`: build/tag/push backend & frontend images (`latest` + commit SHA) to ECR, rewrite ECS task definition container images by name, register new revision, and update the ECS service.

## How the Workflow Runs
1. User enters a trip request in Streamlit (`app.py`), which posts JSON `{ "question": "<prompt>" }` to `POST /query`.
2. FastAPI (`main.py`) builds a LangGraph via `GraphBuilder`, selecting the configured LLM and binding tools.
3. Agent executes:
   - Calls place search (Google Places/Tavily) for attractions, restaurants, activities, transport.
   - Calls weather info for current/forecast.
   - Uses calculator for budgets; currency converter for FX.
4. The agent returns a Markdown itinerary (tourist + off-beat options, day-by-day, costs, weather). Backend returns `{ "answer": "<markdown>" }`.
5. Frontend renders the Markdown, keeps a short history, and offers download.

## Environment Variables (required)
- `BACKEND_URL` (frontend override; defaults to `http://localhost:8000`)
- `GROQ_API_KEY` or `OPENAI_API_KEY`
- `GPLACES_API_KEY`
- `OPENWEATHERMAP_API_KEY`
- `EXCHANGE_RATE_API_KEY`
- `TAVILY_API_KEY`

## Running Locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# backend
uvicorn main:app --reload --port 8000

# frontend (new shell)
BACKEND_URL=http://localhost:8000 streamlit run app.py
```

## Docker
```bash
docker compose up --build
# UI: http://localhost:8501 , API: http://localhost:8000
```

## Deployment (ECS)
- Set GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REGISTRY`, `ECR_REPO_BACKEND`, `ECR_REPO_FRONTEND`, `ECS_CLUSTER`, `ECS_SERVICE`, and optional `ECS_BACKEND_CONTAINER_NAME`/`ECS_FRONTEND_CONTAINER_NAME`.
- Push to `main`; GitHub Actions builds and pushes images, rewrites the ECS task definition with the new SHA tags, registers it, and updates the service.

## Notes on Extending
- Modify the system prompt (`prompt_library/prompt.py`) to change tone/format.
- Add new tools under `tools/` and wire them in `GraphBuilder`.
- Swap LLM provider or model via `config/config.yaml` and env keys.

