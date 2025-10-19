Exercise Bank TODO:
1.  _update_exercise_list to not reset if a tag is selected.
2.  add so tag is deselected if selected tag is clicked.
3.  fix create_collapsible_section for open_add_exercise_window (currently not aligned and not in view) -> either make it adaptable to window size, or individualize manually for each use instead of a generalized function (in other words, remove the create_collapsible_section function).
4.  add scrollbar for tag list
5.  


Workout
- time
- weights / reps / sets (from last session (default at the first session))
- exercises (list)
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
