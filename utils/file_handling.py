
import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import ImageTk
import webbrowser



def save_qr_code(self):
        """
        Display a QR code with the application's URL.

        This method generates a QR code using the application's URL and displays it in a separate window. The QR code can be clicked to save it as an image file.

        Parameters:
            None

        Returns:
            None
        """
        url = f"http://{self.local_ip}:{self.port_number}"
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
        