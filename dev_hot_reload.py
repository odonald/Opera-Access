import os
import signal
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers the restart of an application when a Python file is modified.

    Attributes:
        observer_process (subprocess.Popen): The process that runs the application.
        path (str): The path to the directory being observed.

    Methods:
        on_modified(event): Handles the on_modified event triggered by the watchdog observer. If the modified file is a Python file, it terminates the observer process and starts the application.
        start_application(): Starts the application by running the 'run.py' file with the '--debug' flag.

    """

    def __init__(self):
        self.observer_process = None
        self.path = None

    def on_modified(self, event):
        """
        Handles the on_modified event triggered by the watchdog observer. If the modified file is a Python file, it terminates the observer process and starts the application.

        Parameters:
            event (FileSystemEvent): The event object representing the file system event.

        """
        if event.is_directory or not event.src_path.endswith('.py'):
            return
        print(f'File changed: {event.src_path}')
        if self.observer_process:
            self.observer_process.terminate()
            self.observer_process.wait()
        print('Hot reload triggered. Restarting application...')
        self.start_application()

    def start_application(self):
        """
        Starts the application by running the 'run.py' file with the '--debug' flag.

        """
        command = ['python', os.path.join(self.path, 'run.py'), '--debug']
        self.observer_process = subprocess.Popen(command, cwd=self.path)


def start_observer(path):
    """
    Starts an observer to monitor file system events in a specified directory and triggers the restart of an application when a Python file is modified.

    Parameters:
        path (str): The path to the directory to be observed.

    Raises:
        KeyboardInterrupt: If the observer is interrupted by a keyboard interrupt.

    Example:
        start_observer('/path/to/directory')
    """
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
    """
    Runs the main function of the program.

    This function sets up the necessary signal handling and starts the observer to monitor file system events in the current directory. It then calls the 'start_observer' function to begin monitoring for changes in Python files and trigger the restart of the application.

    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    path = os.path.dirname(os.path.abspath(__file__))
    start_observer(path)


if __name__ == '__main__':
    main()
