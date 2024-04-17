from logic.application import Application
from ui.ui import create_main_window
from utils.logger_config import setup_logging, parse_arguments
from logic.application import Application
from utils.logger_config import setup_logging

debug_mode = parse_arguments()

setup_logging(debug_mode)

def main():
    root = create_main_window()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
