import time
import yaml

from sensors.temperature.controlDHT22 import controlDHT22


def controlManager():

    with open('./config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    serve_name = config["SERVER"]["SENSOR_LOCATION_NAME"]
    debug = config["SERVER"]["DEBUG"]

    temperature_server_name = config["TEMPERATURE_SERVER"]['NAME']
    minutes_between_reads = config["TEMPERATURE_SERVER"]["MINUTES_BETWEEN_READS"]
    unit_type = config["TEMPERATURE_SERVER"]["METRICS_UNIT"]

    dh22_01_name = config["TEMPERATURE_SENSOR_01"]["NAME"]
    dh22_02_name = config["TEMPERATURE_SENSOR_02"]["NAME"]

    dh22_01_port = config["TEMPERATURE_SENSOR_01"]["PORT"]
    dh22_02_port = config["TEMPERATURE_SENSOR_02"]["PORT"]

    sensor_DHT22_01 = controlDHT22(
        dh22_01_port, unit_type, dh22_01_name, debug)

    if (debug):
        print(serve_name)

    result = {}
    while True:
        if (debug):
            print(temperature_server_name)

        result[dh22_01_name] = sensor_DHT22_01.run()
        print(result)
        print(60*minutes_between_reads)
        time.sleep(60*minutes_between_reads)
