import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, StringVar, Entry, simpledialog
import requests
import json

import pickle
import threading
from functools import partial
import iso639
import socket
import charset_normalizer
import qrcode
from PIL import ImageTk, Image
from io import BytesIO
import webbrowser

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

language_switcher_values = []


local_ip = socket.gethostbyname(socket.gethostname())
port_number = 3210
def change_port():
    global port_number, url
    reserved_ports = [80, 443, 8080, 8443]  # list of reserved ports
    while True:
        new_port = simpledialog.askstring("Change Port", "Enter new port number between 1024 and 65535:", parent=root)
        if new_port:
            try:
                port_int = int(new_port)
                if 1024 <= port_int <= 65535 and port_int not in reserved_ports:
                    port_number = port_int
                    url = f"http://{local_ip}:{port_number}/stream/push"  # Update the url variable
                    break
                else:
                    tk.messagebox.showerror("Invalid Port", "The selected port is already reserved or invalid.")
            except ValueError:
                tk.messagebox.showerror("Invalid Port", "Please enter a valid port number.")
        else:
            break

url = f"http://{local_ip}:{port_number}/stream/push"

original_file = None
translation_file = None
original_lines = []
translation_lines = []
additional_languages = {}
combined_lines = []
current_line = 0
imported_languages_label = []

if original_lines:
    combined_lines.extend(original_lines)

if translation_lines:
    combined_lines.extend(translation_lines)

current_line = 0 if combined_lines else None

# Create a dictionary of all available languages using the iso639 package
available_languages = {lang.name: lang.alpha2 for lang in iso639.languages}

def save_qr_code(url):
    url = f"http://{local_ip}:{port_number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        img.save(file_path)

def show_qr_code(url):
    url = f"http://{local_ip}:{port_number}"
    global qr_img
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_tk = ImageTk.PhotoImage(img)

    qr_img = img

    qr_window = tk.Toplevel()
    qr_window.title("QR Code")
    qr_window.geometry("600x600")

    qr_label = tk.Label(qr_window, image=img_tk)
    qr_label.image = img_tk
    qr_label.pack()

    qr_window.mainloop()

def open_url_in_browser(local_ip, port_number):
    url = f"http://{local_ip}:{port_number}"
    webbrowser.open(url)

def import_original():
    global original_file, original_lines
    original_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if original_file:
        with open(original_file, "r", encoding="utf-8") as file_a:
            original_lines = [line.strip() for line in file_a if line.strip()]
        combine_files()


class LanguageDialog(tk.simpledialog.Dialog):
    def body(self, master):
        sorted_languages = dict(sorted({**available_languages, **additional_languages}.items(), key=lambda item: item[0]))
        
        # Create a search bar with autofill functionality
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = tk.Entry(master, textvariable=self.search_var, width=25)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Create the language listbox
        self.language_listbox = tk.Listbox(master, selectmode="single", exportselection=False)
        for language in sorted_languages.keys():
            self.language_listbox.insert(tk.END, language)
        self.language_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.language_listbox.bind("<<ListboxSelect>>", self.on_select)
        
        # Change the font color of the listbox to white
        # self.language_listbox.configure(fg="white")
        
        self.update_list()
        
        return self.entry

    def update_list(self, *args):
        search_term = self.search_var.get().lower()
        self.language_listbox.delete(0, tk.END)
        items = []
        if len(search_term) >= 3:
            for language in {**available_languages, **additional_languages}.keys():
                if search_term in language.lower():
                    items.append(language)
            items = sorted(items, key=lambda x: (len(x), x.startswith(search_term), x))
        for item in items:
            self.language_listbox.insert(tk.END, item)

    def on_select(self, event):
        selected_language = self.language_listbox.get(self.language_listbox.curselection())
        language_code = {**available_languages, **additional_languages}[selected_language]
        import_additional_translation(selected_language, language_code)

    def apply(self):
        pass

