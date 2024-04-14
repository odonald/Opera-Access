import customtkinter as ctk
from ui.ui import UserInterface
import tkinter as tk

class TestUserInterface:
    def test_progress_bar(self, user_interface):
        print(" -> test_progress_bar: ", end="")
        assert isinstance(user_interface.progress, ctk.CTkProgressBar)
        assert user_interface.progress.cget("mode") == "determinate"
        print("successful")
    
    def test_create_optionmenu_with_values(self, user_interface):
        optionmenu = user_interface.create_appearance_mode_optionmenu()
        assert isinstance(optionmenu, ctk.CTkOptionMenu)
        # assert optionmenu.values == ["Light", "Dark", "System"]
        
    def test_create_current_line_label(self):
        root = tk.Tk()
        ui = UserInterface(root)
        ui.create_current_line_label()
        label = ui.current_line_label
        assert label.cget("text") == "Please import a language or load a session.\n +\n <--- Choose display language"
        assert label.cget("font") == ("", 25)

class TestMainFrame:
    def test_returns_label_frame_object(self, user_interface):
        result = user_interface.main_frame()
        assert isinstance(result, tk.LabelFrame)

    def test_create_label_frame_with_height_900(self, user_interface):
        frame = user_interface.main_frame()
        assert isinstance(frame, tk.LabelFrame)
        assert frame['height'] == 900
                
    def test_root_object_is_none(self):
        ui = UserInterface(None)
        result = ui.main_frame()
        assert isinstance(result, tk.LabelFrame)