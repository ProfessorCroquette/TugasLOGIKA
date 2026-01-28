# System Architecture

## Overview

Traffic Simulation Indonesia uses a multi-threaded architecture with JSON-based data storage:

1. **CLI Simulation Engine** (main.py) - Runs traffic simulation in background
2. **GUI Dashboard** (gui_traffic_simulation.py) - Real-time monitoring interface
3. **JSON File Storage** - Persistent data across sessions

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     GUI Dashboard Layer                         │
│  gui_traffic_simulation.py (PyQt5) - 950+ lines                │
│  - TrafficSimulationGUI (QMainWindow)                           │
│  - ViolationDetailDialog (Dialog)                              │
│  - SimulationWorker (QThread)                                  │
│  - Auto-refresh every 500ms                                    │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────▼──────────────────┐
        │   Real-Time Data Files          │
        │  (JSON - Auto-updated)          │
        ├─────────────────────────────────┤
        │ tickets.json (Violations)       │
        │ traffic_data.json (Vehicles)    │
        │ worker_status.json (Sensors)    │
        └──────────────┬──────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│         Simulation Engine Layer (Background)             │
│  main.py (275 lines) - Spawned as subprocess             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ SpeedingTicketSimulator (Main Controller)          │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ TrafficSensor - Generates vehicles            │  │ │
│  │ │   - Creates random vehicles                   │  │ │
│  │ │   - Assigns speeds                            │  │ │
│  │ │   - Detects violations                        │  │ │
│  │ │   - Puts data in queue                        │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ QueuedCarProcessor - 5 parallel workers       │  │ │
│  │ │   - Worker 1: Processes vehicle queue         │  │ │
│  │ │   - Worker 2: Detects violations              │  │ │
│  │ │   - Worker 3: Writes to tickets.json          │  │ │
│  │ │   - Worker 4: Updates worker_status.json      │  │ │
│  │ │   - Worker 5: Calculates fines                │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ SpeedAnalyzer - Analyzes speeds              │  │ │
│  │ │   - Monitors data queue                       │  │ │
│  │ │   - Calculates statistics                     │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Dashboard - Console output                    │  │ │
│  │ │   - Displays violations                       │  │ │
│  │ │   - Shows statistics                          │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│            Data Generation & Utilities Layer             │
├──────────────────────────────────────────────────────────┤
│ utils/generators.py - DataGenerator class               │
│   - Generates vehicles with random attributes           │
│   - 50% Pribadi, 40% Barang/Truk, 5% Pemerintah, 5% K │
│   - Creates owner data with NIK                         │
│                                                          │
│ utils/indonesian_plates.py - PlateGenerator             │
│   - Generates 30+ region license plates                 │
│   - Format: [Region] [Numbers] [Letters]                │
│   - Example: B 1234 ABC (Jakarta)                       │
│                                                          │
│ utils/violation_utils.py - Fine calculation             │
│   - Base fines: $50, $25, $100 USD                      │
│   - Penalty multipliers: 1.0x, 1.2x, 1.4x              │
│   - USD to IDR conversion: 15,500x                      │
│                                                          │
│ utils/car_database.py, motorcycle_database.py, etc.     │
│   - Vehicle make/model databases                        │
│   - Owner names & NIK generation                        │
└──────────────────────────────────────────────────────────┘
```

## Component Details

### 1. GUI Layer (gui_traffic_simulation.py)

**TrafficSimulationGUI** - Main window (1400x800)
- Inherits from QMainWindow
- Two-panel layout: Left (controls), Right (violations table)
- Auto-refresh timer (500ms interval)
- Signal/slot connections for real-time updates

**Key Methods:**
```
__init__()              - Initialize GUI, load violations
start_simulation()      - Reset counters, spawn SimulationWorker
stop_simulation()       - Stop background process
auto_refresh()          - Called every 500ms
  ├─ Read JSON files
  ├─ Update violations table
  ├─ Update sensor panels (IDLE/SAFE/VIOLATION)
  └─ Recalculate statistics
