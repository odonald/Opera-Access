import tkinter as tk
from tkinter import ttk, messagebox


class ImportLanguageDialog(tk.simpledialog.Dialog):
    """
    A dialog window for importing additional languages.

    This class represents a dialog window that allows the user to import additional languages for translation. It inherits from the `tk.simpledialog.Dialog` class.

    Attributes:
        available_languages (dict): A dictionary containing the available languages and their corresponding language codes.
        additional_languages (dict): A dictionary containing additional languages and their corresponding language codes.
        import_additional_translation (function): A function that handles the import of additional translations.
        search_var (tk.StringVar): A string variable used for searching languages in the dialog window.

    Methods:
        body(master): Creates the body of the dialog window.
        update_list(): Updates the list of languages based on the search term.
        apply(): Applies the selected language for import.
        on_select(event): Handles the selection of a language from the listbox.
        buttonbox(): Creates the button box with "Import" and "Cancel" buttons.

    """

    def __init__(self, parent, available_languages, additional_languages, import_additional_translation, **kwargs):
        """
        A dialog window for importing additional languages.

        This class represents a dialog window that allows the user to import additional languages for translation. It inherits from the `tk.simpledialog.Dialog` class.

        Attributes:
            available_languages (dict): A dictionary containing the available languages and their corresponding language codes.
            additional_languages (dict): A dictionary containing additional languages and their corresponding language codes.
            import_additional_translation (function): A function that handles the import of additional translations.
            search_var (tk.StringVar): A string variable used for searching languages in the dialog window.

        Methods:
            body(master): Creates the body of the dialog window.
            update_list(): Updates the list of languages based on the search term.
            apply(): Applies the selected language for import.
            on_select(event): Handles the selection of a language from the listbox.
            buttonbox(): Creates the button box with "Import" and "Cancel" buttons.
        """
        self.available_languages = available_languages
        self.additional_languages = additional_languages
        self.import_additional_translation = import_additional_translation
        self.search_var = tk.StringVar()
        self.selected_language = None
        self.entry = None
        self.language_listbox = None

        super().__init__(parent, **kwargs)

    def body(self, master):
        """
        Creates the body of the dialog window.

        This method is responsible for creating the body of the dialog window in the ImportLanguageDialog class. It sets up the necessary widgets such as labels, entry fields, listboxes, and scrollbars. It also binds the necessary event handlers for user interactions.

        Parameters:
            master (tkinter.Tk or tkinter.Toplevel): The master window in which the dialog is displayed.

        Returns:
            tkinter.Entry: The entry field widget for searching languages.

        """
        sorted_languages = dict(sorted(
            {**self.available_languages, **self.additional_languages}.items(), key=lambda item: item[0]))
        label = tk.Label(master, text="Search for a language:")
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.search_var.trace_add("write", lambda *_: self.update_list())
        self.entry = tk.Entry(master, textvariable=self.search_var, width=25)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.language_listbox = tk.Listbox(
            master, selectmode="single", exportselection=False, height=10)
        for language in sorted_languages.keys():
            self.language_listbox.insert(tk.END, language)
        self.language_listbox.grid(
            row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.language_listbox.bind("<<ListboxSelect>>", self.on_select)
        scrollbar = ttk.Scrollbar(
            master, orient="vertical", command=self.language_listbox.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.language_listbox.configure(yscrollcommand=scrollbar.set)
        self.update_list()
        return self.entry

    def update_list(self):
        """
        Updates the list of languages based on the search term.

        This method is responsible for updating the list of languages displayed in the dialog window based on the search term entered by the user. It clears the current list of languages in the language_listbox and then populates it with the languages that match the search term. If the search term is less than 3 characters, it displays a predefined list of languages. The languages are sorted based on their length, whether they start with the search term, and their alphabetical order.

        """
        search_term = self.search_var.get().lower()
        self.language_listbox.delete(0, tk.END)
        prefilled_languages = ["English", "Spanish", "French", "German",
                               "Chinese", "Japanese", "Russian", "Portuguese", "Italian"]
        items = []
        if len(search_term) < 3:
            items = prefilled_languages
        else:
            for language in {**self.available_languages, **self.additional_languages}.keys():
                if search_term in language.lower():
                    items.append(language)
            items = sorted(items, key=lambda x: (
                len(x), x.startswith(search_term), x))

        for item in items:
            self.language_listbox.insert(tk.END, item)

    def apply(self):
        """
        Applies the selected language for import.

        This method is responsible for applying the selected language for import. It retrieves the language code corresponding to the selected language from the available_languages and additional_languages dictionaries. If a valid language code is found, it calls the import_additional_translation function with the selected language and language code as arguments. If no valid language code is found, it displays an error message using the messagebox.showerror method.

        """
        language_code = {**self.available_languages, **
                         self.additional_languages}.get(self.selected_language, None)
        if language_code:
            self.import_additional_translation(
                self.selected_language, language_code)
        else:
            messagebox.showerror(
                "Error", "Selected language is not valid or does not have a code.")

    def on_select(self, event):
        """
        Handles the selection of a language from the listbox.

        This method is called when a language is selected from the listbox in the ImportLanguageDialog class. It retrieves the selected language from the listbox and stores it in the instance variable 'selected_language'. It also prints the selected language to the console.

        Parameters:
            event (tkinter.Event): The event object that triggered the method call.

        """
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.selected_language = widget.get(index)
            print(f"Selected language: {self.selected_language}")

    def buttonbox(self):
        """
        Creates the button box with "Import" and "Cancel" buttons.

        This method is responsible for creating the button box in the ImportLanguageDialog class. It creates a frame widget to hold the buttons and then creates the "Import" and "Cancel" buttons using the tk.Button class. The buttons are packed into the frame with appropriate padding and side alignment. The method also binds the "<Return>" and "<Escape>" events to the self.ok and self.cancel methods respectively.

        """
        box = tk.Frame(self)

        import_button = tk.Button(
            box, text="Import", width=10, command=self.ok, default=tk.ACTIVE)
        import_button.pack(side=tk.LEFT, padx=5, pady=5)

        cancel_button = tk.Button(
            box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
