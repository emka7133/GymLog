import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.exercises import get_exercises_by_tag, add_exercise

class ExercisesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Search/Filter Section ---
        frame = ttk.Frame(self)
        frame.pack(pady=10)

        ttk.Label(frame, text="Tag:").pack(side="left", padx=5)
        self.tag_entry = ttk.Entry(frame)
        self.tag_entry.pack(side="left", padx=5)

        ttk.Button(frame, text="Search", command=self.search_exercises).pack(side="left", padx=5)
        ttk.Button(frame, text="Add Exercise", command=self.open_add_exercise_window).pack(side="left", padx=5)

        # --- Exercise List ---
        self.exercise_list = tk.Listbox(self, height=15, width=60)
        self.exercise_list.pack(pady=10)

    def search_exercises(self):
        tag = self.tag_entry.get().strip()
        self.exercise_list.delete(0, tk.END)

        results = get_exercises_by_tag(tag)
        if not results:
            self.exercise_list.insert(tk.END, f"No exercises found for tag: {tag}")
        else:
            for ex in results:
                tags_str = ", ".join(ex.get("tags", []))
                self.exercise_list.insert(tk.END, f"{ex['title']} ({tags_str})")

    def open_add_exercise_window(self):
        popup = tk.Toplevel(self)
        popup.title("Add Exercise")
        popup.geometry("400x500")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add New Exercise", font=("Arial", 16)).pack(pady=10)
        form = ttk.Frame(popup)
        form.pack(pady=10)

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
        title = self.entries["Title"].get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return

        description = self.entries["Description"].get().strip()
        tags = [t.strip() for t in self.entries["Tags (comma-separated)"].get().split(",") if t.strip()]
        try:
            default_weight = float(self.entries["Default Weight (kg)"].get().strip() or 0)
        except ValueError:
            default_weight = 0
        default_reps = int(self.entries["Default Reps"].get().strip() or 0)
        default_sets = int(self.entries["Default Sets"].get().strip() or 0)

        exercise = {
            "id": title.lower().replace(" ", "_"),
            "title": title,
            "description": description,
            "tags": tags,
            "has_weight": default_weight > 0,
            "default_weight_kg": default_weight,
            "goal_weight_kg": default_weight,
            "has_reps": default_reps > 0,
            "default_reps": default_reps,
            "goal_reps": default_reps,
            "has_sets": default_sets > 0,
            "default_sets": default_sets,
            "goal_sets": default_sets,
            "unit": "kg",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

        try:
            add_exercise(exercise)
            messagebox.showinfo("Success", f"Added new exercise: {title}")
            popup.destroy()
            self.search_exercises()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save exercise:\n{e}")
