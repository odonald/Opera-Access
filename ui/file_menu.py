import tkinter as tk

class FileMenu:
    def __init__(self, master, callbacks):
        self.master = master
        self.callbacks = callbacks

        menu_bar = tk.Menu(master)
        master.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        qr_menu = tk.Menu(file_menu, tearoff=0)
        qr_menu.add_command(label="Save QR Code", command=callbacks["save_qr_code"])
        qr_menu.add_command(label="Show QR Code", command=callbacks["show_qr_code"])
        file_menu.add_command(label="Import additional language", command=callbacks["import_additional_language"])
        file_menu.add_command(label="Save Session", command=callbacks["save_session"])
        file_menu.add_command(label="Load Session", command=callbacks["load_session"])
        file_menu.add_command(label="Open Website", command=callbacks["open_url_in_browser"])
        file_menu.add_cascade(label="QR-Code", menu=qr_menu)
        file_menu.add_command(label="Change Port", command=callbacks["change_port"])
        file_menu.add_command(label="Reset", command=callbacks["clear_program"])
        file_menu.add_command(label="Exit", command=callbacks["close_program"])