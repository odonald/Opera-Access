import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

@pytest.mark.usefixtures("root", "ui")
class TestUIComponents:
    def test_create_website_button(self, ui):
        website_button = ui.create_website_button()
        assert isinstance(website_button, ctk.CTkButton)
        assert website_button.cget("text") == "Open Website"

    def test_create_website_button_disabled(self, ui):
        website_button = ui.create_website_button()
        website_button.configure(state="disabled")
        assert website_button.cget("state") == "disabled"

    def test_create_import_translation_button(self, ui):
        import_translation_button = ui.create_import_translation_button()
        assert isinstance(import_translation_button, ctk.CTkButton)
        assert import_translation_button.cget("text") == "Import Text"

    def test_create_show_qr_button(self, ui):
        show_qr_button = ui.create_show_qr_button()
        assert isinstance(show_qr_button, ctk.CTkButton)
        assert show_qr_button.cget("text") == "Show QR"

    def test_create_show_qr_button_hidden(self, ui):
        show_qr_button = ui.create_show_qr_button()
        show_qr_button.grid_remove()
        assert not show_qr_button.winfo_viewable()

    def test_create_appearance_mode_optionmenu(self, ui):
        appearance_mode_optionmenu = ui.create_appearance_mode_optionmenu()
        assert isinstance(appearance_mode_optionmenu, ctk.CTkOptionMenu)
        assert appearance_mode_optionmenu.cget("values") == ["Light", "Dark", "System"]

    def test_create_appearance_mode_optionmenu_default_value(self, ui):
        appearance_mode_optionmenu = ui.create_appearance_mode_optionmenu()
        assert appearance_mode_optionmenu.get() == "Dark"

    def test_create_previous_line_button(self, ui):
        previous_line_button = ui.create_previous_line_button()
        assert isinstance(previous_line_button, ctk.CTkButton)
        assert previous_line_button.cget("text") == "Previous"

    def test_create_previous_line_button_state(self, ui):
        previous_line_button = ui.create_previous_line_button()
        previous_line_button.configure(state="normal")
        assert previous_line_button.cget("state") == "normal"

    def test_create_next_line_button(self, ui):
        next_line_button = ui.create_next_line_button()
        assert isinstance(next_line_button, ctk.CTkButton)
        assert next_line_button.cget("text") == "Next"

    def test_create_line_number_entry(self, ui):
        line_number_entry = ui.create_line_number_entry()
        assert isinstance(line_number_entry, ctk.CTkEntry)
        assert line_number_entry.cget("placeholder_text") == "Jump to line"

    def test_create_line_number_entry_initial_value(self, ui):
        line_number_entry = ui.create_line_number_entry()
        assert line_number_entry.get() == ""

    def test_create_go_button(self, ui):
        go_button = ui.create_go_button(None)
        assert isinstance(go_button, ctk.CTkButton)
        assert go_button.cget("text") == "Go"

    def test_create_go_button_state(self, ui):
        go_button = ui.create_go_button(None)
        go_button.configure(state="disabled")
        assert go_button.cget("state") == "disabled"

    def test_create_progress_bar(self, ui):
        progress_bar = ui.create_progress_bar()
        assert isinstance(progress_bar, ctk.CTkProgressBar)
        assert progress_bar.cget("mode") == "determinate"

    def test_create_progress_bar_initial_value(self, ui):
        progress_bar = ui.create_progress_bar()
        assert progress_bar.get() == 0.0

    def test_main_frame(self, ui):
        navigation_frame, navigation_frame2, navigation_frame3 = ui.main_frame()
        assert isinstance(navigation_frame, tk.LabelFrame)
        assert isinstance(navigation_frame2, ctk.CTkFrame)
        assert isinstance(navigation_frame3, ctk.CTkFrame)

    def test_create_canvas(self, ui):
        canvas = ui.create_canvas()
        assert isinstance(canvas, tk.Canvas)

    def test_create_inner_frame(self, ui):
        inner_frame = ui.create_inner_frame()
        assert isinstance(inner_frame, ctk.CTkFrame)

    def test_create_inner_frame_children(self, ui):
        inner_frame = ui.create_inner_frame()
        assert len(inner_frame.winfo_children()) == 0

    def test_create_canvas_frame(self, ui):
        canvas_frame = ui.create_canvas_frame()
        assert isinstance(canvas_frame, int)

    def test_create_sidebar_frame(self, ui):
        sidebar_frame = ui.create_sidebar_frame()
        assert isinstance(sidebar_frame, ctk.CTkFrame)

    def test_create_sidebar_label(self, ui):
        sidebar_label = ui.create_sidebar_label()
        assert isinstance(sidebar_label, ctk.CTkLabel)
        assert sidebar_label.cget("text") == "Menu:"

    def test_create_sidebar_label_font(self, ui):
        sidebar_label = ui.create_sidebar_label()
        assert sidebar_label.cget("font") == ("", 20)

    def test_create_navigation_label(self, ui):
        navigation_label = ui.create_navigation_label()
        assert isinstance(navigation_label, ctk.CTkLabel)
        assert navigation_label.cget("text") == "Display:"

    def test_create_navigation_label_font(self, ui):
        navigation_label = ui.create_navigation_label()
        assert navigation_label.cget("font") == ("", 20)

    def test_labels_inner_frame(self, ui):
        current_line_label, prev_line_labels, next_line_labels = ui.labels_inner_frame()
        assert isinstance(current_line_label, ctk.CTkLabel)
        assert len(prev_line_labels) == 5
        assert len(next_line_labels) == 20

    def test_labels_inner_frame_current_line_label_font(self, ui):
        current_line_label, _, _ = ui.labels_inner_frame()
        assert current_line_label.cget("font") == ("", 25)
    @patch("tkinter.Toplevel")
    @patch("qrcode.QRCode.make_image")
    @patch("PIL.ImageTk.PhotoImage")
    @patch("tkinter.Label")
    def test_show_qr_button_opens_window_with_qr_code(self, mock_label, mock_photoimage, mock_make_image, mock_toplevel, ui):
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window

        def mock_mainloop():
            pass

        mock_window.mainloop = mock_mainloop

        ui.show_qr_button.invoke()

        mock_toplevel.assert_called_once()
        mock_window.title.assert_called_once_with("QR Code")
        mock_window.geometry.assert_called_once_with("600x600")

        mock_make_image.assert_called_once()
        mock_photoimage.assert_called_once_with(mock_make_image.return_value)

        mock_label.assert_called_once_with(mock_window, image=mock_photoimage.return_value)
        mock_label.return_value.pack.assert_called_once()