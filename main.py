import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, StringVar, simpledialog
import requests
import pickle
import threading
from functools import partial
import iso639
import socket
import charset_normalizer
import qrcode
from PIL import ImageTk, Image
from io import BytesIO
import webbrowser

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



def combine_files():
    global combined_lines
    if original_lines and translation_lines:
        combined_lines = list(zip(original_lines, translation_lines))
    else:
        combined_lines = [(line, "") for line in original_lines]
    update_label()

def on_key_press(event):
    if event.keysym == 'Right':
        next_line()
    elif event.keysym == 'Left':
        previous_line()



def run_server():
    from app import app
    host = local_ip
    port = port_number  # Replace with your desired port number
    app.run(debug=True, port=port, host=host, use_reloader=False)


# def start_stop_server(start):
#     global server_thread, server_running
#     if start:
#         server_thread = threading.Thread(target=run_server, daemon=True)
#         server_thread.start()
#         server_running = True
#         # server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
#         server_indicator.configure(bg="green")
#     else:
#         server_running = False
#         # server_button.configure(text="Start Server", command=partial(start_stop_server, True))
#         server_indicator.configure(bg="red")
#         # Stopping the Flask server is not straightforward; for now, the server will keep running
#         # You might want to look into using other server options (like Gunicorn)

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

previous_button = ctk.CTkButton(navigation_frame3,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Previous", command=previous_line)
previous_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

next_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Next", command=next_line)
next_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Create a text box for entering the line number
line_number_var = StringVar()
line_number_entry = ctk.CTkEntry(navigation_frame3, placeholder_text="Jump to line")
line_number_entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Create a 'Go' button to jump to the specified line number
go_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Go", command=jump_to_line)
go_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create the menu bar
menu_bar = tk.Menu(root)
root.configure(menu=menu_bar)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a submenu for "Import" option
qr_menu = tk.Menu(file_menu, tearoff=0)
qr_menu.add_command(label="Save QR Code", command=lambda: save_qr_code(url))
qr_menu.add_command(label="Show QR Code", command=lambda: show_qr_code(url))

file_menu.add_command(label="Import additional language", command=import_additional_language)
file_menu.add_command(label="Save Session", command=save_session)
file_menu.add_command(label="Load Session", command=load_session)
file_menu.add_command(label="Open Website", command=lambda: open_url_in_browser(local_ip, port_number))
file_menu.add_cascade(label="QR-Code", menu=qr_menu)
file_menu.add_command(label="Change Port", command=change_port)
file_menu.add_command(label="Reset", command=clear_program)
file_menu.add_command(label="Exit", command=close_program)





root.configure(menu=menu_bar)

root.protocol("WM_DELETE_WINDOW", close_program)



# configure rows and columns


# Place buttons in the left frame (column 0)




# save_button = ctk.CTkButton(root, text="Save Session", command=save_session)
# save_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# load_button = ctk.CTkButton(root, text="Load Session", command=load_session)
# load_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Place progress bar, label, and navigation buttons in the middle frame (column 1)
# CCREATE A LANGUAGE SWITCHER



# Place server button and indicator in the right frame (column 2)


# # If you want to update the server indicator color when the server starts or stops, you can use the following function
# def update_server_indicator(status):
#     if status:
#         server_indicator.configure(bg="green")
#     else:
#         server_indicator.configure(bg="red")

# # Update the start_stop_server function to call update_server_indicator
# def start_stop_server(status):
#     if status:
#         server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
#         update_server_indicator(True)
#     else:
#         server_button.configure(text="Start Server", command=partial(start_stop_server, True))
#         update_server_indicator(False)


# Get the directory where the application is running
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# Check the type of operating system
if os.name == 'nt':  # For Windows
    logs_folder = 'logs'
else:  # For Unix and MacOS
    logs_folder = '.logs'  # Use a dot to make the folder hidden on Unix systems

log_dir = os.path.join(application_path, logs_folder)

# Ensure the directory exists, if not, create it
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

stdout_log_path = os.path.join(log_dir, 'my_stdout.log')
stderr_log_path = os.path.join(log_dir, 'my_stderr.log')

sys.stdout = open(stdout_log_path, 'w')
sys.stderr = open(stderr_log_path, 'w')

root.bind("<KeyPress>", on_key_press)
# Run the Tkinter root
root.mainloop()