import pytest
import tkinter as tk
import customtkinter as ctk
from ui.ui import UserInterface, create_main_window

@pytest.fixture
def user_interface():
    root = create_main_window()
    yield UserInterface(root)
    root.quit()
    root.withdraw()

class TestUserInterface:
    def test_progress_bar(self, user_interface):
        print(" -> test_progress_bar: ", end="")
        assert isinstance(user_interface.progress, ctk.CTkProgressBar)
        assert user_interface.progress.cget("mode") == "determinate"
        print("successful")

       # Returns a tkinter LabelFrame object.
class TestMainFrame:

    # Returns a tkinter LabelFrame object.
    def test_returns_label_frame_object(self):
        root = tk.Tk()
        ui = UserInterface(root)
        result = ui.main_frame()
        assert isinstance(result, tk.LabelFrame)

    def test_create_label_frame_with_height_900(self):
                root = tk.Tk()
                ui = UserInterface(root)
                frame = ui.main_frame()
                assert isinstance(frame, tk.LabelFrame)
                assert frame['height'] == 900
                
    # The root object is None.
    def test_root_object_is_none(self):
        ui = UserInterface(None)
        result = ui.main_frame()
        assert isinstance(result, tk.LabelFrame)

    # Define other test methods similarly, accepting the user_interface fixture as an argument