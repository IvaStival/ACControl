import Adafruit_DHT


class controlDHT22:
    def __init__(self, port, unit, name, debug=False) -> None:
        self.port = port
        self.metric = unit
        self.name = name
        self.debug = debug

    def run(self):
        result = {}
        humidity, temp_c = Adafruit_DHT.read_retry(
            Adafruit_DHT.DHT11, self.port)

        result['humidity'] = humidity

        if (self.metric):
            if self.debug:
                print(self.name + " Temperature(C)", temp_c)
                print(self.name + " Humidity", humidity)

            result['temperature'] = temp_c

        else:
            if self.debug:
                print(temp_f)

            temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
            result['temperature'] = temp_f

        return result
