from logic.application import Application
from ui.ui import create_main_window
from utils.logger_config import setup_logging, parse_arguments

debug_mode = parse_arguments()

setup_logging(debug_mode)


def main():
    """
    Main function to start the application.

    This function creates the main window using the 'create_main_window' function from the 'ui' module.
    Then, it creates an instance of the 'Application' class and passes the root window as an argument.
    The 'app' variable is used to keep the Application instance alive.
    Finally, it starts the main event loop using the 'mainloop' method of the root window.

    Note: The 'app' variable must exist to keep the Application instance alive.

"""
    root = create_main_window()
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
