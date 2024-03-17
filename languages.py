import tkinter as tk
from tkinter import  filedialog, ttk
import charset_normalizer
import requests
import iso639


language_switcher_values = []



COMMON_LANGUAGES = ['Arabic', 'Bengali', 'Chinese', 'English', 'French', 'German', 'Hindi', 'Indonesian', 'Italian', 'Japanese', 'Javanese', 'Korean', 'Malay', 'Marathi', 'Portuguese', 'Punjabi', 'Russian', 'Spanish', 'Tamil', 'Telugu', 'Turkish', 'Ukrainian', 'Urdu', 'Vietnamese', 'Wu', 'Xhosa', 'Yoruba', 'Zulu', 'Cantonese', 'Farsi', 'Filipino', 'Gujarati', 'Hausa', 'Haitian Creole', 'Igbo', 'Kannada', 'Maithili', 'Odia', 'Romanian', 'Thai']

class LanguageDialog(tk.simpledialog.Dialog):
    def body(self, master):
        sorted_languages = dict(sorted({**available_languages, **additional_languages}.items(), key=lambda item: item[0]))
        
        # Label for the search bar
        label = tk.Label(master, text="Search for a language:")
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Create a search bar with autofill functionality
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(master, textvariable=self.search_var, width=25)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Create the language listbox
        self.language_listbox = tk.Listbox(master, selectmode="single", exportselection=False, height=10)
        for language in sorted_languages.keys():
            self.language_listbox.insert(tk.END, language)
        self.language_listbox.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.language_listbox.bind("<<ListboxSelect>>", self.on_select)
        
        # Add a scrollbar to the listbox
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.language_listbox.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.language_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.update_list()
        
        return self.entry

    
    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        self.language_listbox.delete(0, tk.END)
        items = []
        if len(search_term) < 3:
            items = COMMON_LANGUAGES
        else:
            for language in {**available_languages, **additional_languages}.keys():
                if search_term in language.lower():
                    items.append(language)
            items = sorted(items, key=lambda x: (len(x), x.startswith(search_term), x))
            
        for item in items:
            self.language_listbox.insert(tk.END, item)

    def on_select(self, event):
        self.selected_language = self.language_listbox.get(self.language_listbox.curselection())

    def apply(self):
        language_code = {**available_languages, **additional_languages}[self.selected_language]
        import_additional_translation(self.selected_language, language_code)
        # You can add a message here for feedback to the user about the successful import

    def buttonbox(self):
        box = tk.Frame(self)
        w = ttk.Button(box, text="Import", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

def import_additional_language():
    global language_switcher_values
    LanguageDialog(root)
    # Automatically switch to the first imported language
    if language_switcher_values:
        language.set(language_switcher_values[0])
        update_label()
    


def import_additional_translation(language_name, language_code):
    global language_switcher_values, additional_languages
    additional_translation_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    if additional_translation_file:
        with open(additional_translation_file, "rb") as file:
            # Use charset_normalizer to detect the file encoding
            result = charset_normalizer.detect(file.read())
            additional_translation_lines = []
            file.seek(0)
            for line in file:
                line = line.decode(result['encoding']).strip()
                line = line.replace('\\n', '\n')
                if line:
                    additional_translation_lines.append(line)

        additional_translation_lines.insert(0, "")  # Consistency with original format

        # Perform line length comparison with existing translations
        if additional_languages and any(len(lines) != len(additional_translation_lines) for lines in additional_languages.values()):
            example_language, example_lines = next(iter(additional_languages.items()))
            tk.messagebox.showerror("Line Length Mismatch",
                                    f"The imported text does not match the line count of the existing translations.\n"
                                    f"Example mismatch with '{example_language}': {len(example_lines)} lines.\n"
                                    f"Imported text lines: {len(additional_translation_lines)}")
            return  # Do not proceed with the import

        # Update additional_languages with the new translation
        additional_languages[language_code] = additional_translation_lines
        imported_languages_label.configure(text="Imported Languages: \n " + ", ".join(additional_languages.keys()))
        language_switcher_values = list(language_switcher.cget("values"))
        
        if language_code not in language_switcher_values:
            language_switcher_values.append(language_name)
            language_switcher_values.sort()
            language_switcher.configure(values=tuple(language_switcher_values))



def send_to_server(line_number):
    global additional_languages
    message = {
        "type": "message",
        "content": {
        }
    }
    for lang_code, lang_lines in additional_languages.items():
        lang_name = iso639.languages.get(alpha2=lang_code).name
        message["content"][lang_name] = lang_lines[line_number]
    requests.post(url, json=message)