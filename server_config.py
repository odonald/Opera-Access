import os
import sys
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk, StringVar, simpledialog
import requests
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
