import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import StringVar
from logic.application import Application
from ui.ui import create_main_window
import logging
import argparse

parser = argparse.ArgumentParser(description='My Application')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(filename='app_debug.log', level=logging.DEBUG)

logging.debug('This message will go to the debug log file or terminal')

def main():
    root = create_main_window()
    app = Application(root)


    for index, label in enumerate(app.ui.prev_line_labels, start=0):
        label.grid(row=index, column=0, padx=10, pady=10)

    app.ui.current_line_label.grid(row=5, column=0, padx=10, pady=10)

    for index, label in enumerate(app.ui.next_line_labels, start=6):
        label.grid(row=index, column=0, padx=10, pady=10)



    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    if not args.debug:
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