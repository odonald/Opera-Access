import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import StringVar
from logic.application import Application
from ui.ui import create_main_window
import logging

logging.basicConfig(filename='app_debug.log', level=logging.DEBUG)

logging.debug('This message will go to the debug log file')

def main():
    root = create_main_window()
    app = Application(root)

    import_translation_button = ctk.CTkButton(app.ui.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Import Text", command=app.import_additional_language)
    import_translation_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")

    show_qr_button = ctk.CTkButton(app.ui.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Show QR", command=lambda: app.show_qr_code())
    show_qr_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")

    website_button = ctk.CTkButton(app.ui.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Open Website", command=app.open_url_in_browser)
    website_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")

    for index, label in enumerate(app.ui.prev_line_labels, start=0):
        label.grid(row=index, column=0, padx=10, pady=10)

    app.ui.current_line_label.grid(row=5, column=0, padx=10, pady=10)

    for index, label in enumerate(app.ui.next_line_labels, start=6):
        label.grid(row=index, column=0, padx=10, pady=10)

    previous_button = ctk.CTkButton(app.ui.navigation_frame3, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Previous", command=app.previous_line)
    previous_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    next_button = ctk.CTkButton(app.ui.navigation_frame2, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Next", command=app.next_line)
    next_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    line_number_var = StringVar()
    app.ui.line_number_entry = ctk.CTkEntry(app.ui.navigation_frame3, placeholder_text="Jump to line")
    app.ui.line_number_entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    go_button = ctk.CTkButton(app.ui.navigation_frame2, fg_color="transparent", text_color=("gray10", "#DCE4EE"), border_width=2, text="Go", command=app.jump_to_line)
    go_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    if os.name == 'nt':
        logs_folder = 'logs'
    else:
        logs_folder = '.logs'

    log_dir = os.path.join(application_path, logs_folder)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    stdout_log_path = os.path.join(log_dir, 'my_stdout.log')
    stderr_log_path = os.path.join(log_dir, 'my_stderr.log')

    sys.stdout = open(stdout_log_path, 'w')
    sys.stderr = open(stderr_log_path, 'w')

    root.mainloop()
    
if __name__ == "__main__":
    main()