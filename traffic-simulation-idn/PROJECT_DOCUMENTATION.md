# Indonesian Traffic Violation Simulation System - Complete Documentation

## System Overview
This is a complete Indonesian traffic violation simulation system that generates realistic traffic violations, calculates fines according to Indonesian law, and provides a real-time GUI dashboard for monitoring violations.

---

## Core System Files

### 1. **main.py** - Simulation Engine
**Purpose:** Runs the traffic violation simulation in background mode

**Key Components:**
- `SpeedingTicketSimulator` class: Main application controller
  - `start()`: Starts the simulation with sensor, analyzer, and dashboard
  - `_control_loop()`: Handles user input (q=quit, p=pause/resume)
  - `_display_final_stats()`: Shows final statistics

**Features:**
- Accepts optional command-line duration argument (minutes)
- Runs indefinitely if no duration specified
- Generates vehicle batches with random speeds (2-100 vehicles per batch)
- Detects violations (speeding > 75 km/h OR too slow < 40 km/h)
- Saves violations to `data_files/tickets.json`
- Queue size: 500 messages

**Run Command:**
```bash
python main.py              # Run indefinitely
python main.py 5            # Run for 5 minutes
```

**Output Files Created:**
- `data_files/tickets.json` - All violations detected
- `data_files/traffic_data.json` - All vehicles processed
- `logs/simulation_*.log` - Detailed simulation logs

---

### 2. **gui_traffic_simulation.py** - Real-Time Dashboard GUI
**Purpose:** Qt5-based GUI for monitoring violations in real-time

**Key Classes:**

#### **SignalEmitter (QObject)**
- Emits signals: `violation_detected`, `simulation_started`, `simulation_finished`, `stats_updated`
- Used for thread-safe communication between simulation and GUI

#### **SimulationWorker (QThread)**
- Runs simulation in background thread
- `run()`: Executes `main.py` process without duration (continuous)
- `_get_current_stats()`: Reads violation data and vehicle count every 1 second
- `stop()`: Terminates simulation process

#### **TrafficSimulationGUI (QMainWindow)**
- Main application window (1400x800 pixels)
- Left Panel (300px width):
  - **Control Group**: "Mulai Simulasi" (Start) and "Hentikan Simulasi" (Stop) buttons
  - **Statistics Group**: Real-time counts and fines in IDR
  - **Checking Status Group**: Shows current vehicle being checked

- Right Panel (Violations Table):
  - Columns: License Plate, Owner Name, Speed, Fine (IDR), STNK Status, Detail Button
  - Auto-refreshes every 500ms
  - Instant updates when violations detected

**Key Methods:**
- `start_simulation()`: Starts background worker, clears old data, enables refresh timer
- `stop_simulation()`: Stops background worker process
- `auto_refresh()`: Polls JSON files every 500ms for real-time updates
- `refresh_violations_table()`: Updates table with new violations
- `on_violation_detected()`: Handles new violation signal
- `on_simulation_finished()`: Re-enables start button when simulation stops
- `_flatten_violation()`: Converts nested JSON to flat structure for GUI display
- `show_violation_detail()`: Opens detailed dialog for selected violation

#### **ViolationDetailDialog (QDialog)**
Shows comprehensive violation information:
- Owner details (name, NIK format, vehicle info)
- Violation details (speed, timestamp, excess speed)
- Fine calculation (base fine, penalty multiplier, total in both USD and IDR)
- Status indicators (STNK status, SIM status with color coding)

**Features:**
- Real-time updates from JSON files
- 500ms auto-refresh timer
- Live vehicle checking status display
- Color-coded violations (green=OK, red=violation)
- Penalty multiplier explanation:
  - 1.0x: Both STNK active & SIM valid
  - 1.2x: STNK non-active OR SIM expired
  - 1.4x: Both STNK non-active AND SIM expired

**Run Command:**
```bash
cd traffic-simulation-idn
python gui_traffic_simulation.py
```

---

### 3. **config/__init__.py** - Configuration Management
**Purpose:** Central configuration for the entire system

**Key Settings:**

#### Simulation Parameters
```python
SIMULATION_INTERVAL = 5          # Seconds between batch generation
SPEED_LIMIT = 75                 # km/h - normal speed limit
MIN_SPEED_LIMIT = 40             # km/h - minimum safe speed
MIN_VEHICLES_PER_BATCH = 2       # Min vehicles per batch
MAX_VEHICLES_PER_BATCH = 100     # Max vehicles per batch (allows up to 100)
```

#### Speed Distribution
```python
SPEED_MEAN = 65 km/h
SPEED_STD_DEV = 15 km/h
MIN_SPEED = 30 km/h
MAX_SPEED = 140 km/h
```

