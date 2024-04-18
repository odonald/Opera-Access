import qrcode
import tkinter as tk
from PIL import ImageTk
from tkinter import filedialog
from config.config import AppConfig

url = AppConfig.HOST

class QrCode:
    def show_qr_code(url):

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

        qr_window = tk.Toplevel()
        qr_window.title("QR Code")
        qr_window.geometry("600x600")

        qr_label = tk.Label(qr_window, image=img_tk)
        qr_label.image = img_tk
        qr_label.pack()

        qr_window.mainloop()

    def save_qr_code(url):
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