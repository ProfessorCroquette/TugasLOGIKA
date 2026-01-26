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

After installation, start the application:

**GUI:**
```bash
python src/main_gui.py
```

**CLI:**
```bash
python src/main.py
```

## CLI Interface

### Help Command
```bash
python src/main.py --help
```

### Start Simulation
```bash
python src/main.py simulate \
  --duration 3600 \
  --vehicles 100 \
  --speed-variation 10 \
  --violation-chance 0.05
```

Parameters:
- `--duration`: Simulation time in seconds
- `--vehicles`: Number of vehicles to simulate
- `--speed-variation`: Speed variation percentage
- `--violation-chance`: Probability of violations (0-1)

### Generate Report
```bash
python src/main.py report \
  --type daily \
  --format csv \
  --date 2024-01-26
```

### Manage Vehicles
```bash
# List vehicles
python src/main.py vehicle list

# Add vehicle
python src/main.py vehicle add \
  --plate "B1234ABC" \
  --type "sedan" \
  --owner "John Doe"

# Update vehicle
python src/main.py vehicle update 1 --status inactive
```

### Manage Violations
```bash
# List violations
python src/main.py violation list

# Record violation
python src/main.py violation record \
  --vehicle-id 1 \
  --type speed \
  --speed 75 \
  --location "Jalan Sudirman"
```

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

## Troubleshooting

### Application Won't Start
- Check Python version: `python --version` (should be 3.9+)
- Verify dependencies: `pip install -r requirements.txt`
- Check .env file exists and is valid

### Database Connection Error
- Verify MySQL is running
- Check credentials in .env
- Test connection: `python -c "from src.database import get_session"`

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
- Check [API Documentation](API_DOCUMENTATION.md) for REST API
- Review [Architecture](ARCHITECTURE.md) for system design
- Visit project GitHub for issue reporting
