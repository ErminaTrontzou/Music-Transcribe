import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np

#Global Variables
FPB = 3200 #Frames per Buffer: number of data points processed (recorder and captured) in each buffer (second)
CHANNELS = 1 #Number of channels in the audio file (1 for mono, 2 for stereo)
RATE = 44100 #Sample rate of the audio file in Hz (44.1 kHz) or samples per second
FORMAT = pyaudio.paInt16 #Format of the audio file (16-bit signed integer) or bytes per sample (2 bytes per sample)

#44.1 sample rate and 32 buffer size are the typical values for audio recording from a microphone.



class Recorder(object):

    def __init__(self, channels=CHANNELS, rate=RATE, frames_per_buffer=FPB):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)
    

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.p = pyaudio.PyAudio()
        self.wavefile = self.prepare_file(self.fname, self.mode)
        self.stream = None

    def start_recording(self):
        #Stream with a callback in non-blocking mode
        self.stream = self.p.open(format=FORMAT,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self.stream.start_stream()
        return self

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return self.fname

    def apply_auto_amplification(audio):
        print(f"Audio Min: {audio.min()}, Max: {audio.max()}")
        print(f"Ideal Audio Min: {(-32767/audio.min())*audio.min()}, Ideal Audio Max: {+32767/audio.max()}")
        if(np.abs(audio.min())>np.abs(audio.max())):
            audio = (audio/audio.min())*32767
        else:
            audio = (audio/audio.max())*32767
        
        print(f"Audiooooo {audio}")

        # print(audio)
        # for i in range(1, len(audio)):
        #     print(f" {audio[i]}")

    #Returns a callback function that writes the input data to a wave file.
    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.p.get_sample_size(FORMAT))
        wavefile.setframerate(self.rate)
        return wavefile
    
    def read_wave_file(self):
        wave_file = wave.open(self.fname, 'rb')
        #-1 indicates to read all frames from the file
        signal = wave_file.readframes(-1)
        # Convert the bytes to numpy array of int16
        signal = np.frombuffer(signal, dtype=np.int16)
        return signal

    def plot_waveform(self):
        signal = self.read_wave_file()
        # Create a time array for the x-axis of the plot. 
        # The length of the time array is the same as that of the signal array.
        time = np.linspace(0., len(signal) / self.rate, len(signal))
        plt.figure(figsize=(15, 5))
        plt.ylabel('Signal Wave')
        plt.xlabel('Time (s)')
        plt.plot(time, signal, lw=0.5)
        plt.show()
