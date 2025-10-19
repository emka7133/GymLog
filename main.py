import tkinter as tk
from tkinter import ttk

from tabs.exercises_tab import ExercisesTab
from tabs.workout_tab import WorkoutTab
from tabs.logs_tab import LogsTab
from tabs.settings_tab import SettingsTab

# ---------- MAIN ----------
class GymLogApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gym Log App")
        self.geometry("400x600")
        self.minsize(500, 500)
        self.resizable(False, False)

        # Style
        style = ttk.Style(self)
        self.configure(bg="#f7f7f7")
        style.theme_use("clam")

        # Create tab control
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Add tabs
        self.tabs = [
            ("Exercise Bank", ExercisesTab(self.tab_control)),
            ("Workout Tracker", WorkoutTab(self.tab_control)),
            ("Logs", LogsTab(self.tab_control)),
            ("Settings", SettingsTab(self.tab_control))
        ]

        for text, frame in self.tabs:
            self.tab_control.add(frame, text=text)

        # Configure tab style to stretch
        self.style = style
        self.update_tab_widths()
        self.tab_control.bind("<Configure>", self.on_resize)  # update widths on resize 
        
    def update_tab_widths(self):
        tab_count = len(self.tab_control.tabs())
        if tab_count == 0:
            return
        total_width = self.tab_control.winfo_width() or 800  # fallback width
        tab_width = total_width // tab_count
        self.style.configure('TNotebook.Tab', width=tab_width, anchor='center', justify='center')

    def on_resize(self, event):
        self.update_tab_widths()


if __name__ == "__main__":
    app = GymLogApp()
    app.mainloop()
