import xml.etree.ElementTree as ET


def render_svg(doc):
    svg = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": f"{doc['canvas']['width_mm']}mm",
            "height": f"{doc['canvas']['height_mm']}mm",
            "viewBox": f"0 0 {doc['canvas']['width_pt']} {doc['canvas']['height_pt']}",
        },
    )

    defs = ET.SubElement(svg, "defs")
    for pattern in doc.get("patterns", []):
        attrs = {
            "id": pattern["id"],
            "patternUnits": pattern["patternUnits"],
            "width": str(pattern["width"]),
            "height": str(pattern["height"]),
        }
        if "rotate" in pattern:
            attrs["patternTransform"] = f"rotate({pattern['rotate']})"
        pat_el = ET.SubElement(defs, "pattern", attrs)
        line = pattern["line"]
        ET.SubElement(
            pat_el,
            "line",
            {
                "x1": str(line["x1"]),
                "y1": str(line["y1"]),
                "x2": str(line["x2"]),
                "y2": str(line["y2"]),
                "stroke": line["stroke"],
                "stroke-width": str(line["strokeWidth"]),
            },
        )

    for el in doc.get("elements", []):
        if el["type"] == "line":
            ET.SubElement(
                svg,
                "line",
                {
                    "id": el.get("id", ""),
                    "x1": str(el["x1"]),
                    "y1": str(el["y1"]),
                    "x2": str(el["x2"]),
                    "y2": str(el["y2"]),
                    "stroke": el.get("stroke", "#000"),
                    "stroke-width": str(el.get("strokeWidth", 0.6)),
                    "stroke-linecap": el.get("strokeLinecap", "butt"),
                    "stroke-linejoin": el.get("strokeLinejoin", "miter"),
                },
            )
        elif el["type"] == "rect":
            fill = el.get("fill", "none")
            if isinstance(fill, str) and fill.startswith("pattern:"):
                fill = f"url(#{fill.split(':', 1)[1]})"
            ET.SubElement(
                svg,
                "rect",
                {
                    "id": el.get("id", ""),
                    "x": str(el["x"]),
                    "y": str(el["y"]),
                    "width": str(el["width"]),
                    "height": str(el["height"]),
                    "fill": fill,
                    "stroke": el.get("stroke", "none"),
                    "stroke-width": str(el.get("strokeWidth", 0)),
                },
            )
        elif el["type"] == "text":
            text_el = ET.SubElement(
                svg,
                "text",
                {
                    "id": el.get("id", ""),
                    "x": str(el["x"]),
                    "y": str(el["y"]),
                    "font-family": el.get("fontFamily"),
                    "font-size": str(el.get("fontSize")),
                    "text-anchor": el.get("textAnchor", "start"),
                    "dominant-baseline": el.get("dominantBaseline", "alphabetic"),
                    "fill": el.get("fill", "#000"),
                },
            )
            if "rotation" in el:
                text_el.set(
                    "transform",
                    f"rotate({el['rotation']} {el['x']} {el['y']})",
                )
            text_el.text = el["text"]

    return ET.tostring(svg, encoding="unicode")
