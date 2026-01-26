# System Architecture

## Overview

Traffic Simulation Indonesia is a multi-layer architecture application with two main interfaces:

1. **CLI Interface** - Command-line tool for core simulation (main.py)
2. **GUI Interface** - PyQt5 desktop application for interactive monitoring (gui_traffic_simulation.py)

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces Layer                     │
├──────────────────┬──────────────────────────────────────────┤
│   CLI Simulation │   PyQt5 GUI Dashboard                    │
│   (main.py)      │   (gui_traffic_simulation.py)            │
└────────┬─────────┴────────┬─────────────────────────────────┘
         │                  │
         └──────────────────┼──────────────────────┘
                            │
         ┌──────────────────▼─────────────────────┐
         │      Application Core Layer            │
         ├──────────────────────────────────────┤
         │ Application Controller (core/)        │
         │ Simulation Engine                    │
         │ Event Bus                            │
         │ Config Manager                       │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │      Services Layer                   │
         ├──────────────────────────────────────┤
         │ Generators    Analyzers              │
         │ Notifiers     Exporters              │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │      Data Access Layer               │
         ├──────────────────────────────────────┤
         │ Repositories (CRUD Operations)       │
         │ Database Models (SQLAlchemy ORM)     │
         │ Session Management                   │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │    Database & Cache Layer            │
         ├──────────────────────────────────────┤
         │ MySQL Database                       │
         │ Redis Cache                          │
         │ External APIs (RapidAPI, Twilio)     │
         └──────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### CLI (src/main.py)
- Command-line interface using argparse
- Suitable for batch operations and automation
- Supports scripting and cron jobs

#### GUI (src/main_gui.py)
- PyQt5-based desktop application
- Responsive UI with real-time updates
- Dashboard, simulation control, reports generation

### 2. Core Application Layer

**simulation/sensor.py**
- Traffic sensor simulation
- Vehicle speed detection
- Real-time data collection

**simulation/analyzer.py**
- Speed violation detection
- Penalty calculation
- Traffic analysis

**dashboard/display.py**
- Console-based dashboard
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
