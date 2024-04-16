import tkinter as tk
import customtkinter as ctk

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.navigation_frame, self.navigation_frame2, self.navigation_frame3 = self.main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.canvas = self.create_canvas()
        self.inner_frame = self.create_inner_frame()
        self.canvas_frame = self.create_canvas_frame()
        self.current_line_label, self.prev_line_labels, self.next_line_labels = self.labels_inner_frame()
        self.appearance_mode_optionmenu = self.create_appearance_mode_optionmenu()
        self.sidebar_label = self.create_sidebar_label()
        self.navigation_label = self.create_navigation_label()
        self.progress = self.create_progress_bar()
        self.website_button = self.create_website_button()

    def create_website_button(self):
        website_button = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Open Website")
        website_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")
        return website_button

    def create_show_qr_button(self, show_qr_code_command):
        show_qr_button = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Show QR", command=show_qr_code_command)
        show_qr_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
        return show_qr_button

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
        navigation_frame2 = ctk.CTkFrame(self.root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
        navigation_frame2.grid(row=8, column=2,rowspan=1, padx=0, pady=0, sticky="w")
        navigation_frame3 = ctk.CTkFrame(self.root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
        navigation_frame3.grid(row=8, column=1,rowspan=1, padx=0, pady=0, sticky="e")
        return navigation_frame, navigation_frame2, navigation_frame3
    
    def create_canvas(self):
        canvas = tk.Canvas(self.navigation_frame)
        canvas.grid(row=0, column=0, sticky="nsew")
        return canvas
    
    def create_inner_frame(self):
        inner_frame = ctk.CTkFrame(self.canvas)
        inner_frame.grid_rowconfigure((0, 1, 2), weight=1)
        inner_frame.grid_columnconfigure(0, weight=1)
        return inner_frame
    
    def create_canvas_frame(self):
        canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        return canvas_frame

    def create_sidebar_frame(self):
        sidebar_frame = ctk.CTkFrame(self.root, width=100, corner_radius=0, border_width=2)
        sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        sidebar_frame.grid_rowconfigure(8, weight=1)
        sidebar_frame.grid_columnconfigure(1, weight=1)
        return sidebar_frame
        
    def button_go_to_website(self):
        website_button = ctk.CTkButton(app.ui.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Open Website", command=app.open_url_in_browser)
        website_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")
        return website_button
    def create_sidebar_label(self):
        sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Menu:", font=("", 20))
        sidebar_label.grid(row=0, column=0, padx=20, pady=10, sticky="nwe")
        return sidebar_label

    def create_navigation_label(self):
        navigation_label = ctk.CTkLabel(self.root, text="Display:", font=("", 20))
        navigation_label.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="nwe")
        return navigation_label
    
    def labels_inner_frame(self):
        current_line_label = ctk.CTkLabel(self.inner_frame, text_color=("Yellow", "#FFD90F"), text="Please import a language or load a session.\n +\n <--- Choose display language", font=("", 25))
        current_line_label.grid(row=1, column=0, padx=10, pady=10)
        prev_line_labels = [ctk.CTkLabel(self.inner_frame, wraplength=400, text="---") for _ in range(5)]
        next_line_labels = [ctk.CTkLabel(self.inner_frame, wraplength=400, text="---") for _ in range(20)]
        return current_line_label, prev_line_labels, next_line_labels

    def create_appearance_mode_optionmenu(self):
        appearance_mode_optionmenu = ctk.CTkOptionMenu(self.root, values=["Light", "Dark", "System"], command=Events.change_appearance_mode_event)
        appearance_mode_optionmenu.grid(row=9, column=0, padx=10, pady=10, sticky="s")
        appearance_mode_optionmenu.set("Dark")
        return appearance_mode_optionmenu

class Events:
    def change_appearance_mode_event(new_appearance_mode: str):
            ctk.set_appearance_mode(new_appearance_mode)
            
def create_main_window():
    root = ctk.CTk()
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    root.title("Opera Access 1.0")
    root.configure(bg=ctk.set_appearance_mode("System"))
    root.geometry(f"{1000}x{550}")
    root.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    root.columnconfigure((0,1,2), weight=1)

    return root