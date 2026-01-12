# SVG Pipeline & Provider UI


This project provides a PNG → IR JSON → SVG pipeline plus a front-end settings UI for configuring
OpenAI-compatible proxy providers (API relay).

## Layout


- `src/` – pipeline, AI client, validation, rendering

- `schema/` – JSON schema for IR

- `prompts/` – AI prompt template

- `web/` – static settings UI

- `data/` – input/output folders
  
## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the pipeline (requires implementing `call_ai_to_json` credentials via env vars):

```bash
python scripts/run_pipeline.py
```

Serve the UI:

```bash
python -m http.server 8000 --directory web
```

Then open `http://localhost:8000`.