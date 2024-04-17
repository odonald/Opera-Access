from logic.application import Application
from ui.ui import create_main_window
from logic.application import Application

def main():
    root = create_main_window()
    Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()