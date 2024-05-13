import pytest
from unittest.mock import patch
from logic.application import Application

def test_combine_files_both_files_not_empty():
    original_lines = ["line 1", "line 2", "line 3"]
    translation_lines = ["translation 1", "translation 2", "translation 3"]

    combined_lines = Application.combine_files(original_lines, translation_lines)

    expected_combined_lines = [
        ("line 1", "translation 1"),
        ("line 2", "translation 2"),
        ("line 3", "translation 3"),
    ]

    assert combined_lines == expected_combined_lines

def test_combine_files_both_files_empty():
    original_lines = []
    translation_lines = []

    combined_lines = Application.combine_files(original_lines, translation_lines)

    expected_combined_lines = []

    assert combined_lines == expected_combined_lines

def test_combine_files_translation_file_empty():
    original_lines = ["line 1", "line 2", "line 3"]
    translation_lines = []

    combined_lines = Application.combine_files(original_lines, translation_lines)

    expected_combined_lines = [("line 1", ""), ("line 2", ""), ("line 3", "")]

    assert combined_lines == expected_combined_lines

def test_combine_files_original_file_empty():
    original_lines = []
    translation_lines = ["translation 1", "translation 2", "translation 3"]

    combined_lines = Application.combine_files(original_lines, translation_lines)

    expected_combined_lines = []

    assert combined_lines == expected_combined_lines

def test_combine_files_with_empty_lines():
    original_lines = ["line 1", "", "line 3"]
    translation_lines = ["translation 1", "translation 2", ""]

    combined_lines = Application.combine_files(original_lines, translation_lines)

    expected_combined_lines = [
        ("line 1", "translation 1"),
        ("", "translation 2"),
        ("line 3", ""),
    ]

    assert combined_lines == expected_combined_lines

@patch("requests.post")
def test_send_to_server(mock_post, app):
    line_number = 2

    app.send_to_server(line_number)

    expected_message = {
        "type": "message",
        "content": {"English": "Line 3", "Spanish": "Línea 3"},
    }
    mock_post.assert_called_once_with(app.sse_url, json=expected_message)

@patch("requests.post")
def test_send_to_server_non_existent_language_code(mock_post, app):
    app.additional_languages = {
        "en": ["Line 1", "Line 2", "Line 3"],
        "invalid": ["Invalid 1", "Invalid 2", "Invalid 3"],
    }
    line_number = 1

    with pytest.raises(KeyError):
        app.send_to_server(line_number)

    mock_post.assert_not_called()

@patch("requests.post")
def test_send_to_server_non_integer_line_number(mock_post, app):
    line_number = "Not an Integer"

    with pytest.raises(TypeError):
        app.send_to_server(line_number)

    mock_post.assert_not_called()

@patch("logic.application.Application.send_to_server")
def test_set_current_line_single_click(mock_send_to_server, app):
    line = 5
    app.empty_line = 0
    app.current_line_clicks = 0

    app.set_current_line(line)

    assert app.current_line_clicks == 1
    mock_send_to_server.assert_called_once_with(app.empty_line)
    assert app.current_line != line

@patch("logic.application.Application.send_to_server")
@patch("logic.application.Application.update_label")
def test_set_current_line_two_clicks(mock_update_label, mock_send_to_server, app):
    line = 5
    app.current_line_clicks = 1

    app.set_current_line(line)

    assert app.current_line == line
    assert app.current_line_clicks == 0
    assert app.next_button_clicks == 0
    assert app.prev_button_clicks == 0
    mock_send_to_server.assert_called_once_with(line)
    mock_update_label.assert_called_once()