import customtkinter as ctk
from components.instrument_buttons import InstrumentButtons
from components.input_options import OptionsPageContent

# About Window
class AboutWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("500x400")
        self.attributes('-topmost', True)

        self.title("About")

        self.about_text = ctk.CTkTextbox(self, wrap="word", font=("arial", 15))
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


class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        # Fonts
        title_font = ctk.CTkFont(family="sans-serif", size=40, weight="bold")
        subtitle_font = ctk.CTkFont(family="Roboto", size=15, slant="italic")

        # Main Window
        title = ctk.CTkLabel(self, text="Music Transcribe", font=title_font)
        title.pack(side="top", fill="x", pady=10)
        subtitle = ctk.CTkLabel(self, text="Your Melodic Maestro – Turning Sound into Sheets Effortlessly!", font=subtitle_font)
        subtitle.pack(side="top", fill="x", pady=10)
    
        #Instrument Choice
        choice = ctk.CTkLabel(self, text="Choose an instrument", font=("Roboto", 30))
        choice.pack(side="top", fill="x", pady=10)

        instrument_buttons_frame = InstrumentButtons(self, self.create_custom_instrument)
        instrument_buttons_frame.pack()

    def create_custom_instrument(self):
        # TODO
        pass


class InputOptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        options_component = OptionsPageContent(self)
        options_component.pack(side="top", fill="x", pady=10)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.geometry("800x600")

        

        # Container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, InputOptions):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        

        #About Window
        self.about_button = ctk.CTkButton(self, text="About", command=self.open_about)
        self.about_button.pack()
        self.about_window = None

        #Copyright Label
        copyright_label = ctk.CTkLabel(self, text="Copyright: Ermina Trontzou 2023")
        copyright_label.pack()

        
    
    def open_options_component(self):
        self.show_frame("InputOptions")

    def open_about(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self) 
        else:
            self.about_window.focus()  # if window exists focus it

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.title("Music Transcribe")
    app.mainloop()


































# import tkinter
# import customtkinter
# from components.instrument_buttons import InstrumentButtons
# from components.input_options import OptionsPageContent


# #About Window
# class AboutWindow(customtkinter.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.geometry("500x400")
#         self.attributes('-topmost', True)

#         self.title("About")

#         self.about_text = customtkinter.CTkTextbox(self,wrap="word", 
#                                            font=("arial", 15))
#         self.about_text.insert("1.0", 
#                        "  Music Transcribe is a Python-based application developed as part of my bachelor's thesis. "
#                        "With a user-friendly interface, it focuses on the precise recognition of musical notes, "
#                        "distinguishing pitch and duration.\n\n"
#                        "  The application supports sourcing notes from either .mp3 "
#                        "files or the sounds of various musical instruments directly from your mic. Users have the "
#                        "flexibility to add new instruments too.\n\n"
#                        "  Notably, Music Transcribe utilizes Fast Fourier Transform "
#                        "(FFT) for the implementation of note recognition. It efficiently transcribes notes onto a "
#                        "pentagram and allows for the export of these pentagram files, offering a versatile tool for "
#                        "everyone, professional or not.")
#         self.about_text.pack(fill="both", expand=True, padx=10, pady=50)




# class App(customtkinter.CTk):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         customtkinter.set_appearance_mode("System")
#         customtkinter.set_default_color_theme("blue")
#         self.geometry("800x600")

#         #Fonts
#         title_font = customtkinter.CTkFont(family="sans-serif", size=40, weight="bold")
#         subtitle_font = customtkinter.CTkFont(family="Roboto", size=15, slant="italic")

#         # Main Window
#         title = customtkinter.CTkLabel(self, text="Music Transcribe", font=title_font)
#         title.pack(padx=10, pady=(30, 0)) 
#         subtitle = customtkinter.CTkLabel(self, text="Your Melodic Maestro – Turning Sound into Sheets Effortlessly!", font=subtitle_font)
#         subtitle.pack(padx=10)  

#         #Instrument Choice
#         choice = customtkinter.CTkLabel(self, text="Choose an instrument", font=("Roboto", 30))
#         choice.pack(padx=10, pady=(40,30)) 

#         # Copyright Label
#         copyright_label = customtkinter.CTkLabel(self, text="Copyright: Ermina Trontzou 2023")
#         copyright_label.pack(side="bottom", padx=10, pady=10)

#         def create_custom_instrument():
#             # TODO
#             pass

#         instrument_buttons_frame = InstrumentButtons(self, create_custom_instrument)
#         instrument_buttons_frame.pack(pady=(40,0))

#         self.about_button = customtkinter.CTkButton(self, text="About", command=self.open_about)
#         self.about_button.pack(side="bottom", padx=20, pady=20)

#         self.about_window = None
#         self.options_component = None

#     def open_about(self):
#         if self.about_window is None or not self.about_window.winfo_exists():
#             self.about_window = AboutWindow(self) 
#         else:
#             self.about_window.focus()  # if window exists focus it
     
#     def open_options_component(self):
#         if self.options_component is None or not self.options_component.winfo_exists():
#             # Create the options page content frame
#             self.options_component = OptionsPageContent(self)
#             self.options_component.pack(fill="both", expand=True)
#         else:
#             self.options_component.lift()  

# app = App()
# app.title("Music Transcribe")
# app.mainloop()