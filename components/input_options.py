import tkinter as tk
import customtkinter


class OptionsPageContent(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        options_container = customtkinter.CTkFrame(self)
        options_container.grid(row=0, column=0, padx=100, pady=(200,0))  # Adjust padx and pady as needed

        options_tab = customtkinter.CTkTabview(options_container)
        options_tab.grid(row=0, column=0, sticky="nsew")
        options_tab.configure(width=600) 

        file_tab = options_tab.add("MP3 File")
        file_tab_label = customtkinter.CTkLabel(file_tab, text="Content of Tab 1")

        mic_tab = options_tab.add("Microphone")
        mic_tab_label = customtkinter.CTkLabel(mic_tab, text="Content of Tab 2")

        file_tab_label.pack(fill="both", expand=True)
        mic_tab_label.pack(fill="both", expand=True)

        # Configure grid layout so that container will always be in the desired place of the window (padx=100, pady=200)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        options_container.grid(columnspan=3, rowspan=3)