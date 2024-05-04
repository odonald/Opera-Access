import os
import signal
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    """Restart the application if a .py file changes."""

    def __init__(self):
        self.observer_process = None
        self.path = None  
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        print(f'File changed: {event.src_path}')
        if self.observer_process:
            self.observer_process.terminate()
            self.observer_process.wait()
        print('Hot reload triggered. Restarting application...')
        self.start_application()

    def start_application(self):
        command = ['python', os.path.join(self.path, 'run.py'), '--debug']
        self.observer_process = subprocess.Popen(command, cwd=self.path)

def start_observer(path):
    event_handler = ChangeHandler()
    event_handler.path = path  
    event_handler.start_application() 
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    path = os.path.dirname(os.path.abspath(__file__))
    start_observer(path)

if __name__ == '__main__':
    main()
