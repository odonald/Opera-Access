import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

# Create the Tkinter root
root = ctk.CTk()
root.title("Opera Access 1.0")
root.configure(bg=ctk.set_appearance_mode("System"))
root.geometry(f"{1000}x{550}")

# configure grid layout (4x4)
root.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
root.columnconfigure((0,1,2), weight=1)

def on_mousewheel(event):
    platform = event.widget.tk.call('tk', 'windowingsystem')
    
    # For macOS
    if platform == "aqua":
        canvas.yview_scroll(-1*(event.delta), "units")
    # For Windows
    elif platform == "win32":
        canvas.yview_scroll(-1*(event.delta//120), "units")
    # For Linux
    else:
        canvas.yview_scroll(-1 if event.num == 4 else 1, "units")


navigation_frame = tk.LabelFrame(root, height=900)
navigation_frame.grid(row=1, rowspan=6, column=1, columnspan=2, padx=20, pady=10, sticky="nwse")
navigation_frame.grid_rowconfigure(0, weight=1)
navigation_frame.grid_columnconfigure(0, weight=1)


canvas = tk.Canvas(navigation_frame)
canvas.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(navigation_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=3, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = ctk.CTkFrame(canvas)
canvas_frame = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Binding the scrolling action to the navigation_frame and its children
# inner_frame.bind_class('Tk', '<MouseWheel>', on_mousewheel)  # for Windows
# inner_frame.bind_class('Tk', '<Button-4>', on_mousewheel)    # for macOS and Linux (scroll up)
# inner_frame.bind_class('Tk', '<Button-5>', on_mousewheel)    # for macOS and Linux (scroll down)

def resize_inner_frame(event):
    canvas.itemconfig(canvas_frame, width=event.width)


canvas.bind("<Configure>", resize_inner_frame)
canvas.bind("<MouseWheel>", on_mousewheel)
inner_frame.bind("<MouseWheel>", on_mousewheel)


# Calculate and set scrollbar position to 50% on load

# Configure row and column weights for resizing


# language = tk.StringVar(value="German")
# language_switcher = ttk.OptionMenu(navigation_frame, language, command=lambda _: update_label())
# language_switcher.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Create the percentage label
# percentage_label = ctk.CTkLabel(navigation_frame, text="%")
# percentage_label.grid(row=1, column=1, sticky="ns")


def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


inner_frame.bind("<Configure>", on_canvas_configure)

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.configure(scrollregion=canvas.bbox("all"))
scrollbar.configure(command=canvas.yview)

inner_frame.bind("<Configure>", on_canvas_configure)

def bind_scroll_to_widget(widget):
    widget.bind("<MouseWheel>", on_mousewheel)
    for child in widget.winfo_children():
        bind_scroll_to_widget(child)

bind_scroll_to_widget(inner_frame)

def set_scroll_to_center():
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0.1)

root.after(100, set_scroll_to_center)

# progress = ctk.CTkProgressBar(navigation_frame, length=500, maximum=len(combined_lines), mode='determinate', value=current_line)

# label = tk.Label(root, wraplength=500)
# label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
navigation_frame2 = ctk.CTkFrame(root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
navigation_frame2.grid(row=8, column=2,rowspan=1, padx=0, pady=0, sticky="w")
navigation_frame3 = ctk.CTkFrame(root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
navigation_frame3.grid(row=8, column=1,rowspan=1, padx=0, pady=0, sticky="e")

# Create a 'Go' button to jump to the specified line number
go_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Go", command=jump_to_line)
go_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

previous_button = ctk.CTkButton(navigation_frame3,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Previous", command=previous_line)
previous_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

next_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Next", command=next_line)
next_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")