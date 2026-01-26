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

### Main Window

The GUI consists of several tabs:

#### 1. Dashboard Tab
- Real-time statistics
- Active vehicles count
- Recent violations
- System status

#### 2. Simulation Tab
- Start/Stop simulation
- Adjust vehicle count
- Set simulation parameters
- View simulation progress

#### 3. Violations Tab
- List all violations
- Filter by type, date range, vehicle
- View violation details
- Print tickets

#### 4. Reports Tab
- Generate daily/monthly reports
- Export to CSV, PDF, Excel
- View historical reports
- Compare periods

#### 5. Settings Tab
- Database configuration
- Email settings
- UI preferences
- System logging

### Using the Dashboard

1. **Start Simulation**
   - Click "Simulation" tab
   - Set vehicle count (1-500)
   - Click "Start" button
   - Monitor progress bar

2. **View Violations**
   - Click "Violations" tab
   - Use filters at top
   - Click row for details
   - Right-click for options

3. **Generate Report**
   - Click "Reports" tab
   - Select date range
   - Choose report type
   - Select export format
   - Click "Generate"

### Keyboard Shortcuts
- `Ctrl+N`: New simulation
- `Ctrl+E`: Export current view
- `Ctrl+P`: Print
- `Ctrl+S`: Save settings
- `Ctrl+Q`: Quit application

## Managing Data

### Adding Vehicles
1. Go to Violations tab
2. Click "Add Vehicle" button
3. Fill in form:
   - License Plate
   - Vehicle Type
   - Owner Name
   - Owner ID (KTP)
4. Click "Save"

### Editing Records
1. Select record in table
2. Right-click and select "Edit"
3. Modify fields
4. Click "Save"

### Deleting Records
1. Select record
2. Right-click → "Delete"
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
