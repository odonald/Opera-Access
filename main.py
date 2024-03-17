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





# Create a text box for entering the line number
line_number_var = StringVar()
line_number_entry = ctk.CTkEntry(navigation_frame3, placeholder_text="Jump to line")
line_number_entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")



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