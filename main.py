import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, StringVar, Entry, simpledialog
import requests
import json
import platform
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

# sys.stdout = open('my_stdout.log', 'w')
# sys.stderr = open('my_stderr.log', 'w')

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

language_switcher_values = []


local_ip = socket.gethostbyname(socket.gethostname())

port_number = 7832
def change_port():
    global port_number, server_running
    reserved_ports = [80, 443, 8080, 8443]  # List of reserved ports

    # Stop the existing server if it's running
    if server_running:
        start_server_thread(start=False)
        server_running = False
        server_status_label.configure(text=f"Idle")
        server_indicator.configure(bg="red")

    while True:
        new_port = simpledialog.askstring("Change Port", "Enter new port number between 1024 and 65535:", parent=root)
        if new_port:
            try:
                port_int = int(new_port)
                if 1024 <= port_int <= 65535 and port_int not in reserved_ports:
                    port_number = port_int
                    url = f"http://{local_ip}:{port_number}/stream/push"  # Update the url variable

                    # Start a new server with the updated port
                    server_thread = threading.Thread(target=run_server, daemon=True)
                    server_thread.start()
                    server_running = True
                    if local_ip == "127.0.0.1":
                        server_status_label.configure(text=f"LOCAL - No network detected")
                        server_indicator.configure(bg="red")
                    else:
                        server_status_label.configure(text=f"Live\n http://{local_ip}:{port_number}")
                        server_indicator.configure(bg="green")
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
    
    def on_qr_click(event):
        save_qr_code(url)
    
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

    # Bind the click event to the label
    qr_label.bind("<Button-1>", on_qr_click)

    qr_window.mainloop()

def open_url_in_browser(local_ip, port_number):
    url = f"http://{local_ip}:{port_number}"
    webbrowser.open(url)

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
            additional_translation_lines.insert(0, "")  # Add an empty line at the beginning
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
    print("close_program called")  # Debug print
    result = messagebox.askyesnocancel("Save Session",
                                       "Do you want to save before closing?")
    
    if result is None:  # The user pressed 'Cancel'
        print("Cancel pressed in the first dialog")  # Debug print
        return
    elif result:  # The user wants to save the session.
        if save_session():  # The session is saved successfully.
            print("Session saved successfully, closing application")  # Debug print
            root.destroy()  # Now close the application.
        else:
            print("Session not saved, application remains open")  # Debug print
    else:  # The user doesn't want to save the session.
        print("No pressed, closing application")  # Debug print
        root.destroy()  

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
    language_switcher.configure(values=())
    update_label()
        
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
        language_switcher.configure(values=tuple(language_switcher_values))


        update_label()

def run_server():
    from app import app
    host = local_ip
    port = port_number  # Replace with your desired port number
    app.run(debug=True, port=port, host=host, use_reloader=False)


# def start_stop_server(start):
#     global server_thread, server_running
#     if start:
#         server_thread = threading.Thread(target=run_server, daemon=True)
#         server_thread.start()
#         server_running = True
#         # server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
#         server_indicator.configure(bg="green")
#     else:
#         server_running = False
#         # server_button.configure(text="Start Server", command=partial(start_stop_server, True))
#         server_indicator.configure(bg="red")
#         # Stopping the Flask server is not straightforward; for now, the server will keep running
#         # You might want to look into using other server options (like Gunicorn)

def start_server_thread(start):
    global server_running  # Declare server_running as a global variable
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Allow the thread to exit when the main program exits
    server_thread.start()
    if start:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        server_running = True
        if local_ip == "127.0.0.1":
            server_status_label.configure(text=f"LOCAL - No network detected")
            server_indicator.configure(bg="red")
        else:
            server_status_label.configure(text=f"Live\n http://{local_ip}:{port_number}")
            server_indicator.configure(bg="green")
    else:
        server_running = False
        server_status_label.configure(text=f"Idle")
        server_indicator.configure(bg="red")

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


empty_line = 0
next_button_clicks = 0
prev_button_clicks = 0

