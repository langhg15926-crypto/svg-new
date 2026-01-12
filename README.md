# SVG Pipeline & Provider UI

This project provides a PNG → IR JSON → SVG pipeline plus a front-end settings UI for configuring
OpenAI-compatible proxy providers (API relay).

## Layout

- `src/` – pipeline, AI client, validation, rendering
- `schema/` – JSON schema for IR
- `prompts/` – AI prompt template
- `web/` – static settings UI
- `data/` – input/output folders
- `config/` – provider configuration (local, not committed)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure the provider

Create `config/provider.json` (use `config/provider.sample.json` as a template). **Do not commit
real API keys.**

```json
{
  "base_url": "https://x666.me/v1",
  "api_key": "sk-REPLACE_WITH_YOUR_KEY",
  "model": "gemini-3-flash-preview",
  "timeout_s": 120
}
```

### Run the pipeline

```bash
python scripts/run_pipeline.py
```

On Windows, make sure you run the command from the project root so `src/` is on the module path.

### Serve the UI

```bash
python -m http.server 8000 --directory web
```

Then open `http://localhost:8000`.

The UI lets you export a `provider.json` file and import it locally.
