from threading import Thread
import pyaudio
import wave
import time


class threadPlayer(Thread):
    # Plays the audio file passed as argument when play_sound() is called

    def __init__(self, path_to_file):
        Thread.__init__(self)

        self.playing = False
        self.blockSize = 1024
        
        self.audio_file_data = []
        self.audio_file = wave.open(path_to_file, "rb")
        

        # load the audio file into audio_file_data array
        while True:
            data = self.audio_file.readframes(self.blockSize)
            if data != b'':
                self.audio_file_data.append(data)
            else:
                break
        
        self.audioObj = pyaudio.PyAudio()

        audio_format = self.audioObj.get_format_from_width(self.audio_file.getsampwidth())
        self.audio_stream = self.audioObj.open(format=audio_format,                                                    
                                                      rate=self.audio_file.getframerate(),
                                                      channels=self.audio_file.getnchannels(),
                                                      input=False,
                                                      output=True)
        self.play_sound_now = False
        self.audio_file.close()
    
    #this function is to indicate the program to play the ticking sound
    def play_sound(self):
        self.play_sound_now = True

    def run(self):
        self.playing = True
        while self.playing:

            if self.play_sound_now is True:
                for curr_audio_chunk in self.audio_file_data:
                    self.audio_stream.write(curr_audio_chunk)

                self.play_sound_now = False
                time.sleep(1)
            else:
                time.sleep(0.2)
        
        self.audioObj.terminate()
        self.audio_stream.stop_stream()
        self.audio_stream.close()