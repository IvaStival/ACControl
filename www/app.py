import requests
from flask import Flask, render_template
from manageData import ManageData

app = Flask(__name__)

url = "http://localhost:8000/api/v1/sensors/last_n/100"
result = requests.get(url)

manage_data = ManageData()
grouped_data = manage_data.grouped_data(raw=result)

@app.route('/', methods=['GET'])
def main():
    labels = [x[0] for x in grouped_data]
    sensor1_temperuture = [x[1] for x in grouped_data]
    sensor2_temperature = [x[2] for x in grouped_data]
    
    return render_template('index.html', template_labels=labels, 
                           template_sensor1_temperature=sensor1_temperuture,
                           template_sensor2_temperature=sensor2_temperature,
                           )

@app.route('/data_from_rest')
def get_data_from_rest():
    url = "http://localhost:8000/api/v1/sensors/last_n/100"
    result = requests.get(url)

    grouped_data = manage_data.grouped_data(raw=result)
    return grouped_data

if __name__ == '__main__':
    app.run(debug=True)