import tkinter as tk
from tkinter import ttk
import json
import datetime
from modules.workout import *


class WorkoutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.current_workout = {}
        self.current_workout_list = []

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(padx = 5, pady = 20)
        
        # select exercise button
        ttk.Button(self.title_frame, text="Select Exercise", command = self.open_exercise_selector).pack()

        #top side
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack()
        
        self.id_to_exercise = {}
        
        
    # select exercise pop-up window
    def open_exercise_selector(self):
        
        selector = tk.Toplevel(self)
        selector.geometry("200x300")
        selector.title("Select Exercises")

        # load exercise dictionary
        with open("data/exercises.json", mode = "r") as file:
            self.exercises = json.load(file)
        self.id_to_exercise = {i["id"]: i for i in self.exercises}

        exercise_list = tk.Listbox(selector, selectmode = "browse")
        exercise_list.pack(expand = True, fill = "both", padx = 10, pady = 10)

        exercise_ids = []
        for i in self.exercises:
            exercise_list.insert(tk.END, i["title"])
            exercise_ids.append(i["id"])

        def confirm_selection():
            
            # make a list of chosen exercise ids
            selection = exercise_list.curselection()
            selected_ids = [exercise_ids[i] for i in selection]

            # update exercise list in main tab
            self.exercise_listbox.delete(0, tk.END)
            for id in selected_ids:
                self.exercise_listbox.insert(tk.END, self.id_to_exercise[id]["title"])


            selector.destroy()

            # I want to make a dictionary json file with the selected exercises

        ttk.Button(selector, text = "Confirm", command = confirm_selection).pack(pady = 10)


    def show_exercise_details(self, event):
        
        if not hasattr(self, self.top_frame):
            return

        selection = self.exercise_listbox.curselection()

        index = selection[0]
        selected_title = self.exercise_listbox.get(index)
        
        current_exercise = {}        


        # find the data for the selected exercise
        for ex in self.exercises:
            if ex["title"] == selected_title:
                data = ex

                current_exercise["exercise_id"] = ex["id"]

                info = {
                    "weight": ex["weight"]["default"],
                    "reps": ex["reps"]["default"],
                    "sets": ex["sets"]["default"]
                }
                current_exercise["info"] = info
                break
        else:
            return
        
        self.current_workout["id"] = datetime.now().isoformat(timespec="seconds")
        self.current_workout["exercises"] = self.current_workout_list

        # refresh screen
        for widget in self.top_frame.winfo_children():
            widget.destroy()



        ttk.Label(self.top_frame, text = data["title"], font = ("Arial", 14, "bold")).grid(row = 0, column = 0, columnspan = 3, pady = 10)

        ttk.Label(self.top_frame, text = "Weight ").grid(row=1, column=1)
        ttk.Label(self.top_frame, text = "Reps").grid(row=1, column=2)

        previous_sets = [
            {"weight": 50, "reps": 10},
            {"weight": 55, "reps": 8},
            {"weight": 60, "reps": 6},
        ]

        set_number = 3
        self.entries = []
        
        for i in range(set_number):
            
            ttk.Label(self.top_frame, text=str(i + 1)).grid(row = i*2+2, column = 0, sticky = "w", pady = (5, 0))
            
            if i < len(previous_sets):
                
                prev = previous_sets[i]
                
                ttk.Label(
                    self.top_frame,
                    text=f" {prev['weight']} kg x {prev['reps']} reps", foreground="gray"
                ).grid(row = i*2+2, column = 1, columnspan = 2, sticky = "w")
            
            weight_entry = ttk.Entry(self.top_frame, width=8)
            reps_entry = ttk.Entry(self.top_frame, width=8)
                        
            weight_entry.grid(row = i*2 + 3, column = 1, padx = 5, pady = (0, 5))
            reps_entry.grid(row = i*2+3, column = 2, padx = 5, pady = (0, 5))
            
            self.entries.append((weight_entry, reps_entry))  

        ttk.Button(self.top_frame, text="Add", command=lambda: self.current_workout_list.append(current_exercise) ).grid(row = i*2+4, column = 1, padx = 5, pady = (0,5))
        ttk.Button(self.top_frame, text="Save", command=lambda: add_workout(self.current_workout)).grid(row = i*2+4, column = 0, padx = 5, pady = (0,5))
