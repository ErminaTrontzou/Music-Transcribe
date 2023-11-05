import tkinter as tk
import customtkinter


class OptionsPageContent(customtkinter.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.controller = controller

        #Fonts
        tab_font_style = customtkinter.CTkFont(size=25)
        tab_content_style = customtkinter.CTkFont(size=20)

        options_container = customtkinter.CTkFrame(self)
        options_container.grid(row=0, column=0, pady=(50,0)) 

        # Label and tab frame
        frame_with_label = customtkinter.CTkFrame(options_container)
        frame_with_label.grid(row=0, column=0, sticky="nsew")

        choose_method_label = customtkinter.CTkLabel(frame_with_label, text="Choose an input method", font=("sans-serif", 30))
        choose_method_label.grid(row=0, column=0, padx=150, pady=(0,50), sticky="w")

        # Grid of the whole tab
        options_tab = customtkinter.CTkTabview(frame_with_label)
        options_tab.grid(row=1, column=0, sticky="nsew")
        options_tab.configure(width=600)

        #Tab Styling
        options_tab._segmented_button.configure(font=tab_font_style)

        file_tab = options_tab.add("MP3 File")
        file_tab_label = customtkinter.CTkLabel(file_tab, text="Content of Tab 1", font=tab_content_style)

        mic_tab = options_tab.add("Microphone")
        mic_tab_label = customtkinter.CTkLabel(mic_tab, text="Content of Tab 2", font=tab_content_style)

        file_tab_label.pack(fill="both", expand=True)
        mic_tab_label.pack(fill="both", expand=True)

        #Return  button
        return_button = customtkinter.CTkButton(self, text="Return", command=self.return_to_start)
        return_button.grid(row=0, column=1,padx=(0,100) , pady=(450,5), sticky="w")

        # Configure grid layout so that container will always be in the desired place of the window (padx=100, pady=200)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        options_container.grid(columnspan=3, rowspan=3)

       

        
    def return_to_start(self):
        self.controller.show_frame("StartPage")