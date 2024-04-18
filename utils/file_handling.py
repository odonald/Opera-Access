
import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import ImageTk
import webbrowser
from config.config import AppConfig
from ui.ui import UserInterface
from ui.file_menu import FileMenu



class QrCode:
    def __init__(self, root):
        self.root = root
        self.ui = UserInterface(root) 
        self.bind_show_qr_button()

    local_ip = AppConfig.HOST
    port_number = AppConfig.PORT

    def bind_show_qr_button(self):
        self.ui.show_qr_button.configure(command=lambda: self.show_qr_code())          

    def show_qr_code(self):
            url = f"http://{self.local_ip}:{self.port_number}"

            def on_qr_click(event):
                self.save_qr_code()

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

            qr_label.bind("<Button-1>", on_qr_click)

            qr_window.mainloop()
            