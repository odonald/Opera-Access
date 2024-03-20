import tkinter as tk
import frame_window_setup
import session_mgmt
import server_config
import qr_code_setup
import languages

# Create the menu bar
menu_bar = tk.Menu(frame_window_setup.root)
frame_window_setup.root.configure(menu=menu_bar)

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a submenu for "Import" option
qr_menu = tk.Menu(file_menu, tearoff=0)
qr_menu.add_command(label="Save QR Code", command=lambda: qr_code_setup.save_qr_code(qr_code_setup.url))
qr_menu.add_command(label="Show QR Code", command=lambda: qr_code_setup.show_qr_code(qr_code_setup.url))

file_menu.add_command(label="Import additional language", command=languages.import_additional_language)
file_menu.add_command(label="Save Session", command=session_mgmt.save_session)
file_menu.add_command(label="Load Session", command=session_mgmt.load_session)
file_menu.add_command(label="Open Website", command=lambda: qr_code_setup.open_url_in_browser(server_config.local_ip, server_config.port_number))
file_menu.add_cascade(label="QR-Code", menu=qr_menu)
file_menu.add_command(label="Change Port", command=server_config.change_port)
file_menu.add_command(label="Reset", command=session_mgmt.clear_program)
file_menu.add_command(label="Exit", command=session_mgmt.close_program)

frame_window_setup.root.configure(menu=menu_bar)