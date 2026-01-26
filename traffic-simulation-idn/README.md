# Indonesian Traffic Violation Simulation System

A clean, real-time traffic violation simulation system for Indonesian traffic law compliance. Generates realistic traffic violations, calculates fines, and provides a live dashboard GUI.

## Quick Start

### Run the GUI Dashboard
```bash
cd traffic-simulation-idn
python gui_traffic_simulation.py
```

Click "Mulai Simulasi" to start - violations appear in real-time!

### Run Simulation Only
```bash
python main.py              # Run indefinitely
python main.py 5            # Run for 5 minutes
```

## Key Features

✅ **Real-Time Monitoring** - Violations appear instantly in GUI
✅ **Indonesian Law Compliant** - Follows Pasal 287 ayat 5 UU No. 22/2009
✅ **High Violation Rate** - 2-100 vehicles every 5 seconds
✅ **Scalable** - Supports up to 100 records
✅ **Accurate Data** - Indonesian NIK format, regional plates
✅ **Live Dashboard** - 500ms refresh rate
✅ **Penalty System** - 1.0x/1.2x/1.4x multipliers

## Documentation

**See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for complete system documentation including:**

- Detailed file descriptions and functions
- Configuration options
- Data structures
- Usage examples
- Performance notes
- Troubleshooting guide

## Core Files

| File | Purpose |
|------|---------|
| `main.py` | Simulation engine (traffic generation & violation detection) |
| `gui_traffic_simulation.py` | Real-time dashboard GUI (Qt5) |
| `config/__init__.py` | System configuration (fines, speeds, limits) |
| `PROJECT_DOCUMENTATION.md` | Complete system documentation |

## System Architecture

```
┌─────────────────┐
│  Sensor Layer   │  → Generates 2-100 vehicles every 5 seconds
└────────┬────────┘
         │
┌────────▼────────────┐
│  Analyzer Layer     │  → Detects violations & calculates fines
└────────┬────────────┘
         │
┌────────▼────────────────┐
│  Storage Layer          │  → Saves to JSON (tickets.json)
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│  GUI Dashboard (Qt5)    │  → Displays in real-time
└─────────────────────────┘
```

## Configuration

Edit `config/__init__.py` to customize:

```python
SIMULATION_INTERVAL = 5              # Seconds between batches
MIN_VEHICLES_PER_BATCH = 2          # Min vehicles per batch
MAX_VEHICLES_PER_BATCH = 100        # Max vehicles per batch
SPEED_LIMIT = 75                    # Speed limit in km/h
MIN_SPEED_LIMIT = 40                # Minimum safe speed
USD_TO_IDR = 15500                  # Currency conversion
MAX_FINE_IDR = 1250000              # Maximum fine
```

## Data Output

Violations are saved to `data_files/tickets.json`:
```json
{
  "license_plate": "B 1234 XY",
  "owner_name": "Budi Santoso",
  "owner_nik": "3606010195123456",
  "speed": 95.5,
  "fine_amount": 50.0,
  "penalty_multiplier": 1.2,
  "stnk_status": "Active",
  "sim_status": "Expired",
  "violation_type": "SPEEDING"
}
```

## Indonesian Law Compliance

**Source:** Pasal 287 ayat (5) UU No. 22 Tahun 2009 tentang Lalu Lintas dan Angkutan Jalan

✅ Maximum fine: **Rp 1,250,000** (enforced)
✅ Detects both speeding AND driving too slow
✅ Realistic penalty multipliers
✅ Indonesian NIK format (16-digit)
✅ Regional license plates
✅ Rupiah currency display

## Fine Tiers

| Violation | Speed Range | Fine USD | Fine IDR |
|-----------|-------------|----------|----------|
| Too Slow (Mild) | 30-39 km/h | $20 | Rp 310,000 |
| Too Slow (Severe) | 0-29 km/h | $35 | Rp 542,500 |
| Speeding Level 1 | 76-90 km/h | $30 | Rp 465,000 |
| Speeding Level 2 | 91-110 km/h | $50 | Rp 775,000 |
| Speeding Level 3 | 111-130 km/h | $75 | Rp 1,162,500 |

## Penalty Multiplier

- **1.0x** - Both STNK active & SIM valid
- **1.2x** - STNK non-active OR SIM expired
- **1.4x** - Both STNK non-active AND SIM expired

## Requirements

- Python 3.13
- PyQt5 (for GUI)
- Standard libraries: json, threading, subprocess, queue

## Installation

```bash
pip install -r requirements.txt
```

## Performance

- **Simulation Speed**: 2-100 vehicles per 5 seconds
- **GUI Refresh**: 500ms
- **Queue Capacity**: 500 messages
- **Max Violations**: Unlimited
- **Max Vehicles**: Unlimited

## Troubleshooting

**Q: GUI shows no violations**
A: Click "Mulai Simulasi" - simulation takes 5 seconds to generate first batch

**Q: Violations not updating**
A: Check `data_files/` directory exists and is writable

**Q: Fine amounts show $0**
A: Ensure `USD_TO_IDR = 15500` in `config/__init__.py`

**Q: GUI takes long to start**
A: Normal - simulation is generating background data

## License

Indonesian Traffic Violation Simulation System - Educational Purpose

---

For complete documentation, see **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)**
