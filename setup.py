import os
import sys
from setuptools import setup, find_packages
import frame_window_setup

APP = ['main.py']
APP_NAME = "Opera Access"
DATA_FILES = ["app.py" "static", "templates",]
OPTIONS = {}

OPTIONS = {
    'iconfile': 'favicon.icns',
}

setup(
    name="Opera Access",
    version="0.1",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    packages=find_packages(),

)



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

frame_window_setup.root.bind("<KeyPress>", frame_window_setup.on_key_press)
# Run the Tkinter root
frame_window_setup.root.mainloop()