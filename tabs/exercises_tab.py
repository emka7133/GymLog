import tkinter as tk
from tkinter import ttk, messagebox
from modules.exercises import *


class ExercisesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Entry field with live search
        self.search_var = tk.StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.search_var)
        self.entry.pack(side="left", padx=5, fill="x", expand=True)

        # Placeholder text
        self.placeholder_text = "Search"
        self._add_placeholder()
        self.entry.bind("<FocusIn>", self._remove_placeholder)
        self.entry.bind("<FocusOut>", self._add_placeholder)

        ttk.Button(frame, text="Add Exercise", command=self.open_add_exercise_window).pack(side="left", padx=5)

        # Exercise list
        self.exercise_list = tk.Listbox(self, height=15, width=60)
        self.exercise_list.pack(pady=10, padx=10, fill="both", expand=True)

        self.search_var.trace_add("write", self._on_search_change)
        self.exercise_list.bind("<Double-Button-1>", self._on_exercise_double_click)
        self.displayed_exercises = []
        self._update_exercise_list()

    # ---------- PLACEHOLDER HANDLERS ----------
    def _add_placeholder(self, event=None):
        if not self.search_var.get().strip():
            self.entry.insert(0, self.placeholder_text)
            self.entry.config(foreground="gray")

    def _remove_placeholder(self, event=None):
        if self.entry.get() == self.placeholder_text:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground="black")

    # ---------- LIVE SEARCH ----------
    def _on_search_change(self, *args):
        self._update_exercise_list()

    def _update_exercise_list(self):
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
                self.exercise_list.insert(tk.END, f"{ex['title']}")

    # ---------- DOUBLE-CLICK ----------
    def _on_exercise_double_click(self, event):
        selection = self.exercise_list.curselection()
        if not selection:
            return
        index = selection[0]
        if index >= len(self.displayed_exercises):
            return
        ex = self.displayed_exercises[index]
        self.open_exercise_details(ex)

    # ---------- EXERCISE DATA HANDLER ----------
    def _get_exercise_data_from_entries(self, entries):
        title = entries["Title"].get().strip()
        if not title:
            raise ValueError("Title is required.")
        description = entries["Description"].get().strip()
        tags = [t.strip() for t in entries["Tags (comma-separated)"].get().split(",") if t.strip()]

        def parse_float(key):
            try:
                return float(entries[key].get().strip() or 0)
            except ValueError:
                return 0.0

        def parse_int(key):
            try:
                return int(entries[key].get().strip() or 0)
            except ValueError:
                return 0

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "weight": {
                "default": parse_float("Default Weight"),
                "goal": parse_float("Default Weight"),
                "unit": self.unit_weight.get()
            },
            "reps": {
                "default": parse_int("Default Reps"),
                "goal": parse_int("Default Reps")
            },
            "sets": {
                "default": parse_int("Default Sets"),
                "goal": parse_int("Default Sets")
            },
            "time": {
                "default": parse_int("Default Time"),
                "goal": parse_int("Default Time"),
                "unit": self.unit_time.get()
            },
            "distance": {
                "default": parse_int("Default Distance"),
                "goal": parse_int("Default Distance"),
                "unit": self.unit_distance.get()
            }
        }

    # ---------- ADD EXERCISE POPUP ----------
    def open_add_exercise_window(self):
        popup = tk.Toplevel(self)
        popup.title("Add Exercise")
        popup.geometry("400x600")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add New Exercise", font=("Arial", 16)).pack(pady=10)
        main_frame = ttk.Frame(popup)
        main_frame.pack(pady=10, fill="x")

        self.entries = {}

        # Always visible fields
        for label in ["Title", "Description", "Tags (comma-separated)"]:
            ttk.Label(main_frame, text=label).pack(anchor="w", padx=10, pady=3)
            entry = ttk.Entry(main_frame, width=40)
            entry.pack(padx=10)
            self.entries[label] = entry

        # ---------- COLLAPSIBLE SECTION CREATOR ----------
        def create_collapsible_section():
            # ---------- COLLAPSIBLE CHECKBOX GRID ----------
            checkbox_frame = ttk.Frame(main_frame)
            checkbox_frame.pack(fill="x", padx=10, pady=5)

            self.section_vars = {}

            sections = [
                ("weight", ["Default", "Goal"], ["bodyweight", "kg", "lb"]),
                ("reps", ["Default", "Goal"], None),
                ("sets", ["Default", "Goal"], None),
                ("time", ["Default", "Goal"], ["sec", "min", "hr"]),
                ("distance", ["Default", "Goal"], ["m", "km"]),
            ]

            for col, (name, fields, units) in enumerate(sections):
                var = tk.IntVar(value=0)
                self.section_vars[name] = var

                chk = ttk.Checkbutton(checkbox_frame, text=name.capitalize(), variable=var)
                chk.grid(row=0, column=col, padx=5, sticky="w")

                # Create hidden section frame
                section_frame = ttk.Frame(main_frame)
                section_frame.pack(fill="x", padx=20, pady=2)
                section_frame.pack_forget()  # initially hidden

                def toggle(var=var, frame=section_frame):
                    if var.get():
                        frame.pack(fill="x", padx=20, pady=2)
                    else:
                        frame.pack_forget()

                var.trace_add("write", lambda *args, v=var, f=section_frame: toggle(v, f))

                # Add entries side by side
                for i, f in enumerate(fields):
                    ttk.Label(section_frame, text=f).grid(row=0, column=i*2, sticky="w", padx=5, pady=2)
                    entry = ttk.Entry(section_frame, width=10)
                    entry.grid(row=0, column=i*2+1, padx=5, pady=2)
                    self.entries[f"{name}_{f}"] = entry

                # Add unit combobox if needed
                if units:
                    ttk.Label(section_frame, text=f"{name.capitalize()} Unit").grid(row=1, column=0, sticky="w", padx=5, pady=2)
                    combo = ttk.Combobox(section_frame, values=units, width=10)
                    combo.set(units[0])
                    combo.grid(row=1, column=1, padx=5, pady=2)
                    self.entries[f"{name}_unit"] = combo

        create_collapsible_section()

        # ---------- SAVE FUNCTION ----------
        def save_exercise():
            try:
                title = self.entries["Title"].get().strip()
                if not title:
                    raise ValueError("Title is required.")
                description = self.entries["Description"].get().strip()
                tags = [t.strip() for t in self.entries["Tags (comma-separated)"].get().split(",") if t.strip()]

                def parse_float(key):
                    try:
                        return float(self.entries.get(key, tk.Entry()).get().strip() or 0)
                    except ValueError:
                        return 0.0

                def parse_int(key):
                    try:
                        return int(self.entries.get(key, tk.Entry()).get().strip() or 0)
                    except ValueError:
                        return 0

                exercise = {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "weight": {
                        "has": parse_float("weight_Default") > 0,
                        "default": parse_float("weight_Default"),
                        "goal": parse_float("weight_Goal"),
                        "unit": self.entries.get("weight_unit", tk.Entry()).get() if "weight_unit" in self.entries else "kg"
                    },
                    "reps": {
                        "has": parse_int("reps_Default") > 0,
                        "default": parse_int("reps_Default"),
                        "goal": parse_int("reps_Goal")
                    },
                    "sets": {
                        "has": parse_int("sets_Default") > 0,
                        "default": parse_int("sets_Default"),
                        "goal": parse_int("sets_Goal")
                    },
                    "time": {
                        "has": parse_int("time_Default") > 0,
                        "default": parse_int("time_Default"),
                        "goal": parse_int("time_Goal"),
                        "unit": self.entries.get("time_unit", tk.Entry()).get() if "time_unit" in self.entries else "sec"
                    },
                    "distance": {
                        "has": parse_int("distance_Default") > 0,
                        "default": parse_int("distance_Default"),
                        "goal": parse_int("distance_Goal"),
                        "unit": self.entries.get("distance_unit", tk.Entry()).get() if "distance_unit" in self.entries else "m"
                    }
                }

                # Normalize, add, update list
                normalized = normalize_exercise_data(exercise)
                add_exercise(normalized)
                messagebox.showinfo("Success", f"Added new exercise: {exercise['title']}")
                popup.destroy()
                self._update_exercise_list()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save exercise:\n{e}")

        ttk.Button(popup, text="Save Exercise", command=save_exercise).pack(side="bottom", pady=15)

    # ---------- EXERCISE DETAILS POPUP ----------
    def open_exercise_details(self, ex):
        popup = tk.Toplevel(self)
        popup.title(ex["title"])
        popup.geometry("400x600")
        popup.resizable(False, False)

        ttk.Label(popup, text=ex["title"], font=("Arial", 16, "bold")).pack(pady=10)
        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        info = {
            "Description": ex.get("description", "No description"),
            "Tags": ", ".join(ex.get("tags", [])) or "None",
            "Created": ex.get("created_at", "Unknown"),
            "Last Updated": ex.get("last_updated", "Unknown")
        }

        # Show only if data exists
        if ex["weight"]["has"]:
            info["Default Weight"] = f"{ex['weight']['default']} {ex['weight']['unit']}"
        if ex["reps"]["has"]:
            info["Default Reps"] = str(ex["reps"]["default"])
        if ex["sets"]["has"]:
            info["Default Sets"] = str(ex["sets"]["default"])
        if ex["time"]["has"]:
            info["Default Time"] = f"{ex['time']['default']} {ex['time']['unit']}"
        if ex["distance"]["has"]:
            info["Default Distance"] = f"{ex['distance']['default']} {ex['distance']['unit']}"

        for key, value in info.items():
            ttk.Label(frame, text=f"{key}:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
            ttk.Label(frame, text=value, wraplength=350).pack(anchor="w", padx=10)

        ttk.Button(frame, text="Edit", command=lambda: self.edit_exercise_popup(ex, popup)).pack(side="left", padx=10)
        ttk.Button(frame, text="Remove", command=lambda: self.remove_exercise_popup(ex, popup)).pack(side="left", padx=10)
        ttk.Button(frame, text="Close", command=popup.destroy).pack(side="left", padx=10)

    # ---------- EDIT EXERCISE ----------
    def edit_exercise_popup(self, ex, parent_popup=None):
        popup = tk.Toplevel(self)
        popup.title(f"Edit Exercise: {ex['title']}")
        popup.geometry("400x600")
        popup.resizable(False, False)

        ttk.Label(popup, text=f"Edit {ex['title']}", font=("Arial", 16)).pack(pady=10)
        frame = ttk.Frame(popup)
        frame.pack(pady=10, fill="x")

        entries = {}

        # --- Helper to create a row with label, entry, and optional unit ---
        def create_row(row, label_text, value="", unit_options=None, unit_value=None):
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", padx=10, pady=3)
            entry = ttk.Entry(frame, width=20)
            entry.grid(row=row, column=1, padx=5, pady=3, sticky="w")
            entry.insert(0, value)
            entries[label_text] = entry

            combo = None
            if unit_options:
                combo = ttk.Combobox(frame, values=unit_options, width=5)
                combo.grid(row=row, column=2, padx=5, pady=3, sticky="w")
                combo.set(unit_value or unit_options[0])
                entries[f"{label_text}_unit"] = combo
            return entry, combo

        row_idx = 0
        # Always visible fields
        create_row(row_idx, "Title", ex["title"])
        row_idx += 1
        create_row(row_idx, "Description", ex.get("description", ""))
        row_idx += 1
        create_row(row_idx, "Tags (comma-separated)", ", ".join(ex.get("tags", [])))
        row_idx += 1

        # Collapsible sections: weight, reps, sets, time, distance
        # Using Checkbuttons to toggle display
        def create_collapsible(name, default_val, goal_val, unit_options=None, unit_value=None):
            nonlocal row_idx
            var = tk.IntVar(value=1 if default_val > 0 else 0)
            chk = ttk.Checkbutton(frame, text=name.capitalize(), variable=var)
            chk.grid(row=row_idx, column=0, sticky="w", padx=10, pady=3)
            section_frame = ttk.Frame(frame)
            section_frame.grid(row=row_idx+1, column=0, columnspan=3, padx=20, sticky="w")
            row_idx_local = 0

            def toggle():
                if var.get():
                    section_frame.grid()
                else:
                    section_frame.grid_remove()
            var.trace_add("write", lambda *args: toggle())
            toggle()

            # Default and Goal entries
            create_row_inside = lambda r, label, val: ttk.Entry(section_frame, width=10).grid(row=r, column=0, padx=5, pady=2)
            default_entry, unit_combo = create_row_inside(0, "Default", default_val), None
            goal_entry, _ = create_row_inside(1, "Goal", goal_val), None

            # Use actual Entry widgets to store in entries dict
            default_entry = ttk.Entry(section_frame, width=10)
            default_entry.grid(row=0, column=0, padx=5, pady=2)
            default_entry.insert(0, default_val)
            entries[f"{name}_Default"] = default_entry

            goal_entry = ttk.Entry(section_frame, width=10)
            goal_entry.grid(row=0, column=1, padx=5, pady=2)
            goal_entry.insert(0, goal_val)
            entries[f"{name}_Goal"] = goal_entry

            if unit_options:
                unit_combo = ttk.Combobox(section_frame, values=unit_options, width=5)
                unit_combo.grid(row=0, column=2, padx=5, pady=2)
                unit_combo.set(unit_value or unit_options[0])
                entries[f"{name}_unit"] = unit_combo

            row_idx += 2  # leave space for the section
            return var

        create_collapsible("weight", ex["weight"]["default"], ex["weight"]["goal"], ["bodyweight", "kg", "lb"], ex["weight"].get("unit"))
        create_collapsible("reps", ex["reps"]["default"], ex["reps"]["goal"])
        create_collapsible("sets", ex["sets"]["default"], ex["sets"]["goal"])
        create_collapsible("time", ex["time"]["default"], ex["time"]["goal"], ["sec", "min", "hr"], ex["time"].get("unit"))
        create_collapsible("distance", ex["distance"]["default"], ex["distance"]["goal"], ["m", "km"], ex["distance"].get("unit"))

        # --- Save / Cancel buttons at bottom ---
        button_frame = ttk.Frame(popup)
        button_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Button(button_frame, text="Save Changes", command=lambda: self._save_edit(entries, ex, popup, parent_popup)).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10)

    # ---------- REMOVE EXERCISE ----------
    def remove_exercise_popup(self, ex, parent_popup=None):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{ex['title']}'?")
        if confirm:
            try:
                remove_exercise(ex["id"])
                messagebox.showinfo("Deleted", f"Exercise '{ex['title']}' has been removed.")
                self._update_exercise_list()
                if parent_popup: parent_popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove exercise:\n{e}")
