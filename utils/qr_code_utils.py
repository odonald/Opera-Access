"""
This code defines a class called QrCode with two methods: show_qr_code and save_qr_code. 

The show_qr_code method generates a QR code image using the qrcode library and displays it in a tkinter window. The URL to be encoded in the QR code is passed as an argument to the method.

The save_qr_code method also generates a QR code image using the qrcode library, but instead of displaying it, it prompts the user to choose a file path to save the image as a PNG file. The URL to be encoded in the QR code is passed as an argument to the method.

Both methods use the AppConfig class from the config.config module to retrieve the URL to be encoded in the QR code.
"""

import qrcode
import tkinter as tk
from PIL import ImageTk
from tkinter import filedialog
from config.config import AppConfig

url = AppConfig.URL


class QrCode:
    """
    This class represents a QR Code generator.

    The QrCode class has two methods:
    - show_qr_code(url): Generates a QR code image using the qrcode library and displays it in a tkinter window. The URL to be encoded in the QR code is passed as an argument to the method.
    - save_qr_code(url): Generates a QR code image using the qrcode library and prompts the user to choose a file path to save the image as a PNG file. The URL to be encoded in the QR code is passed as an argument to the method.

    Both methods use the AppConfig class from the config.config module to retrieve the URL to be encoded in the QR code.

    Example usage:
        qr = QrCode()
        qr.show_qr_code("https://example.com")
        qr.save_qr_code("https://example.com")
    """
    @staticmethod
    def show_qr_code():
        """
        Generates a QR code image using the qrcode library and displays it in a tkinter window.

        Parameters:
        - url (str): The URL to be encoded in the QR code.

        Returns:
        None

        Example:
            qr = QrCode()
            qr.show_qr_code("https://example.com")
        """

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

    @staticmethod
    def save_qr_code():
        """
        Generates a QR code image using the qrcode library and prompts the user to choose a file path to save the image as a PNG file.

        Parameters:
        - url (str): The URL to be encoded in the QR code.

        Returns:
        None

        Example:
            qr = QrCode()
            qr.save_qr_code("https://example.com")
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            img.save(file_path)

    def __init__(self):
        pass
