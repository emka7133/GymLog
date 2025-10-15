Exercise Bank
- See existing exercises
	- sort (alphabetical, tags)
- Edit existing exercises
	- edit title / description
	- edit defaults
	- remove exercise
- Add new exercises

Workout
- time
- weights / reps / sets (from last session (default at the first session))
- exercises (list)

Workout (current)
	- start / end workout
    - choose exercise -> do exercise -> assign weight / reps -> finish exercise
    - rests (None, 30s, 60s, Custom, Unlimited)


Logs
- General
    - statistics
        - total nr of workouts
        - nr of workouts this week
    - list of past workouts
    - highlight pb's
- Workouts
    - exercises / time / date
    - increase weight reminder for next session
      (ex: if you do a set and feel like you could do x more kg)
- over time progress (graphs)
	- sort by exercise
	- determine range (week / month / from start)

Settings 
-



from modules.exercises import add_exercise, list_exercises, edit_exercise

# Example exercise dictionary
'''
new_exercise = {
    "id": "squats",
    "title": "Squats",
    "description": "A lower-body compound exercise.",
    "notes": "Chest up, knees out.",
    "has_weight": True,
    "default_weight_kg": 50,
    "goal_weight_kg": 100,
    "has_reps": True,
    "default_reps": 10,
    "goal_reps": 10,
    "has_sets": True,
    "default_sets": 3,
    "goal_sets": 3,
    "has_time": False,
    "default_time_sec": 60,
    "goal_time": 120,
    "tags": ["legs", "compound"],
    "unit": "kg",
    "created_at": "2025-10-14T12:00:00",
    "last_updated": "2025-10-14T12:00:00"
}
'''
