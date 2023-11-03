import Adafruit_DHT

# CLASS CONTROL
# class controlDHT22:
#     def __init__(self, port, unit, name, debug=False) -> None:
#         self.port = port
#         self.metric = unit
#         self.name = name
#         self.debug = debug

#     def run(self):
#         result = {}
#         humidity, temp_c = Adafruit_DHT.read_retry(
#             Adafruit_DHT.DHT22, self.port)

#         result['humidity'] = humidity

#         if (self.metric):
#             if self.debug:
#                 print(f"[TEMPERATURE]{self.name} Temperature(C):{temp_c} Humidity:{humidity}")

#             result['temperature'] = temp_c

#         else:
#             if self.debug:
#                 print(temp_f)

#             temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
#             result['temperature'] = temp_f

#         result["name"] = self.name

#         return result


# import Adafruit_DHT
import adafruit_dht
import time

import utils.ACBoard as ACBoard

STATUS_OK = 1
STATUS_SENSOR_ERR = -1

# CLASS CONTROL
class controlDHT22:
    def __init__(self, port, unit, name, debug=False) -> None:
        self.port = port
        self.metric = unit
        self.name = name
        self.debug = debug

        board_port = ACBoard.getBoard(str(port))

        self.dhtDevice = adafruit_dht.DHT22(board_port)

    def run(self):
        result = {}
        
        while True:
            try:
                # humidity, temp_c = Adafruit_DHT.read_retry(
                #     Adafruit_DHT.DHT22, self.port)
                temp_c = self.dhtDevice.temperature
                humidity = self.dhtDevice.humidity
                result['humidity'] = humidity

                if (self.metric):
                    if self.debug:
                        print(f"[TEMPERATURE]{self.name} Temperature(C):{temp_c} Humidity:{humidity}")

                    result['temperature'] = temp_c

                else:
                    if self.debug:
                        print(temp_f)

                    temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
                    result['temperature'] = temp_f

                result["name"] = self.name
                if self.debug:
                    print(result)
                
                break
            except RuntimeError as error:
                if self.debug:
                    print(error)
                
                if(str(error) == "DHT sensor not found, check wiring"):
                    result['temperature'] = None
                    result['humidity'] = None
                    result["name"] = self.name
                    break

                elif("Try again" in str(error)):
                    pass
                
            time.sleep(2.0)
                
        return result
