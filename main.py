import tkinter
import customtkinter
from components.instrument_buttons import InstrumentButtons


class AboutWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("500x400")
        self.attributes('-topmost', True)

        self.title("About")

        self.about_text = customtkinter.CTkTextbox(self,wrap="word", 
                                           font=("arial", 15))
        self.about_text.insert("1.0", 
                       "  Music Transcribe is a Python-based application developed as part of my bachelor's thesis. "
                       "With a user-friendly interface, it focuses on the precise recognition of musical notes, "
                       "distinguishing pitch and duration.\n\n"
                       "  The application supports sourcing notes from either .mp3 "
                       "files or the sounds of various musical instruments directly from your mic. Users have the "
                       "flexibility to add new instruments too.\n\n"
                       "  Notably, Music Transcribe utilizes Fast Fourier Transform "
                       "(FFT) for the implementation of note recognition. It efficiently transcribes notes onto a "
                       "pentagram and allows for the export of these pentagram files, offering a versatile tool for "
                       "everyone, professional or not.")
        self.about_text.pack(fill="both", expand=True, padx=10, pady=50)




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
        choice.pack(padx=10, pady=(40,30)) 

        # Copyright Label
        copyright_label = customtkinter.CTkLabel(self, text="Copyright: Ermina Trontzou 2023")
        copyright_label.pack(side="bottom", padx=10, pady=10)

        def create_custom_instrument():
            # TODO
            pass

        instrument_buttons_frame = InstrumentButtons(self, create_custom_instrument)
        instrument_buttons_frame.pack(pady=(40,0))

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