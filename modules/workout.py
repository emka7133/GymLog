from datetime import datetime
from pathlib import Path
from utils.json_handler import load_json, save_json
from utils.helpers import add

WORKOUT_FILE = Path("data/workouts.json")

def load_workout():
    if not WORKOUT_FILE.exists():
        WORKOUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_json(WORKOUT_FILE, [])
        return []
    return load_json(WORKOUT_FILE) or []

def save_workout(workout):
    save_json(WORKOUT_FILE, workout)

def add_workout(new_workout):
    workout = load_workout()
    updated, added = add(workout, new_workout)
    save_workout(updated)
    return added

def get_previous_sets(exercise_id):
    workouts = load_workout()

    #check workouts file in reverse order and load 
    #the latest one with the matching id
    for workout in reversed(workouts):
        for exercise in workout.get("exercises", []):
            if exercise.get("exercise_id") == exercise_id:
                return exercise.get("sets", [])
    return []

