import tkinter as tk
import customtkinter as ctk
from  definitions.definition import change_appearance_mode_event

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.progress = self.create_progress_bar()
        self.navigation_frame = self.main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.appearance_mode_optionmenu = self.create_appearance_mode_optionmenu()

    def create_progress_bar(self):
        progress = ctk.CTkProgressBar(self.root, orientation="horizontal")
        progress.grid(row=0, column=1, columnspan=3, padx=0, pady=0, sticky="new")
        progress.configure(mode="determinate")
        progress.set(0)
        return progress

    def main_frame(self):
        navigation_frame = tk.LabelFrame(self.root, height=900)
        navigation_frame.grid(row=1, rowspan=6, column=1, columnspan=2, padx=20, pady=10, sticky="nwse")
        navigation_frame.grid_rowconfigure(0, weight=1)
        navigation_frame.grid_columnconfigure(0, weight=1)
        return navigation_frame

    def create_sidebar_frame(self):
        sidebar_frame = ctk.CTkFrame(self.root, width=100, corner_radius=0, border_width=2)
        sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        sidebar_frame.grid_rowconfigure(8, weight=1)
        sidebar_frame.grid_columnconfigure(1, weight=1)
        return sidebar_frame

    def create_appearance_mode_optionmenu(self):
        appearance_mode_optionmenu = ctk.CTkOptionMenu(self.root, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
        appearance_mode_optionmenu.grid(row=9, column=0, padx=10, pady=10, sticky="s")
        appearance_mode_optionmenu.set("Dark")
        return appearance_mode_optionmenu

def create_main_window():
    root = ctk.CTk()
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    root.title("Opera Access 1.0")
    root.configure(bg=ctk.set_appearance_mode("System"))
    root.geometry(f"{1000}x{550}")
    root.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    root.columnconfigure((0,1,2), weight=1)
    return root