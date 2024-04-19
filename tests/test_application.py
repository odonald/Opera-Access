import unittest
from unittest.mock import patch
from logic.application import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application(None)
        self.app.sse_url = "http://example.com/sse"
        self.app.additional_languages = {
            "en": ["Line 1", "Line 2", "Line 3"],
            "es": ["Línea 1", "Línea 2", "Línea 3"]
        }

    def test_combine_files_both_files_not_empty(self):
        original_lines = ["line 1", "line 2", "line 3"]
        translation_lines = ["translation 1", "translation 2", "translation 3"]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", "translation 1"), ("line 2", "translation 2"), ("line 3", "translation 3")]

        self.assertEqual(combined_lines, expected_combined_lines)

    def test_combine_files_both_files_empty(self):
        original_lines = []
        translation_lines = []

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = []

        self.assertEqual(combined_lines, expected_combined_lines)

    def test_combine_files_translation_file_empty(self):
        original_lines = ["line 1", "line 2", "line 3"]
        translation_lines = []

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", ""), ("line 2", ""), ("line 3", "")]

        self.assertEqual(combined_lines, expected_combined_lines)

    def test_combine_files_original_file_empty(self):
        original_lines = []
        translation_lines = ["translation 1", "translation 2", "translation 3"]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = []

        self.assertEqual(combined_lines, expected_combined_lines)

    def test_combine_files_with_empty_lines(self):
        original_lines = ["line 1", "", "line 3"]
        translation_lines = ["translation 1", "translation 2", ""]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", "translation 1"), ("", "translation 2"), ("line 3", "")]

        self.assertEqual(combined_lines, expected_combined_lines)


    @patch("requests.post")
    def test_send_to_server(self, mock_post):
        line_number = 2

        self.app.send_to_server(line_number)

        expected_message = {
            "type": "message",
            "content": {
                "English": "Line 3",
                "Spanish": "Línea 3"
            }
        }
        mock_post.assert_called_once_with(self.app.sse_url, json=expected_message)

    @patch("requests.post")
    def test_send_to_server_non_existent_language_code(self, mock_post):
        self.app.additional_languages = {
            "en": ["Line 1", "Line 2", "Line 3"],
            "invalid": ["Invalid 1", "Invalid 2", "Invalid 3"]
        }
        line_number = 1

        with self.assertRaises(KeyError):
            self.app.send_to_server(line_number)

        mock_post.assert_not_called()

    @patch("requests.post")
    def test_send_to_server_non_integer_line_number(self, mock_post):
        line_number = "Not and Integer"

        with self.assertRaises(TypeError):
            self.app.send_to_server(line_number)

        mock_post.assert_not_called()