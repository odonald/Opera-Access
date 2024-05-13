import pytest
import tkinter as tk
from ui.ui import UserInterface
from logic.application import Application

@pytest.fixture(scope="session")
def root():
    root = tk.Tk()
    root.withdraw() 
    yield root
    root.destroy()

@pytest.fixture(scope="session")
def ui(root):
    ui = UserInterface(root)
    yield ui

@pytest.fixture(scope="function")
def app():
    app = Application(None)
    app.sse_url = "http://example.com/sse"
    app.additional_languages = {
        "en": ["Line 1", "Line 2", "Line 3"],
        "es": ["Línea 1", "Línea 2", "Línea 3"]
    }
    yield app