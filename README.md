# InsightBot - Multi-Agent Data Analyst (Microsoft AutoGen)

Ask questions about a CSV in plain English. A team of AutoGen agents
(Planner -> Coder -> Executor -> Reviewer) plans the analysis, writes Python,
executes it (locally or in Docker), saves charts and returns a summary.

## Setup (UV)
```bash
uv sync                       # installs everything from pyproject.toml
cp .env.example .env          # then fill in your Azure OpenAI values
```

## Run
```bash
uv run python -m insightbot.main "Which region has the highest revenue? Plot revenue by region." sales.csv
```
Charts are saved to `data/outputs/`. Put your own CSVs in `data/uploads/`.

## Docker execution (safe mode)
Start Docker Desktop, set `USE_DOCKER=true` in `.env`, run again.
Note: with `python:3.12-slim` the coder must install pandas/matplotlib inside
the container - add that instruction to the coder's system message, or build
a custom image with the libraries preinstalled.

## Roadmap
- Week 3: register `load_csv_summary` as a real tool (register_function + Pydantic)
- Week 4: nested-chat front agent + human-in-the-loop approval before execution
- Later: Streamlit UI -> Azure Blob Storage -> deploy on Azure Container Apps