def update_label():
    global current_line, next_button_clicks, prev_button_clicks
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
        # prev_line_label.configure(text=f"Last Line ({prev_line + 1}):\n{prev_lang_line}")
        # prev_line_label.unbind("<Button-1>")
        # prev_line_label.bind("<Button-1>", lambda event, line=prev_line: set_current_line(line))

        current_line_label.configure(text=f"Current Line:\n{current_lang_line}")
        current_line_label.unbind("<Button-1>")
        current_line_label.bind("<Button-1>", lambda event, line=current_line: set_current_line(line))

        # next_line_label.configure(text=f"Next Line ({next_line + 1}):\n{next_lang_line}")
        # next_line_label.unbind("<Button-1>")
        # next_line_label.bind("<Button-1>", lambda event, line=next_line: set_current_line(line))

        progress.set(current_line / (max(len(combined_lines), max(len(lang_lines) for lang_lines in additional_languages.values())) - 1))
            # Inside update_label()
        for i in range(5):
            prev_index = max(current_line - (5-i), 0)
            prev_lang_line = additional_languages[lang_code][prev_index]
            prev_line_labels[i].configure(text=f"Line {prev_index + 1}:\n{prev_lang_line}")
            prev_line_labels[i].unbind("<Button-1>")
            prev_line_labels[i].bind("<Button-1>", lambda event, line=prev_index: set_current_line(line))

        for i in range(20):
            next_index = min(current_line + (i+1), max(len(combined_lines), max(len(lang_lines) for lang_lines in additional_languages.values())) - 1)
            next_lang_line = additional_languages[lang_code][next_index]
            next_line_labels[i].configure(text=f"Line {next_index + 1}:\n{next_lang_line}")
            next_line_labels[i].unbind("<Button-1>")
            next_line_labels[i].bind("<Button-1>", lambda event, line=next_index: set_current_line(line))
            

    else:
        # percentage_label.configure(text="0%")
        # prev_line_label.configure(text="")
        current_line_label.configure(text="No lines loaded.")
        # next_line_label.configure(text="")
        progress.configure(value=0)

def set_current_line(line):
    global current_line, next_button_clicks, prev_button_clicks

    current_line = line
    next_button_clicks = 0
    prev_button_clicks = 0
    send_to_server(current_line)  # Send the clicked line to the server
    update_label()

# Modify the next_line() and previous_line() functions
def next_line():
    global current_line,empty_line, additional_languages, next_button_clicks, prev_button_clicks
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line is not None and current_line < len(additional_languages[lang_code]) - 1:
        next_button_clicks += 1
        if next_button_clicks == 1:
            send_to_server(empty_line)

        if next_button_clicks == 2:
            current_line += 1
            next_button_clicks = 0
            prev_button_clicks = 0  # Reset the count for Previous button
            update_label()
            send_to_server(current_line)
    else:
        next_button_clicks = 0

def previous_line():
    global current_line, additional_languages, next_button_clicks, prev_button_clicks
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line > 0:
        prev_button_clicks += 1
        # canvas.yview_moveto(0.2)

        if prev_button_clicks ==1:
            send_to_server(empty_line)
        if prev_button_clicks == 2:
            current_line -= 1
            prev_button_clicks = 0
            next_button_clicks = 0  # Reset the count for Next button
            update_label()
            send_to_server(current_line)
    else:
        prev_button_clicks = 0

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
root.geometry(f"{1000}x{550}")



# configure grid layout (4x4)
root.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
root.columnconfigure((0,1,2), weight=1)


# create sidebar frame with widgets
sidebar_frame = ctk.CTkFrame(root, width=100, corner_radius=0, border_width=2)
sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
sidebar_frame.grid_rowconfigure(8, weight=1)
sidebar_frame.grid_columnconfigure(1, weight=1)
Sidebar_label = ctk.CTkLabel(sidebar_frame, text="Menu:",font=("", 20))
Sidebar_label.grid(row=0, column=0,  padx=20, pady=10, sticky="nwe")
import_translation_button = ctk.CTkButton(sidebar_frame ,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Import Text", command=import_additional_language)
import_translation_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")

show_qr_button = ctk.CTkButton(sidebar_frame,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2,text="Show QR", command=lambda: show_qr_code(url))
show_qr_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")

# server_button = ctk.CTkButton(sidebar_frame,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Start Server", command=partial(start_stop_server, True))
# server_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")


port_button = ctk.CTkButton(sidebar_frame,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2,text="Change Port", command=change_port)
port_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")


language_label = ctk.CTkLabel(sidebar_frame, text="Switch Display Language:")
language_label.grid(row=4, column=0, padx=10, pady=0, sticky="nw")

language = tk.StringVar(root)
language.set("Choose")

language_switcher = ctk.CTkOptionMenu(sidebar_frame, variable=language, state="normal", values=(), width=10)
language_switcher.grid(row=5, column=0, padx=10, pady=0, sticky="nwe")
language_switcher.configure(values=(), command=lambda choice: update_label())

imported_languages_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text="Imported Languages:")
imported_languages_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

