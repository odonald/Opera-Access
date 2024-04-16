import pytest
from unittest.mock import Mock, patch
from utils.language_util import LanguageDialog
import tkinter as tk

@pytest.fixture
def language_dialog_setup():
    with patch('tkinter.Toplevel') as ToplevelMock:
        root = Mock()
        available_languages = {'English': 'en', 'Spanish': 'es'}
        additional_languages = {'German': 'de'}
        import_additional_translation = Mock()
        
        # Set up the mock to handle the tkinter calls expected by LanguageDialog
        ToplevelMock.return_value = Mock(spec=tk.Toplevel)
        ToplevelMock.return_value.winfo_children.return_value = [Mock()]
        
        yield root, available_languages, additional_languages, import_additional_translation

def test_language_dialog_init(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    assert dialog.available_languages == available_languages
    assert dialog.additional_languages == additional_languages
    assert dialog.import_additional_translation == import_additional_translation

def test_language_dialog_body(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    assert dialog.search_var.get() == ''
    assert dialog.language_listbox.size() == len(available_languages) + len(additional_languages)

def test_language_dialog_update_list_with_common_languages(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    dialog.update_list()
    assert dialog.language_listbox.size() == len(LanguageDialog.COMMON_LANGUAGES)

def test_language_dialog_update_list_with_search_term(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    dialog.search_var.set('ger')
    dialog.update_list()
    assert dialog.language_listbox.size() == 1
    assert dialog.language_listbox.get(0) == 'German'

def test_language_dialog_apply(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    dialog.selected_language = 'German'
    dialog.apply()
    import_additional_translation.assert_called_once_with('German', 'de')

def test_language_dialog_on_select(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    dialog.language_listbox.insert(tk.END, 'German')
    dialog.language_listbox.event_generate("<<ListboxSelect>>")
    dialog.language_listbox.selection_set(0)
    dialog.on_select(Mock(widget=dialog.language_listbox))
    assert dialog.selected_language == 'German'

def test_language_dialog_buttonbox(language_dialog_setup):
    root, available_languages, additional_languages, import_additional_translation = language_dialog_setup
    dialog = LanguageDialog(root, available_languages, additional_languages, import_additional_translation)
    dialog.body(root)
    dialog.buttonbox()
    assert dialog.children['!frame'].winfo_children()  # Check if buttonbox has children (buttons)
