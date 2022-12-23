import tkinter
from math import sin, radians


class MainFrame(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)

        self.app_pointer = master
        self.themeObj = self.app_pointer.themeObj
        self.size = 300

        self.configure(bg=self.themeObj.colorTheme['background_layer_1'])

        self.canvas_low = tkinter.Canvas(master=self,
                                           bg=self.themeObj.colorTheme['background_layer_1'],
                                           highlightthickness=0,
                                           height=self.size,
                                           width=self.size)

        self.canvas_low.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        self.circle_ui_big = self.canvas_low.create_line(  self.size * 0.2,
                                                                    20,
                                                                    self.size * 0.4,
                                                                    20,
                                                                  fill='red',
                                                                  width=25)

        self.circle_ui_big = self.canvas_low.create_line(  self.size * 0.6,
                                                                    20,
                                                                    self.size * 0.8,
                                                                    20,
                                                                  fill='red',
                                                                  width=25)                                                         
                                                                
        self.circle_ui_big = self.canvas_low.create_line(  self.size * 0.4,
                                                                    20,
                                                                    self.size * 0.48,
                                                                    20,
                                                                  fill='yellow',
                                                                  width=25)

        self.circle_ui_big = self.canvas_low.create_line(  self.size * 0.52,
                                                                    20,
                                                                    self.size * 0.6,
                                                                    20,
                                                                  fill='yellow',
                                                                  width=25)

        self.circle_ui_big = self.canvas_low.create_line(  self.size * 0.48,
                                                                    20,
                                                                    self.size * 0.52,
                                                                    20,
                                                                  fill='green',
                                                                  width=25)                                                         

        

        self.needle_width = 8
        self.display_needle = self.canvas_low.create_line(self.size * 0.5,
                                                            self.size * 0.5,
                                                            self.size * 0.5,
                                                            self.size * 0.05,
                                                            fill=self.themeObj.colorTheme['needle'],
                                                            width=self.needle_width,
                                                            capstyle=tkinter.ROUND)

        self.circle_ui_small = self.canvas_low.create_oval(self.size * 0.2,
                                                                    self.size * 0.2,
                                                                    self.size * 0.8,
                                                                    self.size * 0.8,
                                                                    fill='black',
                                                                    width=0)

        self.botton_frame = tkinter.Frame(master=self, bg=self.themeObj.colorTheme['background_layer_0'])
        self.botton_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)


        self.higher_note_text = self.canvas_low.create_text(self.size * 0.95, self.size * 0.1,
                                                              anchor=tkinter.E,
                                                              text="A#",
                                                              fill=self.themeObj.colorTheme['text_2'],
                                                              font=self.themeObj.typography['note_display_font_medium'])

        self.lower_note_text = self.canvas_low.create_text(self.size * 0.05, self.size * 0.1,
                                                             anchor=tkinter.W,
                                                             text="B#",
                                                             fill=self.themeObj.colorTheme['text_2'],
                                                             font=self.themeObj.typography['note_display_font_medium'])

        self.canvas_high = tkinter.Canvas(master=self.botton_frame,
                                           bg=self.themeObj.colorTheme['background_layer_0'],
                                           highlightthickness=0,
                                           height=self.size / 2,
                                           width=self.size)
        self.canvas_high.place(anchor=tkinter.N, relx=0.5, rely=0)

        self.display_inner_circle_2 = self.canvas_high.create_oval(self.size * 0.2,
                                                                    -self.size * 0.3,
                                                                    self.size * 0.8,
                                                                    self.size * 0.3,
                                                                    fill='black',
                                                                    width=0)

        self.note_label = tkinter.Label(master=self,
                                        text="A",
                                        bg='black',
                                        fg=self.themeObj.colorTheme['text_2'],
                                        font=self.themeObj.typography['note_display_font'])
        self.note_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.frequency_text = self.canvas_high.create_text(self.size * 0.5, self.size * 0.16,
                                                            anchor=tkinter.N,
                                                            text="- Hz",
                                                            fill=self.themeObj.colorTheme['text_2'],
                                                            font=self.themeObj.typography['frequency_text_font'])

        self.label_info_text = tkinter.Label(master=self,
                                             bg='grey',
                                             fg=self.rgb_to_hex((26, 51, 82)),
                                             font=("Avenir", 14),
                                             text="GUITAR TUNER - Final Project by Rishabh and Prakriti")
        self.label_info_text.place(anchor=tkinter.CENTER, relx=0.5, rely=0.12, relheight=0.1, relwidth=0.8)                                                   

    def set_needle_color(self, color):
        if color == "green":
            self.canvas_low.itemconfig(self.display_needle, fill=self.themeObj.colorTheme['needle_hit'])
            self.note_label.configure(fg=self.themeObj.colorTheme['text_2_highlight'], font=self.themeObj.typography['note_display_font'])
        elif color == "yellow":
            self.canvas_low.itemconfig(self.display_needle, fill="yellow")
            self.note_label.configure(fg=self.themeObj.colorTheme['text_2'], font=self.themeObj.typography['note_display_font'])
        elif color == "red":
            self.canvas_low.itemconfig(self.display_needle, fill=self.themeObj.colorTheme['needle'])
            self.note_label.configure(fg=self.themeObj.colorTheme['text_2'], font=self.themeObj.typography['note_display_font'])

    def set_needle_angle(self, deg):
        x = sin(radians(180 - deg))
        y = sin(radians(270 - deg))

        self.canvas_low.coords(self.display_needle,
                                 self.size * 0.5,
                                 self.size * 0.5,
                                 self.size * 0.5 + (self.size * 0.45 * x),
                                 self.size * 0.5 + (self.size * 0.45 * y))
        return x, y

    def set_note_names(self, note_name, note_name_lower, note_name_higher):
        self.note_label.configure(text=note_name, width=3)
        self.canvas_low.itemconfig(self.higher_note_text, text=note_name_higher)
        self.canvas_low.itemconfig(self.lower_note_text, text=note_name_lower)

    def set_frequency(self, frequency):
        self.canvas_high.itemconfig(self.frequency_text, text=str(round(frequency, 1)) + " Hz")

    @staticmethod
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb
