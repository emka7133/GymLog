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
    # Add a new exercise if ID is unique.
    exercises = load_exercises()
    if any(ex["id"] == new_exercise["id"] for ex in exercises):
        raise ValueError(f"Exercise with id '{new_exercise['id']}' already exists.")
    
    new_exercise["created_at"] = datetime.now().isoformat(timespec="seconds")
    new_exercise["last_updated"] = new_exercise["created_at"]
    
    exercises.append(new_exercise)
    save_exercises(exercises)
    return new_exercise

def edit_exercise(exercise_id, updates):
    # Edit existing exercise by ID.
    exercises = load_exercises()
    for ex in exercises:
        if ex["id"] == exercise_id:
            ex.update(updates)
            ex["last_updated"] = datetime.now().isoformat(timespec="seconds")
            save_exercises(exercises)
            return exercise_id
    raise ValueError(f"No exercise found with id '{exercise_id}'")

def remove_exercise(exercise_id):
    # Delete exercise by ID.
    exercises = load_exercises()
    updated = [ex for ex in exercises if ex["id"] != exercise_id]
    
    if len(updated) == len(exercises):
        raise ValueError(f"No exercise found with id '{exercise_id}'")
    
    save_exercises(updated)
    return exercise_id

def list_exercises():
    # Return all exercises (sorted alphabetically).
    exercises = load_exercises()
    return sorted(exercises, key=lambda x: x["title"].lower())

def get_exercise_by_id(exercise_id):
    exercises = load_exercises()
    for ex in exercises:
        if ex["id"] == exercise_id:
            return ex
    return None

def search_exercises(query=None, sort_alpha=True):
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