server_status_menu_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent",font=("", 20), text_color=("gray10", "#DCE4EE"), text=f"Server Status:")
server_status_menu_label.grid(row=7, column=0, padx=10, pady=0, sticky="nwe")

server_status_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text=f"{url}")
server_status_label.grid(row=8, column=0, padx=10, pady=0, sticky="nw")

server_indicator = tk.Canvas(sidebar_frame, width=12, height=12, bg="red", bd=0, highlightthickness=0)
server_indicator.grid(row=7, column=0, padx=10, pady=10, sticky="e")

appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=9, column=0, padx=10, pady=10, sticky="s")
appearance_mode_optionemenu.set("Dark")

def on_mousewheel(event):
    platform = event.widget.tk.call('tk', 'windowingsystem')
    
    # For macOS
    if platform == "aqua":
        canvas.yview_scroll(-1*(event.delta), "units")
    # For Windows
    elif platform == "win32":
        canvas.yview_scroll(-1*(event.delta//120), "units")
    # For Linux
    else:
        canvas.yview_scroll(-1 if event.num == 4 else 1, "units")


navigation_frame = tk.LabelFrame(root, height=900)
navigation_frame.grid(row=1, rowspan=6, column=1, columnspan=2, padx=20, pady=10, sticky="nwse")
navigation_frame.grid_rowconfigure(0, weight=1)
navigation_frame.grid_columnconfigure(0, weight=1)


canvas = tk.Canvas(navigation_frame)
canvas.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(navigation_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=3, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = ctk.CTkFrame(canvas)
canvas_frame = canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Binding the scrolling action to the navigation_frame and its children
# inner_frame.bind_class('Tk', '<MouseWheel>', on_mousewheel)  # for Windows
# inner_frame.bind_class('Tk', '<Button-4>', on_mousewheel)    # for macOS and Linux (scroll up)
# inner_frame.bind_class('Tk', '<Button-5>', on_mousewheel)    # for macOS and Linux (scroll down)

def resize_inner_frame(event):
    canvas.itemconfig(canvas_frame, width=event.width)


canvas.bind("<Configure>", resize_inner_frame)
canvas.bind("<MouseWheel>", on_mousewheel)
inner_frame.bind("<MouseWheel>", on_mousewheel)




# Calculate and set scrollbar position to 50% on load

# Configure row and column weights for resizing


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

inner_frame.grid_rowconfigure((0, 1, 2), weight=1)
inner_frame.grid_columnconfigure(0, weight=1)

prev_line_labels = [ctk.CTkLabel(inner_frame, wraplength=400, text="---") for _ in range(5)]

current_line_label = ctk.CTkLabel(inner_frame, text_color=("Yellow", "#FFD90F"), text="Please import a language or load a session.\n +\n <--- Choose display language", font=("", 25))
current_line_label.grid(row=1, column=0, padx=10, pady=10)

next_line_labels = [ctk.CTkLabel(inner_frame, wraplength=400, text="---") for _ in range(20)]

for index, label in enumerate(prev_line_labels, start=0):
    label.grid(row=index, column=0, padx=10, pady=10)

current_line_label.grid(row=5, column=0, padx=10, pady=10)

for index, label in enumerate(next_line_labels, start=6):
    label.grid(row=index, column=0, padx=10, pady=10)

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


inner_frame.bind("<Configure>", on_canvas_configure)

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.configure(scrollregion=canvas.bbox("all"))
scrollbar.configure(command=canvas.yview)

inner_frame.bind("<Configure>", on_canvas_configure)

def bind_scroll_to_widget(widget):
    widget.bind("<MouseWheel>", on_mousewheel)
    for child in widget.winfo_children():
        bind_scroll_to_widget(child)

bind_scroll_to_widget(inner_frame)

def set_scroll_to_center():
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0.1)

root.after(100, set_scroll_to_center)

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
file_menu.add_command(label="Change Port", command=change_port)
file_menu.add_command(label="Reset", command=clear_program)
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


# # If you want to update the server indicator color when the server starts or stops, you can use the following function
# def update_server_indicator(status):
#     if status:
#         server_indicator.configure(bg="green")
#     else:
#         server_indicator.configure(bg="red")

# # Update the start_stop_server function to call update_server_indicator
# def start_stop_server(status):
#     if status:
#         server_button.configure(text="Stop Server", command=partial(start_stop_server, False))
#         update_server_indicator(True)
#     else:
#         server_button.configure(text="Start Server", command=partial(start_stop_server, True))
#         update_server_indicator(False)

start_server_thread(start=True)

root.bind("<KeyPress>", on_key_press)
# Run the Tkinter root
root.mainloop()