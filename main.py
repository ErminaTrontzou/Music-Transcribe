import tkinter
import customtkinter

from tkinter import font



class AboutWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("500x400")
        self.attributes('-topmost', True)

        self.title("About")



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        self.geometry("800x600")

        #Fonts
        title_font = customtkinter.CTkFont(family="sans-serif", size=40, weight="bold")
        subtitle_font = customtkinter.CTkFont(family="Roboto", size=15, slant="italic")

        # Main Window
        title = customtkinter.CTkLabel(self, text="Music Transcribe", font=title_font)
        title.pack(padx=10, pady=(30, 0)) 

        subtitle = customtkinter.CTkLabel(self, text="Your Melodic Maestro – Turning Sound into Sheets Effortlessly!", font=subtitle_font)
        subtitle.pack(padx=10)  

        #Instrument Choice
        choice = customtkinter.CTkLabel(self, text="Choose an instrument", font=("Roboto", 30))
        choice.pack(padx=10, pady=30) 

        # Copyright Label
        copyright_label = customtkinter.CTkLabel(self, text="Copyright: Ermina Trontzou 2023")
        copyright_label.pack(side="bottom", padx=10, pady=10)

        self.about_button = customtkinter.CTkButton(self, text="About", command=self.open_about)
        self.about_button.pack(side="bottom", padx=20, pady=20)

        self.about_window = None

    def open_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self) 
        else:
            self.about_window.focus()  # if window exists focus it


app = App()
app.title("Music Transcribe")
app.mainloop()