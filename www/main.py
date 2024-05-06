from manageData import ManageData
import requests
import datetime
if __name__ == "__main__":
    url = "http://192.168.1.8:8000/api/v1/sensors/last_n/500"

    result = requests.get(url)

    manage_data = ManageData(result)
    grouped_data = manage_data.grouped_data()

    print(grouped_data)
