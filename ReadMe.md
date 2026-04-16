# SmartCampus IoT Data Hub

## What This Is
Central API server that collects temperature/humidity readings from
9 campus room sensors every 60 seconds and displays a live dashboard.

## Tech Stack
- Python 3.11 + Flask (API server)
- SQLite (time-series database)
- Nginx (reverse proxy)
- Docker + Docker Compose (deployment)

## Prerequisites
- Docker and Docker Compose installed
- Port 80 and 5000 free on host machine

## Quick Start (Docker)
```bash
docker-compose up -d
```
Then open: http://localhost

## Run Without Docker
```bash
pip3 install flask
python3 server.py
```

## Simulate Sensor Data
```bash
pip3 install requests
python3 sensor_simulator.py
```

## API Reference

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/sensor-data | Submit sensor reading |
| GET | /api/latest | Get latest per sensor |
| GET | / | Live HTML dashboard |

## POST Body Example
```json
{
  "sensor_id": "TEMP-001",
  "location": "Room 1",
  "temperature_celsius": 21.5,
  "humidity_percent": 55.0,
  "timestamp": "2026-04-16T22:00:00Z"
}
```

## Database Schema
Table: readings
- id (INTEGER PRIMARY KEY)
- sensor_id (TEXT)
- location (TEXT)
- temperature (REAL)
- humidity (REAL)
- timestamp (TEXT)

## File Structure
smartcampus/
├── server.py
├── sensor_simulator.py
├── docker-compose.yml
├── nginx.conf
├── Dockerfile
├── requirements.txt
├── ReadMe.md
└── data/ (SQLite DB stored here)
