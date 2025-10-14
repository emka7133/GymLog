from datetime import datetime
from pathlib import Path
from utils.json_handler import load_json, save_json

EXERCISE_FILE = Path("data/exercises.json")

def load_exercises():
    return load_json(EXERCISE_FILE)

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
    print(f"Added exercise: {new_exercise['title']}")

def edit_exercise(exercise_id, updates):
    # Edit existing exercise by ID.
    exercises = load_exercises()
    for ex in exercises:
        if ex["id"] == exercise_id:
            ex.update(updates)
            ex["last_updated"] = datetime.now().isoformat(timespec="seconds")
            save_exercises(exercises)
            print(f"Updated exercise '{exercise_id}'")
            return
    raise ValueError(f"No exercise found with id '{exercise_id}'")

def remove_exercise(exercise_id):
    # Delete exercise by ID.
    exercises = load_exercises()
    updated = [ex for ex in exercises if ex["id"] != exercise_id]
    
    if len(updated) == len(exercises):
        raise ValueError(f"No exercise found with id '{exercise_id}'")
    
    save_exercises(updated)
    print(f"Removed exercise '{exercise_id}'")

def list_exercises():
    # Return all exercises (sorted alphabetically).
    exercises = load_exercises()
    return sorted(exercises, key=lambda x: x["title"].lower())

def get_exercises_by_tag(tags=None, sort_alpha=True):
    exercises = load_exercises()
    if not exercises:
        return []

    if tags is None:
        filtered = exercises
    else:
        if isinstance(tags, str):
            tags = [tags]
        filtered = [
            ex for ex in exercises 
            if any(tag.lower() in [t.lower() for t in ex.get("tags", [])] for tag in tags)
        ]

    if sort_alpha:
        filtered.sort(key=lambda x: x.get("title", "").lower())

    return filtered
