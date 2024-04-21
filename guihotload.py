import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GuiReloader(FileSystemEventHandler):
    def __init__(self, gui_script):
        self.gui_script = gui_script
        self.gui_process = None

    def on_modified(self, event):
        if event.src_path.endswith(self.gui_script):
            print(f"Detected changes in {self.gui_script}. Reloading GUI...")
            self.reload_gui()

    def reload_gui(self):
        if self.gui_process:
            self.gui_process.terminate()
            self.gui_process.wait()
        self.gui_process = subprocess.Popen(["python", self.gui_script])

if __name__ == "__main__":
    gui_script = "run.py"  # Replace with the name of your GUI script
    event_handler = GuiReloader(gui_script)
    observer = Observer()
    observer.schedule(event_handler, path=os.getcwd(), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()