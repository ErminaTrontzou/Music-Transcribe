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
            'F4': 349.228,
            'G4': 391.995,
            'A4': 440.0,
            'B4': 493.883
        }

    def process(self, file):
        if file is None:
            print("File not found")
            return

        rate, data = wavfile.read(file)

        if data.ndim == 2: # this is a two channel / stereo file
            data = np.mean(data, axis=1)
        
        window_size = 2295 
        overlap = 256
        step = window_size - overlap

        # #Calculate the ideal size, currently for section 4 mostly for debugging and saving me some time
        # frequencies = [261.626 , 277.183 , 293.665, 311.127, 
        #     329.628, 349.228 , 369.994 , 391.995, 415.305]

        # distances = [frequencies[i+1] - frequencies[i] for i in range(len(frequencies)-1)]

        # average_distance = sum(distances) / len(distances)

        # sample_rate = 44100
        # ideal_window_size = int(sample_rate / average_distance)

        # print("Average distance between consecutive notes:", average_distance)
        # print("Ideal window size:", ideal_window_size)

        for i in range(0, len(data), step):
            window = data[i:i+window_size]
            window_hamming = np.hamming(window_size)
            window *= window_hamming

            #Perform fft on windowed data
            data_fft = rfft(window)
            frequencies = np.abs(data_fft)
            freq_bins = rfftfreq(len(window), 1.0/rate)
            print("freq_bins:", freq_bins) #understanding what an fft bin is

            # Remove the DC component for better visualization
            frequencies = frequencies[1:]
            freq_bins = freq_bins[1:]

            #Print fft frequencies mostly for debug and analyze reasons
            print("FFT frequencies:", frequencies)

            #Visualize windowed data and FFT
            plt.figure()
            plt.subplot(2, 1, 1)
            plt.plot(window)
            plt.title(f'Windowed Data - Window {i//step}')
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            plt.subplot(2, 1, 2)
            plt.plot(freq_bins, frequencies)
            plt.title(f'FFT of Window {i//step}')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.xscale('log')
            plt.show()

            #Find the frequency with the highest amplitude
            max_freq_index = np.argmax(frequencies)
            max_freq = freq_bins[max_freq_index]

            #Map the frequency to the closest note and print the closest note again mostly for debug reasons
            closest_note = self.frequency_to_note(max_freq)
            print(f"Closest note to max frequency in window {i//step}: {closest_note}")

    def frequency_to_note(self, frequency):
        closest_note = min(self.note_freqs.items(), key=lambda x: abs(x[1] - frequency))
        return closest_note[0]



