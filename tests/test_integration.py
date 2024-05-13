import unittest
from unittest.mock import patch
import customtkinter as ctk
from logic.application import Application


class TestApplicationIntegration(unittest.TestCase):
    @patch.object(Application, 'run_server')
    def setUp(self, mock_run_server):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.app = Application(self.root)
        self.mock_languages = {
            "English": "en",
            "French": "fr"
        }
        self.mock_lines = ["Line 1", "Line 2", "Line 3"]
        self.mock_additional_languages = {
            "fr": ["Ligne 1", "Ligne 2", "Ligne 3"]
        }

    def tearDown(self):
        self.root.destroy()

    def mock_load_text(self):
        self.app.original_lines = self.mock_lines
        self.app.translation_lines = self.mock_lines
        self.app.additional_languages = self.mock_additional_languages
        self.app.combined_lines = list(zip(self.mock_lines, self.mock_lines))
        self.app.language_switcher.configure(
            values=list(self.mock_languages.keys()))
        self.app.language.set("French")
        self.app.update_label()

    def test_initialization(self):
        self.assertIsInstance(self.app, Application)
        self.assertIsNotNone(self.app.ui)
        self.assertEqual(self.app.current_line, 0)

    def test_next_line_button(self):
        self.mock_load_text()

        self.assertEqual(self.app.language.get(), "French")
        self.assertEqual(self.app.additional_languages["fr"], [
                         "Ligne 1", "Ligne 2", "Ligne 3"])

        with patch.object(Application, 'next_line', wraps=self.app.next_line) as mock_next_line:
            self.app.bind_next_line_button()
            self.app.ui.next_line_button.invoke()
            self.app.ui.next_line_button.invoke()
            self.assertEqual(mock_next_line.call_count, 2)
            self.assertEqual(self.app.current_line, 1)
            self.assertEqual(self.app.ui.current_line_label.cget(
                "text"), "Current Line:\nLigne 2")

    def test_previous_line_button(self):
        self.mock_load_text()
        self.assertEqual(self.app.language.get(), "French")
        self.assertEqual(self.app.additional_languages["fr"], [
                         "Ligne 1", "Ligne 2", "Ligne 3"])

        with patch.object(Application, 'next_line', wraps=self.app.previous_line) as mock_previous_line:
            self.app.bind_next_line_button()
            self.app.ui.previous_line_button.invoke()
            self.app.ui.previous_line_button.invoke()
            self.assertEqual(mock_previous_line.call_count, 0)
            self.assertEqual(self.app.current_line, 0)
            self.assertEqual(self.app.ui.current_line_label.cget(
                "text"), "Current Line:\nLigne 1")


if __name__ == '__main__':
    unittest.main()
