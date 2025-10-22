import tkinter as tk
from tkinter import ttk, messagebox


class SettingsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        # Factory Reset
        ttk.Button(frame, text="Factory Reset", command=self.factory_reset)

    def factory_reset():
        """ Remove all exercises, workout, and statistics."""
        confirm = messagebox.askyesno("Confirm Factory Reset", "Are you sure you would like to remove all exercise, workout, and statistics data?")
        if confirm:
            double_confirm = messagebox.askyesno("Double Check", "Are you REALLY sure? All data will be lost and cannot me recovered.")
            if double_confirm:
                tripple_confirm = messagebox.askyesno("LAST CHANCE", "This is your last chance at not removing all data.")
                if tripple_confirm:
                    """"Logic for removing all data. Easy memthod is to clear all .json files"""
                    return
