import tkinter as tk
import customtkinter
from tkinter import filedialog
from tkinter import messagebox
import os
from.microphone_handler import MicrophoneHandler
from.music_file_handler import MusicFileHandler

class OptionsPageContent(customtkinter.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.microphone_handler = MicrophoneHandler()
        self.music_file_handler = MusicFileHandler()
        self.chosen_file = tk.StringVar()
        self.recorded_file_path = ""
        self.controller = controller

        # Fonts
        self.tab_font_style = customtkinter.CTkFont(size=25)
        self.tab_content_style = customtkinter.CTkFont(size=20)
        self.chosen_file_name_style = customtkinter.CTkFont(size=12, slant="italic")

        self.options_container = customtkinter.CTkFrame(self)
        self.options_container.grid(row=0, column=0, pady=(50,0))

        # Label and tab frame
        self.frame_with_label = customtkinter.CTkFrame(self.options_container)
        self.frame_with_label.grid(row=0, column=0, sticky="nsew")

        self.choose_method_label = customtkinter.CTkLabel(self.frame_with_label, text="Choose an input method", font=("sans-serif", 30))
        self.choose_method_label.grid(row=0, column=0, padx=150, pady=(0,50), sticky="w")

        # Grid of the whole tab
        self.options_tab = customtkinter.CTkTabview(self.frame_with_label)
        self.options_tab.grid(row=1, column=0, sticky="nsew")
        self.options_tab.configure(width=600)

        # Tab Styling
        self.options_tab._segmented_button.configure(font=self.tab_font_style)

        # Music File Tab
        self.file_tab = self.options_tab.add("MP3 File")
        self.file_tab_label = customtkinter.CTkLabel(self.file_tab, text="Choose a file to process", font=self.tab_content_style)
        self.file_tab_label.pack(fill="both", expand=True)

        self.file_button = customtkinter.CTkButton(self.file_tab, text="Choose File", command=self.choose_file)
        self.file_button.pack(side="bottom", padx=10, pady=10)

        self.chosen_file_name = customtkinter.CTkLabel(self.file_tab, textvariable=self.chosen_file, font=self.chosen_file_name_style, width=15, height=1)
        self.chosen_file_name.pack(fill="both", padx=10, pady=20)

        self.process_button = customtkinter.CTkButton(self.file_tab, text="Start process", state="disabled", command=self.process_chosen_file)
        self.process_button.pack(side="bottom", padx=20, pady=10)

        self.status_message_label = customtkinter.CTkLabel(self.file_tab, text="Ready", font=self.tab_content_style)
        self.status_message_label.pack(fill="both", expand=True)

        # Microphone Tab
        self.mic_tab = self.options_tab.add("Microphone")
        self.mic_tab_label = customtkinter.CTkLabel(self.mic_tab, text="Click Start recording to start", font=self.tab_content_style)
        self.mic_tab_label.pack(fill="both", expand=True)

        self.button_frame = customtkinter.CTkFrame(self.mic_tab)
        self.button_frame.pack(side="top", pady=10)

        self.mic_tab_start_button = customtkinter.CTkButton(self.button_frame, text="Start Recording", command=self.start_recording)
        self.mic_tab_start_button.pack(side="left", padx=10)

        self.mic_tab_stop_button = customtkinter.CTkButton(self.button_frame, text="Stop Recording and Save", command=self.stop_recording, state="disabled")
        self.mic_tab_stop_button.pack(side="left", padx=10)

        self.mic_tab_process_button = customtkinter.CTkButton(self.button_frame, text="Process File", command=self.process_recording, state="disabled")
        self.mic_tab_process_button.pack(side="left", padx=10)

        # Return to Start Page button
        self.return_button = customtkinter.CTkButton(self, text="Return", command=self.return_to_start)
        self.return_button.grid(row=0, column=1, padx=(0,100), pady=(450,5), sticky="w")

        # Configure grid layout so that container will always be in the desired place of the window (padx=100, pady=200)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.options_container.grid(columnspan=3, rowspan=3)

    def return_to_start(self):
        self.chosen_file.set("")
        self.chosen_file_name.configure(text="")
        self.process_button.configure(state="disabled")
        self.controller.show_frame("StartPage")

    def choose_file(self):
        success = self.music_file_handler.choose_file()
        if success:
            self.chosen_file.set(self.music_file_handler.chosen_file)
            self.process_button.configure(state="normal")

    def process_chosen_file(self):
        success = self.music_file_handler.process_file()
        if success:
            self.status_message_label.configure(text="File processed successfully!")
            self.chosen_file.set("")
            self.chosen_file_name.configure(text="")
            self.process_button.configure(state="disabled")

    def start_recording(self):
        self.microphone_handler.start_recording()
        self.mic_tab_start_button.configure(state="disabled")
        self.mic_tab_stop_button.configure(state="normal")
        self.mic_tab_process_button.configure(state="disabled")

        self.mic_tab_label.configure(text="Recording...")

    def stop_recording(self):
        self.microphone_handler.stop_recording()
        self.mic_tab_stop_button.configure(state="disabled")
        self.mic_tab_process_button.configure(state="normal")
        self.mic_tab_start_button.configure(state="normal")

        self.mic_tab_start_button.configure(text="Start New Recording")
        self.mic_tab_label.configure(text="Recording stopped. Click Process to make it into a sheet!")

    def process_recording(self):
        success = self.microphone_handler.process_recording()
        if success:
            self.mic_tab_label.configure(text="Recording processed successfully!")
            self.mic_tab_start_button.configure(state="normal")
            self.mic_tab_process_button.configure(state="disabled")
