import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, simpledialog
import requests
import pickle
import threading
import iso639
import charset_normalizer
import logging
import webbrowser
from ui.ui import UserInterface
from config.config import AppConfig
from utils.language_util import ImportLanguageDialog
from ui.file_menu import FileMenu
from utils.qr_code_utils import QrCode


class Application:
    def __init__(self, root):

        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.path.dirname(__file__)
        self.current_line = None
        self.root = root
        if root is not None:
            self.ui = UserInterface(root)
            self.url = AppConfig.URL
            self.sse_url = AppConfig.SSE_URL
            self.local_ip = AppConfig.HOST
            self.port_number = AppConfig.PORT
            self.save_qr_code = QrCode.save_qr_code
            self.show_qr_code = QrCode.show_qr_code
            self.language_switcher_values = []
            self.original_file = None
            self.translation_file = None
            self.original_lines = []
            self.translation_lines = []
            self.additional_languages = {}
            self.combined_lines = []
            self.current_line = 0
            self.imported_languages_label = []

            self.current_line_clicks = 0
            self.last_confirmed_line = 0
            self.empty_line = 0
            self.next_button_clicks = 0
            self.prev_button_clicks = 0

            self.available_languages = {
                lang.name: lang.alpha2 for lang in iso639.languages}
            self.server_running = False
            self.setup_ui()
            self.bind_events()
            self.start_server_thread(start=True)

            self.scrollbar = ttk.Scrollbar(
                self.ui.navigation_frame, orient="vertical", command=self.ui.canvas.yview)
            self.scrollbar.grid(row=0, column=3, sticky="ns")

            self.ui.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.ui.canvas.bind("<Configure>", self.resize_inner_frame)
            self.ui.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            self.ui.inner_frame.bind("<Configure>", self.on_canvas_configure)
            self.bind_scroll_to_widget(self.ui.inner_frame)
            self.bind_website_button()
            self.bind_import_translation_button()
            self.bind_previous_line_button()
            self.bind_next_line_button()
            self.bind_go_button()
            self.bind_show_qr_button()

            self.root.after(100, self.set_scroll_to_center)
            self.file_menu = FileMenu(root, {
                "save_qr_code": lambda: self.save_qr_code(self.url),
                "show_qr_code": lambda: self.show_qr_code(self.url),
                "import_additional_language": self.import_additional_language,
                "save_session": self.save_session,
                "load_session": self.load_session,
                "open_url_in_browser": self.open_url_in_browser,
                "change_port": self.change_port,
                "clear_program": self.clear_program,
                "close_program": self.close_program
            })

    def bind_show_qr_button(self):
        self.ui.show_qr_button.configure(
            command=lambda: self.show_qr_code(url=self.url))

    def resize_inner_frame(self, event):
        self.ui.canvas.itemconfig(self.ui.canvas_frame, width=event.width)

    def on_mousewheel(self, event):
        self.ui.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_canvas_configure(self):
        self.ui.canvas.configure(scrollregion=self.ui.canvas.bbox("all"))

    def bind_scroll_to_widget(self, widget):
        widget.bind("<MouseWheel>", self.on_mousewheel)
        for child in widget.winfo_children():
            self.bind_scroll_to_widget(child)

    def set_scroll_to_center(self):
        self.ui.canvas.configure(scrollregion=self.ui.canvas.bbox("all"))
        self.ui.canvas.yview_moveto(0.1)

    def setup_ui(self):
        self.language_label = ctk.CTkLabel(
            self.ui.sidebar_frame, text="Switch Display Language:")
        self.language_label.grid(row=4, column=0, padx=10, pady=0, sticky="nw")

        self.language = tk.StringVar(self.root)
        self.language.set("Choose")

        self.language_switcher = ctk.CTkOptionMenu(
            self.ui.sidebar_frame, variable=self.language, state="normal", values=(), width=10)
        self.language_switcher.grid(
            row=5, column=0, padx=10, pady=0, sticky="nwe")
        self.language_switcher.configure(
            values=(), command=lambda choice: self.update_label())

        self.imported_languages_label = ctk.CTkLabel(self.ui.sidebar_frame, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), text="Imported Languages:")
        self.imported_languages_label.grid(
            row=6, column=0, padx=10, pady=10, sticky="w")

        self.server_status_menu_label = ctk.CTkLabel(self.ui.sidebar_frame, fg_color="transparent", font=(
            "", 20), text_color=("gray10", "#DCE4EE"), text=f"Server Status:")
        self.server_status_menu_label.grid(
            row=7, column=0, padx=10, pady=0, sticky="nw")

        self.server_status_label = ctk.CTkLabel(
            self.ui.sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text=f"{self.url}")
        self.server_status_label.grid(
            row=8, column=0, padx=10, pady=0, sticky="nw")

        self.server_indicator = tk.Canvas(
            self.ui.sidebar_frame, width=12, height=12, bg="red", bd=0, highlightthickness=0)
        self.server_indicator.grid(
            row=7, column=0, padx=10, pady=10, sticky="e")

    def bind_events(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)

    def start_server_thread(self, start):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        if start:
            server_thread = threading.Thread(
                target=self.run_server, daemon=True)
            server_thread.start()
            self.server_running = True
            if self.local_ip == "127.0.0.1":
                self.server_status_label.configure(
                    text=f"LOCAL - No network detected")
                self.server_indicator.configure(bg="red")
            else:
                self.server_status_label.configure(
                    text=f"Live\n http://{self.local_ip}:{self.port_number}")
                self.server_indicator.configure(bg="green")
        else:
            self.server_running = False
            self.server_status_label.configure(text=f"Idle")
            self.server_indicator.configure(bg="red")

    def change_port(self):
        reserved_ports = [80, 443, 8080, 8443]

        if self.server_running:
            self.start_server_thread(start=False)
            self.server_running = False
            self.server_status_label.configure(text=f"Idle")
            self.server_indicator.configure(bg="red")

        while True:
            new_port = simpledialog.askstring(
                "Change Port", "Enter new port number between 1024 and 65535:", parent=self.root)
            if new_port:
                try:
                    port_int = int(new_port)
                    if 1024 <= port_int <= 65535 and port_int not in reserved_ports:
                        self.port_number = port_int
                        self.url = f"http://{self.local_ip}:{self.port_number}/stream/push"
                        server_thread = threading.Thread(
                            target=self.run_server, daemon=True)
                        server_thread.start()
                        self.server_running = True
                        if self.local_ip == "127.0.0.1":
                            self.server_status_label.configure(
                                text=f"LOCAL - No network detected")
                            self.server_indicator.configure(bg="red")
                        else:
                            self.server_status_label.configure(
                                text=f"Live\n http://{self.local_ip}:{self.port_number}")
                            self.server_indicator.configure(bg="green")
                        break
                    else:
                        tk.messagebox.showerror(
                            "Invalid Port", "The selected port is already reserved or invalid.")
                except ValueError:
                    tk.messagebox.showerror(
                        "Invalid Port", "Please enter a valid port number.")
            else:
                break

    def bind_website_button(self):
        self.ui.website_button.configure(command=self.open_url_in_browser)

    def bind_import_translation_button(self):
        self.ui.import_translation_button.configure(
            command=self.import_additional_language)

    def bind_previous_line_button(self):
        self.ui.previous_line_button.configure(command=self.previous_line)

    def bind_next_line_button(self):
        self.ui.next_line_button.configure(command=self.next_line)

    def bind_go_button(self):
        self.ui.go_button.configure(command=self.jump_to_line)

    def open_url_in_browser(self):
        url = f"http://{self.local_ip}:{self.port_number}"
        webbrowser.open(url)

    def import_additional_language(self):
        logging.info("Opening Language Import Dialog...")
        dialog = ImportLanguageDialog(self.root, self.available_languages, self.additional_languages,
                                      self.import_additional_translation, title="Select Language")
        self.root.wait_window(dialog.top)
        self.update_ui_after_language_import()

    def import_additional_translation(self, language_name, language_code):
        additional_translation_file = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")])

        if additional_translation_file:
            with open(additional_translation_file, "rb") as file:
                result = charset_normalizer.detect(file.read())
                additional_translation_lines = []
                file.seek(0)
                for line in file:
                    line = line.decode(result['encoding']).strip()
                    line = line.replace('\\n', '\n')
                    if line:
                        additional_translation_lines.append(line)

            additional_translation_lines.insert(0, "")

            if self.additional_languages and any(len(lines) != len(additional_translation_lines) for lines in self.additional_languages.values()):
                example_language, example_lines = next(
                    iter(self.additional_languages.items()))
                tk.messagebox.showerror("Line Length Mismatch",
                                        f"The imported text does not match the line count of the existing translations.\n"
                                        f"Example mismatch with '{example_language}': {len(example_lines)} lines.\n"
                                        f"Imported text lines: {len(additional_translation_lines)}")
                return

            self.additional_languages[language_code] = additional_translation_lines
            self.imported_languages_label.configure(
                text="Imported Languages: \n " + ", ".join(self.additional_languages.keys()))
            self.language_switcher_values = list(
                self.language_switcher.cget("values"))

            if language_code not in self.language_switcher_values:
                self.language_switcher_values.append(language_name)
                self.language_switcher_values.sort()
                self.language_switcher.configure(
                    values=tuple(self.language_switcher_values))

            self.language.set(language_name)
            self.update_label()

    @staticmethod
    def combine_files(original_lines, translation_lines):
        if original_lines and translation_lines:
            return list(zip(original_lines, translation_lines))
        else:
            return [(line, "") for line in original_lines]

    def on_key_press(self, event):
        if event.keysym == 'Right':
            self.next_line()
        elif event.keysym == 'Left':
            self.previous_line()

    def close_program(self):
        print("close_program called")
        result = messagebox.askyesnocancel("Save Session",
                                           "Do you want to save before closing?")

        if result is None:
            print("Cancel pressed in the first dialog")
            return
        elif result:
            if self.save_session():
                print("Session saved successfully, closing application")
                self.root.destroy()
            else:
                print("Session not saved, application remains open")
        else:
            print("No pressed, closing application")
            self.root.destroy()

    def clear_program(self):
        self.original_file = None
        self.translation_file = None
        self.original_lines = []
        self.translation_lines = []
        self.additional_languages = {}
        self.combined_lines = []
        self.current_line = 0
        self.imported_languages_label.configure(text="")
        self.language_switcher_values = []
        self.language_switcher.configure(values=())
        self.update_label()

    def save_session(self):
        session_data = {
            'original_file': self.original_file,
            'translation_file': self.translation_file,
            'original_lines': self.original_lines,
            'translation_lines': self.translation_lines,
            'additional_languages': self.additional_languages,
            'combined_lines': self.combined_lines,
            'current_line': self.current_line,
            'imported_languages_label': self.imported_languages_label.cget("text"),
            'language_switcher_values': self.language_switcher.cget("values")
        }

        save_file = filedialog.asksaveasfilename(
            defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if save_file:
            with open(save_file, 'wb') as f:
                pickle.dump(session_data, f)
            return True
        return False

    def load_session(self):
        load_file = filedialog.askopenfilename(
            filetypes=[("Pickle files", "*.pkl")])
        if load_file:
            with open(load_file, 'rb') as f:
                session_data = pickle.load(f)
            self.original_file = session_data['original_file']
            self.translation_file = session_data['translation_file']
            self.original_lines = session_data['original_lines']
            self.translation_lines = session_data['translation_lines']
            self.additional_languages = session_data['additional_languages']
            self.combined_lines = session_data['combined_lines']
            self.current_line = session_data['current_line']
            self.imported_languages_label.configure(
                text=session_data.get('imported_languages_label', ''))
            self.language_switcher_values = session_data.get(
                'language_switcher_values', [])
            self.language_switcher.configure(
                values=tuple(self.language_switcher_values))

            self.update_label()

    def run_server(self):
        from logic.flask_app import app
        host = self.local_ip
        port = self.port_number
        app.run(debug=AppConfig.DEBUG, port=port,
                host=host, use_reloader=False)

    def send_to_server(self, line_number):
        message = {
            "type": "message",
            "content": {
            }
        }
        for lang_code, lang_lines in self.additional_languages.items():
            lang_name = iso639.languages.get(alpha2=lang_code).name
            message["content"][lang_name] = lang_lines[line_number]
        requests.post(self.sse_url, json=message)

    def update_label(self):
        if self.additional_languages:

            selected_language = self.language.get()

            lang_code = self.available_languages[selected_language]
            current_lang_line = self.additional_languages[lang_code][self.current_line]

            self.ui.current_line_label.configure(
                text=f"Current Line:\n{current_lang_line}")
            self.ui.current_line_label.unbind("<Button-1>")
            self.ui.current_line_label.bind(
                "<Button-1>", lambda event, line=self.current_line: self.set_current_line(line))

            self.ui.progress.set(self.current_line / (max(len(self.combined_lines), max(
                len(lang_lines) for lang_lines in self.additional_languages.values())) - 1))

            for i in range(5):
                prev_index = max(self.current_line - (5-i), 0)
                prev_lang_line = self.additional_languages[lang_code][prev_index]
                self.ui.prev_line_labels[i].configure(
                    text=f"Line {prev_index + 1}:\n{prev_lang_line}")
                self.ui.prev_line_labels[i].unbind("<Button-1>")
                self.ui.prev_line_labels[i].bind(
                    "<Button-1>", lambda event, line=prev_index: self.set_current_line(line))

            for i in range(20):
                next_index = min(self.current_line + (i+1), max(len(self.combined_lines), max(
                    len(lang_lines) for lang_lines in self.additional_languages.values())) - 1)
                next_lang_line = self.additional_languages[lang_code][next_index]
                self.ui.next_line_labels[i].configure(
                    text=f"Line {next_index + 1}:\n{next_lang_line}")
                self.ui.next_line_labels[i].unbind("<Button-1>")
                self.ui.next_line_labels[i].bind(
                    "<Button-1>", lambda event, line=next_index: self.set_current_line(line))

        else:
            self.ui.current_line_label.configure(text="No lines loaded.")
            self.ui.progress.configure(value=0)

    def set_current_line(self, line):
        self.current_line_clicks += 1
        if self.current_line_clicks == 1:
            self.send_to_server(self.empty_line)

        if self.current_line_clicks == 2:
            self.current_line = line
            self.current_line_clicks = 0
            self.next_button_clicks = 0
            self.prev_button_clicks = 0
            self.send_to_server(self.current_line)
            self.update_label()

    def next_line(self):
        selected_language = self.language.get()
        lang_code = self.available_languages[selected_language]

        if self.current_line is not None and self.current_line < len(self.additional_languages[lang_code]) - 1:
            self.next_button_clicks += 1
            if self.next_button_clicks == 1:
                self.send_to_server(self.empty_line)
                self.last_confirmed_line = self.current_line

                if self.prev_button_clicks == 1:
                    self.current_line = self.last_confirmed_line
                    self.next_button_clicks = 0
                    self.prev_button_clicks = 0
                    self.update_label()
                    self.send_to_server(self.current_line)
                    return

            if self.next_button_clicks == 2:
                self.current_line += 1
                self.next_button_clicks = 0
                self.prev_button_clicks = 0
                self.current_line_clicks = 0
                self.update_label()
                self.send_to_server(self.current_line)
        else:
            self.next_button_clicks = 0

    def previous_line(self):


        if self.current_line > 0:
            self.prev_button_clicks += 1
            if self.prev_button_clicks == 1:
                self.send_to_server(self.empty_line)
                self.last_confirmed_line = self.current_line

                if self.next_button_clicks == 1:
                    self.current_line = self.last_confirmed_line
                    self.next_button_clicks = 0
                    self.prev_button_clicks = 0
                    self.update_label()
                    self.send_to_server(self.current_line)
                    return

            if self.prev_button_clicks == 2:
                self.current_line -= 1
                self.prev_button_clicks = 0
                self.next_button_clicks = 0
                self.current_line_clicks = 0
                self.update_label()
                self.send_to_server(self.current_line)
        else:
            self.prev_button_clicks = 0

    def jump_to_line(self):
        selected_language = self.language.get()
        lang_code = self.available_languages[selected_language]

        try:
            new_line = int(self.ui.line_number_entry.get()) - 1
            if 0 <= new_line < len(self.additional_languages[lang_code]):
                self.current_line = new_line
                self.update_label()
                self.send_to_server(self.current_line)
            else:
                messagebox.showerror(
                    "Error", f"Line number should be between 1 and {len(self.additional_languages[lang_code])}.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid line number.")
