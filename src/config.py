from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

DATA_DIR = BASE / "data"
if not DATA_DIR.exists():
    legacy_dir = BASE / "date"
    if legacy_dir.exists():
        DATA_DIR = legacy_dir
INPUT_DIR = DATA_DIR / "input"
JSON_OUT_DIR = DATA_DIR / "json_out"
SVG_OUT_DIR = DATA_DIR / "svg_out"
PNG_OUT_DIR = DATA_DIR / "png_out"
DIFF_OUT_DIR = DATA_DIR / "diff_out"

PROMPT_PATH = BASE / "prompts" / "ir_prompt.txt"
SCHEMA_PATH = BASE / "schema" / "ir_schema.json"
