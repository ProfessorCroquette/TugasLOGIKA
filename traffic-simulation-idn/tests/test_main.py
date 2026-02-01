#!/usr/bin/env python3
"""Test main.py for 5 seconds"""
import subprocess
import time
import json
from pathlib import Path

print("Starting main.py...")
proc = subprocess.Popen(["python", "main.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Wait 5 seconds
time.sleep(5)

# Stop it
proc.terminate()
try:
    proc.wait(timeout=2)
except subprocess.TimeoutExpired:
    proc.kill()

# Check data
tickets_file = Path("data_files/tickets.json")
vehicles_file = Path("data_files/traffic_data.json")

print(f"\nChecking data files:")
if tickets_file.exists():
    with open(tickets_file) as f:
        tickets = json.load(f)
    print(f"  Tickets: {len(tickets)} records")
    if tickets:
        print(f"    First ticket: {tickets[0].get('license_plate')}, ${tickets[0].get('fine_amount', 0)}")

if vehicles_file.exists():
    with open(vehicles_file) as f:
        vehicles = json.load(f)
    print(f"  Vehicles: {len(vehicles)} records")
    if vehicles:
        print(f"    First vehicle: {vehicles[0].get('license_plate')}, {vehicles[0].get('speed')} km/h")
