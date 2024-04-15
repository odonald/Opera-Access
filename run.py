from ui.ui import create_main_window
from main import start_application

def run():
    root = create_main_window()
    start_application(root)
    root.mainloop()

if __name__ == "__main__":
    run()