import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
from modules.workout import *
from tabs.logs_tab import LogsTab


class WorkoutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.current_workout = {}
        self.current_workout_list = []

        # title
        self.left_frame = ttk.Frame(self, width = 100, height = 300)
        self.left_frame.pack(side='left', fill = 'y', padx = 20, pady = 20, expand = False)
        self.left_frame.pack_propagate(False)

        self.right_frame = ttk.Frame(self, width = 250, height = 300)
        self.right_frame.pack(side = 'right', fill = 'both', padx = 20, pady = 20, expand = True)
        
        # select exercise button
        ttk.Button(self.left_frame, text="Select Exercise", command = self.open_exercise_selector).pack(pady = 20)

        self.selection = ""
        
        self.current_exercise_list = tk.Listbox(self.left_frame)
        self.current_exercise_list.pack(fill = "both", expand = True)


        ttk.Button(
            self.left_frame, 
            text="Save Workout", 
            command=lambda: [add_workout(self.current_workout), self.reset_workout_tab()]).pack(pady = 20)
        
        
    #reset window after a workout is saved
    def reset_workout_tab(self):

        self.current_exercise_list.delete(0, tk.END)

        for widget in self.right_frame.winfo_children():
            widget.destroy()
        
        self.current_workout = {}
        self.current_workout_list = []    
    

    # select exercise pop-up window
    def open_exercise_selector(self):
        
        selector = tk.Toplevel(self)
        selector.geometry("200x300")
        selector.title("Select Exercises")

        # load exercise dictionary
        with open("data/exercises.json", mode = "r") as file:
            self.exercises = json.load(file)
        
        #alphabetical order
        self.exercises.sort(key=lambda x: x["title"].lower())

        #make listbox
        exercise_list = tk.Listbox(selector, selectmode = "browse")
        exercise_list.pack(expand = True, fill = "both", padx = 10, pady = 10)

        #populate with titles from exercises file
        for i in self.exercises:
            exercise_list.insert(tk.END, i["title"])

        def confirm_selection():
            selected_index = exercise_list.curselection()

            self.selection = self.exercises[selected_index[0]]
            selector.destroy()
            self.show_exercise_details()


        ttk.Button(selector, text = "Confirm", command = confirm_selection).pack(pady = 10)


    def show_exercise_details(self, set_number=1, entries=None):
        if set_number < 1:
            set_number = 1

        ex = self.selection
        previous_sets = get_previous_sets(ex["id"])

        # Read current entries before destroying frame
        preserved_values = []
        if entries:
            for weight_entry, reps_entry in entries:
                preserved_values.append((weight_entry.get(), reps_entry.get()))

        # Reset UI
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.right_frame,
            text=ex["title"],
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(20, 10))

        ttk.Label(self.right_frame, text="Weight").grid(row=1, column=1)
        ttk.Label(self.right_frame, text="Reps").grid(row=1, column=2)

        self.entries = []

        for i in range(set_number):
            ttk.Label(self.right_frame, text=str(i + 1)).grid(row=i * 2 + 3, column=0, padx=5, pady=(0, 5))

            # Show previous set (if exists)
            if i < len(previous_sets):
                prev = previous_sets[i]
                ttk.Label(self.right_frame, text=f"{prev['weight']} kg", foreground="gray").grid(row=i*2+2, column=1, sticky="w", padx=20)
                ttk.Label(self.right_frame, text=f"{prev['reps']} reps", foreground="gray").grid(row=i*2+2, column=2, sticky="w", padx=20)

            # Create entry fields
            weight_entry = ttk.Entry(self.right_frame, width=8)
            reps_entry = ttk.Entry(self.right_frame, width=8)
            weight_entry.grid(row=i*2+3, column=1, padx=5, pady=(0, 5))
            reps_entry.grid(row=i*2+3, column=2, padx=5, pady=(0, 5))

            # Restore preserved values if available
            if i < len(preserved_values):
                weight_entry.insert(0, preserved_values[i][0])
                reps_entry.insert(0, preserved_values[i][1])

            self.entries.append((weight_entry, reps_entry))

        # Add and remove set buttons
        ttk.Button(
            self.right_frame,
            text="+",
            command=lambda: self.show_exercise_details(set_number=set_number + 1, entries=self.entries)
        ).grid(row=set_number*2+4, column=1, padx=5, pady=10)

        ttk.Button(
            self.right_frame,
            text="-",
            command=lambda: self.show_exercise_details(set_number=set_number - 1, entries=self.entries)
        ).grid(row=set_number*2+4, column=2, padx=5, pady=10)

        # Add exercise button
        
        def add_exercise():
            sets = []
            invalid_entries = False

            for weight_entry, reps_entry in self.entries:
                weight = weight_entry.get()
                reps = reps_entry.get()

                # Validate input
                if not weight or not reps:
                    invalid_entries = True
                    continue

                try:
                    weight = float(weight)
                    reps = int(reps)
                except ValueError:
                    messagebox.showwarning("Invalid entry", "Please enter valid numbers for weight and reps.")
                    return

                if reps <= 0:
                    messagebox.showwarning("Invalid reps", "Reps must be greater than zero.")
                    return

                sets.append({"weight": weight, "reps": reps})

            # Check for missing entries
            if invalid_entries or not sets:
                messagebox.showwarning("Incomplete entry", "Please fill in all weight and reps fields before adding.")
                return

            # Build exercise record
            current_exercise = {
                "exercise_id": ex["id"],
                "title": ex["title"],
                "sets": sets,
            }

            # Append
            self.current_workout_list.append(current_exercise.copy())

            # Update current workout summary
            self.current_workout = {
                "id": datetime.now().isoformat(timespec="seconds"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "exercises": self.current_workout_list,
            }

            # Add exercise title to list
            self.current_exercise_list.insert(tk.END, ex["title"])
        
        ttk.Button(self.right_frame, text="Add", command=add_exercise).grid(row=set_number*2+5, column=0, columnspan=3, pady=10)