#### Fine Structure (Compliant with Indonesian Law - Pasal 287 ayat 5 UU No. 22 Tahun 2009)
Maximum fine: **Rp 1,250,000** (enforced cap)

Five tiers:
1. **SPEED_LOW_MILD** (30-39 km/h): $20 = Rp 310,000
2. **SPEED_LOW_SEVERE** (0-29 km/h): $35 = Rp 542,500
3. **SPEED_HIGH_LEVEL_1** (76-90 km/h): $30 = Rp 465,000
4. **SPEED_HIGH_LEVEL_2** (91-110 km/h): $50 = Rp 775,000
5. **SPEED_HIGH_LEVEL_3** (111-130 km/h): $75 = Rp 1,162,500

#### Currency Conversion
```python
USD_TO_IDR = 15500              # 1 USD = 15,500 IDR
MAX_FINE_IDR = 1,250,000        # Maximum allowed by law
```

#### Directory Structure
```python
BASE_DIR = project root
LOGS_DIR = logs/
DATA_DIR = data_files/
```

---

### 4. **config.py** - Alternate Configuration
**Purpose:** Duplicate config (for compatibility)
**Note:** Use `config/__init__.py` as primary source

---

## Support Modules

### **simulation/sensor.py** - TrafficSensor
- Generates batches of random vehicles every 5 seconds
- Outputs: license plate, speed, vehicle type, owner info
- Puts data in queue for analyzer

### **simulation/analyzer.py** - SpeedAnalyzer
- Reads vehicle data from queue
- Detects violations:
  - SPEEDING: speed > 75 km/h
  - DRIVING_TOO_SLOW: speed < 40 km/h
- Calculates fines and penalty multipliers
- Saves violations to JSON

### **utils/generators.py** - DataGenerator
- `generate_vehicle_batch()`: Creates 2-100 random vehicles
- `generate_random_owner()`: Creates owner with:
  - Random name
  - 16-digit Indonesian NIK (format: AA BB CC DD MM YY ZZZZ)
  - STNK status (Active/Non-Active)
  - SIM status (Valid/Expired)

### **utils/indonesian_plates.py** - License Plate Generator
- `VehicleOwner.generate_random_owner()`: Creates realistic Indonesian vehicle owners
- Generates authentic NIK format with regional prefixes
- Random birth dates and status information

### **data_models/storage.py** - Data Persistence
- `DataStorage` class handles JSON file I/O
- Saves violations to `data_files/tickets.json`
- Saves vehicles to `data_files/traffic_data.json`

---

## Data Files

### **data_files/tickets.json**
Violation records structure:
```json
{
  "license_plate": "B 1234 XY",
  "owner_name": "Budi Santoso",
  "owner_nik": "3606010195123456",
  "vehicle_type": "car",
  "speed": 95.5,
  "fine_amount": 50.0,
  "penalty_multiplier": 1.0,
  "stnk_status": "Active",
  "sim_status": "Valid",
  "timestamp": "2026-01-26 20:22:23",
  "violation_type": "SPEEDING"
}
```

### **data_files/traffic_data.json**
Vehicle records structure:
```json
{
  "license_plate": "B 1234 XY",
  "speed": 85.3,
  "vehicle_type": "car",
  "timestamp": "2026-01-26 20:22:20",
  "owner_name": "Budi Santoso",
  "owner_nik": "3606010195123456"
}
```

### **logs/simulation_*.log**
Detailed simulation logs with timestamps and events

---

## Workflow

### Starting the System

#### Method 1: GUI Mode (Recommended)
```bash
cd traffic-simulation-idn
python gui_traffic_simulation.py
```
1. Click "Mulai Simulasi" (Start)
2. Violations appear in real-time
3. Click "Hentikan Simulasi" (Stop) to end

#### Method 2: Command Line
```bash
cd traffic-simulation-idn
python main.py              # Run until you press 'q'
python main.py 10           # Run for 10 minutes
```

### Simulation Flow

1. **Sensor** generates batch of 2-100 vehicles every 5 seconds
2. **Analyzer** checks speeds against limits (40-75 km/h normal range)
3. **Violations detected**: Speed too high (>75) or too low (<40)
4. **Fine calculated** using 5-tier structure with penalty multiplier
5. **Data saved** to JSON files
6. **GUI updates** every 500ms from JSON files
7. **Statistics** displayed in real-time:
   - Total violations count
   - Vehicles processed count
   - Total fines in IDR
   - Average speed
   - Maximum speed
   - Current vehicle being checked

---

## Penalty Multiplier System

