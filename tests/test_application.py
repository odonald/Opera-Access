from logic.application import Application
import pytest
class TestApplication:
    def test_combine_files_both_files_not_empty(self):
        original_lines = ["line 1", "line 2", "line 3"]
        translation_lines = ["translation 1", "translation 2", "translation 3"]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", "translation 1"), ("line 2", "translation 2"), ("line 3", "translation 3")]

        assert combined_lines == expected_combined_lines
    
    def test_combine_files_both_files_empty(self):
        original_lines = []
        translation_lines = []

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = []

        assert combined_lines == expected_combined_lines
    
    def test_combine_files_with_empty_lines(self):
        original_lines = ["line 1", "", "line 3"]
        translation_lines = ["translation 1", "translation 2", ""]

        combined_lines = Application.combine_files(original_lines, translation_lines)

        expected_combined_lines = [("line 1", "translation 1"), ("", "translation 2"), ("line 3", "")]

        assert combined_lines == expected_combined_lines

