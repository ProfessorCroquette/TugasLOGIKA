# Setup Guide

## System Requirements

- Python 3.9 or higher
- PyQt5 for GUI (installed via pip)
- 2GB RAM minimum
- 5GB disk space
- Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)

**Note:** This application uses JSON file storage, not MySQL or Redis. Previous database requirements have been removed.

## Installation Steps

### 1. Prerequisites

Ensure Python 3.9+ is installed:
```bash
python --version  # Should be 3.9 or higher
```

### 2. Clone Repository
```bash
git clone https://github.com/ProfessorCroquette/TugasLOGIKA.git
cd TugasLOGIKA/traffic-simulation-idn
```

### 3. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

Key dependencies (from requirements.txt):
- PyQt5 - GUI framework
- pathlib - File operations
- json - Data storage
- subprocess - Process management

### 5. Verify Installation

Test imports and basic setup:
```bash
python -c "from gui_traffic_simulation import TrafficSimulationGUI; print('✓ GUI imports successful')"
python -c "from simulation.sensor import TrafficSensor; print('✓ Simulation imports successful')"
```

### 6. Run the Application

**GUI Mode (Recommended):**
```bash
python gui_traffic_simulation.py
```

**CLI Mode:**
```bash
python main.py
```

## Configuration

### Environment Setup

Configuration is handled in `config/` folder:
- `config/settings.py` - General settings
- `config/gui_config.py` - GUI-specific configuration
- `config/logging_config.py` - Logging setup

No .env file needed - configuration is code-based.

### Key Configuration Parameters

**From config/settings.py:**
- `SIMULATION_INTERVAL` - Time between vehicle generations
- `BASE_SPEED_LIMIT` - Speed limit threshold
- `USD_TO_IDR` - Currency conversion (1 USD = 15,500 IDR)

**GUI Configuration:**
- Auto-refresh interval: 500ms (hardcoded in gui_traffic_simulation.py)
- Number of sensors: 5 (parallel vehicle processors)
- Vehicle batch size: Configurable via DataGenerator

### Data Directory Structure

The application automatically creates these directories:
```
data_files/
├── tickets.json         # All detected violations
├── traffic_data.json    # All processed vehicles
└── worker_status.json   # Current sensor status

logs/
└── simulation_*.log     # Simulation logs (auto-cleanup of old logs)

outputs/
├── backups/            # Data backups
├── logs/              # Additional logs
├── reports/           # Generated reports
└── screenshots/       # GUI screenshots
```

## First Run

1. Open terminal/PowerShell in project directory
2. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
3. Run GUI: `python gui_traffic_simulation.py`
4. Click "Mulai Simulasi" (Start Simulation) button
5. Monitor violations appearing in real-time

## Troubleshooting

### Issue: PyQt5 Import Error
**Solution:**
```bash
pip install PyQt5 --upgrade
```

### Issue: "No module named 'config'"
**Solution:** Ensure you're running from the project root directory:
```bash
cd traffic-simulation-idn
python gui_traffic_simulation.py
```

### Issue: Permission Denied on Linux/Mac
**Solution:**
```bash
chmod +x gui_traffic_simulation.py
python gui_traffic_simulation.py
```

### Issue: Data Files Not Found
**Solution:** The application auto-creates data_files/ directory on first run. If missing:
```bash
python -c "from config import Config; Config.setup_directories()"
```
# Test GUI launch
python gui_traffic_simulation.py

# Test CLI (main simulation)
python main.py &

# Run tests (if available)
pytest tests/ -v
```

## Running the Application

### GUI Mode (Recommended)
```bash
python gui_traffic_simulation.py
```
Launches the PyQt5 GUI application with real-time traffic simulation display.

### CLI Mode (Background Simulation)
```bash
python main.py
```
Runs the core simulation engine in the background, continuously updating JSON data files (traffic_data.json, tickets.json).

## Docker Setup

### Using Docker Compose
```bash
docker-compose up -d
```

This will start:
- MySQL database (port 3306)
- Application services (traffic simulation)

Check logs:
```bash
docker-compose logs -f
```

## Troubleshooting

### Database Connection Error
- Verify MySQL is running: `mysql -u root -p -e "SELECT 1"`
- Check credentials in `.env`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES"`

### Redis Connection Error
- Verify Redis is running: `redis-cli ping`
- Check host and port in `.env`
- On Windows, consider using WSL or Docker

### Port Already in Use
```bash
# Find and kill process using port
# Linux/Mac: lsof -i :8000
# Windows: netstat -ano | findstr :8000
```

### Import Errors
```bash
# Reinstall in development mode
pip install -e .
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

## Log Cleanup

The application automatically manages log files:
- **Location**: `logs/` directory
- **Cleanup Trigger**: Automatic on every application startup
- **Max Files Kept**: 10 (oldest logs deleted when exceeded)
- **Log Names**: `simulation_YYYYMMDD_HHMMSS.log`

This prevents unlimited disk space usage during long-running simulations.

## Next Steps

1. Read the [User Manual](USER_MANUAL.md)
2. Review [Architecture](ARCHITECTURE.md)
3. See [Database Schema](DATABASE_SCHEMA.md)
