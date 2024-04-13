import pytest
import tkinter as tk
from ui.ui import UserInterface, create_main_window

@pytest.fixture
def user_interface():
    root = create_main_window()
    yield UserInterface(root)
    root.quit()
    root.withdraw()