def import_additional_language():
    global language_switcher_values
    LanguageDialog(root)
    # Automatically switch to the first imported language
    if language_switcher_values:
        language.set(language_switcher_values[0])
        update_label()
    
    


def import_additional_translation(language_name, language_code):
    global language_switcher_values
    additional_translation_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if additional_translation_file:
        with open(additional_translation_file, "rb") as file:
            # Use charset_normalizer to detect the file encoding
            result = charset_normalizer.detect(file.read())
            additional_translation_lines = []
            file.seek(0)
            for line in file:
                line = line.decode(result['encoding']).strip()
                if line:
                    additional_translation_lines.append(line)
        additional_languages[language_code] = additional_translation_lines
        # Update the imported languages label
        imported_languages_label.configure(text="Imported Languages: \n " + ", ".join(additional_languages.keys()))
        # Update the language switcher values
        language_switcher_values = list(language_switcher.cget("values"))
        if language_code not in language_switcher_values:
            language_switcher_values.append(language_name)
            language_switcher_values.sort()
            language_switcher.configure(values=tuple(language_switcher_values))



def combine_files():
    global combined_lines
    if original_lines and translation_lines:
        combined_lines = list(zip(original_lines, translation_lines))
    else:
        combined_lines = [(line, "") for line in original_lines]
    update_label()

def on_key_press(event):
    if event.keysym == 'Right':
        next_line()
    elif event.keysym == 'Left':
        previous_line()

def close_program():
    result = messagebox.askyesnocancel("Save Session", "Do you want to save before closing?")
    if result:
        save_session()
        root.destroy()
    elif result is False:
        root.destroy()

        
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
        'language_switcher_values': language_switcher.cget("values")
    }

    save_file = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
    if save_file:
        with open(save_file, 'wb') as f:
            pickle.dump(session_data, f)

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
        language_switcher.configure(values=tuple(language_switcher_values))


        update_label()

def run_server():
    from app import app
    host = local_ip
    port = port_number  # Replace with your desired port number
    app.run(debug=True, port=port, host=host, use_reloader=False)


def start_stop_server(start):
    global server_thread, server_running
    if start:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        server_running = True
        server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
        server_indicator.configure(bg="green")
    else:
        server_running = False
        server_button.configure(text="Start Server", command=partial(start_stop_server, True))
        server_indicator.configure(bg="red")
        # Stopping the Flask server is not straightforward; for now, the server will keep running
        # You might want to look into using other server options (like Gunicorn)

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


def update_label():
    global current_line
    if additional_languages:
        percentage = (current_line / (max(len(combined_lines), max(len(lang_lines) for lang_lines in additional_languages.values())) - 1)) * 100
        # percentage_label.configure(text=f"{percentage:.2f}%")
        prev_line = max(current_line - 1, 0)
        next_line = min(current_line + 1, max(len(combined_lines), max(len(lang_lines) for lang_lines in additional_languages.values())) - 1)

        selected_language = language.get()

        lang_code = available_languages[selected_language]
        prev_lang_line = additional_languages[lang_code][prev_line]
        current_lang_line = additional_languages[lang_code][current_line]
        next_lang_line = additional_languages[lang_code][next_line]

        # Update the labels with line numbers and make them clickable
        prev_line_label.configure(text=f"Last Line ({prev_line + 1}):\n{prev_lang_line}")
        prev_line_label.unbind("<Button-1>")
        prev_line_label.bind("<Button-1>", lambda event, line=prev_line: set_current_line(line))

        current_line_label.configure(text=f"Current Line {current_line + 1}:\n{current_lang_line}")
        current_line_label.unbind("<Button-1>")
        current_line_label.bind("<Button-1>", lambda event, line=current_line: set_current_line(line))

        next_line_label.configure(text=f"Next Line ({next_line + 1}):\n{next_lang_line}")
        next_line_label.unbind("<Button-1>")
        next_line_label.bind("<Button-1>", lambda event, line=next_line: set_current_line(line))

        progress.set(current_line / (max(len(combined_lines), max(len(lang_lines) for lang_lines in additional_languages.values())) - 1))
        
        if language_switcher_values:
            language.set(language_switcher_values[0])
    else:
        # percentage_label.configure(text="0%")
        prev_line_label.configure(text="")
        current_line_label.configure(text="No lines loaded.")
        next_line_label.configure(text="")
        progress.configure(value=0)

