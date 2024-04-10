import tkinter as tk
import customtkinter as ctk

def create_progress_bar(root):
    progress = ctk.CTkProgressBar(root, orientation="horizontal")
    progress.grid(row=0, column=1, columnspan=3, padx=0, pady=0, sticky="new")
    progress.configure(mode="determinate")
    progress.set(0)
    return progress

def create_main_window():
    root = ctk.CTk()
    root.title("Opera Access 1.0")
    root.configure(bg=ctk.set_appearance_mode("System"))
    root.geometry(f"{1000}x{550}")
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(3, weight=3)

    progress = create_progress_bar(root)

    return root, progress