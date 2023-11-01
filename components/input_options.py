import tkinter as tk
import customtkinter


class OptionsPageContent(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        options_tab = customtkinter.CTkTabview(self);
        options_tab.pack(fill="both", expand=True)

        file_tab = options_tab.add("MP3 File")
        file_tab_label = customtkinter.CTkLabel(file_tab, text="Content of Tab 1")

        mic_tab = options_tab.add("Microphone")
        mic_tab_label = customtkinter.CTkLabel(mic_tab, text="Content of Tab 2")

        file_tab_label.pack(fill="both", expand=True)
        mic_tab_label.pack(fill="both", expand=True)