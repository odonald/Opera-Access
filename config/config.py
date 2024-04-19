import socket

class AppConfig:
    APPEARANCE_MODE = "System"
    APP_TITLE = "Opera Access 1.0"
    WINDOW_SIZE = "1000x550"
    DEBUG = False
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 7832
    URL = f"http://{HOST}:{PORT}"
    SSE_URL = f"http://{HOST}:{PORT}/stream/push"