def set_current_line(line):
    global current_line
    current_line = line
    send_to_server(current_line)  # Send the clicked line to the server
    update_label()

def next_line():
    global current_line, additional_languages
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line is not None and current_line < len(additional_languages[lang_code]) - 1:
        current_line += 1
        update_label()
        send_to_server(current_line)

def previous_line():
    global current_line, additional_languages
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line > 0:
        current_line -= 1
        update_label()
        send_to_server(current_line)
    

current_line = 0

def jump_to_line():
    global current_line
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    try:
        new_line = int(line_number_entry.get()) - 1
        if 0 <= new_line < len(additional_languages[lang_code]):
            current_line = new_line
            update_label()
            send_to_server(current_line)
        else:
            messagebox.showerror("Error", f"Line number should be between 1 and {len(additional_languages[lang_code])}.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid line number.")

def change_appearance_mode_event(new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

# Create the Tkinter root
root = ctk.CTk()
root.title("Opera Access 1.0")
root.configure(bg=ctk.set_appearance_mode("System"))
root.geometry(f"{900}x{550}")



# configure grid layout (4x4)
root.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
root.columnconfigure((1, 2), weight=1)


# create sidebar frame with widgets
sidebar_frame = ctk.CTkFrame(root, width=100, corner_radius=0, border_width=2)
sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
sidebar_frame.grid_rowconfigure(8, weight=1)
sidebar_frame.grid_columnconfigure(1, weight=1)
Sidebar_label = ctk.CTkLabel(sidebar_frame, text="Menu:",font=("", 20))
Sidebar_label.grid(row=0, column=0,  padx=20, pady=10, sticky="nwe")
import_translation_button = ctk.CTkButton(sidebar_frame ,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Import Text", command=import_additional_language)
import_translation_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")
server_button = ctk.CTkButton(sidebar_frame,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Start Server", command=partial(start_stop_server, True))
server_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")

server_indicator = tk.Canvas(sidebar_frame, width=15, height=15, bg="red", bd=0, highlightthickness=0)
server_indicator.grid(row=2, column=0, padx=0, pady=0, sticky="nse")

port_button = ctk.CTkButton(sidebar_frame,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2,text="Change Port", command=change_port)
port_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")


language_label = ctk.CTkLabel(sidebar_frame, text="Switch Display Language:")
language_label.grid(row=4, column=0, padx=10, pady=0, sticky="nwe")

language = tk.StringVar(root)
language.set("Choose")

language_switcher = ctk.CTkOptionMenu(sidebar_frame, variable=language, state="normal", values=(), width=10)
language_switcher.grid(row=5, column=0, padx=10, pady=0, sticky="nwe")
language_switcher.configure(values=(), command=lambda choice: update_label())

imported_languages_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text="Imported Languages:")
imported_languages_label.grid(row=6, column=0, padx=10, pady=10, sticky="nwe")


appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=8, column=0, padx=10, pady=10, sticky="s")
appearance_mode_optionemenu.set("Dark")

navigation_frame = ctk.CTkFrame(root, width=100, height=200, corner_radius=4, border_width=2)
navigation_frame.grid(row=1, column=1,columnspan=2, padx=10, pady=0, sticky="nwe")
navigation_frame.grid_rowconfigure(4, weight=1)
navigation_frame.grid_columnconfigure(1, weight=1)

# language = tk.StringVar(value="German")
# language_switcher = ttk.OptionMenu(navigation_frame, language, command=lambda _: update_label())
# language_switcher.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Create the percentage label
# percentage_label = ctk.CTkLabel(navigation_frame, text="%")
# percentage_label.grid(row=1, column=1, sticky="ns")

# Create previous, current, and next line labels

progress = ctk.CTkProgressBar(root, orientation="horizontal")
progress.grid(row=0, column=1,columnspan=3, padx=0, pady=0, sticky="new")
progress.configure(mode="determinate")
progress.set(0)

navigation_label = ctk.CTkLabel(root, text="Display:", font=("", 20))
navigation_label.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="nwe")

