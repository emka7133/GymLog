import json
from pathlib import Path

def load_json(path):
    # Loads JSON data, or returns an empty list if file doesn't exist or is empty.
    path = Path(path)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json(path, data):
    # Saves Python object to JSON file with pretty formatting.
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
