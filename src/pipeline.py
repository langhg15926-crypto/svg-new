import json
import subprocess

from .ai_client import call_ai_to_json
from .config import (
    DIFF_OUT_DIR,
    INPUT_DIR,
    JSON_OUT_DIR,
    PNG_OUT_DIR,
    PROMPT_PATH,
    SCHEMA_PATH,
    SVG_OUT_DIR,
)
from .diff_check import compare_images
from .ir_cleaner import clean_ir
from .ir_validator import validate_ir
from .svg_renderer import render_svg


def svg_to_png(svg_path, png_path):
    subprocess.run(
        [
            "inkscape",
            str(svg_path),
            "--export-type=png",
            "--export-filename",
            str(png_path),
        ],
        check=True,
    )


def run():
    JSON_OUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    PNG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_OUT_DIR.mkdir(parents=True, exist_ok=True)

    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    for img_file in INPUT_DIR.glob("*.*"):
        if img_file.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue

        ir_text = call_ai_to_json(str(img_file), prompt)
        ir_json = json.loads(ir_text)
        ir_json = clean_ir(ir_json)
        validate_ir(ir_json, SCHEMA_PATH)

        json_path = JSON_OUT_DIR / f"{img_file.stem}.json"
        json_path.write_text(
            json.dumps(ir_json, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        svg_text = render_svg(ir_json)
        svg_path = SVG_OUT_DIR / f"{img_file.stem}.svg"
        svg_path.write_text(svg_text, encoding="utf-8")

        png_path = PNG_OUT_DIR / f"{img_file.stem}.png"
        svg_to_png(svg_path, png_path)

        diff_path = DIFF_OUT_DIR / f"{img_file.stem}_diff.png"
        diff_ratio = compare_images(img_file, png_path, diff_path)

        print(f"{img_file.name}: diff_ratio={diff_ratio:.4f}")
