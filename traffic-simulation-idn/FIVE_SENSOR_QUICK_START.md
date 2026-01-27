# Quick Start - Five Sensor GUI

## One-Minute Setup

### 1. Start the GUI
```bash
cd i:\TugasLOGIKA\traffic-simulation-idn
python gui_traffic_simulation.py
```

### 2. Click "Mulai Simulasi"

### 3. Watch 5 Sensors Process Cars

That's it! The interface automatically shows:
- Each of the 5 concurrent workers
- What car each is checking
- Real-time status (IDLE, CHECKING, SAFE, VIOLATION)
- Fine amounts in Rupiah

---

## What You'll See

### Five Sensor Panels

```
┌──────────┬──────────┬──────────┐
│ Sensor 1 │ Sensor 2 │ Sensor 3 │
├──────────┼──────────┼──────────┤
│ SAFE     │VIOLATION │ IDLE     │
│B 1234 XY │D 5678 AB │ -        │
│70 km/h   │95 km/h   │ -        │
│-         │Rp50.000  │ -        │
├──────────┼──────────┼──────────┤
│ Sensor 4 │ Sensor 5 │          │
├──────────┼──────────┤          │
│CHECKING  │ IDLE     │          │
│H 9012 CD │ -        │          │
│80 km/h   │ -        │          │
│ -        │ -        │          │
└──────────┴──────────┴──────────┘
```

Each sensor updates **every 500ms** with real-time data.

---

## Status Colors

| Status | Color | Meaning |
|--------|-------|---------|
| **IDLE** | Gray | Waiting for car |
| **CHECKING** | Blue | Processing car |
| **SAFE** | Green | Car passed (speed OK) |
| **VIOLATION** | Red | Speeding detected |

---

## Information Per Sensor

Each sensor panel shows:

1. **Status Badge** - Current state (IDLE/CHECKING/SAFE/VIOLATION)
2. **Plat** - License plate number (or "-" if idle)
3. **Kecepatan** - Detected speed (or "-" if idle)
4. **Denda** - Fine in Rupiah (or "-" if no violation)

---

## Real-Time Example

### Processing Starts
```
Sensor 1: CHECKING         Sensor 2: CHECKING
Plat: B 1234 XY            Plat: D 5678 AB
Speed: 85 km/h             Speed: 95 km/h
Fine: -                    Fine: -
```

### Check Completes (0.15s later)
```
Sensor 1: SAFE             Sensor 2: VIOLATION
Plat: B 1234 XY            Plat: D 5678 AB
Speed: 85 km/h             Speed: 95 km/h
Fine: -                    Fine: Rp 50,000
```

### Clears for Next Car (0.5s later)
```
Sensor 1: IDLE             Sensor 2: IDLE
Plat: -                    Plat: -
Speed: -                   Speed: -
Fine: -                    Fine: -
```

---

## Key Features

✅ **5 Concurrent Workers** - All process cars in parallel
✅ **Real-Time Updates** - See changes instantly
✅ **Color Coded** - Violations in red, safe in green
✅ **Auto-Refresh** - Updates every 500ms automatically
✅ **No Setup Needed** - Just run the GUI
✅ **Live Statistics** - Total violations, fines, speeds

---

## Tips

### Pause/Resume
Click "Hentikan Simulasi" to pause, "Mulai Simulasi" to resume.

### Clear Data
Click "Hapus Data" to reset all statistics and violations list.

### View Violation Details
Double-click any violation in the right panel to see full details.

### Monitor Performance
Check left panel for:
- Total violations count
- Total fines in Rupiah
- Average speed
- Maximum speed

---

## What's Happening Behind the Scenes

```
Every 3 seconds:
1. Sensor generates batch of 10-15 cars
2. Adds cars to queue
3. 5 workers pick cars from queue
4. Each worker checks a car (100-200ms)
5. Sends verdict (SAFE or VIOLATION)
6. Callback updates worker_status.json
7. GUI reads file every 500ms
8. Display updates automatically

Result: 5x faster than sequential!
10 cars processed in 400ms instead of 2000ms
```

---

## Troubleshooting

### Sensors Always Show IDLE?
Make sure simulation is running. Click "Mulai Simulasi" button.

### Not Seeing Updates?
Check that:
1. GUI window is in focus
2. Simulation is running
3. No errors in console

### Want to Change Settings?

To use 3 sensors instead of 5:
- Edit `main.py`: Change `num_workers=5` to `num_workers=3`
- Edit `gui_traffic_simulation.py`: Change `range(1, 6)` to `range(1, 4)`

---

## Performance

- **Each car check**: 100-200ms
- **5 cars in parallel**: ~200ms total
- **Display refresh**: Every 500ms
- **System impact**: Minimal (file I/O only)

---

## Files Used

- `simulation/queue_processor.py` - Core worker management
- `main.py` - Status callbacks and file writing
- `gui_traffic_simulation.py` - Display and updates
- `data_files/worker_status.json` - Live worker status

All automatically maintained during execution.

---

## Need Help?

### Documentation Files
1. **FIVE_SENSOR_IMPLEMENTATION_COMPLETE.md** - Full technical details
2. **FIVE_SENSOR_GUI_INTERFACE.md** - Architecture and configuration
3. **FIVE_SENSOR_VISUAL_GUIDE.md** - Visual examples and diagrams

### Quick Reference
- **Status updates**: Every 500ms
- **Max workers**: 5 (easily configurable)
- **Check time**: 100-200ms per car
- **Batch size**: 10-15 cars per 3 seconds

---

## Summary

🎯 Run: `python gui_traffic_simulation.py`
🎯 Click: "Mulai Simulasi"
🎯 Watch: 5 sensors process cars in real-time
🎯 Enjoy: Real-time monitoring of all 5 concurrent workers

Perfect for seeing your 5x parallel efficiency in action!
