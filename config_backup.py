#!/usr/bin/env python3
"""
QNI Network Device Configuration Backup
Connects to all 11 network devices via SSH,
retrieves running-config, saves timestamped files.
Schedule with cron: 0 2 * * * /usr/bin/python3 ~/config_backup.py
"""

from netmiko import ConnectHandler
from datetime import datetime
import os

BACKUP_DIR = os.path.expanduser("~/qni_config_backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

DEVICES = [
    {"name": "sw-room1",  "host": "172.20.10.11", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room2",  "host": "172.20.10.12", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room3",  "host": "172.20.10.13", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room4",  "host": "172.20.10.14", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room5",  "host": "172.20.10.15", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room6",  "host": "172.20.10.16", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room7",  "host": "172.20.10.17", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room8",  "host": "172.20.10.18", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "sw-room9",  "host": "172.20.10.19", "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "core-sw1",  "host": "172.20.10.2",  "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
    {"name": "core-sw2",  "host": "172.20.10.3",  "device_type": "cisco_ios",
     "username": "admin", "password": "SecurePass123!", "secret": "EnableSecret123!"},
]

def backup_device(device):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = os.path.join(BACKUP_DIR, f"{device['name']}_{timestamp}.txt")
    try:
        conn = ConnectHandler(
            device_type=device["device_type"],
            host=device["host"],
            username=device["username"],
            password=device["password"],
            secret=device["secret"]
        )
        conn.enable()
        config = conn.send_command("show running-config")
        conn.disconnect()
        with open(filename, "w") as f:
            f.write(f"! Device: {device['name']}\n")
            f.write(f"! Backup: {timestamp}\n")
            f.write(f"! Host:   {device['host']}\n!\n")
            f.write(config)
        print(f"[OK]    {device['name']} → {filename}")
    except Exception as e:
        print(f"[ERROR] {device['name']} ({device['host']}): {e}")

def main():
    start = datetime.now()
    print(f"QNI Config Backup Started — {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Saving to: {BACKUP_DIR}\n")
    for device in DEVICES:
        backup_device(device)
    elapsed = (datetime.now() - start).seconds
    print(f"\nBackup complete. {len(DEVICES)} devices. Time: {elapsed}s")

if __name__ == "__main__":
    main()
