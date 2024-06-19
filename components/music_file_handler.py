import os
from tkinter import filedialog
from tkinter import messagebox
from.fft import FFT

class MusicFileHandler:
    def __init__(self):
        self.fft = FFT()
        self.chosen_file = ""

    def choose_file(self):
        self.chosen_file = filedialog.askopenfilename(filetypes=[("wav files", "*.wav")])
        if self.chosen_file:
            print(self.chosen_file)
            return True
        return False

    def process_file(self):
        if self.chosen_file:
            self.fft.process_audio_file(self.chosen_file)
            return True
        return False
