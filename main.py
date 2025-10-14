import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from modules.exercises import list_exercises, get_exercises_by_tag, add_exercise
# from modules.workout import ...
# from modules.logs import ...
# from modules.settings import ...

# ---------- MAIN APP ----------
class GymLogApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gym Log App")
        self.geometry("800x600")
        self.minsize(700, 500)

        # Style
        style = ttk.Style(self)
        self.configure(bg="#f7f7f7")
        style.theme_use("clam")

        # Create tabs
        tab_control = ttk.Notebook(self)
        self.exercise_tab = ttk.Frame(tab_control)
        tab_control.add(self.exercise_tab, text="Exercise Bank")
        tab_control.pack(expand=1, fill="both")

        # Build tab
        self.build_exercise_tab()

    # ---------- EXERCISE TAB ----------
    def build_exercise_tab(self):
        title = ttk.Label(self.exercise_tab, text="Exercise Bank", font=("Arial", 18))
        title.pack(pady=10)

        # Search/filter area
        frame = ttk.Frame(self.exercise_tab)
        frame.pack(pady=10)

        ttk.Label(frame, text="Filter by tag:").pack(side="left", padx=5)
        self.tag_entry = ttk.Entry(frame)
        self.tag_entry.pack(side="left", padx=5)
        ttk.Button(frame, text="Search", command=self.search_exercises).pack(side="left", padx=5)
        ttk.Button(frame, text="Add Exercise", command=self.open_add_exercise_window).pack(side="left", padx=5)
        ttk.Button(frame, text="Refresh", command=self.load_all_exercises).pack(side="left", padx=5)


        # Results listbox
        self.exercise_list = tk.Listbox(self.exercise_tab, height=15, width=60)
        self.exercise_list.pack(pady=10)

    def load_all_exercises(self):
        """Load and display all exercises at startup."""
        self.exercise_list.delete(0, tk.END)
        try:
            exercises = get_exercises_by_tag()  # No filter = all
            if not exercises:
                self.exercise_list.insert(tk.END, "No exercises found.")
                return
            for ex in exercises:
                tags_str = ", ".join(ex.get("tags", []))
                self.exercise_list.insert(tk.END, f"{ex['title']} ({tags_str})")
        except FileNotFoundError:
            self.exercise_list.insert(tk.END, "⚠️ No exercise data found (exercises.json missing).")


    def search_exercises(self):
        """Placeholder for filtering exercises."""
        tag = self.tag_entry.get()
        self.exercise_list.delete(0, tk.END)

        results = [
            ex for ex in get_exercises_by_tag()
            if not tag or any(tag.lower() in t.lower() for t in ex["tags"])
        ]

        if not results:
            self.exercise_list.insert(tk.END, f"No exercises found for tag: {tag}")
        else:
            for ex in results:
                self.exercise_list.insert(tk.END, f"{ex['title']} ({', '.join(ex['tags'])})")


# ---------- RUN APP ----------
if __name__ == "__main__":
    app = GymLogApp()
    app.mainloop()
