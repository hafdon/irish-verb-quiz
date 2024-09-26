import json
import sys
from jsonschema import validate, ValidationError

def validate_json(json_file, schema_file):
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    try:
        validate(instance=data, schema=schema)
        print("JSON file is valid.")
    except ValidationError as e:
        print("JSON file is invalid.")
        print("Validation Error:", e.message)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print("Invalid JSON format.")
        print("JSON Error:", e.msg)
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Validate JSON file against a schema.')
    parser.add_argument('json_file', help='Path to the JSON file to validate.')
    parser.add_argument('schema_file', help='Path to the JSON schema file.')
    args = parser.parse_args()
    validate_json(args.json_file, args.schema_file)
