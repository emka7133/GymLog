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

        # title
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(padx = 5, pady = 20)
        
        # select exercise button
        ttk.Button(self.title_frame, text="Select Exercise", command = self.open_exercise_selector).pack()

        # top side
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack()

        self.id_to_exercise = {}
        self.selection = ""

        # bottom side
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(expand = True, fill = "both", padx=10, pady=10)
        
        self.current_exercise_list = tk.Listbox(self.bottom_frame)
        self.current_exercise_list.pack(fill = "both", expand = True)


        ttk.Button(self.bottom_frame, text="Save", command=lambda: add_workout(self.current_workout)).pack()
        
        
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
            selected_index = exercise_list.curselection()

            self.selection = self.exercises[selected_index[0]]
            selector.destroy()
            print("confirm")
            self.show_exercise_details()

            # I want to make a dictionary json file with the selected exercises


        ttk.Button(selector, text = "Confirm", command = confirm_selection).pack(pady = 10)


    def show_exercise_details(self):

        print("show")
        current_exercise = {}        


        # find the data for the selected exercise
        ex = self.selection

        current_exercise = {
            "exercise_id": ex["id"],
            "info": {
                "weight": ex["weight"]["default"],
                "reps": ex["reps"]["default"],
                "sets": ex["sets"]["default"],
            },
        }
        
        def add_exercise():
            self.current_workout["id"] = datetime.now().isoformat(timespec="seconds")
            self.current_workout["exercises"] = self.current_workout_list

            self.current_workout_list.append(current_exercise)

            self.current_exercise_list.insert(tk.END, ex["title"])

            
        

        # refresh screen
        for widget in self.top_frame.winfo_children():
            widget.destroy()



        ttk.Label(self.top_frame, text = ex["title"], font = ("Arial", 14, "bold")).grid(row = 0, column = 0, columnspan = 3, pady = 10)

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

            current_exercise["weight"] = weight_entry.get()
                        
            weight_entry.grid(row = i*2 + 3, column = 1, padx = 5, pady = (0, 5))
            reps_entry.grid(row = i*2+3, column = 2, padx = 5, pady = (0, 5))
            
            self.entries.append((weight_entry, reps_entry))  

        ttk.Button(self.top_frame, text="Add", command=add_exercise).grid(row = i*2+4, column = 2, padx = 10, pady = 10)
        
        #ttk.Button(self.top_frame, text="Save", command=lambda: add_workout(self.current_workout)).grid(row = i*2+4, column = 0, padx = 5, pady = (0,5))
