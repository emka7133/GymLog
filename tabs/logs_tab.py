import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.workout import load_workout


class LogsTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Top section for dropdown
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="x", padx=20, pady=(20, 10))

        ttk.Label(self.top_frame, text="Select Exercise:").pack(side="left", padx=(0, 10))

        self.exercise_dropdown = ttk.Combobox(self.top_frame, state="readonly", width=30)
        self.exercise_dropdown.pack(side="left", padx=(0, 10))
        self.exercise_dropdown.bind("<<ComboboxSelected>>", self.show_graph)

        # Right section for graph
        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))

        # Load data and populate dropdown
        self.exercise_select()

    def exercise_select(self):
        self.workouts = load_workout()

        titles = set()
        for workout in self.workouts:
            for exercise in workout["exercises"]:
                titles.add(exercise["title"])

        sorted_titles = sorted(titles)

        self.exercise_dropdown["values"] = sorted_titles

        # Auto-select the first exercise if available
        if sorted_titles:
            self.exercise_dropdown.set(sorted_titles[0])
            self.show_graph(None)

    def show_graph(self, event):
        exercise_name = self.exercise_dropdown.get()
        if not exercise_name:
            return

        dates = []
        weights = []

        for workout in self.workouts:
            date = workout["date"]
            true_date = workout["id"]
            for exercise in workout["exercises"]:
                if exercise["title"] == exercise_name:
                    # Average weight of all sets
                    if exercise["sets"]:
                        average_weight = sum(s["weight"] for s in exercise["sets"]) / len(exercise["sets"])
                        dates.append(true_date)
                        weights.append(average_weight)

        # Clear previous widgets
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if not dates:
            ttk.Label(self.right_frame, text="No data available for this exercise.").pack(pady=20)
            return

        # Create graph
        figure = Figure(figsize=(3, 5), dpi=80)
        graph = figure.add_subplot(111)
        graph.plot(dates, weights, marker="o", linestyle="-")

        graph.set_title(exercise_name)
        graph.set_facecolor("#dcdad5")
        figure.patch.set_facecolor("#dcdad5")
        graph.grid(True)
        figure.tight_layout()
        figure.autofmt_xdate()

        # Embed matplotlib figure into Tkinter
        canvas = FigureCanvasTkAgg(figure, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
