import json

import jsonschema


def validate_ir(doc, schema_path):
    with open(schema_path, "r", encoding="utf-8") as handle:
        schema = json.load(handle)
    jsonschema.validate(instance=doc, schema=schema)
