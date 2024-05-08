import requests
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pytz


def collect_data():
    url = 'http://innov8dev.com/sampleapi/getdata.php'
    log_file = 'sensor_data.log'

    for _ in range(300):
        response = requests.get(url)
        data = response.json()

        timestamp = data['timestamp']
        mst_time = datetime.fromtimestamp(timestamp, pytz.timezone('MST'))
        data['timestamp'] = mst_time.strftime('%Y-%m-%d %H:%M:%S')

        with open(log_file, 'a') as file:
            file.write(json.dumps(data) + '\n')

        time.sleep(2)


def plot_data():
    with open('sensor_data.log', 'r') as file:
        lines = file.readlines()

    timestamps = []
    temperatures = []
    rains = []

    for line in lines:
        data = json.loads(line)
        timestamps.append(data['timestamp'])
        temperatures.append(data['temperature'])
        rains.append(data['rain'])

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature', color='tab:red')
    ax1.plot(timestamps, temperatures, 'r-')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Rain', color='tab:blue')
    ax2.plot(timestamps, rains, 'b-')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.title('Temperature and Rain Data Over Time')
    plt.savefig('temperature_and_rain_chart.jpg')
    plt.show()


if __name__ == "__main__":
    collect_data()
    plot_data()
