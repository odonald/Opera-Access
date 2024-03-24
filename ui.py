import tkinter as tk
import customtkinter as ctk

def create_main_window():
    root = ctk.CTk()
    root.title("Opera Access 1.0")
    root.configure(bg=ctk.set_appearance_mode("System"))
    root.geometry(f"{1000}x{550}")
    return root