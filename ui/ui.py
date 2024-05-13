import tkinter as tk
import customtkinter as ctk
from utils.qr_code_utils import QrCode
from config.config import AppConfig


class UserInterface:
    """
The UserInterface class represents the graphical user interface of the application. It contains methods for creating various UI elements such as buttons, labels, frames, and progress bars.

Attributes:
    root (tk.Tk): The root window of the application.
    navigation_frame (tk.LabelFrame): The frame that contains the main navigation elements.
    navigation_frame2 (ctk.CTkFrame): The frame that contains the previous and next line buttons.
    navigation_frame3 (ctk.CTkFrame): The frame that contains the line number entry and go button.
    sidebar_frame (ctk.CTkFrame): The frame that contains the sidebar elements.
    canvas (tk.Canvas): The canvas widget for displaying the main content.
    inner_frame (ctk.CTkFrame): The frame inside the canvas for displaying the content.
    canvas_frame (int): The ID of the canvas window.
    current_line_label (ctk.CTkLabel): The label for displaying the current line.
    prev_line_labels (list[ctk.CTkLabel]): The labels for displaying the previous lines.
    next_line_labels (list[ctk.CTkLabel]): The labels for displaying the next lines.
    appearance_mode_optionmenu (ctk.CTkOptionMenu): The option menu for selecting the appearance mode.
    sidebar_label (ctk.CTkLabel): The label for the sidebar.
    navigation_label (ctk.CTkLabel): The label for the navigation section.
    progress (ctk.CTkProgressBar): The progress bar for indicating the progress.
    website_button (ctk.CTkButton): The button for opening the website.
    show_qr_button (ctk.CTkButton): The button for showing the QR code.
    import_translation_button (ctk.CTkButton): The button for importing the translation.
    previous_line_button (ctk.CTkButton): The button for navigating to the previous line.
    next_line_button (ctk.CTkButton): The button for navigating to the next line.
    line_number_entry (ctk.CTkEntry): The entry field for entering the line number.
    go_button (ctk.CTkButton): The button for jumping to a specific line.

Methods:
    create_website_button: Creates the website button.
    create_import_translation_button: Creates the import translation button.
    create_show_qr_button: Creates the show QR button.
    create_appearance_mode_optionmenu: Creates the appearance mode option menu.
    create_previous_line_button: Creates the previous line button.
    create_next_line_button: Creates the next line button.
    create_line_number_entry: Creates the line number entry field.
    create_go_button: Creates the go button.
    create_progress_bar: Creates the progress bar.
    main_frame: Creates the main navigation frame.
    create_canvas: Creates the canvas widget.
    create_inner_frame: Creates the inner frame inside the canvas.
    create_canvas_frame: Creates the canvas frame.
    create_sidebar_frame: Creates the sidebar frame.
    create_sidebar_label: Creates the sidebar label.
    create_navigation_label: Creates the navigation label.
    labels_inner_frame: Creates the labels inside the inner frame.
"""

    def __init__(self, root):
        self.root = root
        self.url = AppConfig.URL
        self.navigation_frame, self.navigation_frame2, self.navigation_frame3 = self.main_frame()
        self.sidebar_frame = self.create_sidebar_frame()
        self.canvas = self.create_canvas()
        self.inner_frame = self.create_inner_frame()
        self.canvas_frame = self.create_canvas_frame()
        self.current_line_label, self.prev_line_labels, self.next_line_labels = self.labels_inner_frame()
        self.appearance_mode_optionmenu = self.create_appearance_mode_optionmenu()
        self.sidebar_label = self.create_sidebar_label()
        self.navigation_label = self.create_navigation_label()
        self.progress = self.create_progress_bar()
        self.website_button = self.create_website_button()
        self.show_qr_button = self.create_show_qr_button()
        self.bind_show_qr_button(lambda: QrCode.show_qr_code(self.url))
        self.import_translation_button = self.create_import_translation_button()
        self.previous_line_button = self.create_previous_line_button()
        self.next_line_button = self.create_next_line_button()
        self.line_number_entry = self.create_line_number_entry()
        self.go_button = self.create_go_button(None)

    def create_website_button(self):
        """
        Creates the website button.

        Returns:
            ctk.CTkButton: The created website button.
        """
        website_button = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Open Website")
        website_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")
        return website_button

    def create_import_translation_button(self):
        """
        Creates the import translation button.

        Returns:
            ctk.CTkButton: The created import translation button.
        """
        import_translation_button = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Import Text")
        import_translation_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsw")
        return import_translation_button

    def create_show_qr_button(self):
        """
        Creates the show QR button.

        Returns:
            ctk.CTkButton: The created show QR button.
        """
        show_qr_button = ctk.CTkButton(self.sidebar_frame, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Show QR")
        show_qr_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsw")
        return show_qr_button

    def bind_show_qr_button(self, command):
        self.show_qr_button.configure(command=command)

    def create_appearance_mode_optionmenu(self):
        """
        Creates the appearance mode option menu.

        Returns:
            ctk.CTkOptionMenu: The created appearance mode option menu.
        """
        appearance_mode_optionmenu = ctk.CTkOptionMenu(self.sidebar_frame, values=[
                                                       "Light", "Dark", "System"], command=Events.change_appearance_mode_event)
        appearance_mode_optionmenu.grid(
            row=10, column=0, padx=0, pady=10, sticky="s")
        appearance_mode_optionmenu.set("Dark")
        return appearance_mode_optionmenu

    def create_previous_line_button(self):
        """
        Creates the previous line button.

        Returns:
            ctk.CTkButton: The created previous line button.
        """
        previous_line_button = ctk.CTkButton(self.navigation_frame2, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Previous")
        previous_line_button.grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        return previous_line_button

    def create_next_line_button(self):
        """
        Creates the next line button.

        Returns:
            ctk.CTkButton: The created next line button.
        """
        next_line_button = ctk.CTkButton(self.navigation_frame2, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Next")
        next_line_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        return next_line_button

    def create_line_number_entry(self):
        """
        Creates the line number entry field.

        Returns:
            ctk.CTkEntry: The created line number entry field.
        """
        line_number_entry = ctk.CTkEntry(
            self.navigation_frame3, placeholder_text="Jump to line")
        line_number_entry.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        return line_number_entry

    def create_go_button(self, jump_to_line_command):
        """
        Creates the go button.

        Parameters:
            jump_to_line_command (function): The command to be executed when the go button is clicked.

        Returns:
            ctk.CTkButton: The created go button.
        """
        go_button = ctk.CTkButton(self.navigation_frame3, fg_color="transparent", text_color=(
            "gray10", "#DCE4EE"), border_width=2, text="Go", command=jump_to_line_command)
        go_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        return go_button

    def create_progress_bar(self):
        """
        Creates the progress bar.

        Returns:
            ctk.CTkProgressBar: The created progress bar.
        """
        progress = ctk.CTkProgressBar(self.root, orientation="horizontal")
        progress.grid(row=0, column=1, columnspan=4,
                      padx=0, pady=0, sticky="new")
        progress.configure(mode="determinate")
        progress.set(0)
        return progress

    def main_frame(self):
        """
        Creates the main navigation frame.

        Returns:
            tuple: A tuple containing the navigation frames.
                - navigation_frame (tk.LabelFrame): The frame that contains the main navigation elements.
                - navigation_frame2 (ctk.CTkFrame): The frame that contains the previous and next line buttons.
                - navigation_frame3 (ctk.CTkFrame): The frame that contains the line number entry and go button.
        """
        navigation_frame = tk.LabelFrame(self.root, height=900)
        navigation_frame.grid(row=1, rowspan=6, column=1,
                              columnspan=4, padx=20, pady=10, sticky="nesw")
        navigation_frame.grid_rowconfigure(0, weight=1)
        navigation_frame.grid_columnconfigure(0, weight=1)
        navigation_frame2 = ctk.CTkFrame(
            self.root, fg_color="transparent", corner_radius=4, border_width=0)
        navigation_frame2.grid(row=7, column=1, rowspan=1,
                               columnspan=4, padx=0, pady=0, sticky="n")
        navigation_frame3 = ctk.CTkFrame(
            self.root, fg_color="transparent", corner_radius=4, border_width=0)
        navigation_frame3.grid(row=7, column=1, rowspan=1,
                               columnspan=4, padx=0, pady=0, sticky="s")
        return navigation_frame, navigation_frame2, navigation_frame3

    def create_canvas(self):
        """
        Creates the canvas widget.

        Returns:
            tk.Canvas: The created canvas widget.
        """
        canvas = tk.Canvas(self.navigation_frame)
        canvas.grid(row=0, column=0, sticky="nsew")
        return canvas

    def create_inner_frame(self):
        """
        Creates the inner frame inside the canvas.

        Returns:
            ctk.CTkFrame: The created inner frame.
        """
        inner_frame = ctk.CTkFrame(self.canvas)
        inner_frame.grid_rowconfigure((0, 1, 2), weight=1)
        inner_frame.grid_columnconfigure(0, weight=1)
        return inner_frame

    def create_canvas_frame(self):
        """
        Creates the canvas frame.

        Returns:
            int: The ID of the canvas window.
        """
        canvas_frame = self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw")
        return canvas_frame

    def create_sidebar_frame(self):
        """
        Creates the sidebar frame.

        Returns:
            ctk.CTkFrame: The created sidebar frame.
        """
        sidebar_frame = ctk.CTkFrame(
            self.root, width=100, corner_radius=0, border_width=2)
        sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsw")
        sidebar_frame.grid_rowconfigure(8, weight=1)
        sidebar_frame.grid_columnconfigure(0, weight=0)
        return sidebar_frame

    def create_sidebar_label(self):
        """
        Creates the sidebar label.

        Returns:
            ctk.CTkLabel: The created sidebar label.
        """
        sidebar_label = ctk.CTkLabel(
            self.sidebar_frame, text="Menu:", font=("", 20))
        sidebar_label.grid(row=0, column=0, padx=20, pady=10, sticky="nwe")
        return sidebar_label

    def create_navigation_label(self):
        """
        Creates the navigation label.

        Returns:
            ctk.CTkLabel: The created navigation label.
        """
        navigation_label = ctk.CTkLabel(
            self.root, text="Display:", font=("", 20))
        navigation_label.grid(row=0, column=1, columnspan=4,
                              padx=20, pady=10, sticky="we")
        return navigation_label

    def labels_inner_frame(self):
        """
        Creates the labels inside the inner frame.

        Returns:
            tuple: A tuple containing the labels.
                - current_line_label (ctk.CTkLabel): The label for displaying the current line.
                - prev_line_labels (list[ctk.CTkLabel]): The labels for displaying the previous lines.
                - next_line_labels (list[ctk.CTkLabel]): The labels for displaying the next lines.
        """
        current_line_label = ctk.CTkLabel(self.inner_frame, text_color=(
            "Yellow", "#FFD90F"), text="Please import a language or load a session.\n +\n <--- Choose display language", font=("", 25))
        current_line_label.grid(row=5, column=0, padx=10, pady=10)
        prev_line_labels = [ctk.CTkLabel(
            self.inner_frame, wraplength=400, text="---") for _ in range(5)]
        for index, label in enumerate(prev_line_labels, start=0):
            label.grid(row=index, column=0, padx=10, pady=10)
        next_line_labels = [ctk.CTkLabel(
            self.inner_frame, wraplength=400, text="---") for _ in range(20)]
        for index, label in enumerate(next_line_labels, start=6):
            label.grid(row=index, column=0, padx=10, pady=10)
        return current_line_label, prev_line_labels, next_line_labels


class Events:
    """
    The Events class provides static methods for handling various events in the application.

    Methods:
        change_appearance_mode_event: Handles the event of changing the appearance mode.

    """

    def __init__(self):
        raise NotImplementedError(
            "This class is not meant to be instantiated.")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        """
        Handles the event of changing the appearance mode.

        Parameters:
            new_appearance_mode (str): The new appearance mode to be set.

        """
        ctk.set_appearance_mode(new_appearance_mode)


def create_main_window():
    """
    Creates the main window for the application.

    Returns:
        ctk.CTk: The root window of the application.
    """
    root = ctk.CTk()
    # Modes: "System" (standard), "Dark", "Light"
    ctk.set_appearance_mode("System")
    root.title("Opera Access 1.0")
    root.configure(bg=ctk.set_appearance_mode("System"))
    root.geometry(f"{1000}x{550}")
    root.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
    root.columnconfigure(0, weight=0, minsize=100)
    root.columnconfigure((1, 2, 3, 4), weight=1)

    return root
