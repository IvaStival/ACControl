# # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# # SPDX-License-Identifier: MIT

# import time
# import board
# import adafruit_dht

# # Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D4)

# # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# # This may be necessary on a Linux single board computer like the Raspberry Pi,
# # but it will not work in CircuitPython.
# # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
# print(board.D4)

# while True:
#     try:
#         # Print the values to the serial port
#         temperature_c = dhtDevice.temperature
#         temperature_f = temperature_c * (9 / 5) + 32
#         humidity = dhtDevice.humidity
#         print(
#             "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
#                 temperature_f, temperature_c, humidity
#             )
#         )


#     except RuntimeError as error:
#         # Errors happen fairly often, DHT's are hard to read, just keep going
#         print(error)
#         time.sleep(2.0)
#         continue
#     except Exception as error:
#         dhtDevice.exit()
#         raise error

#     time.sleep(2.0)

import time
import board
import adafruit_dht
import adafruit_character_lcd.character_lcd as characterlcd
import digitalio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dhtDevice = adafruit_dht.DHT22("D4")


# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D11)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D13)
# lcd_backlight = digitalio.DigitalInOut(board.D4)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

while True:
    try:
        dhtDevice.measure()
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        lcd.message = ("Temp: {:.1f} C \nHumidity: {}% ".format(
                           temperature_c, temperature_f, humidity
                       )
                   )
        print(humidity)
        time.sleep(1.0)
    except RuntimeError as error:
        
        if(str(error) == "DHT sensor not found, check wiring"):
            print("I cant read the sensor")
            time.sleep(1.0)
        
        if("Try again" in str(error)):
            print(error)
            time.sleep(2.0)
            pass

    