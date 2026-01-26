# Usage Guide & Examples

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Customization Examples](#customization-examples)
3. [Data Analysis](#data-analysis)
4. [Advanced Usage](#advanced-usage)
5. [Extending the System](#extending-the-system)

## Basic Usage

### 1. Run Validation Tests (FIRST TIME)

```powershell
cd i:\TugasLOGIKA\traffic-simulation-idn
python test_system.py
```

Output should show:
```
======================================================================
   TRAFFIC SIMULATION SYSTEM - VALIDATION TEST
======================================================================

🔍 Testing imports...
✅ All imports successful

🔍 Testing configuration...
✅ Configuration OK
   Speed Limit: 75 km/h
   Simulation Interval: 10s
   Vehicle Types: ['car', 'truck', 'motorcycle', 'bus']
   Fine Levels: ['LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4']

[... more tests ...]

======================================================================
   TEST SUMMARY
======================================================================
Imports..........................................✅ PASS
Configuration.....................................✅ PASS
Directories........................................✅ PASS
Data Generation....................................✅ PASS
Models.............................................✅ PASS
Storage............................................✅ PASS
======================================================================
Results: 6/6 tests passed

🎉 All tests passed! System is ready to use.

Run the simulation with:
   python main.py
```

### 2. Run the Simulation

```powershell
python main.py
```

Output:
```
🚗 SPEEDING TICKET SIMULATION SYSTEM
==================================================
This system simulates:
1. Traffic sensor generating random vehicles every 10 seconds
2. Speed analyzer issuing tickets for speeds > 75 km/h
3. Real-time dashboard showing statistics
==================================================
How long to run simulation (minutes)? [Enter for continuous]: 
```

Options:
- Press **Enter** for continuous run (quit with `q`)
- Type **5** for 5-minute run
- Type **60** for 1-hour run

### 3. Monitor the Dashboard

The dashboard updates every 5 seconds showing:

```
======================================================================
              TRAFFIC SPEEDING TICKET SIMULATION DASHBOARD
======================================================================
Time: 2024-01-26 14:35:42
Runtime: 00:05:22
----------------------------------------------------------------------

📡 TRAFFIC SENSOR
   Status: RUNNING
   Vehicles Generated: 237
   Interval: 10 seconds
----------------------------------------------------------------------

⚡ SPEED ANALYZER
   Vehicles Processed: 237
   Speeding Violations: 68
   Total Fines: $11,400
   Average Speed: 68.3 km/h
   Maximum Speed: 132.5 km/h
----------------------------------------------------------------------

📊 SPEED DISTRIBUTION
   Within Limit (≤75 km/h): 169 (71.3%)
   Speeding (>75 km/h): 68 (28.7%)
   [ ███████████████ ████ ]
----------------------------------------------------------------------

🚨 RECENT SPEEDING TICKETS
   1. [14:35:38] ZXC 456: 98 km/h - Fine: $200
   2. [14:35:28] QWE 789: 115 km/h - Fine: $500
   3. [14:35:18] RTY 012: 85 km/h - Fine: $100
   4. [14:35:08] UIO 345: 122 km/h - Fine: $500
   5. [14:34:58] ASD 678: 91 km/h - Fine: $200

----------------------------------------------------------------------

🎮 CONTROLS
   Press 'q' to quit simulation
   Press 'p' to pause/resume sensor
   Press 'r' to reset statistics
======================================================================
```

### 4. Check Generated Data

After running, examine the generated files:

```powershell
# View most recent tickets
python -c "import json; data = json.load(open('data_files/tickets.json')); print('\n'.join([f\"{t['license_plate']}: {t['speed']} km/h - ${t['fine_amount']}\" for t in data[-5:]]))"

# View statistics
type data_files\statistics.csv

# View logs
type logs\simulation_*.log | more
```

## Customization Examples

### Example 1: Strict Enforcement (Lower Speed Limit)

**Before:**
```python
# config.py
SPEED_LIMIT = 75
FINES = {
    "LEVEL_1": {"min": 76, "max": 90, "fine": 100},
    ...
}
```

**After:**
```python
# config.py
SPEED_LIMIT = 60  # More strict
FINES = {
    "LEVEL_1": {"min": 61, "max": 80, "fine": 150},   # Higher fine
    "LEVEL_2": {"min": 81, "max": 100, "fine": 300},
    "LEVEL_3": {"min": 101, "max": 120, "fine": 600},
    "LEVEL_4": {"min": 121, "max": float('inf'), "fine": 1200}
}
```

Run and see higher violation rate and higher fines:
```powershell
python main.py
# Enter 5 (for 5 minute run)
# Wait for results
```

### Example 2: More Traffic (Busy Highway)

**Before:**
```python
MIN_VEHICLES_PER_BATCH = 1
MAX_VEHICLES_PER_BATCH = 10
SIMULATION_INTERVAL = 10  # seconds
```

**After:**
```python
MIN_VEHICLES_PER_BATCH = 20      # More vehicles
MAX_VEHICLES_PER_BATCH = 50      # Much more
SIMULATION_INTERVAL = 5          # More frequent
```

This generates 200-500 vehicles per minute instead of 50-100.

### Example 3: Indonesian Festival (More Speeding)

**Before:**
```python
SPEED_MEAN = 65
SPEED_STD_DEV = 15
```

**After:**
```python
SPEED_MEAN = 75         # More aggressive driving
SPEED_STD_DEV = 20      # More variation
```

Results in more speeding violations detected.

### Example 4: Aggressive Enforcement (Higher Fines)

**Before:**
```python
FINES = {
    "LEVEL_1": {"min": 76, "max": 90, "fine": 100},
    "LEVEL_2": {"min": 91, "max": 110, "fine": 200},
    "LEVEL_3": {"min": 111, "max": 130, "fine": 500},
    "LEVEL_4": {"min": 131, "max": float('inf'), "fine": 1000}
}
```

**After:**
```python
FINES = {
    "LEVEL_1": {"min": 76, "max": 90, "fine": 250},     # x2.5
    "LEVEL_2": {"min": 91, "max": 110, "fine": 500},    # x2.5
    "LEVEL_3": {"min": 111, "max": 130, "fine": 1200},  # x2.4
    "LEVEL_4": {"min": 131, "max": float('inf'), "fine": 2500}  # x2.5
}
```

## Data Analysis

### Python Analysis Script

Create `analyze_results.py`:

```python
import json
import csv
from datetime import datetime
from collections import Counter

# Load tickets
with open('data_files/tickets.json') as f:
    tickets = json.load(f)

# Load vehicles
with open('data_files/traffic_data.json') as f:
    vehicles = json.load(f)

print("=" * 60)
print("TRAFFIC SIMULATION ANALYSIS")
print("=" * 60)

print(f"\nTotal Vehicles Detected: {len(vehicles)}")
print(f"Total Tickets Issued: {len(tickets)}")
print(f"Violation Rate: {len(tickets)/len(vehicles)*100:.1f}%")

# Fine distribution
fine_dist = Counter(t['fine_amount'] for t in tickets)
print(f"\nFine Distribution:")
for fine_amount in sorted(fine_dist.keys()):
    count = fine_dist[fine_amount]
    pct = count / len(tickets) * 100
    print(f"  ${fine_amount}: {count} tickets ({pct:.1f}%)")

# Speed statistics
speeds = [v['speed'] for v in vehicles]
print(f"\nSpeed Statistics (All Vehicles):")
print(f"  Min: {min(speeds):.1f} km/h")
print(f"  Max: {max(speeds):.1f} km/h")
print(f"  Avg: {sum(speeds)/len(speeds):.1f} km/h")

speeds_speeding = [t['speed'] for t in tickets]
print(f"\nSpeed Statistics (Speeders Only):")
print(f"  Min: {min(speeds_speeding):.1f} km/h")
print(f"  Max: {max(speeds_speeding):.1f} km/h")
print(f"  Avg: {sum(speeds_speeding)/len(speeds_speeding):.1f} km/h")

# Revenue
total_revenue = sum(t['fine_amount'] for t in tickets)
print(f"\nRevenue: ${total_revenue:,.2f}")
print(f"Average Fine: ${total_revenue/len(tickets):.2f}")

# Vehicle types
type_dist = Counter(v['vehicle_type'] for v in vehicles)
print(f"\nVehicle Type Distribution:")
for vtype in sorted(type_dist.keys()):
    count = type_dist[vtype]
    pct = count / len(vehicles) * 100
    print(f"  {vtype}: {count} ({pct:.1f}%)")

# Peak violation times
times = Counter(t['timestamp'][:19] for t in tickets)  # Group by minute
print(f"\nPeak Violation Times (Top 5):")
for time_str, count in times.most_common(5):
    print(f"  {time_str}: {count} tickets")

print("\n" + "=" * 60)
```

Run analysis:
```powershell
python analyze_results.py
```

### Excel Analysis

1. Open `data_files/statistics.csv` in Excel
2. Create pivot table or chart
3. Analyze revenue over time

```python
# Quick Excel export
import json
import pandas as pd

# Load tickets
tickets = json.load(open('data_files/tickets.json'))

# Create DataFrame
df = pd.DataFrame(tickets)

# Analysis
print("By Vehicle Type:")
print(df.groupby('vehicle_type')['fine_amount'].agg(['count', 'sum', 'mean']))

print("\nBy Fine Amount:")
print(df.groupby('fine_amount').size())

# Export to Excel
df.to_excel('analysis.xlsx', index=False)
```

## Advanced Usage

### Run Multiple Simulations

Create `multi_simulation.py`:

```python
from main import SpeedingTicketSimulator
import json
import time

results = []

for run in range(3):
    print(f"\n===== RUN {run+1}/3 =====")
    simulator = SpeedingTicketSimulator()
    
    # Run for 1 minute
    import threading
    def stop_after_delay():
        time.sleep(60)  # 1 minute
        simulator.stop()
    
    timer = threading.Thread(target=stop_after_delay, daemon=True)
    timer.start()
    
    simulator.start()
    
    # Collect results
    stats = simulator.analyzer.get_stats()
    results.append({
        'run': run + 1,
        'vehicles': stats['total_processed'],
        'violations': stats['speeding_processed'],
        'fines': stats['current_stats']['total_fines']
    })

# Summary
print("\n===== SUMMARY =====")
for r in results:
    print(f"Run {r['run']}: {r['vehicles']} vehicles, "
          f"{r['violations']} violations, "
          f"${r['fines']} in fines")
```

### Compare Configurations

Create `config_comparison.py`:

```python
from config import Config
import json

configs = {
    'Conservative': {
        'SPEED_LIMIT': 75,
        'FINES_LEVEL_1': 100,
    },
    'Moderate': {
        'SPEED_LIMIT': 70,
        'FINES_LEVEL_1': 150,
    },
    'Aggressive': {
        'SPEED_LIMIT': 60,
        'FINES_LEVEL_1': 250,
    }
}

for name, config in configs.items():
    # Apply config
    Config.SPEED_LIMIT = config['SPEED_LIMIT']
    Config.FINES['LEVEL_1']['fine'] = config['FINES_LEVEL_1']
    
    # Run simulation
    # ... collect results
    
    print(f"{name}: Speed Limit {config['SPEED_LIMIT']}, "
          f"Level 1 Fine ${config['FINES_LEVEL_1']}")
```

## Extending the System

### Add Database Support

Create `data_models/db.py`:

```python
import sqlite3

class DatabaseStorage:
    def __init__(self, db_path='traffic.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id TEXT PRIMARY KEY,
                plate TEXT,
                type TEXT,
                speed REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()
    
    def save_vehicle(self, vehicle):
        self.conn.execute('''
            INSERT INTO vehicles VALUES (?, ?, ?, ?, ?)
        ''', (vehicle.vehicle_id, vehicle.license_plate, 
              vehicle.vehicle_type, vehicle.speed, 
              vehicle.timestamp.isoformat()))
        self.conn.commit()
```

### Add Web API

Create `api/app.py`:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/stats')
def stats():
    # Return current simulation stats
    return jsonify({
        'vehicles_processed': 1000,
        'violations': 250,
        'total_fines': 45000
    })

@app.route('/api/tickets')
def tickets():
    # Return recent tickets
    import json
    with open('data_files/tickets.json') as f:
        return jsonify(json.load(f)[-10:])

if __name__ == '__main__':
    app.run(port=5000)
```

Then run with:
```powershell
python api/app.py
```

Visit `http://localhost:5000/api/stats`

## Summary

The system is highly flexible and can be:
- ✅ Customized via config.py
- ✅ Analyzed with Python/Excel
- ✅ Extended with databases
- ✅ Integrated with APIs
- ✅ Used for reports and statistics

Happy simulating! 🚗💨
