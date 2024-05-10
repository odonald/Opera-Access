import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
import customtkinter as ctk
from ui.ui import UserInterface


class TestUIComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        "Set up a hidden Tkinter root window for all tests, ensuring tests run headlessly."
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.ui = UserInterface(cls.root)

    @classmethod
    def tearDownClass(cls):
        "Destroy the Tkinter root window after all tests have run to clean up."
        cls.root.destroy()

    def test_create_website_button(self):
        website_button = self.ui.create_website_button()
        self.assertIsInstance(website_button, ctk.CTkButton)
        self.assertEqual(website_button.cget("text"), "Open Website")

    def test_create_website_button_disabled(self):
        website_button = self.ui.create_website_button()
        website_button.configure(state="disabled")
        self.assertEqual(website_button.cget("state"), "disabled")

    def test_create_import_translation_button(self):
        import_translation_button = self.ui.create_import_translation_button()
        self.assertIsInstance(import_translation_button, ctk.CTkButton)
        self.assertEqual(import_translation_button.cget("text"), "Import Text")

    def test_create_show_qr_button(self):
        show_qr_button = self.ui.create_show_qr_button()
        self.assertIsInstance(show_qr_button, ctk.CTkButton)
        self.assertEqual(show_qr_button.cget("text"), "Show QR")

    def test_create_show_qr_button_hidden(self):
        show_qr_button = self.ui.create_show_qr_button()
        show_qr_button.grid_remove()
        self.assertFalse(show_qr_button.winfo_viewable())

    def test_create_appearance_mode_optionmenu(self):
        appearance_mode_optionmenu = self.ui.create_appearance_mode_optionmenu()
        self.assertIsInstance(appearance_mode_optionmenu, ctk.CTkOptionMenu)
        self.assertEqual(appearance_mode_optionmenu.cget(
            "values"), ["Light", "Dark", "System"])

    def test_create_appearance_mode_optionmenu_default_value(self):
        appearance_mode_optionmenu = self.ui.create_appearance_mode_optionmenu()
        self.assertEqual(appearance_mode_optionmenu.get(), "Dark")

    def test_create_previous_line_button(self):
        previous_line_button = self.ui.create_previous_line_button()
        self.assertIsInstance(previous_line_button, ctk.CTkButton)
        self.assertEqual(previous_line_button.cget("text"), "Previous")

    def test_create_previous_line_button_state(self):
        previous_line_button = self.ui.create_previous_line_button()
        previous_line_button.configure(state="normal")
        self.assertEqual(previous_line_button.cget("state"), "normal")

    def test_create_next_line_button(self):
        next_line_button = self.ui.create_next_line_button()
        self.assertIsInstance(next_line_button, ctk.CTkButton)
        self.assertEqual(next_line_button.cget("text"), "Next")

    def test_create_line_number_entry(self):
        line_number_entry = self.ui.create_line_number_entry()
        self.assertIsInstance(line_number_entry, ctk.CTkEntry)
        self.assertEqual(line_number_entry.cget(
            "placeholder_text"), "Jump to line")

    def test_create_line_number_entry_initial_value(self):
        line_number_entry = self.ui.create_line_number_entry()
        self.assertEqual(line_number_entry.get(), "")

    def test_create_go_button(self):
        go_button = self.ui.create_go_button(None)
        self.assertIsInstance(go_button, ctk.CTkButton)
        self.assertEqual(go_button.cget("text"), "Go")

    def test_create_go_button_state(self):
        go_button = self.ui.create_go_button(None)
        go_button.configure(state="disabled")
        self.assertEqual(go_button.cget("state"), "disabled")

    def test_create_progress_bar(self):
        progress_bar = self.ui.create_progress_bar()
        self.assertIsInstance(progress_bar, ctk.CTkProgressBar)
        self.assertEqual(progress_bar.cget("mode"), "determinate")

    def test_create_progress_bar_initial_value(self):
        progress_bar = self.ui.create_progress_bar()
        self.assertEqual(progress_bar.get(), 0.0)

    def test_main_frame(self):
        navigation_frame, navigation_frame2, navigation_frame3 = self.ui.main_frame()
        self.assertIsInstance(navigation_frame, tk.LabelFrame)
        self.assertIsInstance(navigation_frame2, ctk.CTkFrame)
        self.assertIsInstance(navigation_frame3, ctk.CTkFrame)

    def test_create_canvas(self):
        canvas = self.ui.create_canvas()
        self.assertIsInstance(canvas, tk.Canvas)

    def test_create_inner_frame(self):
        inner_frame = self.ui.create_inner_frame()
        self.assertIsInstance(inner_frame, ctk.CTkFrame)

    def test_create_inner_frame_children(self):
        inner_frame = self.ui.create_inner_frame()
        self.assertEqual(len(inner_frame.winfo_children()), 0)

    def test_create_canvas_frame(self):
        canvas_frame = self.ui.create_canvas_frame()
        self.assertIsInstance(canvas_frame, int)

    def test_create_sidebar_frame(self):
        sidebar_frame = self.ui.create_sidebar_frame()
        self.assertIsInstance(sidebar_frame, ctk.CTkFrame)

    def test_create_sidebar_label(self):
        sidebar_label = self.ui.create_sidebar_label()
        self.assertIsInstance(sidebar_label, ctk.CTkLabel)
        self.assertEqual(sidebar_label.cget("text"), "Menu:")

    def test_create_sidebar_label_font(self):
        sidebar_label = self.ui.create_sidebar_label()
        self.assertEqual(sidebar_label.cget("font"), ("", 20))

    def test_create_navigation_label(self):
        navigation_label = self.ui.create_navigation_label()
        self.assertIsInstance(navigation_label, ctk.CTkLabel)
        self.assertEqual(navigation_label.cget("text"), "Display:")

    def test_create_navigation_label_font(self):
        navigation_label = self.ui.create_navigation_label()
        self.assertEqual(navigation_label.cget("font"), ("", 20))

    def test_labels_inner_frame(self):
        current_line_label, prev_line_labels, next_line_labels = self.ui.labels_inner_frame()
        self.assertIsInstance(current_line_label, ctk.CTkLabel)
        self.assertEqual(len(prev_line_labels), 5)
        self.assertEqual(len(next_line_labels), 20)

    def test_labels_inner_frame_current_line_label_font(self):
        current_line_label, _, _ = self.ui.labels_inner_frame()
        self.assertEqual(current_line_label.cget("font"), ("", 25))

    @patch('tkinter.Toplevel', autospec=True)
    @patch('qrcode.QRCode.make_image', autospec=True)
    @patch('PIL.ImageTk.PhotoImage', autospec=True)
    @patch('tkinter.Label', autospec=True)
    def test_show_qr_button_opens_window_with_qr_code(self, mock_label, mock_photoimage, mock_make_image, mock_toplevel):
        # Arrange
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window

        # Act
        self.ui.show_qr_button.invoke()

        # Assert
        mock_toplevel.assert_called_once()
        mock_window.title.assert_called_once_with("QR Code")
        mock_window.geometry.assert_called_once_with("600x600")
        mock_window.mainloop.assert_called_once()

        # Verify the QR code generation and display
        mock_make_image.assert_called_once()
        mock_photoimage.assert_called_once_with(mock_make_image.return_value)

        # Verify the Label was created with the correct image and added to the window
        mock_label.assert_called_once_with(
            mock_window, image=mock_photoimage.return_value)
        mock_label_instance = mock_label.return_value
        mock_label_instance.pack.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
