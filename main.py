import tkinter as tk
from tkinter import ttk

from tabs.exercises_tab import ExercisesTab
from tabs.workout_tab import WorkoutTab
from tabs.logs_tab import LogsTab
from tabs.settings_tab import SettingsTab

# ---------- MAIN APP ----------
class GymLogApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gym Log App")
        self.geometry("800x600")
        self.minsize(500, 500)

        # Style
        style = ttk.Style(self)
        self.configure(bg="#f7f7f7")
        style.theme_use("clam")

        # Create tab control
        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        # Add tabs (each one is its own class)
        tab_control.add(ExercisesTab(tab_control), text="Exercise Bank")
        tab_control.add(WorkoutTab(tab_control), text="Workout Tracker")
        tab_control.add(LogsTab(tab_control), text="Logs")
        tab_control.add(SettingsTab(tab_control), text="Settings")

# ---------- RUN APP ----------
if __name__ == "__main__":
    app = GymLogApp()
    app.mainloop()
