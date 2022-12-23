import tkinter
import tkinter.messagebox
import os
import sys
import json
import requests
import webbrowser
import time
import random

from display.main_frame import MainFrame
from audio_files.input_handler import inputHandler
from audio_files.play_thread import threadPlayer

from theme.theme_manager import themeObj


class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):

        tkinter.Tk.__init__(self, *args, **kwargs)

        self.main_path = os.path.dirname(os.path.abspath(__file__))

        self.NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

        self.themeObj = themeObj()
        self.frequency_queue = []

        self.main_frame = MainFrame(self)

        self.handleInput = inputHandler(self.frequency_queue)
        self.handleInput.start()

        self.play_sound_thread = threadPlayer(self.main_path + "/assets/sounds/drop.wav")
        self.play_sound_thread.start()

        self.needle_buffer_array = [0 for _ in range(20)]
        self.tone_hit_counter = 0
        self.note_number_counter = 0
        self.nearest_note_number_buffered = 81


        self.title("Tuner Master")
        self.geometry(str(500) + "x" + str(500))
        self.resizable(True, True)
        self.minsize(500, 500)
        self.maxsize(650, 650)
        self.configure(background=self.themeObj.colorTheme['background_layer_1'])

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.draw_main_frame()

        self.open_app_time = time.time()

    def get_note_from_array(self, number):
        # Find the note from NOTES array given the note number relative to A0

        return self.NOTES[int(round(number) % 12.0)]

    def draw_main_frame(self, event=0):
        self.main_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    def on_closing(self, event=0):
        self.handleInput.is_running = False
        self.play_sound_thread.is_running = False
        self.destroy()

    def start(self):
        while self.handleInput.is_running:

            try:

                # get the current frequency from the queue
                freq = None
                if len(self.frequency_queue) != 0:
                    freq = self.frequency_queue[0]
                    del self.frequency_queue[0]

                if freq is not None:

                    # convert frequency to note number
                    number = self.handleInput.freq_to_num(freq)

                    # calculate nearest note number, name and frequency
                    nearest_note_number = round(number)
                    nearest_note_freq = 880 * 2.0**((round(number) - 81) / 12.0)

                    # calculate frequency difference from freq to nearest note
                    freq_difference = nearest_note_freq - freq

                    # calculate the frequency difference to the next note (-1)
                    semitone_step = nearest_note_freq - 880 * 2.0**((round(number-1) - 81) / 12.0)

                    # calculate the angle of the display needle
                    needle_angle = -45 * ((freq_difference / semitone_step) * 2)
                    # buffer the current nearest note number change
                    if nearest_note_number != self.nearest_note_number_buffered:
                        self.note_number_counter += 1
                        if self.note_number_counter >= 20:
                            self.nearest_note_number_buffered = nearest_note_number
                            self.note_number_counter = 0

                    # if needle in range +-3 degrees then make it green, otherwise red
                    if abs(freq_difference) < 0.15:
                        self.main_frame.set_needle_color("green")
                        self.tone_hit_counter += 1
                    elif abs(freq_difference) < 0.3:
                        self.main_frame.set_needle_color("yellow")
                    else:
                        self.main_frame.set_needle_color("red")
                        self.tone_hit_counter = 0

                    # Check for 3 consecutive hits before playing the sound
                    if self.tone_hit_counter > 3:
                        self.tone_hit_counter = 0

                        self.play_sound_thread.play_sound()
                        
                    # update needle buffer array
                    self.needle_buffer_array[:-1] = self.needle_buffer_array[1:]
                    self.needle_buffer_array[-1] = needle_angle

                    # update ui components
                    self.main_frame.set_needle_angle(sum(self.needle_buffer_array)/len(self.needle_buffer_array))
                    self.main_frame.set_note_names(note_name=self.get_note_from_array(self.nearest_note_number_buffered),
                                                   note_name_lower=self.get_note_from_array(self.nearest_note_number_buffered - 1),
                                                   note_name_higher=self.get_note_from_array(self.nearest_note_number_buffered + 1))

                    # set current frequency
                    if freq is not None: self.main_frame.set_frequency(freq)

                self.update()
                
            except IOError as err:
                sys.stderr.write('Error: Line {} {} {}\n'.format(sys.exc_info()[-1].tb_lineno, type(err).__name__, err))
                self.update()
                


if __name__ == "__main__":
    app = App()
    app.start()
