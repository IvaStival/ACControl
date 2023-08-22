from time import sleep
from RPLCD import CharLCD
import RPi.GPIO as GPIO


class controlLCD:
    def __init__(self, m_pin_rs, m_pin_e, m_pins_data):
        self.lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2,
                           pin_rs=m_pin_rs, pin_e=m_pin_e, pins_data=m_pins_data)

        self.lcd.write_string(u"ACControl Ready")

    # WE MUST PASS THE STRINGS INSIDE A LIST: ["T1:20", "T2:10"]
    def write(self, content_line1=None, content_line2=None):
        self.clear()
        if (content_line1):
            for word in content_line1:
                self.lcd.write_string(word)
                self.lcd.cursor_pos = (0, len(word)+1)
                sleep(0.5)

        if (content_line2):
            self.lcd.cursor_pos = (1, 0)
            for word in content_line2:
                self.lcd.write_string(word)
                self.lcd.cursor_pos = (1, len(word)+1)
                sleep(0.5)

    def clear(self):
        self.lcd.clear()

    def set_cursor_position(self, row, col):
        self.lcd.cursor_pos = (row, col)