prev_line_label = ctk.CTkLabel(navigation_frame, wraplength=500, text="---")
prev_line_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(50,20), sticky="nsew")

current_line_label = ctk.CTkLabel(navigation_frame, wraplength=500, text="Please import a language or load a session.\n +\n <--- Choose display language", font=("", 25))
current_line_label.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

next_line_label = ctk.CTkLabel(navigation_frame, wraplength=500, text="---")
next_line_label.grid(row=4, column=0, columnspan=3, padx=10, pady=(20,50), sticky="nsew")

navigation_label = ctk.CTkLabel(root, text=f"", font=("", 20))
navigation_label.grid(row=5, column=1, columnspan=3, padx=20, pady=10, sticky="nwe")


# progress = ctk.CTkProgressBar(navigation_frame, length=500, maximum=len(combined_lines), mode='determinate', value=current_line)

# label = tk.Label(root, wraplength=500)
# label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
navigation_frame2 = ctk.CTkFrame(root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
navigation_frame2.grid(row=8, column=2,rowspan=1, padx=0, pady=0, sticky="w")
navigation_frame3 = ctk.CTkFrame(root,fg_color="transparent", width=500, height=200, corner_radius=4, border_width=0)
navigation_frame3.grid(row=8, column=1,rowspan=1, padx=0, pady=0, sticky="e")

previous_button = ctk.CTkButton(navigation_frame3,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Previous", command=previous_line)
previous_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

next_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Next", command=next_line)
next_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Create a text box for entering the line number
line_number_var = StringVar()
line_number_entry = ctk.CTkEntry(navigation_frame3, placeholder_text="Jump to line")
line_number_entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Create a 'Go' button to jump to the specified line number
go_button = ctk.CTkButton(navigation_frame2,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2, text="Go", command=jump_to_line)
go_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create the menu bar
menu_bar = tk.Menu(root)
root.configure(menu=menu_bar)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a submenu for "Import" option
qr_menu = tk.Menu(file_menu, tearoff=0)
qr_menu.add_command(label="Save QR Code", command=lambda: save_qr_code(url))
qr_menu.add_command(label="Show QR Code", command=lambda: show_qr_code(url))

file_menu.add_command(label="Import additional language", command=import_additional_language)
file_menu.add_command(label="Save Session", command=save_session)
file_menu.add_command(label="Load Session", command=load_session)
file_menu.add_command(label="Open Website", command=lambda: open_url_in_browser(local_ip, port_number))
file_menu.add_cascade(label="QR-Code", menu=qr_menu)
file_menu.add_command(label="Exit", command=close_program)



root.configure(menu=menu_bar)

root.protocol("WM_DELETE_WINDOW", close_program)



# configure rows and columns


# Place buttons in the left frame (column 0)




# save_button = ctk.CTkButton(root, text="Save Session", command=save_session)
# save_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# load_button = ctk.CTkButton(root, text="Load Session", command=load_session)
# load_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Place progress bar, label, and navigation buttons in the middle frame (column 1)
# CCREATE A LANGUAGE SWITCHER



# Place server button and indicator in the right frame (column 2)


# If you want to update the server indicator color when the server starts or stops, you can use the following function
def update_server_indicator(status):
    if status:
        server_indicator.configure(bg="green")
    else:
        server_indicator.configure(bg="red")

# Update the start_stop_server function to call update_server_indicator
def start_stop_server(status):
    if status:
        server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
        update_server_indicator(True)
    else:
        server_button.configure(text="Start Server", command=partial(start_stop_server, True))
        update_server_indicator(False)

root.bind("<KeyPress>", on_key_press)
# Run the Tkinter root
root.mainloop()