import darkdetect
import sys


class themeObj(object):
    def __init__(self):
        self.colorTheme = {
            'background_layer_1' : 'grey',
            'background_layer_0' : 'grey',
            'text_main' : self.rgb_to_hex((255, 255, 255)),
            'text_2' : self.rgb_to_hex((10, 200, 100)),
            'text_2_highlight' : self.rgb_to_hex((240, 240, 240)),
            'theme_main' : self.rgb_to_hex((51, 94, 145)),
            'theme_dark' : self.rgb_to_hex((26, 51, 82)),
            'theme_light' : self.rgb_to_hex((85, 140, 200)),
            'needle' : self.rgb_to_hex((0,0,0)),
            'needle_hit' : self.rgb_to_hex((43, 113, 53))
        }

        self.typography = {
            'button_font' : ("Avenir", 16),
            'note_display_font' : ("Avenir", 72),  # main note Text
            'note_display_font_medium' : ("Avenir", 26),  # text on left and right site
            'frequency_text_font' : ("Avenir", 15),
            'info_text_font' : ("Avenir", 14),
            'settings_text_font' : ("Avenir", 24)
        }
        

    @staticmethod
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb
