import tkinter as tk
import customtkinter

class InstrumentButtons(customtkinter.CTkFrame):
    def __init__(self, master, create_custom_instrument_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Global configuration for instrument_buttons
        button_config = {
            "width": 100,
            "height": 100,
            "corner_radius": 30,
            "font": ("Roboto", 30),
            "text_color": "black",
            "hover_color": "light grey"
        }

        self.piano_button = customtkinter.CTkButton(self, text="Piano", command=self.on_piano_click, **button_config)
        self.piano_button.pack(side="left", padx=5)

        self.guitar_button = customtkinter.CTkButton(self, text="Guitar", command=self.on_guitar_click, **button_config)
        self.guitar_button.pack(side="left", padx=5)

        self.plus_button = customtkinter.CTkButton(self, text="+", command=create_custom_instrument_callback, **button_config)
        self.plus_button.pack(side="left", padx=5)

    def on_piano_click(self):
        self.master.controller.open_options_component()

    def on_guitar_click(self):
        # TODO
        print("Guitar button clicked")