update_stats()          - Update all stat labels
refresh_violations_table() - Refresh violations display
show_detail()           - Show ViolationDetailDialog
```

**SimulationWorker** - Background thread
- Spawns main.py subprocess
- Monitors process continuously
- Emits signals for GUI updates
- Monitors for 1 second intervals

**ViolationDetailDialog** - Detail popup
- Shows all violation information
- Displays fine calculation breakdown
- Shows owner and vehicle details
- Region conversion from NIK

### 2. Simulation Engine (main.py)

**SpeedingTicketSimulator** - Main controller
- Creates queue for inter-process communication
- Initializes TrafficSensor
- Initializes QueuedCarProcessor (5 workers)
- Initializes SpeedAnalyzer
- Initializes Dashboard (console display)

**Data Queue:**
- Size: 500 max elements
- Queue-based communication between sensor and processors
- Thread-safe operations

### 3. Core Simulation Components

**TrafficSensor** (simulation/sensor.py)
- Runs in main.py process
- Generates vehicles at configured intervals
- Assigns random speeds (40-120 km/h)
- Detects violations (speed > limit)
- Puts vehicle data in queue
- Updates traffic_data.json

**QueuedCarProcessor** (simulation/queue_processor.py)
- Manages 5 worker threads in parallel
- Each worker processes vehicles from queue
- Workers write violations to tickets.json
- Updates worker_status.json for each sensor
- Calculates fines and applies multipliers

**SpeedAnalyzer** (simulation/analyzer.py)
- Monitors data queue in real-time
- Analyzes speed patterns
- Calculates statistics
- Detects violation trends

### 4. Data Storage (JSON Files)

**Location:** data_files/ directory (auto-created)

**tickets.json**
- Nested structure with owner and fine details
- Updated by QueuedCarProcessor workers
- Read by GUI every 500ms
- Contains 100+ violations during typical session

**traffic_data.json**
- All vehicles processed by sensors
- Updated continuously during simulation
- Used for vehicle count statistics

**worker_status.json**
- Current status of each sensor (worker 0-4)
- Updated in real-time by processors
- Determines IDLE/CHECKING/VIOLATION display in GUI

### 5. Utilities Layer

**DataGenerator** (utils/generators.py)
- Generates vehicle batches
- Random vehicle distribution (50/40/5/5)
- Creates owner data with 16-digit NIK
- Assigns speeds and timestamp

**PlateGenerator** (utils/indonesian_plates.py)
- Generates 30+ region codes
- Format: [Region] [4-digit] [3-letter]
- Maps regions to Indonesian provinces

**ViolationUtils** (utils/violation_utils.py)
- Fine calculation engine
- Base fines by vehicle type
- Penalty multiplier logic
- USD to IDR conversion (constant: 15,500)

## Data Flow Diagram

```
┌─────────────────────────────────────┐
│  TrafficSensor.generate_vehicles()  │
│  (Creates random vehicles)          │
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  data_queue        │
        │  (500 max size)    │
        └────────┬───────────┘
                 │
        ┌────────┴───────────┐
        │                    │
        ▼                    ▼
   Worker 1-5 Pool (5 concurrent)
   ├─ Check speed limit
   ├─ Calculate fine
   ├─ Apply multiplier
   ├─ Write to tickets.json
   └─ Update worker_status.json
        │
        ▼
   SpeedAnalyzer
   ├─ Analyze speeds
   ├─ Calculate statistics
   ├─ Monitor queue
        │
        └─────────────────────┐
                              │
        ┌─────────────────────▼────────────┐
        │    JSON Data Files                │
        ├───────────────────────────────────┤
        │ • tickets.json (violations)       │
        │ • traffic_data.json (vehicles)    │
        │ • worker_status.json (status)     │
        └──────────┬────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │  GUI Auto-Refresh        │
        │  (Every 500ms)           │
        ├──────────────────────────┤
        │ • Read JSON files        │
        │ • Update table           │
        │ • Update sensors         │
        │ • Recalc statistics      │
        └──────────────────────────┘
