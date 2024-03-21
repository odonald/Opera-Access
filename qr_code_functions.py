import qrcode
from tkinter import messagebox, filedialog, ttk, StringVar, simpledialog
import socket
import tkinter as tk
from PIL import ImageTk, Image


local_ip = socket.gethostbyname(socket.gethostname())
port_number = 7832

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