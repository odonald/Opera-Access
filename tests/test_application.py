import unittest
from unittest import mock
from logic.application import Application

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application(None)

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

    # def test_combine_files_different_lengths(self):
    #     original_lines = ["line 1", "line 2", "line 3"]
    #     translation_lines = ["translation 1", "translation 2"]

    #     combined_lines = Application.combine_files(original_lines, translation_lines)

    #     expected_combined_lines = [("line 1", "translation 1"), ("line 2", "translation 2"), ("line 3", "")]

    #     self.assertEqual(combined_lines, expected_combined_lines)

    def test_combine_files_with_empty_lines(self):
        original_lines = ["line 1", "", "line 3"]
        translation_lines = ["translation 1", "translation 2", ""]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", "translation 1"), ("", "translation 2"), ("line 3", "")]

        self.assertEqual(combined_lines, expected_combined_lines)
    @mock.patch('logic.application.threading.Thread')
    def test_start_server_thread_with_start(self, mock_thread):
        self.app.start_server_thread(start=True)

        mock_thread.assert_called_once_with(target=self.app.run_server, daemon=True)
        mock_thread.return_value.start.assert_called_once()

        self.assertTrue(self.app.server_running)
        self.assertEqual(self.app.server_status_label.cget("text"), "Live\n http://127.0.0.1:5000")
        self.assertEqual(self.app.server_indicator.cget("bg"), "green")

    @mock.patch('logic.application.threading.Thread')
    def test_start_server_thread_without_start(self, mock_thread):
        self.app.start_server_thread(start=False)

        mock_thread.assert_not_called()

        self.assertFalse(self.app.server_running)
        self.assertEqual(self.app.server_status_label.cget("text"), "Idle")
        self.assertEqual(self.app.server_indicator.cget("bg"), "red")

    @mock.patch('logic.application.Application.run_server')
    def test_start_server_thread_with_local_ip(self, mock_run_server):
        self.app.local_ip = "192.168.0.10"
        self.app.port_number = 8000

        self.app.start_server_thread(start=True)

        self.assertTrue(self.app.server_running)
        self.assertEqual(self.app.server_status_label.cget("text"), "Live\n http://192.168.0.10:8000")
        self.assertEqual(self.app.server_indicator.cget("bg"), "green")

    @mock.patch('logic.application.Application.run_server')
    def test_start_server_thread_with_local_ip_no_network(self, mock_run_server):
        self.app.local_ip = "127.0.0.1"
        self.app.port_number = 8000

        self.app.start_server_thread(start=True)

        self.assertTrue(self.app.server_running)
        self.assertEqual(self.app.server_status_label.cget("text"), "LOCAL - No network detected")
        self.assertEqual(self.app.server_indicator.cget("bg"), "red")


if __name__ == '__main__':
    unittest.main()