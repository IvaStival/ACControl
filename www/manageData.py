from datetime import datetime

class ManageData():
    def __init__(self):
        pass

    @staticmethod
    def grouped_data(raw):
        # grouped = list(map(lambda n : datetime.strptime(n["created_at"], '%Y-%m-%dT%H:%M:%SZ').time().strftime("%H:%M:%S"), self.raw.json()["data"]))
        result_list = []
        for data in raw.json()["data"]:
            time = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%SZ').time().strftime("%H:%M:%S")
            t1 = float(data["t1"]) if data["t1"] else 0
            t2 = float(data["t2"]) if data["t2"] else 0
            result_list.append((time, t1, t2))
        return result_list
    
    @staticmethod
    def temperature_data(raw):
        sensor1_temp = list(map(lambda n : float(n["t1"]) if n["t1"] else 0, raw.json()["data"]))
        sensor2_temp = list(map(lambda n : float(n["t2"]) if n["t2"] else 0, raw.json()["data"]))

        return {"sensor1": sensor1_temp, "sensor2": sensor2_temp}
    @staticmethod
    def humidity_data(raw):
        sensor1_temp = list(map(lambda n : float(n["h1"]) if n["h1"] else 0, raw.json()["data"]))
        sensor2_temp = list(map(lambda n : float(n["h2"]) if n["h1"] else 0, raw.json()["data"]))

        return {"sensor1": sensor1_temp, "sensor2": sensor2_temp}