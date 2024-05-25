import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import *

class FFT():
    def __init__(self):
        
        self.note_freqs = {
            'A0': 27.500,'A#0/Bb0': 29.135,'B0': 30.868,

            'C1': 32.703,'C#1/Db1': 34.648,'D1': 36.708,'D#1/Eb1': 38.891,
            'E1': 41.203,'F1': 43.654,'F#1/Gb1': 46.249,'G1': 48.999,
            'G#1/Ab1': 51.913,'A1': 55.000,'A#1/Bb1': 58.270,'B1': 61.735,

            'C2': 65.406,'C#2/Db2': 69.296,'D2': 73.416,'D#2/Eb2': 77.782,
            'E2': 82.407,'F2': 87.307,'F#2/Gb2': 92.499,'G2': 97.999,
            'G#2/Ab2': 103.826,'A2': 110.000,'A#2/Bb2': 116.541,'B2': 123.471,

            'C3': 130.813,'C#3/Db3': 138.591,'D3': 146.832,'D#3/Eb3': 155.563,
            'E3': 164.814,'F3': 174.614,'F#3/Gb3': 184.997,'G3': 195.998,
            'G#3/Ab3': 207.652,'A3': 220.000,'A#3/Bb3': 233.082,'B3': 246.942,

            'C4': 261.626,'C#4/Db4': 277.183,'D4': 293.665,'D#4/Eb4': 311.127,
            'E4': 329.628,'F4': 349.228,'F#4/Gb4': 369.994,'G4': 391.995,
            'G#4/Ab4': 415.305,'A4': 440.000,'A#4/Bb4': 466.164,'B4': 493.883,

            'C5': 523.251,'C#5/Db5': 554.365,'D5': 587.330,'D#5/Eb5': 622.254,
            'E5': 659.255,'F5': 698.456,'F#5/Gb5': 739.989,'G5': 783.991,
            'G#5/Ab5': 830.609,'A5': 880.000,'A#5/Bb5': 932.328,'B5': 987.767,

            'C6': 1046.502,'C#6/Db6': 1108.731,'D6': 1174.659,'D#6/Eb6': 1244.508,
            'E6': 1318.510,'F6': 1396.913,'F#6/Gb6': 1479.978,'G6': 1567.982,
            'G#6/Ab6': 1661.219,'A6': 1760.000,'A#6/Bb6': 1864.655,'B6': 1975.533,
            
            'C7': 2093.005,'C#7/Db7': 2217.461,'D7': 2349.318,'D#7/Eb7': 2489.016,
            'E7': 2637.020,'F7': 2793.826,'F#7/Gb7': 2959.955,'G7': 3135.963,
            'G#7/Ab7': 3322.438,'A7': 3520.000,'A#7/Bb7': 3729.310,'B7': 3951.066,
            
            'C8': 4186.009,'C#8/Db8': 4434.922,'D8': 4698.636,'D#8/Eb8': 4978.032,
            'E8': 5274.041,'F8': 5587.652,'F#8/Gb8': 5919.911,'G8': 6271.927,
            'G#8/Ab8': 6644.875,'A8': 7040.000,'A#8/Bb8': 7458.620, 'B8': 7902.133
        }
        self.closest_notes_with_times = [] 

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
            if len(window)!= window_size: 
                print("End of file") # Check if we're at the end of the file
                break
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

            #Find the frequency with the highest amplitude
            max_freq_index = np.argmax(frequencies)
            max_freq = freq_bins[max_freq_index]

            #Map the frequency to the closest note and print the closest note again mostly for debug reasons
            closest_note = self.frequency_to_note(max_freq)
            time_in_seconds = i / rate  #Calculate the time in seconds for the note at the current window
            self.closest_notes_with_times.append((closest_note, time_in_seconds))
            # print(f"Closest note to max frequency in window {i//step}: {closest_note}")
            # print("Predicted closest notes array with times: ", self.closest_notes_with_times)

            # #Visualize windowed data and FFT
            # fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(12, 8))

            # #Plot windowed data on the first subplot
            # ax1.plot(window)
            # ax1.set_title(f'Windowed Audio Data of Note {closest_note} - Window {i//step}')
            # ax1.set_xlabel('Sample')
            # ax1.set_ylabel('Amplitude')

            # #Plot FFT on the second subplot
            # ax2.plot(freq_bins, frequencies)
            # ax2.set_title(f'FFT of Window')
            # ax2.set_xlabel('Frequency (Hz)')
            # ax2.set_ylabel('Amplitude')
            # ax2.set_xscale('log')

            # plt.tight_layout()  
            # plt.show(block=False)
            # plt.pause(0.2)
            # plt.close(fig) 

        final_notes_array = self.aggregate_notes()
        print("Final notes array: ", final_notes_array)	



    def frequency_to_note(self, frequency):
        closest_note = min(self.note_freqs.items(), key=lambda x: abs(x[1] - frequency))
        return closest_note[0]

    def aggregate_notes(self):
            final_notes_array = []
            last_occurrence = {}

            for note, time in self.closest_notes_with_times:
                if note not in last_occurrence:
                    last_occurrence[note] = time
                    final_notes_array.append((note, time))
                else:
                    last_occurrence[note] += time
            
            for i, (_, time) in enumerate(final_notes_array):
                final_notes_array[i] = (final_notes_array[i][0], last_occurrence[final_notes_array[i][0]])

            return final_notes_array

