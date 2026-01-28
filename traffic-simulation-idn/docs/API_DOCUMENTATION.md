# API Documentation - Simulation & Core Functions

## Overview

The Traffic Simulation Indonesia system provides Python-based APIs for:
- Traffic simulation engine (CLI via main.py)
- GUI interface (PyQt5 based)
- Real-time violation detection
- Data file access (JSON-based)

**Note:** This is a simulation system, not a REST API server. Data access is through JSON files and Python classes.

## Core Classes & Methods

### 1. TrafficSimulationGUI (gui_traffic_simulation.py)

Main GUI window for real-time traffic violation monitoring.

#### Key Methods

**Constructor:**
```python
class TrafficSimulationGUI(QMainWindow):
    def __init__(self):
        # Initialize GUI window (1400x800)
        # Setup timers, data structures
        # Load violations from JSON
```

**Control Methods:**
```python
def start_simulation(self):
    """Start simulation and begin auto-refresh"""
    # Resets counters (not violations data)
    # Launches SimulationWorker thread
    # Starts 500ms refresh timer
    
def stop_simulation(self):
    """Stop simulation"""
    # Stops background worker process
    # Keeps all violation data visible
    
def clear_data(self):
    """Clear all violations and vehicles"""
    # Confirms with user first
    # Clears tickets.json and traffic_data.json
    # Resets GUI statistics
```

**Real-time Update Methods:**
```python
def auto_refresh(self):
    """Called every 500ms during simulation"""
    # Reads violations_file (data_files/tickets.json)
    # Reads vehicles_file (data_files/traffic_data.json)
    # Reads worker_status_file (data_files/worker_status.json)
    # Updates table if violation count changed
    # Always updates vehicle counter
    # Updates 5 sensor status panels
    # Recalculates statistics (fines, speeds)
    
def update_stats(self):
    """Update statistics from JSON files"""
    # Counts violations and vehicles
    # Calculates total fines (USD -> IDR conversion)
    # Computes average and max speeds
    # Updates all stat labels
```

**GUI Display Methods:**
```python
def refresh_violations_table(self):
    """Refresh the violations table with current data"""
    # Displays: Plate, Owner, Speed, Fine, STNK Status
    # Adds Detail button for each row
    
def show_detail(self, violation: Dict):
    """Show violation detail dialog"""
    # Opens ViolationDetailDialog
    
def on_violation_detected(self, violation: Dict):
    """Handle new violation from SimulationWorker"""
    # Flattens nested JSON structure
    # Appends to self.violations
    # Refreshes table
    
def on_stats_updated(self, stats: Dict):
    """Handle stats update from SimulationWorker"""
    # Updates all labels from stats dict
```

### 2. SimulationWorker (gui_traffic_simulation.py)

Background thread that runs main.py simulation.

```python
class SimulationWorker(QThread):
    def __init__(self):
        # Setup signal emitter
        # Initialize process handle
        
    def run(self):
        """Run simulation process"""
        # Spawns main.py subprocess
        # Monitors process while emitting stats
        # Updates stats every 1 second
        
    def stop(self):
        """Stop the simulation"""
        # Sets running = False
        # Process cleanup happens in run()
        
    def _get_current_stats(self) -> Dict:
        """Read current stats from JSON files"""
        # Returns dict with:
        #   violations_count
        #   vehicles_processed
        #   total_fines_idr
        #   avg_speed
        #   max_speed
```

### 3. ViolationDetailDialog (gui_traffic_simulation.py)

Dialog showing detailed violation information.

```python
class ViolationDetailDialog(QDialog):
    def __init__(self, violation: Dict, parent=None):
        # Initialize with violation data
        
    def init_ui(self):
        """Setup dialog UI with violation details"""
        # Shows: General Info (plate, owner, vehicle, region, timestamp)
        # Shows: Fine Calculation (base fine, multiplier, total)
```

### 4. TrafficSensor (simulation/sensor.py)

Simulates traffic sensor detecting vehicles.

```python
class TrafficSensor:
    def __init__(self, data_queue, interval, car_processor=None):
        # Setup sensor configuration
        # Create car processor for 5 concurrent workers
        
    def generate_vehicles(self):
        """Generate vehicle data continuously"""
        # Creates vehicles with random attributes
        # Detects speed violations
        # Puts vehicle data in queue
```

### 5. QueuedCarProcessor (simulation/queue_processor.py)

Manages 5 parallel sensor workers.

```python
class QueuedCarProcessor:
    def __init__(self, num_workers=5):
        # Create 5 worker threads
        # Setup processing queue
        
    def process_vehicle(self, vehicle_data):
        """Process vehicle through queue"""
        # Adds to processing queue
        # Workers check violations
        # Workers update JSON files
```

