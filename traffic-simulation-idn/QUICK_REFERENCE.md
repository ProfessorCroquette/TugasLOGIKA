# Quick Reference - Smooth Queue Processing

## 🚀 Quick Start

```bash
# CLI (Command Line)
cd i:\TugasLOGIKA\traffic-simulation-idn
python main.py

# GUI (Graphical Interface)
python gui_traffic_simulation.py
```

---

## 📊 What You'll See

### Console Output
```
[CHECK] Checking car: ABC 1234 XY (Speed: 85.0 km/h)
[VIOLATION]: ABC 1234 XY - Owner: John Doe - Fine: $50.00
[SAFE]: XYZ 5678 AB
[COMPLETE] Batch done: 10 cars, 3 violations
```

### GUI Status Panel
```
[CHECK] Current Car: ABC 1234 XY
        Owner: John Doe
        Speed: 85.0 km/h
        Status: [VIOLATION]

[QUEUE] Waiting: 7 cars

[RESULT] Latest: ABC 1234 XY - Fine: Rp 775,000
```

---

## 🔧 System Components

| Component | Role |
|-----------|------|
| **QueuedCarProcessor** | Main orchestrator (5 workers) |
| **TrafficSensor** | Generates vehicle batches |
| **SpeedAnalyzer** | Original analyzer (still works) |
| **GUI** | Real-time visualization |

---

## 🎯 Key Metrics

- **Cars per batch**: 10-15
- **Concurrent sensors**: 5
- **Check time per car**: 100-200ms
- **Batch processing**: ~400-500ms
- **Queue display refresh**: 500ms

---

## 📈 Processing Flow

```
Cars Generated (10-15)
        ↓
Queue them
        ↓
5 Sensors check (in parallel)
        ↓
Car 1 → [SAFE]
Car 2 → [VIOLATION] $50
Car 3 → [SAFE]
Car 4 → [VIOLATION] $30
Car 5 → [SAFE]
Car 6 → [VIOLATION] $75
Car 7 → [SAFE]
Car 8 → [VIOLATION] $36
Car 9 → [VIOLATION] $60
Car 10 → [SAFE]
        ↓
Batch Complete (5 violations)
        ↓
Next Batch...
```

---

## 📋 Log Messages

| Message | Meaning |
|---------|---------|
| `[CHECK]` | Starting to check a car |
| `[SAFE]` | Car passed inspection |
| `[VIOLATION]` | Violation detected + fine |
| `[COMPLETE]` | Batch finished |

---

## 🎛️ GUI Controls

### Control Panel
- **Mulai Simulasi** - Start simulation
- **Hentikan Simulasi** - Stop simulation
- **Hapus Data** - Clear all data

### Status Display
- Current car being checked
- Queue size (waiting cars)
- Last violation verdict
- Fine amounts (IDR)
- Statistics (avg/max speed)

---

## ⚙️ Configuration

Located in `config/__init__.py`:

```python
SIMULATION_INTERVAL = 3        # Seconds between batches
SPEED_LIMIT = 75               # km/h
MIN_SPEED_LIMIT = 40           # km/h
MIN_VEHICLES_PER_BATCH = 10    # Minimum cars
MAX_VEHICLES_PER_BATCH = 15    # Maximum cars
NUM_WORKERS = 5                # Concurrent sensors
```

---

## 📁 Data Files

```
data_files/
├── traffic_data.json    # All vehicles generated
├── tickets.json         # All violations detected
└── statistics.csv       # Statistics summary
```

---

## 🔍 Verification

```bash
# Check imports
python -c "from simulation.queue_processor import QueuedCarProcessor; print('OK')"

# Check main module
python -c "import main; print('OK')"

# Check GUI
python -m py_compile gui_traffic_simulation.py && echo "OK"

# Run simulation
python main.py
```

---

## 📊 Statistics Shown

### Processor Stats
- Total cars checked
- Total violations found
- Violation rate (%)
- Current car
- Queue size
- Number of workers

### Display Updates
- Every 500ms (GUI)
- Real-time (Console)
- Per-car (Verdict)
- Per-batch (Complete)

---

## 🛠️ Troubleshooting

**Q: GUI not showing queue?**
- A: Make sure GUI refresh timer is running (auto_refresh callback)

**Q: Simulation too slow?**
- A: Reduce `SIMULATION_INTERVAL` in config

**Q: Simulation too fast?**
- A: Increase `SIMULATION_INTERVAL` in config

**Q: Want more workers?**
- A: Change `QueuedCarProcessor(num_workers=10)` in main.py

---

## 🎓 Learning

Files to understand the system:

1. **queue_processor.py** - Core processing engine
2. **main.py** - Callbacks and integration
3. **gui_traffic_simulation.py** - Real-time display
4. **sensor.py** - Vehicle generation
5. **analyzer.py** - Fine calculation

---

## 📌 Key Takeaways

✅ **Sequential** - Cars processed one by one  
✅ **Smooth** - Verdicts returned continuously  
✅ **Efficient** - 5 concurrent sensors  
✅ **Visual** - GUI shows real-time queue  
✅ **Professional** - Clean logging & callbacks  

---

## 🚦 Status Indicators

```
[CHECK]  = Car checking started
[SAFE]   = No violation
[VIOLATION] = Violation found!
[COMPLETE]  = Batch done
```

---

## 📞 Support

If something doesn't work:
1. Check console for error messages
2. Verify file permissions
3. Ensure data_files/ directory exists
4. Check logs/ folder for detailed logs

---

**Everything is ready to go!** 🎉

Run `python main.py` or `python gui_traffic_simulation.py` to start.
