import tkinter as tk
from tkinter import ttk


class WorkoutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

    def function_name(self, arg):
        return