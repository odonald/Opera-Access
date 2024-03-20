import tkinter as tk
import customtkinter as ctk
import frame_window_setup
import lines_and_labels
import server_config
import qr_code_setup
import languages

# create sidebar frame with widgets
sidebar_frame = ctk.CTkFrame(frame_window_setup.root, width=100, corner_radius=0, border_width=2)
sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
sidebar_frame.grid_rowconfigure(8, weight=1)
sidebar_frame.grid_columnconfigure(1, weight=1)
Sidebar_label = ctk.CTkLabel(sidebar_frame, text="Menu:",font=("", 20))
Sidebar_label.grid(row=0, column=0,  padx=20, pady=10, sticky="nwe")
import_translation_button = ctk.CTkButton(sidebar_frame ,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Import Text", command=languages.import_additional_language)
import_translation_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsw")

show_qr_button = ctk.CTkButton(sidebar_frame,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2,text="Show QR", command=lambda: qr_code_setup.show_qr_code(qr_code_setup.url))
show_qr_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")

# server_button = ctk.CTkButton(sidebar_frame,fg_color="transparent",text_color=("gray10", "#DCE4EE"),border_width=2, text="Start Server", command=partial(start_stop_server, True))
# server_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
frame_window_setup.inner_frame.grid_rowconfigure((0, 1, 2), weight=1)
frame_window_setup.inner_frame.grid_columnconfigure(0, weight=1)

website_button = ctk.CTkButton(sidebar_frame,fg_color="transparent", text_color=("gray10", "#DCE4EE"),border_width=2,text="Open Website", command=lambda: qr_code_setup.open_url_in_browser(qr_code_setup.local_ip, qr_code_setup.port_number))
website_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")


language_label = ctk.CTkLabel(sidebar_frame, text="Switch Display Language:")
language_label.grid(row=4, column=0, padx=10, pady=0, sticky="nw")

language = tk.StringVar(frame_window_setup.root)
language.set("Choose")

language_switcher = ctk.CTkOptionMenu(sidebar_frame, variable=language, state="normal", values=(), width=10)
language_switcher.grid(row=5, column=0, padx=10, pady=0, sticky="nwe")
language_switcher.configure(values=(), command=lambda choice: lines_and_labels.update_label())

imported_languages_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text="Imported Languages:")
imported_languages_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

server_status_menu_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent",font=("", 20), text_color=("gray10", "#DCE4EE"), text=f"Server Status:")
server_status_menu_label.grid(row=7, column=0, padx=10, pady=0, sticky="nw")

server_status_label = ctk.CTkLabel(sidebar_frame, fg_color="transparent", text_color=("gray10", "#DCE4EE"), text=f"{url}")
server_status_label.grid(row=8, column=0, padx=10, pady=0, sticky="nw")

server_indicator = tk.Canvas(sidebar_frame, width=12, height=12, bg="red", bd=0, highlightthickness=0)
server_indicator.grid(row=7, column=0, padx=10, pady=10, sticky="e")

server_config.start_server_thread(start=True)

appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=lines_and_labels.change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=9, column=0, padx=10, pady=10, sticky="s")
appearance_mode_optionemenu.set("Dark")