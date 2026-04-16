#!/usr/bin/env python3
"""
QNI SmartCampus IoT Sensor Simulator
Simulates temperature/humidity sensors in 9 rooms sending
JSON POST requests to a central server every 60 seconds.
"""

import requests
import random
import time
import json
from datetime import datetime

SERVER_URL = "http://localhost:5000/api/sensor-data"

SENSORS = [
    {"id": "TEMP-001", "location": "Room 1", "type": "office"},
    {"id": "TEMP-002", "location": "Room 2", "type": "office"},
    {"id": "TEMP-003", "location": "Room 3", "type": "office"},
    {"id": "TEMP-004", "location": "Room 4", "type": "office"},
    {"id": "TEMP-005", "location": "Room 5", "type": "office"},
    {"id": "TEMP-006", "location": "Room 6", "type": "office"},
    {"id": "TEMP-007", "location": "Room 7", "type": "office"},
    {"id": "TEMP-008", "location": "Room 8 - Data Centre", "type": "datacentre"},
    {"id": "TEMP-009", "location": "Room 9", "type": "office"},
]

def generate_reading(sensor):
    if sensor["type"] == "datacentre":
        temperature = round(random.uniform(18.0, 27.0), 2)
        humidity    = round(random.uniform(40.0, 55.0), 2)
    else:
        temperature = round(random.uniform(19.0, 25.0), 2)
        humidity    = round(random.uniform(35.0, 65.0), 2)

    return {
        "sensor_id":           sensor["id"],
        "location":            sensor["location"],
        "temperature_celsius": temperature,
        "humidity_percent":    humidity,
        "timestamp":           datetime.utcnow().isoformat() + "Z"
    }

def send_reading(payload):
    try:
        response = requests.post(
            SERVER_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"[OK]    {payload['sensor_id']} | "
                  f"Temp: {payload['temperature_celsius']}°C | "
                  f"Humidity: {payload['humidity_percent']}%")
        else:
            print(f"[WARN]  Server returned HTTP {response.status_code} "
                  f"for {payload['sensor_id']}")
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot reach server at {SERVER_URL}")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout for sensor {payload['sensor_id']}")

def main():
    print("=" * 60)
    print(" SmartCampus IoT Sensor Simulator — QNI Infrastructure")
    print(f" Posting to: {SERVER_URL}")
    print(" Interval: 60 seconds | Ctrl+C to stop")
    print("=" * 60)
    cycle = 0
    while True:
        cycle += 1
        print(f"\n--- Cycle {cycle} | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC ---")
        for sensor in SENSORS:
            payload = generate_reading(sensor)
            send_reading(payload)
        print(f"Next cycle in 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()
