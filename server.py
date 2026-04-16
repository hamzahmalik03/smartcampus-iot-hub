# server.py
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sensors.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id TEXT NOT NULL,
        location TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/api/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    required = ['sensor_id', 'location', 'temperature_celsius', 'humidity_percent', 'timestamp']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    conn = sqlite3.connect('sensors.db')
    conn.execute('''INSERT INTO readings (sensor_id, location, temperature, humidity, timestamp)
                    VALUES (?, ?, ?, ?, ?)''',
                 (data['sensor_id'], data['location'],
                  data['temperature_celsius'], data['humidity_percent'],
                  data['timestamp']))
    conn.commit()
    conn.close()
    print(f"[OK] Stored: {data['sensor_id']} | {data['temperature_celsius']}°C")
    return jsonify({'status': 'ok', 'stored': data['sensor_id']}), 200

@app.route('/api/latest', methods=['GET'])
def get_latest():
    conn = sqlite3.connect('sensors.db')
    cur = conn.execute('''SELECT sensor_id, location, temperature, humidity, timestamp
                          FROM readings GROUP BY sensor_id
                          HAVING MAX(timestamp) ORDER BY sensor_id''')
    rows = cur.fetchall()
    conn.close()
    result = [{'sensor_id': r[0], 'location': r[1],
               'temperature': r[2], 'humidity': r[3], 'timestamp': r[4]}
              for r in rows]
    return jsonify(result), 200

@app.route('/', methods=['GET'])
def dashboard():
    conn = sqlite3.connect('sensors.db')
    cur = conn.execute('''SELECT sensor_id, location, temperature, humidity, timestamp
                          FROM readings GROUP BY sensor_id
                          HAVING MAX(timestamp) ORDER BY sensor_id''')
    rows = cur.fetchall()
    conn.close()
    html = '''<!DOCTYPE html><html><head>
    <title>SmartCampus IoT Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <style>
      body{font-family:Arial,sans-serif;background:#1a1a2e;color:#eee;padding:20px;}
      h1{color:#00d4ff;} table{width:100%;border-collapse:collapse;margin-top:20px;}
      th{background:#16213e;padding:12px;text-align:left;color:#00d4ff;}
      td{padding:10px;border-bottom:1px solid #333;}
      tr:hover{background:#16213e;}
      .hot{color:#ff6b6b;font-weight:bold;}
      .ok{color:#51cf66;}
    </style></head><body>
    <h1>🌡 SmartCampus Live Sensor Dashboard</h1>
    <p style="color:#aaa">Auto-refreshes every 30 seconds</p>
    <table><tr><th>Sensor ID</th><th>Location</th>
    <th>Temperature (°C)</th><th>Humidity (%)</th><th>Last Updated</th></tr>'''
    for r in rows:
        temp_class = 'hot' if r[2] > 25 else 'ok'
        html += f'<tr><td>{r[0]}</td><td>{r[1]}</td>'
        html += f'<td class="{temp_class}">{r[2]}°C</td>'
        html += f'<td>{r[3]}%</td><td>{r[4]}</td></tr>'
    html += '</table></body></html>'
    return html

if __name__ == '__main__':
    init_db()
    print("SmartCampus IoT Server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
