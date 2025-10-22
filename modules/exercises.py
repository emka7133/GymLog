from datetime import datetime
from pathlib import Path
from utils.json_handler import load_json, save_json

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
    if any(ex["id"] == new_exercise["id"] for ex in exercises):
        raise ValueError(f"Exercise with id '{new_exercise['id']}' already exists.")
    
    now = datetime.now().isoformat(timespec="seconds")
    new_exercise["created_at"] = now
    new_exercise["last_updated"] = now

    exercises.append(new_exercise)
    save_exercises(exercises)
    return new_exercise

def edit_exercise(exercise_id, updates):
    exercises = load_exercises()
    for ex in exercises:
        if ex["id"] == exercise_id:
            ex.update(updates)
            ex["last_updated"] = datetime.now().isoformat(timespec="seconds")
            save_exercises(exercises)
            return exercise_id 
    raise ValueError(f"No exercise found with id '{exercise_id}'")

def remove_exercise(exercise_id):
    exercises = load_exercises()
    updated = [ex for ex in exercises if ex["id"] != exercise_id]
    
    if len(updated) == len(exercises):
        raise ValueError(f"No exercise found with id '{exercise_id}'")
    
    save_exercises(updated)
    return exercise_id


def get_exercise_by_id(exercise_id):
    exercises = load_exercises()
    for ex in exercises:
        if ex["id"] == exercise_id:
            return ex
    return None

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


def build_metric(data, key, default_unit=None):
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
    "weight":       build_metric(data, "weight", "kg"),
    "reps":         build_metric(data, "reps"),
    "sets":         build_metric(data, "sets"),
    "time":         build_metric(data, "time", "sec"),
    "distance":     build_metric(data, "distance", "m"),
    "created_at":   data.get("created_at", now),
    "last_updated": now,
    }
