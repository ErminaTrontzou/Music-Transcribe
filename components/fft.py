import numpy as np
import scipy.fftpack as fft
import scipy.io.wavfile as wavfile
import scipy.signal  # Import the entire scipy.signal module
import os

class FFT:
    def __init__(self, fps=5, fft_window_seconds=0.25, freq_min=10, freq_max=1000):
        """
        :param fps: Frames per second for the audio playback speed.
        :param fft_window_seconds: Duration of the FFT window in seconds.
        :param freq_min: Minimum frequency of interest in Hz.
        :param freq_max: Maximum frequency of interest in Hz.

        """
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

    def freq_to_number(self, f):
        """
        Convert a frequency in Hz to its equivalent note number.
        
        :param f: Frequency in Hz.
        :return: note number corresponding to the given frequency.

        """
        return round(69 + 12 * np.log2(f / 440.0))
    
    def number_to_freq(self, n):
        """
        Convert a note number to its equivalent frequency in Hz.
        
        :param n: note number.
        :return: Frequency in Hz corresponding to the given note number.

        """
        return 440 * 2.0 ** ((n - 69) / 12.0)

    def note_name(self, n):
        """
        Convert a note number to its corresponding musical note name.
        
        :param n: note number.
        :return: Musical note name (e.g., "C", "D#", "F#", etc.) followed by octave number.

        """
        n = int(n)
        return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][n % 12] + str(int(n // 12 - 1))

    def extract_sample(self, audio, frame_number):
        """
        This method calculates the start and end indices of the sample to be extracted based on the current frame number and the size of the FFT window.
        
        :param audio: Audio data as a NumPy array.
        :param frame_number: Index of the frame to center the sample extraction around.
        :return: Sample of audio data extracted around the given frame number.

        """
        end = frame_number * self.frame_offset
        begin = int(end - self.fft_window_size)

        # If the end index is 0, it means we're trying to extract a sample from the very beginning of the audio.
        if end == 0:
            return np.zeros((np.abs(begin)), dtype=float)
        # If the beginning index is negative, it indicates the sample extends beyond the start of the audio.
        elif begin < 0:
            return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
        else:
            # Otherwise, we simply slice the audio data from the beginning index to the end index.
            return audio[begin:end]

    def process_audio_file(self, file_path):
        """
        This method reads the audio file, sets up the parameters for the FFT analysis, and iterates over each frame of the audio data.
        For each frame, it extracts a sample, performs the FFT on that sample, identifies peaks in the FFT result that likely correspond to musical notes,
        converts those frequencies to note numbers, and appends the note names and frequencies to a list for later output.  

        :param file_path: Path to the audio file to process.

        """
        fs, data = wavfile.read(file_path)
        
        if len(data.shape) == 1:
            audio = data
        else:
            audio = data.T[0] 
        
        self.frame_step = (fs / self.fps)
        self.fft_window_size = int(fs * self.fft_window_seconds)
        self.audio_length = len(audio) / fs

        # Generate a window function for the FFT to reduce spectral leakage.
        window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, self.fft_window_size, False)))

        # Calculate the frequencies corresponding to the FFT window.
        xf = np.fft.rfftfreq(self.fft_window_size, 1 / fs)
        self.frame_count = int(self.audio_length * self.fps)
        self.frame_offset = int(len(audio) / self.frame_count)

        self.final_notes_array = []

        for frame_number in range(self.frame_count):
            sample = self.extract_sample(audio, frame_number)
            fft_result = np.fft.rfft(sample * window)
            fft_magnitude = np.abs(fft_result).real

            # Detect peaks in the FFT magnitude that likely correspond to musical notes.
            # Peaks are identified based on a minimum height threshold and a minimum distance between peaks.
            peaks, _ = scipy.signal.find_peaks(fft_magnitude, height=1500.00, distance=int(self.fft_window_size // 4))


            # Filter out frequencies below 16.35 Hz or above 7902.13 Hz
            valid_peaks = [peak for peak in peaks if 16.35 < xf[peak] < 7902.13]

            # For each detected peak, convert the frequency to a note number and append the note name and frequency to the final list,
            # but only if the frequency passes the filter.
            for peak in valid_peaks:
                freq = xf[peak]
                note = self.freq_to_number(freq)
                if note is not None:
                    note_name = self.note_name(note)
                    self.final_notes_array.append((note_name, freq))

        print("\n\nProcessing file: ", os.path.basename(file_path), "   (c  d  e  f  g  a  b  )")
        print("Recognized notes:", self.final_notes_array, "\n\n")
