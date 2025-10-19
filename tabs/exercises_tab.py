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

        ttk.Button(
            frame, 
            text="Add Exercise", 
            command=self.open_add_exercise_window
            ).pack(side="left", padx=5)

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

    # ---------- LIVE SEARCH HANDLER ----------
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

    # ---------- DOUBLE-CLICK HANDLER ----------
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


    # ---------- CREATE COLLAPSIBLE ----------
    def create_collapsible_sections(self, parent):
        """
        Create collapsible exercise metric sections (weight, reps, sets, time, distance)
        inside the given parent frame. Returns a dict of IntVars for each section.
        """
        checkbox_frame = ttk.Frame(parent)
        checkbox_frame.pack(fill="x", padx=10, pady=5)

        section_vars = {}

        sections = [
            ("weight", ["Default", "Goal"], ["kg", "lb"]),
            ("reps", ["Default", "Goal"], None),
            ("sets", ["Default", "Goal"], None),
            ("time", ["Default", "Goal"], ["sec", "min", "hr"]),
            ("distance", ["Default", "Goal"], ["m", "km"]),
        ]

        for col, (name, fields, units) in enumerate(sections):
            var = tk.IntVar(value=0)
            section_vars[name] = var

            # Checkbutton to toggle visibility
            chk = ttk.Checkbutton(checkbox_frame, text=name.capitalize(), variable=var)
            chk.grid(row=0, column=col, padx=5, sticky="w")

            # Hidden section frame
            section_frame = ttk.Frame(parent)
            section_frame.pack(fill="x", padx=20, pady=2)
            section_frame.pack_forget()  # hidden by default

            # Toggle visibility
            def toggle(var=var, frame=section_frame):
                if var.get():
                    frame.pack(fill="x", padx=20, pady=2)
                else:
                    frame.pack_forget()

            var.trace_add("write", lambda *args, v=var, f=section_frame: toggle(v, f))

            # Add fields (Default, Goal)
            for i, f in enumerate(fields):
                ttk.Label(section_frame, text=f"{name.capitalize()} {f}:").grid(
                    row=0, column=i, sticky="w", padx=5, pady=2
                )
                ttk.Entry(section_frame, width=10).grid(row=1, column=i, padx=5, pady=2)

            # Add unit combo if applicable
            if units:
                ttk.Label(section_frame, text="Unit:").grid(row=0, column=len(fields), sticky="w", padx=5)
                combo = ttk.Combobox(section_frame, values=units, width=8)
                combo.set(units[0])
                combo.grid(row=1, column=len(fields), padx=5, pady=2)

        return section_vars


    # ---------- ADD EXERCISE POPUP ----------
    def open_add_exercise_window(self):
        popup = tk.Toplevel(self)
        popup.title("Add Exercise")
        popup.geometry("400x600")
        popup.resizable(False, False)

        ttk.Label(popup, text="Add New Exercise", font=("Arial", 16)).pack(pady=10)
        frame = ttk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.entries = {}

        # Always visible fields
        for label in ["Title", "Description", "Tags (comma-separated)"]:
            ttk.Label(frame, text=label).pack(anchor="w", padx=10, pady=3)
            entry = ttk.Entry(frame, width=40)
            entry.pack(padx=10)
            self.entries[label] = entry

        self.section_vars = self.create_collapsible_sections(frame)


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

        ttk.Button(frame, text="Save Exercise", command=save_exercise).pack(side="left", padx=10)
        ttk.Button(frame, text="Close", command=popup.destroy).pack(side="left", padx=10)

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
            "Tags": ", ".join(ex.get("tags", [])) or "None"
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

        info["Created"] = ex.get("created_at", "Unknown")
        info["Last Updated"] = ex.get("last_updated", "Unknown")

        for key, value in info.items():
            ttk.Label(frame, text=f"{key}:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 0))
            ttk.Label(frame, text=value, wraplength=350).pack(anchor="w", padx=10)

        ttk.Button(frame, text="Edit", command=lambda: self.edit_exercise_popup(ex, popup)).pack(side="left", padx=10)
        ttk.Button(frame, text="Remove", command=lambda: self.remove_exercise_popup(ex, frame, popup)).pack(side="left", padx=10)
        ttk.Button(frame, text="Close", command=popup.destroy).pack(side="left", padx=10)

    # ---------- EDIT EXERCISE POPUP ----------
    def edit_exercise_popup(self, ex, parent_popup=None):
        popup = tk.Toplevel(self)
        popup.title(f"Edit Exercise: {ex['title']}")
        popup.geometry("400x600")
        popup.resizable(False, False)

        ttk.Label(popup, text=f"Edit {ex['title']}", font=("Arial", 16)).pack(pady=10)
        frame = ttk.Frame(popup)
        frame.pack(pady=10, fill="x")

        # Store entry widgets for later access (title, desc, tags)
        self.entries = {}

        # --- Basic info fields ---
        for label, value in [
            ("Title", ex["title"]),
            ("Description", ex.get("description", "")),
            ("Tags (comma-separated)", ", ".join(ex.get("tags", []))),
        ]:
            ttk.Label(frame, text=label).pack(anchor="w", padx=10, pady=3)
            entry = ttk.Entry(frame, width=40)
            entry.insert(0, value)
            entry.pack(padx=10)
            self.entries[label] = entry

        # --- Collapsible exercise sections ---
        self.section_vars = self.create_collapsible_sections(frame)

        # --- Prefill existing data into collapsible sections ---
        def prefill_section_data():
            for name, var in self.section_vars.items():
                if name not in ex:
                    continue
                section_data = ex[name]

                # Automatically expand section if it has data
                has_data = section_data.get("default", 0) or section_data.get("goal", 0)
                if has_data:
                    var.set(1)

                # Find and fill widgets within this section
                for child in frame.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for subchild in child.winfo_children():
                            if isinstance(subchild, ttk.Label):
                                text = subchild.cget("text").lower()
                                if "default" in text:
                                    # Find the next Entry widget
                                    next_widgets = [w for w in child.winfo_children() if isinstance(w, ttk.Entry)]
                                    if next_widgets:
                                        next_widgets[0].delete(0, tk.END)
                                        next_widgets[0].insert(0, section_data.get("default", 0))
                                elif "goal" in text:
                                    next_widgets = [w for w in child.winfo_children() if isinstance(w, ttk.Entry)]
                                    if len(next_widgets) > 1:
                                        next_widgets[1].delete(0, tk.END)
                                        next_widgets[1].insert(0, section_data.get("goal", 0))
                                elif "unit" in text:
                                    combos = [w for w in child.winfo_children() if isinstance(w, ttk.Combobox)]
                                    if combos:
                                        combos[0].set(section_data.get("unit", combos[0]["values"][0]))

        prefill_section_data()

        # --- Buttons ---
        button_frame = ttk.Frame(popup)
        button_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(button_frame,text="Save Changes",command=lambda: self.save_edit(ex, popup, parent_popup)).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10)


    # ---------- SAVE EDITED EXERCISE CONFIRM ----------
    def save_edit(self, ex, popup=None, parent_popup=None):
        confirm = messagebox.askyesno(
            "Confirm Edit",
            f"Are you sure you want to save changes to '{ex['title']}'?"
        )
        if not confirm:
            return

        try:
            # --- Gather data from fields ---
            title = self.entries["Title"].get().strip()
            if not title:
                raise ValueError("Title is required.")
            description = self.entries["Description"].get().strip()
            tags = [t.strip() for t in self.entries["Tags (comma-separated)"].get().split(",") if t.strip()]

            # Helper to find matching widgets dynamically (so we can reuse the collapsible UI)
            def find_value_for_field(section, label_contains):
                """Finds entry or combobox in a section frame by matching label text."""
                for child in self.section_vars:
                    pass  # placeholder

            # --- Build updated data dict ---
            # We’ll iterate over all sections that are toggled ON
            data = {
                "title": title,
                "description": description,
                "tags": tags,
            }

            for section_name, var in self.section_vars.items():
                if not var.get():
                    continue  # skip collapsed sections

                section_frame = None
                # find frame associated with this section
                for child in popup.winfo_children():
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ttk.Frame):
                            # crude check if it belongs to this section
                            for lbl in grandchild.winfo_children():
                                if isinstance(lbl, ttk.Label) and lbl.cget("text").lower().startswith(section_name):
                                    section_frame = grandchild
                                    break
                    if section_frame:
                        break

                if not section_frame:
                    continue

                # extract values
                entries = [w for w in section_frame.winfo_children() if isinstance(w, ttk.Entry)]
                combo_boxes = [w for w in section_frame.winfo_children() if isinstance(w, ttk.Combobox)]

                default_val = float(entries[0].get() or 0) if entries else 0
                goal_val = float(entries[1].get() or 0) if len(entries) > 1 else default_val
                unit = combo_boxes[0].get() if combo_boxes else None

                metric = {"default": default_val, "goal": goal_val}
                if unit:
                    metric["unit"] = unit
                data[section_name] = metric

            # --- Normalize and Save ---
            normalized = normalize_exercise_data(data, existing_id=ex["id"])
            edit_exercise(ex["id"], normalized)

            messagebox.showinfo("Success", f"Exercise '{title}' updated successfully.")
            self._update_exercise_list()
            if popup:
                popup.destroy()
            if parent_popup:
                parent_popup.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes:\n{e}")


    # ---------- REMOVE EXERCISE CONFIRM ----------
    def remove_exercise_popup(self, ex, parent=None, parent_popup=None):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{ex['title']}'?")
        if confirm:
            try:
                remove_exercise(ex["id"])
                messagebox.showinfo("Deleted", f"Exercise '{ex['title']}' has been removed.")
                self._update_exercise_list()
                if parent: parent.destroy()
                if parent_popup: parent_popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove exercise:\n{e}")
