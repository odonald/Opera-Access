import tkinter as tk
from tkinter import ttk, messagebox
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, StringVar, simpledialog
from PIL import ImageTk, Image
from io import BytesIO
from ui.ui import UserInterface, create_main_window
from config.config import AppConfig
class ImportLanguageDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, available_languages, additional_languages, import_additional_translation, **kwargs):
        self.available_languages = available_languages
        self.additional_languages = additional_languages
        self.import_additional_translation = import_additional_translation
        super().__init__(parent, **kwargs)

    def body(self, master):
        sorted_languages = dict(sorted({**self.available_languages, **self.additional_languages}.items(), key=lambda item: item[0]))

        label = tk.Label(master, text="Search for a language:")
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(master, textvariable=self.search_var, width=25)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.language_listbox = tk.Listbox(master, selectmode="single", exportselection=False, height=10)
        for language in sorted_languages.keys():
            self.language_listbox.insert(tk.END, language)
        self.language_listbox.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.language_listbox.bind("<<ListboxSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.language_listbox.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.language_listbox.configure(yscrollcommand=scrollbar.set)

        self.update_list()

        return self.entry
    

    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        self.language_listbox.delete(0, tk.END)
        COMMON_LANGUAGES = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Russian", "Portuguese", "Italian"]
        items = []
        if len(search_term) < 3:
            items = COMMON_LANGUAGES
        else:
            for language in {**self.available_languages, **self.additional_languages}.keys():
                if search_term in language.lower():
                    items.append(language)
            items = sorted(items, key=lambda x: (len(x), x.startswith(search_term), x))

        for item in items:
            self.language_listbox.insert(tk.END, item)


    def apply(self):
        print("Applying selected language settings...")
        language_code = {**self.available_languages, **self.additional_languages}.get(self.selected_language, None)
        if language_code:
            self.import_additional_translation(self.selected_language, language_code)
        else:
            print("No valid language selected or code found.")
            messagebox.showerror("Error", "Selected language is not valid or does not have a code.")

    def on_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.selected_language = widget.get(index)
            print(f"Selected language: {self.selected_language}")  # Debugging print to check which language is selected


    def buttonbox(self):
        box = tk.Frame(self)
        w = ttk.Button(box, text="Import", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()