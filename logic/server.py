import tkinter as tk
from tkinter import simpledialog
import requests
import threading
import iso639
from config.config import AppConfig



def run_server(self):
        from logic.flask_app import app
        host = self.local_ip
        port = self.port_number
        app.run(debug=AppConfig.DEBUG, port=port, host=host, use_reloader=False)
        

def send_to_server(self, line_number):
        message = {
            "type": "message",
            "content": {
            }
        }
        for lang_code, lang_lines in self.additional_languages.items():
            lang_name = iso639.languages.get(alpha2=lang_code).name
            message["content"][lang_name] = lang_lines[line_number]
        requests.post(self.url, json=message)
        
def start_server_thread(self, start):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()
        if start:
            server_thread = threading.Thread(target=self.run_server, daemon=True)
            server_thread.start()
            self.server_running = True
            if self.local_ip == "127.0.0.1":
                self.server_status_label.configure(text=f"LOCAL - No network detected")
                self.server_indicator.configure(bg="red")
            else:
                self.server_status_label.configure(text=f"Live\n http://{self.local_ip}:{self.port_number}")
                self.server_indicator.configure(bg="green")
        else:
            self.server_running = False
            self.server_status_label.configure(text=f"Idle")
            self.server_indicator.configure(bg="red")
            
def change_port(self):
        reserved_ports = [80, 443, 8080, 8443]

        if self.server_running:
            self.start_server_thread(start=False)
            self.server_running = False
            self.server_status_label.configure(text=f"Idle")
            self.server_indicator.configure(bg="red")

        while True:
            new_port = simpledialog.askstring("Change Port", "Enter new port number between 1024 and 65535:", parent=self.root)
            if new_port:
                try:
                    port_int = int(new_port)
                    if 1024 <= port_int <= 65535 and port_int not in reserved_ports:
                        self.port_number = port_int
                        self.url = f"http://{self.local_ip}:{self.port_number}/stream/push"
                        server_thread = threading.Thread(target=self.run_server, daemon=True)
                        server_thread.start()
                        self.server_running = True
                        if self.local_ip == "127.0.0.1":
                            self.server_status_label.configure(text=f"LOCAL - No network detected")
                            self.server_indicator.configure(bg="red")
                        else:
                            self.server_status_label.configure(text=f"Live\n http://{self.local_ip}:{self.port_number}")
                            self.server_indicator.configure(bg="green")
                        break
                    else:
                        tk.messagebox.showerror("Invalid Port", "The selected port is already reserved or invalid.")
                except ValueError:
                    tk.messagebox.showerror("Invalid Port", "Please enter a valid port number.")
            else:
                break