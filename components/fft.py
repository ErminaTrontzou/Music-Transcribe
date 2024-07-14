import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal
import os
from.lilypond_convert import LilyPondConverter

class PlayedNote:
    def __init__(self, note, duration):
        self.note = note
        self.duration = duration

class FFT:
    def __init__(self, fps=5, fft_window_seconds=0.25, freq_min=10, freq_max=1000):
        self.fps = fps
        self.fft_window_seconds = fft_window_seconds
        self.freq_min = freq_min
        self.freq_max = freq_max
       
        self.frame_step = None
        self.fft_window_size = None
        self.frame_count = None
        self.frame_offset = None
        self.audio_length = None
        self.final_notes_array = []
        self.energy_threshold = 1e-4  # Initial threshold for detecting silence
        self.rolling_window_size = 10  # Number of frames for rolling average

    def freq_to_number(self, f):
        return round(69 + 12 * np.log2(f / 440.0))
    
    def number_to_freq(self, n):
        return 440 * 2.0 ** ((n - 69) / 12.0)

    def note_name(self, n):
        n = int(n)
        return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][n % 12] + str(int(n // 12 - 1))

    def extract_sample(self, audio, frame_number):
        end = frame_number * self.frame_offset
        begin = int(end - self.fft_window_size)

        if end == 0:
            return np.zeros((np.abs(begin)), dtype=float)
        elif begin < 0:
            return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
        else:
            return audio[begin:end]

    def process_audio_file(self, file_path):
        fs, data = wavfile.read(file_path)
        
        if len(data.shape) == 1:
            audio = data
        else:
            audio = data.T[0]
        
        self.frame_step = (fs / self.fps)
        self.fft_window_size = int(fs * self.fft_window_seconds)
        self.audio_length = len(audio) / fs

        window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, self.fft_window_size, False)))
        xf = np.fft.rfftfreq(self.fft_window_size, 1 / fs)
        self.frame_count = int(self.audio_length * self.fps)
        self.frame_offset = int(len(audio) / self.frame_count)

        self.final_notes_array = []
        energy_list = []

        # Initialize an empty list to hold the notes and their durations
        notes_info = []

        # For tracking currently playing note and duration
        current_played_note = PlayedNote(note=None, duration=0)
        notes = []

        for frame_number in range(self.frame_count):
            sample = self.extract_sample(audio, frame_number)
            fft_result = np.fft.rfft(sample * window)
            fft_magnitude = np.abs(fft_result).real

            frame_energy = np.sum(sample ** 2) / len(sample)
            energy_list.append(frame_energy)

            if len(energy_list) > self.rolling_window_size:
                energy_list.pop(0)

            avg_energy = np.mean(energy_list)

            if frame_energy < avg_energy * 0.5:
                current_note = "pause"
            else:
                peaks, _ = scipy.signal.find_peaks(fft_magnitude, height=1500.00, distance=int(self.fft_window_size // 4))
                valid_peaks = [peak for peak in peaks if 16.35 < xf[peak] < 7902.13]

                if len(valid_peaks) == 0:
                    current_note = "pause"
                else:
                    freq = xf[valid_peaks[0]]  # Take the first valid peak
                    note_number = self.freq_to_number(freq)
                    current_note = self.note_name(note_number)

            # Check if the current note is the same as the last noted played
            if notes and current_note == notes[-1].note:
                notes[-1].duration += self.fft_window_seconds
            else:
                notes.append(PlayedNote(note=current_note, duration=self.fft_window_seconds))

        for note in notes:
            notes_info.append({"note": note.note, "duration": note.duration})

        print('Notes for : ', os.path.basename(file_path) ,'\n', notes_info)

        converter = LilyPondConverter(notes_info)
        lilypond_file_name = os.path.splitext(file_path)[0] + ".ly"
        converter.write_to_file(lilypond_file_name)

