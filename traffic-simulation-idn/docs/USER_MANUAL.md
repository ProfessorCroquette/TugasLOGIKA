# User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [CLI Interface](#cli-interface)
3. [GUI Interface](#gui-interface)
4. [Managing Data](#managing-data)
5. [Generating Reports](#generating-reports)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- At least 4GB RAM
- Network connection for API features

### First Run

After installation, start the application from the project root directory:

**GUI:**
```bash
python gui_traffic_simulation.py
```

**CLI:**
```bash
python main.py
```

## CLI Interface

### Help Command
```bash
python main.py --help
```

**Note:** The CLI provides access to core simulation functions. The main simulation runs through the GUI application or CLI script.

### Start Simulation
```bash
python main.py
```

The main.py script runs the core traffic simulation engine that:
- Generates synthetic vehicle data
- Detects speed violations
- Analyzes traffic patterns
- Updates JSON data files (traffic_data.json, tickets.json)

### Generate Reports
Reports are generated through the GUI interface:
1. Launch GUI: `python gui_traffic_simulation.py`
2. Navigate to Reports tab
3. Select date range and report type
4. Export in desired format (CSV, JSON, etc.)

### Managing Vehicles & Violations
All vehicle and violation management is done through the GUI:
1. Launch: `python gui_traffic_simulation.py`
2. Use the Violations tab to view/add vehicles and violations
3. View detailed information by clicking on table rows
4. Right-click for additional options

## GUI Interface

### Main Window - Sistem Monitoring Pelanggaran Lalu Lintas Indonesia

The GUI provides real-time traffic violation monitoring with an integrated dashboard and violations table.

#### Left Panel: Control & Statistics
**Kontrol Simulasi (Simulation Control):**
- **Mulai Simulasi** (Start Simulation) - Green button
- **Hentikan Simulasi** (Stop Simulation) - Red button
- **Hapus Data** (Clear Data) - Delete all violations and vehicle records

**Statistik Real-time (Real-time Statistics):**
- **Total Pelanggaran** - Count of all detected violations
- **Kendaraan Diproses** - Total vehicles processed through sensors
- **Total Denda (IDR)** - Sum of all fines in Indonesian Rupiah
- **Rata-rata Kecepatan** - Average speed of all checked vehicles
- **Kecepatan Maksimal** - Maximum speed detected

**Status Pemeriksaan Real-time (5 Sensor):**
- 5 individual sensor panels (Sensor 1-5)
- Each shows: Status (IDLE/SAFE/VIOLATION), License Plate, Speed, Fine Amount
- Real-time color updates: IDLE (gray), SAFE (green), VIOLATION (red)

#### Right Panel: Violations Table
- **Plat Nomor** (License Plate)
- **Pemilik** (Owner Name)
- **Kecepatan** (Speed in km/h)
- **Denda (IDR)** (Fine in Indonesian Rupiah - shown in red)
- **Status STNK** (Vehicle Registration Status - shows Non-Active if expired)
- **Detail** (View Details button) - Opens violation details dialog

### Using the GUI Dashboard

1. **Start Simulation**
   - Click "Mulai Simulasi" button
   - System generates vehicles through 5 parallel sensors
   - Violations are detected and displayed in real-time
   - Statistics update every 500ms

2. **View Violations**
   - Violations appear in the right panel table
   - Click "Lihat" (Detail) button for complete violation information
   - Detail dialog shows: Plate, Owner Info, Vehicle Type, Speed, Fine Calculation
   - Fine Calculation shows: Base Fine (USD/IDR), Penalty Multiplier, Total Fine

3. **Stop Simulation**
   - Click "Hentikan Simulasi" button
   - Statistics remain displayed (don't reset)
   - Data persists in JSON files
   - Can resume simulation later

4. **Clear All Data**
   - Click "Hapus Data" button
   - Confirms deletion before removing all violations and vehicles
   - Clears tickets.json and traffic_data.json
   - Statistics reset to zero

### Real-Time Data Files Updated

During simulation, the following JSON files are continuously updated:
- **data_files/tickets.json** - All detected violations with complete details
- **data_files/traffic_data.json** - All vehicles processed
- **data_files/worker_status.json** - Current status of each sensor's work

### Violation Detail Dialog - Pengaturan Denda

Shows detailed information for each violation:
1. **Informasi Umum** (General Info)
   - License Plate
   - Owner Name/ID
   - Vehicle Type (Mobil/Motor/Truck)
   - Region (from NIK)
   - Timestamp

2. **Perhitungan Denda** (Fine Calculation)
   - Denda Dasar (Base Fine) in USD and IDR
   - Pengali Penalti (Penalty Multiplier) - highlighted if > 1.0
   - Total Denda (Total Fine) in USD and IDR

## Managing Data

### Violation Detail Structure

When you click "Lihat" (Detail) button, the dialog displays:

```
INFORMASI UMUM
- Plat Nomor: B 1234 ABC (License plate format)
- Pemilik: John Doe
- ID Pemilik: 3275123456789012
- Wilayah: B = Jakarta (DKI)
- Tipe Kendaraan: Mobil / Motor / Truck
- Waktu: 2026-01-29 10:30:45

PERHITUNGAN DENDA
- Denda Dasar: $50.00 / Rp 775,000
- Pengali Penalti: 1.5x (highlighted if > 1.0)
- Total Denda: $75.00 / Rp 1,162,500
```

### JSON Data File Formats

**tickets.json Structure (Violations):**
```json
[
  {
    "license_plate": "B 1234 ABC",
    "speed": 85,
    "timestamp": "2026-01-29T10:30:45",
    "vehicle_type": "Mobil",
    "fine_amount": 50,
    "penalty_multiplier": 1.5,
    "owner": {
      "id": "3275123456789012",
      "name": "John Doe",
      "region": "B"
    },
    "registration": {
      "stnk_status": "Active",
      "sim_status": "Active"
    },
    "fine": {
      "base_fine": 50,
      "penalty_multiplier": 1.5,
      "total_fine": 75
    }
  }
]
```

**traffic_data.json Structure (Vehicles):**
```json
[
  {
    "license_plate": "B 1234 ABC",
    "speed": 85,
    "timestamp": "2026-01-29T10:30:45",
    "vehicle_type": "Mobil",
    "vehicle_make": "Toyota",
    "vehicle_model": "Avanza",
    "owner": {
      "id": "3275123456789012",
      "name": "John Doe"
    }
  }
]
```

**worker_status.json Structure (Sensor Status):**
```json
{
  "0": {
    "status": "CHECKING",
    "vehicle": {
      "license_plate": "B 1234 ABC",
      "speed": 85
    }
  },
  "1": {
    "status": "IDLE",
    "vehicle": null
  }
}
```

### Auto-Refresh Mechanism

The GUI auto-refreshes every 500ms:
- Reads JSON files from disk
- Updates violations table if count changed
- Always updates vehicle counter
- Updates sensor status panels (IDLE/SAFE/VIOLATION)
- Recalculates statistics (fines, speeds)
- Converts nested JSON structure to flat GUI format
3. Confirm deletion

## Generating Reports

### Daily Report
1. Go to Reports tab
2. Select date
3. Click "Generate Daily"
4. Choose format (CSV, PDF, Excel)
5. Click "Export"

### Monthly Report
1. Go to Reports tab
2. Select month and year
3. Click "Generate Monthly"
4. Select export format
5. Click "Export"

### Custom Report
1. Click "Custom Report" button
2. Set filters:
   - Date range
   - Violation type
   - Location
   - Vehicle type
3. Click "Preview"
4. Click "Export"

## Log Management

### Automatic Log Cleanup
The application automatically manages log files to prevent disk space issues:
- **Max Log Files**: System keeps maximum 10 log files
- **Cleanup Trigger**: Runs automatically on application startup
- **Log Location**: `logs/` directory
- **Log Format**: `simulation_YYYYMMDD_HHMMSS.log`

When you start the application:
- If log count exceeds 10, oldest logs are automatically deleted
- Console output shows: `[LOG CLEANUP] Deleted old log: filename`
- This prevents unlimited disk space usage from long-running simulations

### Viewing Logs
```bash
# View latest log file (on Windows)
tail -f logs/simulation_*.log

# List all log files
ls -lah logs/
```

## Troubleshooting

### Application Won't Start
- Check Python version: `python --version` (should be 3.9+)
- Verify dependencies: `pip install -r requirements.txt`
- Check .env file exists and is valid

### Database Connection Error
- Verify MySQL is running
- Check credentials in .env
- Verify config/database.py has correct settings

### GUI Looks Wrong
- Check screen resolution (recommended 1920x1080+)
- Try different theme in Settings
- Restart application

### Slow Performance
- Reduce vehicle count in simulation
- Close other applications
- Check available RAM
- Verify MySQL performance

### Cannot Export Reports
- Check write permissions on outputs/ directory
- Verify disk space available
- Check if office software is installed for Excel export

## Getting Help

- See [Setup Guide](SETUP_GUIDE.md) for installation help
- Review [Architecture](ARCHITECTURE.md) for system design
- Check log files in `logs/` directory for debugging
- Visit project GitHub at https://github.com/ProfessorCroquette/TugasLOGIKA for issue reporting