### 6. SpeedAnalyzer (simulation/analyzer.py)

Analyzes traffic data and violations.

```python
class SpeedAnalyzer:
    def __init__(self, data_queue):
        # Monitor data queue
        
    def analyze(self):
        """Analyze vehicle speeds and violations"""
        # Calculate violation statistics
        # Determine fine amounts
        # Apply penalty multipliers
```

## JSON Data Files

### Accessed by GUI Auto-Refresh

**data_files/tickets.json** - All detected violations
```python
# Read every 500ms in auto_refresh()
violations = json.load(open("data_files/tickets.json"))
# Structure: List of violation dicts with nested structure
```

**data_files/traffic_data.json** - All vehicles processed
```python
# Read every 500ms in auto_refresh()
vehicles = json.load(open("data_files/traffic_data.json"))
# Structure: List of vehicle dicts
```

**data_files/worker_status.json** - Current sensor status
```python
# Read every 500ms in auto_refresh()
worker_statuses = json.load(open("data_files/worker_status.json"))
# Structure: Dict with keys "0"-"4" for each sensor
# Values: {"status": "IDLE/CHECKING", "vehicle": {...}}
```

## Data Transformation Methods

### _flatten_violation(violation: Dict) -> Dict

Converts nested JSON violation structure to flat GUI structure.

```python
def _flatten_violation(self, violation: Dict) -> Dict:
    """
    Input (from JSON file):
    {
        "license_plate": "B 1234 ABC",
        "fine": {"base_fine": 50, "total_fine": 75},
        "owner": {"id": "123", "name": "John"},
        "registration": {"stnk_status": "Active"}
    }
    
    Output (for GUI):
    {
        "license_plate": "B 1234 ABC",
        "fine_amount": 75,
        "base_fine": 50,
        "owner_name": "John",
        "owner_id": "123",
        "stnk_status": "Active",
        ... (all fields flattened)
    }
    """
```

### _convert_region_code_to_name(value: str) -> str

Converts single/double letter region codes to full names.

```python
# Input: "B"
# Output: "Jakarta (DKI)"

# Input: "AB"  
# Output: "Yogyakarta"
```

## Signal/Slot Connections

### SignalEmitter (PyQt5 Signals)

```python
class SignalEmitter(QObject):
    violation_detected = pyqtSignal(dict)        # New violation found
    simulation_started = pyqtSignal()            # Simulation started
    simulation_stopped = pyqtSignal()            # Simulation stopped
    stats_updated = pyqtSignal(dict)            # Stats updated
    simulation_finished = pyqtSignal()          # Simulation finished
```

### Connected Slots

```python
# In start_simulation():
self.simulation_worker.emitter.violation_detected.connect(self.on_violation_detected)
self.simulation_worker.emitter.stats_updated.connect(self.on_stats_updated)
self.simulation_worker.emitter.simulation_finished.connect(self.on_simulation_finished)
```

## Configuration Constants

```python
# In gui_traffic_simulation.py (top of file)
USD_TO_IDR = 15500  # 1 USD = 15,500 IDR

# In TrafficSimulationGUI.__init__():
self.refresh_timer.setInterval(500)  # Auto-refresh every 500ms

# In auto_refresh():
# 5 sensors: range(1, 6) -> Sensor 1-5
for sensor_id in range(1, 6):
    worker_key = str(sensor_id - 1)  # Maps to "0"-"4" in worker_status.json
```

## Example Usage

```python
# Start GUI
python gui_traffic_simulation.py

# In code:
from gui_traffic_simulation import TrafficSimulationGUI
from PyQt5.QtWidgets import QApplication

app = QApplication([])
gui = TrafficSimulationGUI()
gui.show()
app.exec_()
```

## Error Handling

All methods use try-except with silent fail for JSON read errors:

```python
try:
    violations = json.load(file)
except:
    violations = []  # Silent fail - returns empty list
```

This prevents crashes when data files are being written by simulation.
GET /reports/daily?date=2024-01-26
```

#### Monthly Report
```
GET /reports/monthly?year=2024&month=1
```

#### Export Data
```
GET /reports/export?format=csv&type=violations
```

Formats: csv, pdf, excel

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Description of the error",
    "details": {}
  }
}
```

## Rate Limiting

API is rate limited to 1000 requests per hour per IP address.

## Pagination

Responses use limit/offset pagination:
- `limit`: Items per page
- `offset`: Number of items to skip
- `total`: Total number of items available
