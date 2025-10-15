import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


from modules.exercises import get_exercises_by_tag, add_exercise
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
        # Search/filter area
        frame = ttk.Frame(self.exercise_tab)
        frame.pack(pady=10)

        ttk.Label(frame).pack(side="left", padx=5)
        self.tag_entry = ttk.Entry(frame)
        self.tag_entry.pack(side="left", padx=5)
        ttk.Button(frame, text="Search", command=self.search_exercises).pack(side="left", padx=5)
        ttk.Button(frame, text="Adds Exercise", command=self.open_add_exercise_window).pack(side="left", padx=5)

        # Results listbox
        self.exercise_list = tk.Listbox(self.exercise_tab, height=15, width=60)
        self.exercise_list.pack(pady=10)

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

    # ---------- ADD EXERCISE POPUP ----------
    def open_add_exercise_window(self):
        """Open popup for adding a new exercise."""
        popup = tk.Toplevel(self)
        popup.title("Add Exercise")
        popup.geometry("400x500")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add New Exercise", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(popup)
        form.pack(pady=10)

        # Input fields
        labels = ["Title", "Description", "Tags (comma-separated)", 
                  "Default Weight (kg)", "Default Reps", "Default Sets"]
        self.entries = {}
        for label in labels:
            ttk.Label(form, text=label).pack(anchor="w", padx=10, pady=3)
            entry = ttk.Entry(form, width=40)
            entry.pack(padx=10)
            self.entries[label] = entry

        ttk.Button(popup, text="Save Exercise", command=lambda: self.save_exercise(popup)).pack(pady=15)

    def save_exercise(self, popup):
        """Save exercise data from popup to JSON."""
        title = self.entries["Title"].get().strip()
        description = self.entries["Description"].get().strip()
        tags = [t.strip() for t in self.entries["Tags (comma-separated)"].get().split(",") if t.strip()]
        try:
            default_weight = float(self.entries["Default Weight (kg)"].get().strip() or 0)
        except ValueError:
            default_weight = 0
        default_reps = int(self.entries["Default Reps"].get().strip() or 0)
        default_sets = int(self.entries["Default Sets"].get().strip() or 0)

        if not title:
            messagebox.showerror("Error", "Title is required.")
            return

        exercise = {
            "id": title.lower().replace(" ", "_"),
            "title": title,
            "description": description,
            "tags": tags,
            "has_weight": True if default_weight else False,
            "default_weight_kg": default_weight,
            "goal_weight_kg": default_weight,
            "has_reps": True if default_reps else False,
            "default_reps": default_reps,
            "goal_reps": default_reps,
            "has_sets": True if default_sets else False,
            "default_sets": default_sets,
            "goal_sets": default_sets,
            "unit": "kg",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

        try:
            add_exercise(exercise)
            messagebox.showinfo("Success", f"Added new exercise: {title}")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save exercise:\n{e}")

    def exercise_popup(self, popup, ):
        popup = tk.Toplevel(self)
        popup.title()
        popup.geometry("400x500")
        popup.resizable(False, False)


# ---------- RUN APP ----------
if __name__ == "__main__":
    app = GymLogApp()
    app.mainloop()
