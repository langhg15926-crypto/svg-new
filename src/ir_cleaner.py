def clean_ir(doc):
    units = doc.get("units", {})
    units["position"] = "pt"
    units["size"] = "pt"
    units["stroke"] = "pt"
    units["font"] = "pt"
    doc["units"] = units

    styles = doc.get("styles", {})
    styles.setdefault("fontFamily", "FZShuSong-Z01, Times New Roman, SimSun, serif")
    styles.setdefault("defaultFontSizePt", 9)
    styles.setdefault("defaultStrokeWidthPt", 0.6)
    doc["styles"] = styles

    for el in doc.get("elements", []):
        fill = el.get("fill")
        if isinstance(fill, str):
            lowered = fill.lower()
            if lowered in {"hatch", "diag", "diagonal", "slash"}:
                el["fill"] = "pattern:diagHatch"
            elif lowered in {"vertical", "vert", "stripe"}:
                el["fill"] = "pattern:vertHatch"

        if el.get("type") == "line":
            el.setdefault("strokeWidth", 0.6)
        if el.get("type") == "text":
            el.setdefault("fontSize", 9)
            el.setdefault("fontFamily", styles["fontFamily"])

    return doc
