import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.exercises import search_exercises, add_exercise, remove_exercise, edit_exercise


class ExercisesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Entry field with live search
        self.search_var = tk.StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.search_var)
        self.entry.pack(side="left", padx=5, fill="x", expand=True)

        # Placeholder text when not in use
        self.placeholder_text = "Search"
        self._add_placeholder()

        self.entry.bind("<FocusIn>", self._remove_placeholder)
        self.entry.bind("<FocusOut>", self._add_placeholder)

        # Add Exercise button
        ttk.Button(frame, text="Add Exercise", command=self.open_add_exercise_window).pack(side="left", padx=5)

        # --- Exercise List ---
        self.exercise_list = tk.Listbox(self, height=15, width=60)
        self.exercise_list.pack(pady=10, fill="both", expand=True)

        self.search_var.trace_add("write", self.on_search_change)

        # Double-click event
        self.exercise_list.bind("<Double-Button-1>", self.on_exercise_double_click)

        # Keep a reference to currently displayed exercises
        self.displayed_exercises = []

        # Show all exercises initially
        self.update_exercise_list()

    # ---------- PLACEHOLDER HANDLERS ----------
    def _add_placeholder(self, event=None):
        """Show 'Search' placeholder if entry is empty."""
        if not self.search_var.get().strip():
            self.entry.insert(0, self.placeholder_text)
            self.entry.config(foreground="gray")

    def _remove_placeholder(self, event=None):
        """Remove placeholder when user focuses entry."""
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground="black")

    # ---------- LIVE SEARCH HANDLER ----------
    def on_search_change(self, *args):
        """Triggered automatically whenever search text changes."""
        self.update_exercise_list()

    def update_exercise_list(self):
        """Refresh the exercise list based on current search text."""
        query = self.search_var.get().strip()
        self.exercise_list.delete(0, tk.END)

        if not query or query == self.placeholder_text:
            query = ""

        results = search_exercises(query)
        self.displayed_exercises = results  

        if not results:
            self.exercise_list.insert(tk.END, f"No exercises found for: {query}")
        else:
            for ex in results:
                tags_str = ", ".join(ex.get("tags", []))
                self.exercise_list.insert(tk.END, f"{ex['title']} ({tags_str})")

    # ---------- DOUBLE-CLICK HANDLER ----------
    def on_exercise_double_click(self, event):
        """Open a detail popup for the selected exercise."""
        selection = self.exercise_list.curselection()
        if not selection:
            return

        index = selection[0]
        if index >= len(self.displayed_exercises):
            return  # ignore if the user clicked on 'No exercises found'

        ex = self.displayed_exercises[index]
        self.open_exercise_details(ex)

    # ---------- ADD EXERCISE POPUP ----------
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

        ttk.Button(popup, text="Save Exercise", command=lambda: save_exercise()).pack(pady=15)

        def save_exercise():
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
                self.update_exercise_list()  # refresh list immediately
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save exercise:\n{e}")

    # ---------- EXERCISE DETAILS POPUP ----------
    def open_exercise_details(self, ex):
        """Show a popup with full exercise details."""
        popup = tk.Toplevel(self)
        popup.title(ex["title"])
        popup.geometry("400x500")
        popup.resizable(False, False)

        ttk.Label(popup, text=ex["title"], font=("Arial", 16, "bold")).pack(pady=10)

        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        info = {
            "Description":      ex.get("description", "No description"),
            "Tags":             ", ".join(ex.get("tags", [])) or "None",
            "Default Weight":   f"{ex.get('default_weight_kg', 0)} kg" if ex.get("has_weight") else "N/A",
            "Default Reps":     str(ex.get("default_reps", 0)) if ex.get("has_reps") else "N/A",
            "Default Sets":     str(ex.get("default_sets", 0)) if ex.get("has_sets") else "N/A",
            "Created":          ex.get("created_at", "Unknown"),
            "Last Updated":     ex.get("last_updated", "Unknown"),
        }

        for key, value in info.items():
            ttk.Label(frame, text=f"{key}:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
            ttk.Label(frame, text=value, wraplength=350).pack(anchor="w", padx=10)

        ttk.Button(popup, text="Edit", command=lambda: self.edit_exercise_popup(ex, popup)).pack(side="left", padx=10)
        ttk.Button(popup, text="Remove", command=lambda: self.remove_exercise_popup(ex, popup)).pack(side="left", padx=10)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(side="left", padx=10)

    # ---------- Edit Exercise Popup ----------
    def edit_exercise_popup(self, ex, parent_popup=None):
        """Open a popup to edit an existing exercise."""
        popup = tk.Toplevel(self)
        popup.title(f"Edit Exercise: {ex['title']}")
        popup.geometry("400x500")
        popup.resizable(False, False)

        ttk.Label(popup, text=f"Edit {ex['title']}", font=("Arial", 16)).pack(pady=10)
        form = ttk.Frame(popup)
        form.pack(pady=10)

        labels = ["Title", "Description", "Tags (comma-separated)",
                  "Default Weight (kg)", "Default Reps", "Default Sets"]
        entries = {}

        for label in labels:
            ttk.Label(form, text=label).pack(anchor="w", padx=10, pady=3)
            entry = ttk.Entry(form, width=40)
            # pre-fill with existing values
            if label == "Title":
                entry.insert(0, ex["title"])
            elif label == "Description":
                entry.insert(0, ex.get("description", ""))
            elif label == "Tags (comma-separated)":
                entry.insert(0, ", ".join(ex.get("tags", [])))
            elif label == "Default Weight (kg)":
                entry.insert(0, str(ex.get("default_weight_kg", 0)))
            elif label == "Default Reps":
                entry.insert(0, str(ex.get("default_reps", 0)))
            elif label == "Default Sets":
                entry.insert(0, str(ex.get("default_sets", 0)))
            entry.pack(padx=10)
            entries[label] = entry

        def save_changes():
            title = entries["Title"].get().strip()
            if not title:
                messagebox.showerror("Error", "Title is required.")
                return

            description = entries["Description"].get().strip()
            tags = [t.strip() for t in entries["Tags (comma-separated)"].get().split(",") if t.strip()]
            try:
                default_weight = float(entries["Default Weight (kg)"].get().strip() or 0)
            except ValueError:
                default_weight = 0
            default_reps = int(entries["Default Reps"].get().strip() or 0)
            default_sets = int(entries["Default Sets"].get().strip() or 0)

            updates = {
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
                "last_updated": datetime.now().isoformat(),
            }

            try:
                edit_exercise(ex["id"], updates)
                messagebox.showinfo("Success", f"Updated exercise: {title}")
                popup.destroy()
                if parent_popup: parent_popup.destroy()
                self.update_exercise_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit exercise:\n{e}")

        ttk.Button(popup, text="Save Changes", command=save_changes).pack(pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=5)

    # ---------- Remove Exercise Popup ----------
    def remove_exercise_popup(self, ex, parent_popup=None):
        """Confirm deletion and remove exercise."""
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete '{ex['title']}'?")
        if confirm:
            try:
                remove_exercise(ex["id"])
                messagebox.showinfo("Deleted", f"Exercise '{ex['title']}' has been removed.")
                self.update_exercise_list()
                if parent_popup: parent_popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove exercise:\n{e}")