```

## Concurrency Model

**Main Process (main.py):**
- 1 TrafficSensor thread (vehicle generation)
- 5 QueuedCarProcessor worker threads (violation detection)
- 1 SpeedAnalyzer thread (analysis)
- 1 Dashboard thread (console display)
- Total: 8 threads + main thread

**GUI Process (gui_traffic_simulation.py):**
- 1 Main thread (PyQt5 event loop)
- 1 SimulationWorker thread (subprocess monitoring)
- Auto-refresh timer callbacks (non-blocking)
- Total: 2+ threads

**Inter-Process Communication:**
- JSON files (no shared memory)
- File-based synchronization
- No locks needed (JSON overwrite is atomic)

## Error Handling

**Graceful Degradation:**
- If JSON read fails: silent fail, returns empty list
- If process dies: GUI detects and stops
- If file locked: retry in next refresh cycle
- If sensor fails: other workers continue

**Signal Handling:**
- SIGINT (Ctrl+C): Graceful shutdown
- SIGTERM: Stop simulation
- SIGBREAK (Windows): Stop simulation

## Performance Characteristics

**GUI Responsiveness:**
- Auto-refresh: 500ms (fast UI updates)
- No blocking operations
- Queue-based communication prevents deadlocks

**Throughput:**
- ~5-10 violations per second (depends on system)
- 5 workers processing in parallel
- Queue handles burst traffic

**Memory Usage:**
- GUI: ~100-200 MB (PyQt5 + data)
- Simulation: ~150-250 MB (threads + queue)
- Total: ~250-450 MB typical

**Scalability:**
- JSON file approach limits growth (file I/O)
- Currently designed for ~5000 violations max
- Could migrate to database for larger scale
- Real-time statistics display
- Data visualization

**config/__init__.py**
- Configuration management
- Directory setup
- System constants and settings

### 3. Utilities & Data Management

**utils/logger.py**
- Application logging setup
- Automatic log cleanup (keeps max 10 files)
- Console and file output

**utils/car_database.py**
- Vehicle type and brand database
- Vehicle specifications

**utils/indonesian_plates.py**
- License plate generation
- Indonesian plate format validation

**utils/violation_utils.py**
- Violation processing
- Penalty calculations

**data_models/models.py**
- Data structure definitions
- Violation and vehicle data models

### 4. Data Storage

**JSON Files**
- `traffic_data.json`: Real-time traffic simulation data
- `tickets.json`: Recorded violation tickets
- `vehicles_database.json`: Vehicle registry

**data_files/ Directory**
- `traffic_data.json`: Live simulation data
- `tickets.json`: Violation records
- `statistics.csv`: Aggregated statistics

**config/**
- Application configuration files
- Database settings
- Logging configuration

## Data Flow

### CLI Simulation Flow
```
main.py Started
    ↓
Initialize Sensor & Analyzer
    ↓
Generate Vehicle Data
    ↓
Detect Speed Violations
    ↓
Calculate Penalties
    ↓
Update JSON Files
    ├→ traffic_data.json
    └→ tickets.json
    ↓
Continuous Loop (30s intervals)
```

### GUI Display Flow
```
gui_traffic_simulation.py Started
    ↓
Read JSON Data Files
    ↓
Parse Violations & Vehicles
    ↓
Display in Real-time Table
    ↓
Handle User Actions
    ├→ Start/Stop Simulation
    ├→ View Details
    └→ Export Data
```

## Design Patterns Used

1. **MVC Pattern**: Separation of model (data), view (GUI), and controller
2. **Thread-Based Concurrency**: Background simulation with main GUI thread
3. **Queue Pattern**: Thread-safe data communication
4. **Configuration Singleton**: Centralized config management
5. **Observer Pattern**: GUI updates from simulation events

## Security Features

- Configuration file for sensitive settings
- Input validation for vehicle data
- Safe file handling with pathlib
- Signal handling for graceful shutdown

## Performance Optimizations

- JSON file-based data storage (lightweight)
- Efficient queue-based thread communication
- Configurable simulation intervals
- Automatic log cleanup (prevents disk space issues)
- Multi-threaded GUI to prevent blocking

## Testing Architecture

```
tests/
├── test_models.py              # Unit tests
├── integration/
│   └── test_simulation_flow.py  # Integration tests
└── conftest.py                 # Test configuration
```

## Deployment

- **Development**: Direct Python execution
- **Docker**: Containerized deployment (optional)
- **Production**: Docker Compose stack

## Technologies Used

- **Language**: Python 3.9+
- **GUI**: PyQt5
- **Data Storage**: JSON files
- **Configuration**: Python config module
- **Logging**: Python logging module
- **Testing**: pytest
- **Deployment**: Docker, Docker Compose (optional)
