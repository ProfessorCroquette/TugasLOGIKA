# Logic and Code Explanation

**Document:** Complete Logic, File Purpose, and Critical Code Analysis  
**Date:** February 4, 2026 02:30 AM  
**Project:** Indonesian Traffic Violation Simulation System  

---

## Table of Contents

1. [Logical Reasoning in the System](#logical-reasoning)
2. [File Purpose and Responsibility](#file-purposes)
3. [Critical Code Snippets](#critical-code-snippets)
4. [Data Flow Logic](#data-flow-logic)
5. [Decision Logic Trees](#decision-logic-trees)

---

## Logical Reasoning

### Modus Ponens Logic Applied

**Definition:** If P then Q. P is true. Therefore, Q is true.

**Applied in Speed Violation Detection:**

```
P1: If (vehicle_speed > speed_limit) then (vehicle_violates_speed_law)
P2: vehicle_speed = 85 km/h AND speed_limit = 100 km/h
P3: 85 > 100 is FALSE
Conclusion: vehicle_violates_speed_law is TRUE → Issue violation ticket
```

**Code Location:** `simulation/analyzer.py`

```python
def detect_violation(vehicle):
    """
    Modus Ponens: 
    P1: If speed > limit then violation
    P2: Check if speed > limit  
    Conclusion: If true, violation detected
    """
    speed_limit = 75  # km/h
    
    # Premise P1: If vehicle_speed > speed_limit, then violation
    if vehicle['speed'] > speed_limit:  # P2: Check premise P1
        # Conclusion: Violation is true
        violation = {
            'license_plate': vehicle['license_plate'],
            'speed': vehicle['speed'],
            'violation_type': 'SPEEDING'
        }
        return violation
    
    return None  # No violation (conclusion false)
```

**Logical Chain:**
```
IF speed > 100 THEN violation (for cars)
    ↓
speed = 85 (FALSE)
    ↓
violation = FALSE
    ↓
NO TICKET
```

---

### Modus Tollens Logic Applied

**Definition:** If P then Q. Q is false. Therefore, P is false.

**Applied in Registration Status Check:**

```
P1: If (STNK_status == 'Non-Active') then (vehicle_cannot_drive)
P2: vehicle_can_drive is FALSE (observed: vehicle on road)
Conclusion (by Tollens): STNK_status is not 'Non-Active'
```

**Code Location:** `utils/violation_utils.py`

```python
def check_registration_validity(vehicle):
    """
    Modus Tollens:
    P1: If STNK is non-active, then vehicle shouldn't be on road
    P2: Vehicle IS on road (observed)
    Conclusion: Either STNK is active OR violation occurred
    """
    stnk_status = vehicle['registration']['stnk_status']
    
    # P1: If non-active, then should not drive
    if stnk_status == 'Non-Active':
        # Conclusion: Vehicle shouldn't be here (violation)
        return {
            'is_valid': False,
            'reason': 'Non-Active STNK',
            'violation': True
        }
    
    # Tollens: Vehicle is driving, so STNK must be active
    return {
        'is_valid': True,
        'reason': 'Active STNK',
        'violation': False
    }
```

**Logical Chain (Tollens):**
```
IF non-active THEN shouldn't drive
    ↓
Vehicle IS driving (observed)
    ↓
BY TOLLENS: NOT non-active
    ↓
STNK must be active
```

---

### Complex Logic: Fine Calculation with Conditional Reasoning

**Logic Applied:**

```
Base Fine is determined by:
  IF vehicle_type == 'Mobil'       THEN base_fine = $50
  IF vehicle_type == 'Motor'       THEN base_fine = $25
  IF vehicle_type == 'Truck'       THEN base_fine = $100

Penalty Multiplier determined by:
  IF STNK_status == 'Non-Active'   THEN multiplier = 1.4x
  IF speed > 85 km/h               THEN multiplier = 1.2x
  ELSE                             THEN multiplier = 1.0x

Total Fine = base_fine × multiplier × USD_TO_IDR
```

**Code Location:** `utils/violation_utils.py`

```python
def calculate_fine(violation):
    """
    Logical Decision Tree for Fine Calculation
    
    1. Determine base fine by vehicle type
    2. Determine multiplier by violation severity
    3. Calculate total in USD then convert to IDR
    """
    # Step 1: Base Fine Logic (Conditional P1)
    vehicle_type = violation['vehicle_type']
    
    base_fine_usd = {
        'Mobil': 50,      # Cars: $50
        'Motor': 25,      # Motorcycles: $25
        'Truck': 100      # Trucks: $100
    }.get(vehicle_type, 50)  # Default: $50
    
    # Step 2: Penalty Multiplier Logic (Nested Conditionals)
    stnk_status = violation['registration']['stnk_status']
    speed = violation['speed']
    
    # Modus Tollens: If STNK inactive, then more severe penalty
    if stnk_status == 'Non-Active':
        # CONCLUSION: Heavy penalty (1.4x)
        multiplier = 1.4
    # Else if excessive speeding (85+ km/h)
    elif speed > 85:
        # CONCLUSION: Moderate penalty (1.2x)
        multiplier = 1.2
    else:
        # CONCLUSION: Standard fine (1.0x)
        multiplier = 1.0
    
    # Step 3: Calculate Total
    total_fine_usd = base_fine_usd * multiplier
    total_fine_idr = total_fine_usd * 15500  # USD_TO_IDR
    
    return {
        'base_fine': base_fine_usd,
        'penalty_multiplier': multiplier,
        'total_fine': total_fine_usd,
        'total_fine_idr': total_fine_idr
    }
```

**Logical Truth Table:**

| Vehicle Type | STNK Status  | Speed  | Base Fine | Multiplier | Total |
|--------------|-------------|--------|-----------|-----------|--------|
| Mobil        | Active      | 76     | $50       | 1.0x      | $50    |
| Mobil        | Active      | 90     | $50       | 1.2x      | $60    |
| Mobil        | Non-Active  | 76     | $50       | 1.4x      | $70    |
| Mobil        | Non-Active  | 90     | $50       | 1.4x      | $70    |
| Motor        | Active      | 76     | $25       | 1.0x      | $25    |
| Truck        | Active      | 90     | $100      | 1.2x      | $120   |

---

## File Purposes

### 1. gui_traffic_simulation.py (950+ lines)

**Purpose:** Real-time GUI dashboard for monitoring violations

**Main Responsibilities:**
- Display violations in real-time
- Show live statistics
- Manage user interactions (Start/Stop buttons)
- Auto-refresh from JSON files every 500ms
- Show 5 sensor statuses
- Display detail dialogs

**Key Classes:**

#### TrafficSimulationGUI

```python
class TrafficSimulationGUI(QMainWindow):
    """
    Main GUI window - 1400x800 pixels
    
    Responsibility: 
    - Initialize UI with all components
    - Manage simulation start/stop
    - Auto-refresh data every 500ms
    - Display violations table
    - Show real-time statistics
    """
    
    def __init__(self):
        # Initialize GUI window with two panels:
        # Left: Controls + Statistics + 5 Sensor panels
        # Right: Violations table
        
    def auto_refresh(self):
        # Called every 500ms
        # 1. Read JSON files
        # 2. Check if data changed
        # 3. Update table if needed
        # 4. Update sensor displays
        # 5. Recalculate statistics
```

**Critical Logic in `auto_refresh()`:**

```python
def auto_refresh(self):
    """
    Core Logic: File-based data synchronization
    
    Modus Ponens Applied:
    P1: If file was modified, then data changed
    P2: File modification time > last_check_time
    Conclusion: Update display
    """
    # Read violations from JSON file
    with open("data_files/tickets.json", 'r') as f:
        violations = json.load(f) or []
    
    # Modus Ponens: If count changed, THEN update table
    viol_count = len(violations)
    if viol_count != self.last_violation_count:
        # Conclusion: Data changed, update GUI
        self.violations = [self._flatten_violation(v) for v in violations]
        self.refresh_violations_table()  # Update table display
        self.last_violation_count = viol_count  # Update counter
    
    # Update vehicle count (always, every refresh)
    vehicles = json.load(open("data_files/traffic_data.json"))
    vehicle_count = len(vehicles)
    self.vehicles_count_label.setText(str(vehicle_count))
    
    # Update statistics from violation data
    total_fines = sum(v.get('fine_amount', 0) for v in violations)
    self.total_fines_label.setText(f"Rp {total_fines * USD_TO_IDR:,.0f}")
    
    # Calculate speeds
    speeds = [v.get('speed', 0) for v in violations]
    if speeds:
        avg_speed = sum(speeds) / len(speeds)
        max_speed = max(speeds)
        self.avg_speed_label.setText(f"{avg_speed:.1f} km/h")
        self.max_speed_label.setText(f"{max_speed:.1f} km/h")
```

---

### 2. main.py (275 lines)

**Purpose:** Simulation engine that runs in background

**Main Responsibilities:**
- Generate vehicles continuously
- Detect violations
- Process 5 sensors in parallel
- Analyze speed patterns
- Update JSON files
- Coordinate all simulation components

**Key Class:**

#### SpeedingTicketSimulator

```python
class SpeedingTicketSimulator:
    """
    Main Simulation Controller
    
    Responsibility:
    - Create data queue for communication
    - Initialize TrafficSensor (vehicle generator)
    - Initialize QueuedCarProcessor (5 workers)
    - Initialize SpeedAnalyzer (analysis)
    - Initialize Dashboard (console output)
    - Manage threads and graceful shutdown
    """
    
    def __init__(self):
        # 1. Setup queue (max 500 items)
        self.data_queue = queue.Queue(maxsize=500)
        
        # 2. Create processor with 5 workers
        self.car_processor = QueuedCarProcessor(num_workers=5)
        
        # 3. Create sensor that puts data in queue
        self.sensor = TrafficSensor(self.data_queue, 
                                    car_processor=self.car_processor)
        
        # 4. Create analyzer that monitors queue
        self.analyzer = SpeedAnalyzer(self.data_queue)
```

**Data Flow Logic:**

```
┌─────────────────────────────────────┐
│ TrafficSensor.generate_vehicles()   │
│ Creates vehicle every N milliseconds│
└────────────────┬────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   data_queue        │
        │   (max 500 items)   │
        └────────┬────────────┘
                 │
        ┌────────┴──────────────┐
        │                       │
        ▼                       ▼
    Worker 1-5             SpeedAnalyzer
    (Process vehicles)      (Monitor queue)
    └──────────┬───────────────┘
               │
               ▼
    Write to JSON files:
    - tickets.json
    - traffic_data.json
    - worker_status.json
```

---

### 3. simulation/sensor.py

**Purpose:** Generate vehicle data continuously

**Main Responsibility:**
- Create random vehicles
- Assign speeds and attributes
- Detect violations
- Put vehicle data in queue

**Critical Code:**

```python
class TrafficSensor:
    """
    Vehicle Generation Engine
    
    Logic: Modus Ponens
    P1: If random value < threshold, THEN generate vehicle
    P2: Generate random values continuously
    Conclusion: Vehicles generated continuously
    """
    
    def generate_vehicles(self):
        """
        Continuous vehicle generation loop
        
        Logic Flow:
        1. Generate random vehicle attributes
        2. Check: speed > limit? → Violation
        3. Put in queue
        """
        while self.running:
            # Generate vehicle
            vehicle = {
                'license_plate': self._generate_plate(),
                'speed': random.randint(40, 120),  # 40-120 km/h
                'vehicle_type': self._random_vehicle_type(),
                'owner': self._generate_owner(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Put in queue for processors
            try:
                self.data_queue.put(vehicle, timeout=1)
            except queue.Full:
                pass  # Queue full, skip this vehicle
            
            # Wait before next vehicle
            time.sleep(self.interval)
```

---

### 4. simulation/queue_processor.py

**Purpose:** Process vehicles through 5 parallel workers

**Main Responsibility:**
- Manage worker threads
- Process vehicles from queue
- Detect violations
- Write to JSON files
- Update sensor status

**Critical Logic:**

```python
class QueuedCarProcessor:
    """
    5-Worker Parallel Processing System
    
    Logic: Concurrent Modus Ponens
    P1: For each worker: If vehicle in queue THEN process it
    P2: 5 workers checking queue simultaneously
    Conclusion: Up to 5 vehicles processed in parallel
    """
    
    def __init__(self, num_workers=5):
        self.workers = []
        
        # Create 5 worker threads
        for i in range(num_workers):
            worker = threading.Thread(
                target=self._worker_process,
                args=(i,)  # Worker ID 0-4
            )
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def _worker_process(self, worker_id):
        """
        Individual worker logic
        
        Modus Ponens:
        P1: If vehicle in queue THEN process it
        P2: Worker monitors queue continuously
        Conclusion: Vehicle processed
        """
        while self.running:
            try:
                # Get vehicle from queue
                vehicle = self.data_queue.get(timeout=1)
                
                # LOGIC: Detect violation
                is_violation = self._detect_violation(vehicle)
                
                # LOGIC: Calculate fine
                if is_violation:
                    fine = self._calculate_fine(vehicle)
                    
                    # Write to tickets.json
                    self._write_violation(vehicle, fine)
                
                # Update worker status
                self._update_worker_status(worker_id, vehicle)
                
                # Mark task done
                self.data_queue.task_done()
                
            except queue.Empty:
                continue
    
    def _detect_violation(self, vehicle):
        """
        Violation Detection Logic
        
        Modus Ponens:
        P1: If speed > 60 km/h THEN violation
        P2: Check vehicle speed
        Conclusion: violation = (speed > 60)
        """
        speed_limit = 60  # km/h
        return vehicle['speed'] > speed_limit
```

---

### 5. simulation/analyzer.py

**Purpose:** Analyze traffic patterns and statistics

**Main Responsibility:**
- Monitor data queue
- Calculate speed statistics
- Detect violation patterns
- Analyze traffic trends

**Critical Code:**

```python
class SpeedAnalyzer:
    """
    Traffic Analysis Engine
    
    Responsibility:
    - Monitor data queue for patterns
    - Calculate statistics
    - Detect trends
    """
    
    def analyze(self):
        """
        Statistical Analysis Logic
        
        Modus Ponens:
        P1: If average speed > 70 THEN traffic is speeding
        P2: Calculate average speed from violations
        Conclusion: Report traffic pattern
        """
        speeds = []
        
        # Collect speed data
        while not self.data_queue.empty():
            try:
                vehicle = self.data_queue.get_nowait()
                speeds.append(vehicle['speed'])
            except queue.Empty:
                break
        
        # Analyze speeds
        if speeds:
            # Modus Ponens: If avg > 70, then speeding pattern
            avg_speed = sum(speeds) / len(speeds)
            if avg_speed > 70:
                print(f"⚠️ Speeding pattern detected: avg {avg_speed:.1f}")
            
            # Calculate violation percentage
            violations = sum(1 for s in speeds if s > 60)
            violation_rate = (violations / len(speeds)) * 100
            
            return {
                'average_speed': avg_speed,
                'max_speed': max(speeds),
                'violation_count': violations,
                'violation_rate': violation_rate
            }
```

---

### 6. utils/generators.py

**Purpose:** Generate random vehicle and owner data

**Main Responsibility:**
- Create vehicle objects with random attributes
- Generate owner data with 16-digit NIK
- Assign vehicle types (50/40/5/5 distribution)
- Generate license plates

**Critical Logic:**

```python
class DataGenerator:
    """
    Random Data Generation
    
    Logic: Probability Distribution
    P1: If random < 0.5 THEN vehicle_type = 'Mobil' (50%)
    P2: If random 0.5-0.9 THEN vehicle_type = 'Truck' (40%)
    P3: If random 0.9-0.95 THEN vehicle_type = 'Pemerintah' (5%)
    P4: If random > 0.95 THEN vehicle_type = 'Kedutaan' (5%)
    """
    
    @staticmethod
    def generate_vehicle_batch():
        """
        Generate vehicles with distribution
        
        Logical Distribution:
        50% Mobil (Private cars)
        40% Barang/Truk (Goods/Trucks)
        5% Pemerintah (Government)
        5% Kedutaan (Embassy)
        """
        vehicles = []
        
        for _ in range(100):
            rand = random.random()
            
            # Modus Ponens decision tree
            if rand < 0.5:
                # Conclusion: Mobil
                vehicle_type = 'Mobil'
            elif rand < 0.9:
                # Conclusion: Truck
                vehicle_type = 'Truck'
            elif rand < 0.95:
                # Conclusion: Government
                vehicle_type = 'Pemerintah'
            else:
                # Conclusion: Embassy
                vehicle_type = 'Kedutaan'
            
            # Generate vehicle
            vehicle = {
                'vehicle_type': vehicle_type,
                'license_plate': PlateGenerator.generate(),
                'owner': OwnerGenerator.generate_with_nik(),
                'speed': random.randint(40, 120)
            }
            
            vehicles.append(vehicle)
        
        return vehicles
```

---

### 7. utils/indonesian_plates.py

**Purpose:** Generate Indonesian license plates

**Main Responsibility:**
- Create plate format: [Region] [4-digits] [3-letters]
- Support 30+ Indonesian regions
- Map region codes to province names

**Critical Code:**

```python
class PlateGenerator:
    """
    Indonesian License Plate Generation
    
    Logic: Modus Ponens + Lookup Table
    P1: If region code exists in table THEN use mapped region
    P2: Lookup region code
    Conclusion: Generate plate with region prefix
    """
    
    REGION_MAP = {
        'B': 'Jakarta (DKI)',
        'D': 'Bandung (Jawa Barat)',
        'H': 'Semarang (Jawa Tengah)',
        'AB': 'Yogyakarta',
        'L': 'Surabaya (Jawa Timur)',
        # ... 25+ more regions
    }
    
    @staticmethod
    def generate():
        """
        Generate plate: REGION DIGITS LETTERS
        Example: B 1234 ABC (Jakarta)
        
        Logic:
        1. Pick random region code
        2. Generate 4 random digits
        3. Generate 3 random letters
        4. Format as: REGION DIGITS LETTERS
        """
        region = random.choice(list(PlateGenerator.REGION_MAP.keys()))
        digits = f"{random.randint(1000, 9999)}"
        letters = ''.join(
            [chr(random.randint(ord('A'), ord('Z'))) for _ in range(3)]
        )
        
        return f"{region} {digits} {letters}"
    
    @staticmethod
    def get_region_name(region_code):
        """
        Lookup Logic: Modus Ponens
        P1: If code in map THEN return mapped name
        P2: Look up code
        Conclusion: Return region name or 'Unknown'
        """
        return PlateGenerator.REGION_MAP.get(region_code, 'Tidak Diketahui')
```

---

### 8. utils/violation_utils.py

**Purpose:** Calculate fines based on violations

**Main Responsibility:**
- Determine base fine by vehicle type
- Apply penalty multipliers
- Convert USD to IDR
- Calculate final fine amount

**Critical Fine Calculation Logic:**

```python
def calculate_fine(vehicle, speed):
    """
    Fine Calculation Logic Tree
    
    Step 1: Determine Base Fine (Vehicle Type)
    Step 2: Determine Multiplier (Violation Severity)
    Step 3: Calculate Total (base × multiplier × exchange_rate)
    """
    
    # Step 1: Base Fine - Vehicle Type Logic
    # Modus Ponens: If type = X THEN fine = Y
    base_fines = {
        'Mobil': 50,           # Cars: $50
        'Motor': 25,           # Motorcycles: $25  
        'Truck': 100,          # Trucks: $100
        'Pemerintah': 75,      # Government: $75
        'Kedutaan': 100        # Embassy: $100
    }
    
    base_fine = base_fines.get(vehicle['vehicle_type'], 50)
    
    # Step 2: Penalty Multiplier - Violation Severity
    # Nested Modus Ponens
    stnk_status = vehicle.get('stnk_status', 'Active')
    speed_limit = 60
    
    if stnk_status == 'Non-Active':
        # Tollens: Registration non-active = heavy penalty
        multiplier = 1.4  # 40% increase
    elif speed > 85:
        # Excessive speeding penalty
        multiplier = 1.2  # 20% increase
    else:
        # Normal violation
        multiplier = 1.0  # No increase
    
    # Step 3: Calculate Total
    total_usd = base_fine * multiplier
    total_idr = total_usd * 15500  # USD_TO_IDR constant
    
    return {
        'base_fine_usd': base_fine,
        'penalty_multiplier': multiplier,
        'total_fine_usd': total_usd,
        'total_fine_idr': total_idr
    }
```

---

### 9. config/__init__.py

**Purpose:** Configuration management

**Main Responsibility:**
- Define system constants
- Create directories
- Setup logging
- Manage configuration values

**Critical Code:**

```python
class Config:
    """
    System Configuration
    
    Constants and Setup
    """
    
    # Simulation settings
    SIMULATION_INTERVAL = 3  # seconds between batches (3 seconds for target flow)
    SPEED_LIMIT = 75  # km/h - standard speed limit for regular roads
    MIN_SPEED_LIMIT = 40  # km/h - minimum safe speed
    MIN_VEHICLES_PER_BATCH = 10  # at least 10 cars per batch
    MAX_VEHICLES_PER_BATCH = 15  # max 15 per batch for consistent violations
    
    # Speed distribution (normal distribution)
    SPEED_MEAN = 70  # average speed around 70 km/h (below limit)
    SPEED_STD_DEV = 8  # moderate variation in speeds (realistic)
    MIN_SPEED = 45
    MAX_SPEED = 95  # Allow speeds above 75 for natural violations
    
    # Vehicle type distribution (percentages)
    VEHICLE_TYPES = {
        "car": 60,
        "truck": 20,
        "motorcycle": 15,
        "bus": 5
    }
    
    # Currency conversion (DEFINE FIRST - used in fine calculations)
    USD_TO_IDR = 15500  # 1 USD = 15,500 IDR
    
    # Fines structure (in USD, converted to IDR in GUI)
    # Maximum fine: Rp 1,250,000
    # Fines are tiered based on severity of violation
    FINES = {
        "SPEED_LOW_MILD": {"min": 30, "max": 39, "fine": 20, "description": "Terlalu lambat"},
        "SPEED_LOW_SEVERE": {"min": 0, "max": 29, "fine": 35, "description": "Terlalu lambat berat"},
        "SPEED_HIGH_LEVEL_1": {"min": 76, "max": 90, "fine": 30, "description": "Melampaui batas 1-15 km/h"},
        "SPEED_HIGH_LEVEL_2": {"min": 91, "max": 110, "fine": 50, "description": "Melampaui batas 16-35 km/h"},
        "SPEED_HIGH_LEVEL_3": {"min": 111, "max": 130, "fine": 75, "description": "Melampaui batas 36+ km/h"}
    }
    
    # Maximum fine per law
    MAX_FINE_IDR = 1250000  # Rp 1,250,000 - maximum penalty
    MAX_FINE_USD = MAX_FINE_IDR / USD_TO_IDR  # ~USD 80.65
    
    # Output directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    DATA_DIR = os.path.join(BASE_DIR, "data_files")
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
```

---

## Critical Code Snippets

### 1. Violation Detection (Modus Ponens)

**File:** `simulation/queue_processor.py`

```python
def _detect_violation(self, vehicle):
    """
    Core Violation Detection Logic
    
    Logical Form (Modus Ponens):
    P1: If vehicle_speed > speed_limit → violation
    P2: vehicle_speed = 85, speed_limit = 60
    Therefore: violation = TRUE
    """
    SPEED_LIMIT = 60  # km/h
    
    # Premise check
    if vehicle['speed'] > SPEED_LIMIT:
        return True  # Violation detected
    
    return False  # No violation
```

**How It Works:**
1. Set speed limit (60 km/h)
2. Get vehicle speed from data
3. Compare: if speed > limit → violation = True
4. Return violation status

---

### 2. Penalty Multiplier (Nested Conditionals)

**File:** `utils/violation_utils.py`

```python
def apply_penalty_multiplier(violation):
    """
    Nested Conditional Logic
    
    Priority-based decision:
    1. Check registration status (highest priority)
    2. Check speed severity (medium priority)  
    3. Default: standard fine
    """
    stnk = violation['registration']['stnk_status']
    speed = violation['speed']
    
    # Primary condition: Registration status
    # Modus Tollens: If non-active, extra penalty
    if stnk == 'Non-Active':
        return 1.4  # 40% penalty
    
    # Secondary condition: Speed severity
    # Modus Ponens: If high speed, moderate penalty
    if speed > 85:
        return 1.2  # 20% penalty
    
    # Default: No penalty
    return 1.0
```

**Decision Tree:**
```
Is STNK Non-Active?
├─ YES → 1.4x multiplier (highest penalty)
└─ NO  → Is speed > 85?
        ├─ YES → 1.2x multiplier (moderate penalty)
        └─ NO  → 1.0x multiplier (standard fine)
```

---

### 3. Auto-Refresh Logic (File Synchronization)

**File:** `gui_traffic_simulation.py`

```python
def auto_refresh(self):
    """
    Real-time Data Synchronization Logic
    
    Modus Ponens:
    P1: If violation_count_changed THEN update_table
    P2: Check count before and after
    Therefore: Update if different
    """
    # Read current state
    violations = json.load(open("data_files/tickets.json"))
    viol_count = len(violations)
    
    # Modus Ponens: If count different, update
    if viol_count != self.last_violation_count:
        # Conclusion: Count changed, update display
        self.violations = violations
        self.refresh_violations_table()
        self.last_violation_count = viol_count
    
    # Always update vehicle count (no conditional)
    vehicles = json.load(open("data_files/traffic_data.json"))
    self.vehicles_count_label.setText(str(len(vehicles)))
```

**Why This Logic:**
- Violation table only updates when count changes (efficiency)
- Vehicle counter always updates (real-time)
- Prevents unnecessary UI refreshes
- Detects new violations immediately

---

### 4. Worker Status Update (Sensor Mapping)

**File:** `simulation/queue_processor.py`

```python
def _update_worker_status(self, worker_id, vehicle):
    """
    Sensor Status Update Logic
    
    Mapping Logic:
    worker_id (0-4) → worker_status.json['0'-'4']
    
    Modus Ponens:
    P1: If worker processes vehicle THEN update its status
    P2: Worker_id exists
    Therefore: Update worker status in JSON
    """
    # Read current status
    with open("data_files/worker_status.json", 'r') as f:
        statuses = json.load(f) or {}
    
    # Update this worker's status
    # Key: string version of worker_id (0-4)
    worker_key = str(worker_id)
    
    statuses[worker_key] = {
        'status': 'CHECKING',  # Currently processing
        'vehicle': {
            'license_plate': vehicle['license_plate'],
            'speed': vehicle['speed']
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Write back to file
    with open("data_files/worker_status.json", 'w') as f:
        json.dump(statuses, f)
```

**Why Mapping is Important:**
- 5 sensors (1-5 in GUI display)
- Map to workers (0-4 in code)
- Conversion: `worker_key = str(sensor_id - 1)`
- Keeps track of which sensor is doing what

---

### 5. Vehicle Type Distribution (Probability Logic)

**File:** `utils/generators.py`

```python
def _random_vehicle_type():
    """
    Random Vehicle Type Selection
    
    Probability Distribution:
    50% → Mobil (Private cars)
    40% → Truck (Goods/trucks)
    5%  → Pemerintah (Government)
    5%  → Kedutaan (Embassy)
    
    Modus Ponens Applied Probabilistically:
    P1: If random < 0.5 THEN type = Mobil
    P2: If 0.5 ≤ random < 0.9 THEN type = Truck
    P3: If 0.9 ≤ random < 0.95 THEN type = Pemerintah
    P4: If random ≥ 0.95 THEN type = Kedutaan
    """
    rand = random.random()  # 0.0 to 1.0
    
    if rand < 0.50:
        return 'Mobil'          # 50%
    elif rand < 0.90:
        return 'Truck'          # 40%
    elif rand < 0.95:
        return 'Pemerintah'     # 5%
    else:
        return 'Kedutaan'       # 5%
```

**Why This Distribution:**
- Realistic traffic composition
- More private cars than trucks
- Government vehicles are rare
- Ensures variety in simulation

---

## Data Flow Logic

### Complete Data Flow with Logic

```
┌─────────────────────────────────────────────────────────────┐
│ START: GUI auto_refresh() called every 500ms                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────┐
    │ Read from JSON files            │
    │ - tickets.json (violations)     │
    │ - traffic_data.json (vehicles)  │
    │ - worker_status.json (status)   │
    └────────────┬────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────────┐
    │ LOGIC: Count changed?                     │
    │ Modus Ponens:                             │
    │ If violation_count ≠ last_count          │
    │ THEN update violations table              │
    └────────┬─────────────────────────────────┘
             │
    ┌────────┴──────────┐
    │ YES              NO
    │ (Count changed)  (No change)
    ▼                  ▼
Update table      Skip table update
    │                  │
    └────────┬─────────┘
             ▼
    ┌──────────────────────────────────┐
    │ LOGIC: Always update statistics   │
    │ - Vehicle counter                │
    │ - Total fines (sum all)          │
    │ - Avg speed (mean)               │
    │ - Max speed (max)                │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ LOGIC: Update sensor panels      │
    │ For each sensor (1-5):           │
    │   If worker processing vehicle   │
    │   THEN show VIOLATION/SAFE status│
    │   ELSE show IDLE status          │
    └────────┬─────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────┐
    │ Display updated GUI              │
    │ Wait 500ms                       │
    │ Loop back to START               │
    └──────────────────────────────────┘
```

---

## Decision Logic Trees

### 1. Violation Detection Decision Tree

```
Vehicle Speed Check
│
├─ Speed ≤ 60 km/h?
│  ├─ YES → NO VIOLATION
│  │        Return: violation = False
│  │        Action: Show SAFE status
│  │
│  └─ NO (Speed > 60) → VIOLATION DETECTED
│     Return: violation = True
│     Action: Create ticket
│     Next: Goto Fine Calculation
```

### 2. Fine Calculation Decision Tree

```
Fine Calculation Flow
│
├─ Step 1: Determine Base Fine by Vehicle Type
│  ├─ Mobil?        → $50
│  ├─ Motor?        → $25
│  ├─ Truck?        → $100
│  ├─ Pemerintah?   → $75
│  └─ Kedutaan?     → $100
│
├─ Step 2: Determine Multiplier by Severity
│  ├─ STNK Non-Active?
│  │  └─ YES → 1.4x (40% penalty)
│  │
│  └─ NO, Check Speed
│     ├─ Speed > 85 km/h?
│     │  └─ YES → 1.2x (20% penalty)
│     │
│     └─ NO → 1.0x (standard)
│
└─ Step 3: Calculate Total
   ├─ Total USD = Base × Multiplier
   └─ Total IDR = Total USD × 15,500
```

### 3. Vehicle Type Distribution Decision Tree

```
Random Vehicle Type Selection
│
random_value = random(0, 1)
│
├─ random_value < 0.50?
│  └─ YES → Type = Mobil (50%)
│
├─ random_value < 0.90?
│  └─ YES → Type = Truck (40%)
│
├─ random_value < 0.95?
│  └─ YES → Type = Pemerintah (5%)
│
└─ random_value ≥ 0.95?
   └─ YES → Type = Kedutaan (5%)
```

### 4. Worker Processing Decision Tree

```
QueuedCarProcessor Worker Loop
│
while running:
│
├─ Queue empty?
│  ├─ YES → Wait and retry
│  │
│  └─ NO → Get vehicle from queue
│
├─ Detect violation?
│  ├─ YES → Calculate fine
│  │        │
│  │        ├─ Determine base fine
│  │        ├─ Apply multiplier
│  │        └─ Write to tickets.json
│  │
│  └─ NO → Write to traffic_data.json
│
└─ Update worker_status.json
   └─ Mark vehicle as processed
```

---

## Complete Logic Summary

### Modus Ponens Examples in Code

**Example 1: Violation Detection**
```
P1: IF speed > 60 THEN violation
P2: speed = 85
C:  violation (TRUE)
```

**Example 2: Fine Update Needed**
```
P1: IF count_changed THEN update_table  
P2: count_changed = TRUE
C:  update_table (execute)
```

**Example 3: Penalty Multiplier**
```
P1: IF stnk_non_active THEN multiplier = 1.4
P2: stnk_status = Non-Active
C:  multiplier = 1.4
```

### Modus Tollens Examples in Code

**Example 1: Vehicle Registration Check**
```
P1: IF stnk_non_active THEN cannot_drive
P2: vehicle_IS_driving (observed)
C:  BY TOLLENS: NOT stnk_non_active
    (Registration must be active, OR violation)
```

**Example 2: Data Persistence**
```
P1: IF violation_count_increases THEN new_data_added
P2: violation_count_increased (observed)
C:  BY TOLLENS: new_data_WAS_added
```

---

## Conclusion

This system uses:
- **Modus Ponens:** Most common - "If condition then action"
- **Modus Tollens:** For validation - "Vehicle is driving, so STNK must be active"
- **Nested Conditionals:** For complex decisions (fine calculation)
- **Probability Distribution:** For realistic vehicle types
- **File Synchronization:** For GUI-Simulation communication

Every file and function follows logical reasoning to create a coherent traffic violation simulation system.