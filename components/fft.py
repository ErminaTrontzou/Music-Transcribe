import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import *

class FFT():
    def __init__(self):
        self.note_freqs = {
            'C4': 261.626,
            'D4': 293.665,
            'E4': 329.628,
        }

    def process(self, file):
        if file is None:
            print("File not found")
            return

        rate, data = wavfile.read(file)

        if data.ndim == 2:  # this is a two channel / stereo file
            data = np.mean(data, axis=1)


        # Calculate the time domain
        time_domain = np.linspace(0, len(data)/rate, len(data))

        plt.figure(1)
        plt.plot(time_domain, data)
        plt.title('Time Domain Signal')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')

        data_fft = rfft(data)
        frequencies = np.abs(data_fft)
        freq_bins = rfftfreq(len(data), 1.0/rate)

        plt.figure(2)
        plt.plot(freq_bins, frequencies)
        plt.title('FFT of Sound File')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')

        plt.show()
