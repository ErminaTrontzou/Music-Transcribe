import os
from tkinter import messagebox, filedialog
from .recorder import Recorder
from .fft import FFT
import numpy as np
from scipy.io.wavfile import read

class MicrophoneHandler:
    def __init__(self):
        self.rec = Recorder()
        self.running = None
        self.fft = FFT()
        self.recorded_file_path = ""

    def start_recording(self):
        if self.running is not None:
            messagebox.showinfo("Error", "Already recording.")
        else:
            self.running = self.rec.open('instrument_recording.wav', 'wb')
            self.running.start_recording()

    def stop_recording(self):
        if self.running is not None:
            self.recorded_file_path = self.running.stop_recording()
            self.running.wavefile.close()
            self.running = None 
            print(f"Recorded file path: {self.recorded_file_path}")

            # Open file dialog to save the recording
            save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                     filetypes=[("WAV files", "*.wav")],
                                                     title="Save the recording as")
            if save_path:
                if os.path.exists(save_path):
                    overwrite = messagebox.askyesno("File exists", "File already exists. Do you want to overwrite it?")
                    if not overwrite:
                        messagebox.showinfo("Info", "Recording not saved.")
                        return
                    else:
                        os.remove(save_path)
                os.rename(self.recorded_file_path, save_path)
                self.recorded_file_path = save_path
                print(f"Recording saved to: {self.recorded_file_path}")
            else:
                messagebox.showinfo("Info", "Recording not saved.")
        else:
            messagebox.showinfo("Error", "Not recording.")

    def process_recording(self):
        if self.recorded_file_path and os.path.exists(self.recorded_file_path):
            self.fft.process_audio_file(self.recorded_file_path)
            return True
        messagebox.showinfo("Error", "No recording found to process.")
        return False
