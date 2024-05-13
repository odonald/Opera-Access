import pytest
import tkinter as tk
from ui.file_menu import FileMenu
from unittest.mock import Mock

@pytest.fixture(scope="session")
def callbacks():
    return {
        "save_qr_code": Mock(name="save_qr_code"),
        "show_qr_code": Mock(name="show_qr_code"),
        "import_additional_language": Mock(name="import_additional_language"),
        "save_session": Mock(name="save_session"),
        "load_session": Mock(name="load_session"),
        "open_url_in_browser": Mock(name="open_url_in_browser"),
        "change_port": Mock(name="change_port"),
        "clear_program": Mock(name="clear_program"),
        "close_program": Mock(name="close_program"),
    }
    
@pytest.fixture(scope="session")
def file_menu(root, callbacks):
    return FileMenu(root, callbacks)

def test_file_menu_creation(file_menu):
    assert isinstance(file_menu, FileMenu)

def test_file_menu_structure(file_menu):
    menu_bar = file_menu.master.winfo_children()[0]
    assert isinstance(menu_bar, tk.Menu)

    file_menu_widget = menu_bar.winfo_children()[0]
    assert file_menu_widget.entrycget(0, "label") == "Import additional language"
    assert file_menu_widget.entrycget(1, "label") == "Save Session"
    assert file_menu_widget.entrycget(2, "label") == "Load Session"
    assert file_menu_widget.entrycget(3, "label") == "Open Website"
    assert file_menu_widget.entrycget(4, "label") == "QR-Code"
    assert file_menu_widget.entrycget(5, "label") == "Change Port"
    assert file_menu_widget.entrycget(6, "label") == "Reset"
    assert file_menu_widget.entrycget(7, "label") == "Exit"

    qr_menu = file_menu_widget.nametowidget(file_menu_widget.entrycget(4, "menu"))
    assert qr_menu.entrycget(0, "label") == "Save QR Code"
    assert qr_menu.entrycget(1, "label") == "Show QR Code"

def test_file_menu_callbacks(file_menu, callbacks):
    menu_bar = file_menu.master.winfo_children()[0]
    file_menu_widget = menu_bar.winfo_children()[0]

    file_menu_widget.invoke(file_menu_widget.index("Import additional language"))
    callbacks["import_additional_language"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Save Session"))
    callbacks["save_session"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Load Session"))
    callbacks["load_session"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Open Website"))
    callbacks["open_url_in_browser"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Change Port"))
    callbacks["change_port"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Reset"))
    callbacks["clear_program"].assert_called_once()

    file_menu_widget.invoke(file_menu_widget.index("Exit"))
    callbacks["close_program"].assert_called_once()

    qr_menu = file_menu_widget.nametowidget(file_menu_widget.entrycget(file_menu_widget.index("QR-Code"), "menu"))

    qr_menu.invoke(qr_menu.index("Save QR Code"))
    callbacks["save_qr_code"].assert_called_once()

    qr_menu.invoke(qr_menu.index("Show QR Code"))
    callbacks["show_qr_code"].assert_called_once()
