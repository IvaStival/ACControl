from time import sleep
from RPLCD import i2c
import RPi.GPIO as GPIO


class controlLCD:
    def __init__(self, address, port, charmap, cols, rows, i2c_expander):
        self.lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

        self.lcd.clear()
        self.lcd.backlight_enabled = True 
        sleep(1)
        self.lcd.backlight_enabled = True 
        self.lcd.write_string(u"ACControl Ready")

    # WE MUST PASS THE STRINGS INSIDE A LIST: ["T1:20", "T2:10"]
    def write(self, content_line1=None, content_line2=None):
        self.lcd.clear()

        if (content_line1):
            for word in content_line1:
                self.lcd.write_string(word)
                self.lcd.cursor_pos = (0, len(word)+1)

        if (content_line2):
            self.lcd.cursor_pos = (1, 0)
            for word in content_line2:
                self.lcd.write_string(word)
                self.lcd.cursor_pos = (1, len(word)+1)

    def clear(self):
        self.lcd.close(clear=True)

    def set_cursor_position(self, row, col):
        self.lcd.cursor_pos = (row, col)
