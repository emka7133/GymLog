import tkinter as tk
from tkinter import ttk
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LogsTab(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.left_frame = ttk.Frame(self, width = 100, height = 300)
        self.left_frame.pack(side='left', fill = 'y', padx = 20, pady = 20, expand = False)
        self.left_frame.pack_propagate(False)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side = 'right', fill = 'both', padx = 10, pady = 20, expand = True)

        ttk.Label(self.left_frame, text = "Select Exercise").pack(pady = 20)

        self.full_exercise_list = tk.Listbox(self.left_frame, selectmode = "browse")
        self.full_exercise_list.pack(fill = "both", expand = True, pady = (10,70))

        self.exercise_select()

        self.full_exercise_list.bind("<<ListboxSelect>>", self.show_graph)

    def exercise_select(self):
      
        with open("data/example_workouts.json", mode = "r") as file:
            self.workouts = json.load(file)

        titles = set()

        #add all titles to a set
        for workout in self.workouts:
            for exercise in workout["exercises"]:
                titles.add(exercise["title"])

        #fill up the listbox with unique titles
        for title in sorted(titles):
            self.full_exercise_list.insert(tk.END, title)
    
    def show_graph(self, event):
        
        selection = self.full_exercise_list.curselection()
        if not selection:
            return
        
        exercise_name = self.full_exercise_list.get(selection[0])

        dates = []
        weights = []

        for workout in self.workouts:
            date = workout["date"]

            for exercise in workout["exercises"]:

                if exercise["title"] == exercise_name:
                    
                    #average weight of all sets
                    average_weight = sum(s["weight"] for s in exercise["sets"]) / len(exercise["sets"])
                    
                    dates.append(date)
                    weights.append(average_weight)
        
        #clear screen
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        #create graph
        figure = Figure(figsize=(5,3), dpi=100)
        
        graph = figure.add_subplot(111)
        graph.plot(dates, weights, marker="o", linestyle = "-")
        
        graph.set_title(exercise_name)
        graph.set_xlabel("Date")
        graph.set_ylabel("Weight (kg)")

        graph.grid(True)

        #embed in tkinter
        canvas = FigureCanvasTkAgg(figure, master = self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill = "both", expand = True)
                       
