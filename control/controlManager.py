import threading

from .sensorsControl import sensorControl
from .screenControl import screenControl
from .securityControl import securityControl
from sensors.temperature.controlDHT22 import controlDHT22


class controlManager:
    def __init__(self):
        self.sensors_control = sensorControl()
        self.screen_control = screenControl()
        self.security_control = securityControl()

    def run(self):
        
        sensor_thread = threading.Thread(target=self.sensors_control.run)
        screen_thread = threading.Thread(target=self.screen_control.run)
        security_thread = threading.Thread(target=self.security_control.run)

        print("Starting Threads ...")

        sensor_thread.start()
        screen_thread.start()
        security_thread.start()

        # while True:
        #     key = input("Press 'q' to exit")
        #     if key == 'q':
        #         sensor_thread.set()
        #         screen_thread.set()
        #         security_thread.set()
        #         break

        # self.sensors_control.run()
        # self.screen_control.run()
        # self.lcd_control.write([f"T1:{t1}"], [f"H1:{h1}"])

        # TIME OUT
        # time.sleep(60*self.minutes_between_reads)
