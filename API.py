from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('sensor_data.log', 'r') as file:
        data = [json.loads(line) for line in file.readlines()]
    return data

def get_temperature_at(timestamp, data):
    for entry in data:
        if entry['timestamp'] == timestamp:
            return entry['temperature']
    return "No data for given timestamp"

def calculate_rain_percentage(start_time, end_time, data):
    total_count = 0
    rain_count = 0
    for entry in data:
        if start_time <= entry['timestamp'] <= end_time:
            total_count += 1
            if entry['rain']:
                rain_count += 1
    if total_count > 0:
        return (rain_count / total_count) * 100
    else:
        return "No data in the given range"

@app.route('/temperature', methods=['GET'])
def temperature():
    timestamp = request.args.get('timestamp')
    data = load_data()
    temperature = get_temperature_at(timestamp, data)
    return jsonify({'temperature': temperature})

@app.route('/rain_percentage', methods=['GET'])
def rain_percentage():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    data = load_data()
    percentage = calculate_rain_percentage(start_time, end_time, data)
    return jsonify({'rain_percentage': percentage})

if __name__ == '__main__':
    app.run(debug=True)