**How it works:**
- **Base**: 1.0x (no additional penalties)
- **+20%** if STNK is Non-Active (not registered)
- **+20%** if SIM is Expired (driver license expired)
- **Stacking**: Both conditions add separately

**Examples:**
- Both active/valid: 1.0x
- STNK non-active OR SIM expired: 1.2x
- Both STNK non-active AND SIM expired: 1.4x

---

## Indonesian Law Compliance

**Source:** Pasal 287 ayat (5) UU No. 22 Tahun 2009 tentang Lalu Lintas dan Angkutan Jalan

**Key Points:**
- ✅ Maximum fine: Rp 1,250,000 (enforced cap)
- ✅ Detects both speeding AND driving too slow
- ✅ Realistic penalty multipliers
- ✅ Indonesian regional license plates
- ✅ Indonesian NIK format (16 digits)
- ✅ Currency: Rupiah (IDR)

---

## Features

### ✅ Real-Time Monitoring
- Live violation detection and display
- Vehicle speed tracking
- Automatic table updates every 500ms
- Live checking status display

### ✅ Comprehensive Violation Details
- Owner information with NIK
- Vehicle type and license plate
- Detected speed vs speed limit
- Fine calculation breakdown
- Penalty multiplier explanation
- STNK and SIM status indicators

### ✅ Indonesian Accuracy
- Authentic Indonesian license plates
- Indonesian NIK format (16-digit standard)
- Regional plate prefixes
- Correct Indonesian law compliance
- IDR currency display

### ✅ Scalable
- Can generate up to 100 vehicles per batch
- Can process unlimited violations
- Queue size: 500 messages
- Continuous operation until stopped

---

## Common Tasks

### Run GUI with High Violation Rate
```bash
python gui_traffic_simulation.py
# Click "Mulai Simulasi"
# Wait 5 seconds for first batch (2-100 violations)
```

### Run Simulation for Specific Duration
```bash
python main.py 5                # 5 minutes
python main.py 60               # 1 hour
```

### Check Violations Data
```bash
# Open in any JSON viewer
data_files/tickets.json         # All violations
data_files/traffic_data.json    # All vehicles
```

### View Logs
```bash
type logs\simulation_*.log      # Windows
cat logs/simulation_*.log       # Linux/Mac
```

---

## Technical Stack

- **Python 3.13**
- **PyQt5** - GUI framework with signals/slots
- **threading** - Multi-threaded simulation
- **subprocess** - Background process management
- **JSON** - Data storage
- **queue** - Thread-safe communication

---

## Performance Notes

- **Simulation interval**: 5 seconds (customizable)
- **GUI refresh**: 500ms (fast real-time feedback)
- **Batch size**: 2-100 vehicles per batch
- **Queue capacity**: 500 messages
- **Memory**: Grows with violation count (can reach 100+)

---

## System Paths

```
traffic-simulation-idn/
├── main.py                          # Simulation engine
├── gui_traffic_simulation.py         # Dashboard GUI
├── config/
│   └── __init__.py                  # Configuration
├── simulation/
│   ├── sensor.py                    # Vehicle generation
│   └── analyzer.py                  # Violation detection
├── utils/
│   ├── generators.py                # Data generation
│   ├── indonesian_plates.py         # License plates & NIK
│   └── logger.py                    # Logging
├── data_models/
│   ├── models.py                    # Data classes
│   └── storage.py                   # JSON persistence
├── data_files/
│   ├── tickets.json                 # Violations
│   └── traffic_data.json            # Vehicles
└── logs/
    └── simulation_*.log             # Simulation logs
```

---

## Troubleshooting

### Issue: GUI shows no violations
**Solution:** Click "Mulai Simulasi" - simulation takes 5 seconds to generate first batch

### Issue: Violations not updating
**Solution:** Check that `data_files/` directory exists and is writable

### Issue: GUI takes too long to start
**Solution:** GUI is normal - simulation is generating vehicles in background

### Issue: Fine amounts show $0
**Solution:** Ensure `USD_TO_IDR = 15500` is set in `config/__init__.py`

---

## Version History

**v1.0 - Final Release**
- ✅ Real-time GUI with 500ms refresh
- ✅ Continuous simulation (no duration limit needed)
- ✅ High violation rate (2-100 vehicles per 5 seconds)
- ✅ Full Indonesian law compliance (Pasal 287 ayat 5)
- ✅ Penalty multiplier system (1.0x/1.2x/1.4x)
- ✅ Comprehensive violation details dialog
- ✅ Live checking status display
- ✅ Maximum 100 violations per batch supported

---

## License
Indonesian Traffic Violation Simulation System - Educational Purpose

---

## Support
For issues or questions, refer to the inline code documentation in each file.
