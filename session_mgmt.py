from tkinter import messagebox, filedialog
import pickle
import ui.frame_window_setup
import ui.lines_and_labels
import languages


def close_program():
    print("close_program called")  # Debug print
    result = messagebox.askyesnocancel("Save Session",
                                       "Do you want to save before closing?")
    
    if result is None:  # The user pressed 'Cancel'
        print("Cancel pressed in the first dialog")  # Debug print
        return
    elif result:  # The user wants to save the session.
        if save_session():  # The session is saved successfully.
            print("Session saved successfully, closing application")  # Debug print
            ui.frame_window_setup.root.destroy()  # Now close the application.
        else:
            print("Session not saved, application remains open")  # Debug print
    else:  # The user doesn't want to save the session.
        print("No pressed, closing application")  # Debug print
        ui.frame_window_setup.root.destroy()  

def clear_program():
    global original_file, translation_file, original_lines, translation_lines, additional_languages, combined_lines, current_line, imported_languages_label, language_switcher_values

    original_file = None
    translation_file = None
    original_lines = []
    translation_lines = []
    additional_languages = {}
    combined_lines = []
    current_line = 0
    imported_languages_label.configure(text="")
    language_switcher_values = []
    languages.language_switcher.configure(values=())
    ui.lines_and_labels.update_label()
        
def save_session():
    session_data = {
        'original_file': original_file,
        'translation_file': translation_file,
        'original_lines': original_lines,
        'translation_lines': translation_lines,
        'additional_languages': additional_languages,
        'combined_lines': combined_lines,
        'current_line': current_line,
        'imported_languages_label': imported_languages_label.cget("text"),
        'language_switcher_values': languages.language_switcher.cget("values")
    }

    save_file = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
    if save_file:
        with open(save_file, 'wb') as f:
            pickle.dump(session_data, f)
        return True  # Add this line to return True when the file is saved successfully
    return False  # Add this line to return False if the user cancels the save dialog


def load_session():
    global original_file, translation_file, original_lines, translation_lines, additional_languages, combined_lines, current_line
    load_file = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
    if load_file:
        with open(load_file, 'rb') as f:
            session_data = pickle.load(f)
        original_file = session_data['original_file']
        translation_file = session_data['translation_file']
        original_lines = session_data['original_lines']
        translation_lines = session_data['translation_lines']
        additional_languages = session_data['additional_languages']
        combined_lines = session_data['combined_lines']
        current_line = session_data['current_line']
        imported_languages_label.configure(text=session_data.get('imported_languages_label', ''))
        language_switcher_values = session_data.get('language_switcher_values', [])
        languages.language_switcher.configure(values=tuple(language_switcher_values))


        ui.lines_and_labels.update_label()
        

