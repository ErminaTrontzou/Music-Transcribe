import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal
import os
from .lilypond_convert import LilyPondConverter

class PlayedNote:
    def __init__(self, note, duration):
        self.note = note
        self.duration = duration

class FFT:
    def __init__(self, fps=5, fft_window_seconds=0.20, freq_min=10, freq_max=1000):
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
        self.energy_threshold = 1e-4 
        self.rolling_window_size = 10

    def freq_to_number(self, f):
        return 12*np.log2(f/27.5) + 9
    
    def number_to_freq(self, n):
        return 27.5 * 2**((n-9)/12)
    
    def note_name(self, n):
        n = round(n)
        note = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][n % 12]
        octave = str(int(n // 12))
        return note + octave

    def extract_sample(self, audio, frame_number):
        begin = frame_number * self.frame_offset
        end = begin + self.fft_window_size
        if end > len(audio):
            end = len(audio)
            return np.concatenate([audio[begin:], np.zeros((self.fft_window_size - (end - begin)), dtype=float)])

        return audio[begin:end]

        # end = frame_number * self.frame_offset
        # begin = int(end - self.fft_window_size)

        # if end == 0:
        #     return np.zeros((np.abs(begin)), dtype=float)
        # elif begin < 0:
        #     return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
        # else:
        #     return audio[begin:end]
        
    def gcd(self, frequencies):
        """Calculate GCD among a list of frequencies."""
        # Check if the frequencies list is empty
        if not frequencies:
            return None  # Return None if the list is empty
        
        def euclidean_gcd(a, b):
            """Euclidean algorithm for GCD."""
            while b != 0:
                a, b = b, a % b
            return a
        
        int_frequencies = [round(freq * 1e6) for freq in frequencies]
        gcd_freq = int_frequencies[0]
        for freq in int_frequencies[1:]:
            gcd_freq = euclidean_gcd(gcd_freq, freq)
        return gcd_freq / 1e6
  

    def process_audio_file(self, file_path):

        # assert self.gcd([100.0, 100.0]) == 100.0, "Test Case 1 Failed"
        assert self.gcd([292.0, 584.0, 876.0]) == 292.0, "Test Case 2 Failed"
        # assert self.gcd([300.0]) == 300.0, "Test Case 3 Failed"
        # assert self.gcd([13.0, 26.0]) == 13.0, "Test Case 4 Failed"
        # assert self.gcd([]) == None, "Test Case 5 Failed"
        # print("All test cases passed.")


        fs, data = wavfile.read(file_path)
    
        if len(data.shape) == 1:
            audio = data
        else:
            audio = data.T[0]
        
        self.frame_step = (fs / self.fps)
        self.fft_window_size = int(fs * self.fft_window_seconds)
        print(f"FFT windows size of {self.fft_window_seconds} sec leads to FFT windows size of {self.fft_window_size} samples")
        self.audio_length = len(audio) / fs

        window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, self.fft_window_size, False)))
        xf = np.fft.rfftfreq(self.fft_window_size, 1 / fs)
        self.frame_count = int(self.audio_length * self.fps)
        self.frame_offset = int(len(audio) / self.frame_count)

        energy_list = []
        notes_info = []
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

            current_note = None
            if frame_energy < avg_energy * 0.1:
                current_note = "pause"
            else:
                peaks, properties = scipy.signal.find_peaks(fft_magnitude, height=1500.00)
                valid_peaks = [peak for peak in peaks if 16.35 < xf[peak] < 7902.13]
            
                if len(valid_peaks) == 0:
                    current_note = "pause"
                else:
                    main_peak_index = np.argmax(properties['peak_heights'])
                    fundamental_freq = xf[valid_peaks[main_peak_index]]
                    fundamental_amplitude = properties['peak_heights'][main_peak_index]

                    dynamic_threshold = 0.05 * fundamental_amplitude
                    print(f"Frame {frame_number}: Fundamental frequency = {fundamental_freq}, Amplitude = {fundamental_amplitude}, Dynamic Threshold = {dynamic_threshold}")

                    close_harmonics = []
                    for peak in valid_peaks:
                        potential_harmonic_freq = xf[peak]

                        if fft_magnitude[peak] < dynamic_threshold:
                            continue
                        # close_harmonics.append(potential_harmonic_freq)

                        # if potential_harmonic_freq <= fundamental_freq:
                        #     continue

                        if fundamental_freq < potential_harmonic_freq:
                            deviation_from_harmony = potential_harmonic_freq / fundamental_freq - round(potential_harmonic_freq / fundamental_freq)
                            if abs(deviation_from_harmony) <= 0.05:
                                theoretical_harmonic = round(potential_harmonic_freq / fundamental_freq) * fundamental_freq
                                close_harmonics.append(theoretical_harmonic)
                        else:
                            deviation_from_harmony = fundamental_freq / potential_harmonic_freq - round(fundamental_freq / potential_harmonic_freq)
                            if abs(deviation_from_harmony) <= 0.03:
                                theoretical_harmonic = fundamental_freq / round(fundamental_freq / potential_harmonic_freq)
                                close_harmonics.append(theoretical_harmonic)
                        
                        # if potential_harmonic_freq < fundamental_freq:
                        #     deviation_from_harmony = fundamental_freq / potential_harmonic_freq - round(fundamental_freq / potential_harmonic_freq)
                        #     if abs(deviation_from_harmony) <= 0.05:
                        #         theoretical_harmonic = fundamental_freq / round(fundamental_freq / potential_harmonic_freq)
                        #         close_harmonics.append(theoretical_harmonic)
                            


                    # print(f"For {fundamental_freq} found possible harmonics {close_harmonics}")

                    print(f"After applying threshold, close harmonics for {fundamental_freq}: {close_harmonics}")


                    base_frequency = self.gcd(close_harmonics + [fundamental_freq])
                    print(f"Assuming base frequency {base_frequency}")

                    note_number = self.freq_to_number(base_frequency)
                    print(f"Note number {note_number}")
                    current_note = self.note_name(note_number)
                    print(f"Current note {current_note}")

            if notes and current_note == notes[-1].note:
                notes[-1].duration += self.fft_window_seconds
            else:
                notes.append(PlayedNote(note=current_note, duration=self.fft_window_seconds))

        for note in notes:
            notes_info.append({"note": note.note, "duration": note.duration})

        print('Notes for : ', os.path.basename(file_path), '\n', notes_info)

        converter = LilyPondConverter(notes_info)
        lilypond_file_name = os.path.splitext(file_path)[0] + ".ly"
        converter.write_to_file(lilypond_file_name)
        converter.run_lilypond(lilypond_file_name)