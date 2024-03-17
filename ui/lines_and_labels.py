import customtkinter as ctk
from tkinter import messagebox
from functools import partial

empty_line = 0
next_button_clicks = 0
prev_button_clicks = 0

# Create previous, current, and next line labels

progress = ctk.CTkProgressBar(root, orientation="horizontal")
progress.grid(row=0, column=1,columnspan=3, padx=0, pady=0, sticky="new")
progress.configure(mode="determinate")
progress.set(0)

navigation_label = ctk.CTkLabel(root, text="Display:", font=("", 20))
navigation_label.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="nwe")



prev_line_labels = [ctk.CTkLabel(inner_frame, wraplength=400, text="---") for _ in range(5)]

current_line_label = ctk.CTkLabel(inner_frame, text_color=("Yellow", "#FFD90F"), text="Please import a language or load a session.\n +\n <--- Choose display language", font=("", 25))
current_line_label.grid(row=1, column=0, padx=10, pady=10)

next_line_labels = [ctk.CTkLabel(inner_frame, wraplength=400, text="---") for _ in range(20)]

for index, label in enumerate(prev_line_labels, start=0):
    label.grid(row=index, column=0, padx=10, pady=10)

current_line_label.grid(row=5, column=0, padx=10, pady=10)

for index, label in enumerate(next_line_labels, start=6):
    label.grid(row=index, column=0, padx=10, pady=10)


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

current_line_clicks = 0

def set_current_line(line):
    global current_line, next_button_clicks, prev_button_clicks, current_line_clicks

    current_line_clicks += 1
    if current_line_clicks == 1:
        send_to_server(empty_line)

    if current_line_clicks == 2:
        current_line = line
        current_line_clicks = 0  # Reset the current line click count
        next_button_clicks = 0   # Reset the count for Next button
        prev_button_clicks = 0   # Reset the count for Previous button
        send_to_server(current_line)  # Send the clicked line to the server
        update_label()

# And update the global variables section at the top
current_line_clicks = 0
last_confirmed_line = 0  

def next_line():
    global current_line, empty_line, current_line_clicks, additional_languages, next_button_clicks, prev_button_clicks, last_confirmed_line
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line is not None and current_line < len(additional_languages[lang_code]) - 1:
        next_button_clicks += 1
        if next_button_clicks == 1:
            send_to_server(empty_line)
            last_confirmed_line = current_line  # Save the current line state

        if next_button_clicks == 2:
            current_line += 1
            next_button_clicks = 0
            prev_button_clicks = 0
            current_line_clicks = 0
            update_label()
            send_to_server(current_line)
    else:
        next_button_clicks = 0


def next_line():
    global current_line, empty_line, current_line_clicks, additional_languages, next_button_clicks, prev_button_clicks, last_confirmed_line
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line is not None and current_line < len(additional_languages[lang_code]) - 1:
        next_button_clicks += 1
        if next_button_clicks == 1:
            send_to_server(empty_line)
            last_confirmed_line = current_line

            if prev_button_clicks == 1:
                # User clicked previous and then clicked next
                current_line = last_confirmed_line
                next_button_clicks = 0
                prev_button_clicks = 0
                update_label()
                send_to_server(current_line)
                return

        if next_button_clicks == 2:
            current_line += 1
            next_button_clicks = 0
            prev_button_clicks = 0
            current_line_clicks = 0
            update_label()
            send_to_server(current_line)
    else:
        next_button_clicks = 0


def previous_line():
    global current_line, current_line_clicks, additional_languages, next_button_clicks, prev_button_clicks, last_confirmed_line
    selected_language = language.get()
    lang_code = available_languages[selected_language]

    if current_line > 0:
        prev_button_clicks += 1
        if prev_button_clicks == 1:
            send_to_server(empty_line)
            last_confirmed_line = current_line

            if next_button_clicks == 1:
                # User clicked next and then clicked previous
                current_line = last_confirmed_line
                next_button_clicks = 0
                prev_button_clicks = 0
                update_label()
                send_to_server(current_line)
                return

        if prev_button_clicks == 2:
            current_line -= 1
            prev_button_clicks = 0
            next_button_clicks = 0
            current_line_clicks = 0
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