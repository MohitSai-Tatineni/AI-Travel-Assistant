# AI Trip Planner

AI Trip Planner is a two‑service app (FastAPI + Streamlit) that builds an agentic travel concierge on top of LangGraph. It crafts day‑by‑day itineraries, budgets, weather insights, and currency conversions by orchestrating multiple real‑time tools.

- End‑to‑end trip answers in one message, including a “tourist” and an “off‑beat/local” option.
- Groq or OpenAI LLMs (configurable) orchestrated via LangGraph with tool calling.
- Live data: Google Places + Tavily (attractions, restaurants, activities, transport), OpenWeatherMap (weather/forecast), and ExchangeRate (FX).
- Built‑in cost math tools (budgets, hotel cost calculator, currency conversion).
- Streamlit UI backed by a FastAPI `/query` endpoint.

## Project Structure
- `app.py` — Streamlit frontend that calls the backend and renders Markdown itineraries.
- `main.py` — FastAPI app exposing `POST /query` to run the agent.
- `agent/agentic_workflow.py` — LangGraph graph wiring LLM + tools.
- `prompt_library/prompt.py` — System prompt guiding itinerary style (tourist + off‑beat).
- `tools/` — Tool adapters (weather, place search, calculator, currency).
- `utils/` — Service clients and helpers (model loader, config loader, currency, weather, place search, budgeting).
- `config/config.yaml` — LLM model names for Groq and OpenAI.
- `docker-compose.yml`, `Dockerfile.backend`, `Dockerfile.frontend` — Containerized deployment.

## Prerequisites
- Python 3.10+ recommended.
- API keys (add to `.env` in the project root):
  - `GROQ_API_KEY` or `OPENAI_API_KEY` (LLM provider)
  - `GPLACES_API_KEY` (Google Places)
  - `OPENWEATHERMAP_API_KEY`
  - `EXCHANGE_RATE_API_KEY`
  - `TAVILY_API_KEY` (used by Tavily fallback search)
  - Optional: `BACKEND_URL` (frontend override, defaults to `http://localhost:8000`)

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

1) Create `.env` with the keys listed above.  
2) (Optional) Adjust model defaults in `config/config.yaml` (Groq is default in code).  
3) Start the backend:
```bash
uvicorn main:app --reload --port 8000
```
4) Start the frontend (in another shell):
```bash
BACKEND_URL=http://localhost:8000 streamlit run app.py
```
5) Open `http://localhost:8501` and ask for an itinerary (e.g., “Plan a 4‑day family trip to Kyoto, keep it under $1200”).

## Docker Deploy
```bash
docker compose up --build  # builds backend & frontend, ports 8000/8501
```
- UI: `http://localhost:8501`
- Stop: `docker compose down`

Build & run services individually:
```bash
# Backend API
docker build -f Dockerfile.backend -t ai-trip-planner-backend .
docker run --env-file .env -p 8000:8000 ai-trip-planner-backend

# Frontend UI
docker build -f Dockerfile.frontend -t ai-trip-planner-frontend .
docker run --env-file .env -e BACKEND_URL=http://localhost:8000 -p 8501:8501 ai-trip-planner-frontend
```

## API
- `POST /query`  
  - Body: `{"question": "<your travel request>"}`  
  - Response: `{"answer": "<markdown itinerary>"}`  
  - Used by the Streamlit client; you can also call it directly with `curl` or Postman.

## How It Works
1. Streamlit collects the user question and posts it to the backend.
2. `main.py` builds a LangGraph (`agentic_workflow.GraphBuilder`) with the configured LLM and tool set.
3. The agent calls tools as needed:
   - Google Places or Tavily for attractions, restaurants, activities, transport.
   - OpenWeatherMap for current/forecast weather.
   - ExchangeRate for currency conversion.
   - Calculator utilities for budgets and per‑day costs.
4. The final Markdown itinerary is returned and rendered in the UI.

## Development Notes
- Update the system prompt at `prompt_library/prompt.py` to change tone or output shape.
- If you switch LLM providers, confirm the matching key exists in `.env` and the model name in `config/config.yaml`.
- Graph visualization: each request saves `my_graph.png` (Mermaid render of the LangGraph) in the repo root for debugging the tool flow.
