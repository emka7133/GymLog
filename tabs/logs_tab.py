import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.workout import load_workout
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class LogsTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Top section for dropdown
        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side="top", fill="x", padx=20, pady=(20, 10))

        ttk.Label(self.top_frame, text="Select Exercise:").pack(side="top", padx=(50, 10), pady = 10)

        #exercise select dropdown
        self.exercise_dropdown = ttk.Combobox(self.top_frame, state="readonly", width=30)
        self.exercise_dropdown.pack(side="top", padx=(50, 10))
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

        #convert dates to datetime
        dates = [datetime.fromisoformat(d) if isinstance(d, str) else d for d in dates]

        #create graph
        figure = Figure(figsize=(3, 5), dpi=80)

        graph = figure.add_subplot(111)
        graph.plot(dates, weights, marker=".", markersize = 5, linestyle="-", color="#4a7d8c")        

        start_date = min(dates)
        end_date = max(dates)
        span = (end_date - start_date).days

        # if data less than 12 weeks, start from the first date + 12 weeks
        if span < 84:
            end_date = start_date + timedelta(days=84)
        
        #else show last 12 weeks
        else:
            start_date = end_date - timedelta(days=84)
        
        #adjust starting x-value to be Monday
        start_date = start_date - timedelta(days=start_date.weekday())

        graph.set_xlim(start_date, end_date)

        #pretty lines for each week
        for i in range(13): 
            week_line = start_date + timedelta(weeks=i)
            graph.axvline(week_line, color="lightgray", linestyle="--", linewidth=0.4, zorder=0)

        #x-axis labels: monday of each week
        graph.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY, interval=1))
        graph.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))


        graph.set_title(exercise_name)
        graph.set_facecolor("#dcdad5")
        figure.patch.set_facecolor("#dcdad5")
        graph.grid(True, zorder=-1)
        figure.tight_layout()
        figure.autofmt_xdate()

        canvas = FigureCanvasTkAgg(figure, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
