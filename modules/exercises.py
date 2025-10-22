from datetime import datetime
from pathlib import Path
from utils.json_handler import load_json, save_json
from utils.helpers import add, edit, remove

EXERCISE_FILE = Path("data/exercises.json")

def load_exercises():
    if not EXERCISE_FILE.exists():
        EXERCISE_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_json(EXERCISE_FILE, [])
        return []
    return load_json(EXERCISE_FILE) or []

def save_exercises(exercises):
    save_json(EXERCISE_FILE, exercises)

def add_exercise(new_exercise):
    exercises = load_exercises()
    updated, added = add(exercises, new_exercise)
    save_exercises(updated)
    return added

def edit_exercise(exercise_id, updates):
    exercises = load_exercises()
    updated, _ = edit(exercises, exercise_id, updates)
    save_exercises(updated)
    return exercise_id

def remove_exercise(exercise_id):
    exercises = load_exercises()
    updated, _ = remove(exercises, exercise_id)
    save_exercises(updated)
    return exercise_id


def get_all_tags():
    """Return a sorted list of all unique tags from exercises."""
    exercises = search_exercises(None)
    tags = set()
    for ex in exercises:
        tags.update(ex.get("tags", []))
    return sorted(tags)

def search_exercises(query=None, sort_alpha=True):
    """Returns list of exercises matching query. If querry=None, returns the whole list."""
    exercises = load_exercises()
    if not exercises:
        return []

    if not query:
        filtered = exercises
    else:
        q = query.lower()
        filtered = [
            ex for ex in exercises
            if q in ex["title"].lower() or any(q in t.lower() for t in ex.get("tags", []))
        ]

    if sort_alpha:
        filtered.sort(key=lambda x: x.get("title", "").lower())

    return filtered


def exercise_build_metric(data, key, default_unit=None):
    metric = data.get(key, {})
    val = {
        "has": metric.get("default", 0) > 0,
        "default": metric.get("default", 0),
        "goal": metric.get("goal", metric.get("default", 0)),
    }
    if default_unit:
        val["unit"] = metric.get("unit", default_unit)
    return val

def normalize_exercise_data(data, existing_id=None):
    """Builds a properly structured exercise dict."""
    now = datetime.now().isoformat(timespec="seconds")
    ex_id = existing_id or data["title"].lower().replace(" ", "_")

    return {
    "id":           ex_id,
    "title":        data["title"],
    "description":  data.get("description", ""),
    "tags":         data.get("tags", []) if isinstance(data.get("tags", []), list) else [], # ensures tags is a list object
    "weight":       exercise_build_metric(data, "weight", "kg"),
    "reps":         exercise_build_metric(data, "reps"),
    "sets":         exercise_build_metric(data, "sets"),
    "time":         exercise_build_metric(data, "time", "sec"),
    "distance":     exercise_build_metric(data, "distance", "m"),
    "created_at":   data.get("created_at", now),
    "last_updated": now,
    }
