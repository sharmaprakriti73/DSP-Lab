import numpy as np
import copy
from pyaudio import PyAudio, paInt16
import sys
from threading import Thread


class inputHandler(Thread):
    #This class reads data from the microphone and finds the frequency of the loudest tone

    NUM_HPS = 3  
    BLOCK = 1024

    rate = 48000    
    buffer_len = 50  

    def __init__(self, queue, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

        self.queue = queue  
        self.buffer = np.zeros(self.BLOCK * self.buffer_len)
        self.is_running = False

        try:
            self.audio_object = PyAudio()
            self.stream = self.audio_object.open(format=paInt16,
                                                 rate=self.rate,
                                                 input=True,
                                                 output=False,
                                                 channels=1,
                                                 frames_per_buffer=self.BLOCK)
        except Exception as e:
            sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
            return

    @staticmethod
    def freq_to_num(freq):
        """ converts the read frequency to a note number (eg: 880 is 81)"""

        if freq == 0:
            sys.stderr.write("Error: No frequency data found.\n")
            return 0

        return 12 * np.log2(freq / 880) + 81

    def run(self):

        self.is_running = True

        while self.is_running:
            try:
               
                # Read data from stream and buffer
                data = self.stream.read(self.BLOCK, exception_on_overflow=False) 
                data = np.frombuffer(data, dtype=np.int16)

                # append data to the audio buffer
                self.buffer[:-self.BLOCK] = self.buffer[self.BLOCK:]
                self.buffer[-self.BLOCK:] = data

                # apply fourier transformation on the entire buffer (along with padding and the hanning window)

                #zero-padding = 3 in this case
                magnitude_data = abs(np.fft.fft(np.pad(self.buffer * np.hanning(len(self.buffer)),
                                                       (0, len(self.buffer) * 3),
                                                       "constant")))

                # this part is to only use the first half of the fft output
                magnitude_data = magnitude_data[:int(len(magnitude_data) * 0.5)]

                # HPS: multiply data by itself with different scalings (Harmonic Product Spectrum)
                magnitude_data_orig = copy.deepcopy(magnitude_data)

                for num_hps in range(2, self.NUM_HPS+1, 1):
                    hps_length = int(np.ceil(len(magnitude_data) / num_hps))
                    magnitude_data[:hps_length] *= magnitude_data_orig[::num_hps]  # multiply every element

                # get the corresponding frequency array
                frequencies = np.fft.fftfreq(int((len(magnitude_data) * 2) / 1),
                                             1. / self.rate)

                # Implementing high-pass filter ( only frequencies above 60hz )
                for curr, freq in enumerate(frequencies):
                    if freq > 60:
                        magnitude_data[:curr - 1] = 0
                        break

                # calculate and put the frequency of the loudest tone into the queue
                self.queue.append(round(frequencies[np.argmax(magnitude_data)], 2))
                if len(self.queue) > 10:
                    self.queue.pop(0)

            except Exception as e:
                print(e)
        
        self.stream.close()
        self.stream.stop_stream()
        self.audio_object.terminate()