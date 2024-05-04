import socket


class AppConfig:
    """
    The AppConfig class represents the configuration settings for the application.

    Attributes:
        APPEARANCE_MODE (str): The appearance mode of the application. Default is "System".
        APP_TITLE (str): The title of the application. Default is "Opera Access 1.0".
        WINDOW_SIZE (str): The size of the application window. Default is "1000x550".
        DEBUG (bool): Flag indicating whether debug mode is enabled. Default is False.
        HOST (str): The host IP address. Default is the IP address of the current machine.
        PORT (int): The port number for the application. Default is 7832.
        URL (str): The URL of the application. Default is "http://<HOST>:<PORT>".
        SSE_URL (str): The URL for server-sent events. Default is "http://<HOST>:<PORT>/stream/push".

    Methods:
        __init__(): Initializes an instance of the AppConfig class.

    """
    APPEARANCE_MODE = "System"
    APP_TITLE = "Opera Access 1.0"
    WINDOW_SIZE = "1000x550"
    DEBUG = False
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 7832
    URL = f"http://{HOST}:{PORT}"
    SSE_URL = f"http://{HOST}:{PORT}/stream/push"

    def __init__(self):
        pass
