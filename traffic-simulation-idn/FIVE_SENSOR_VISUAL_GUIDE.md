# Five Sensor GUI - Quick Visual Reference

## Main Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Traffic Violation Monitoring System                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ LEFT PANEL                              RIGHT PANEL                     │
│ ┌────────────────┐                   ┌──────────────────────┐           │
│ │ Kontrol        │                   │ DAFTAR PELANGGARAN   │           │
│ │ Simulasi       │                   │ (Violations List)    │           │
│ │ ─────────────  │                   │ ─────────────────────│           │
│ │ [Mulai]        │                   │                      │           │
│ │ [Hentikan]     │                   │ ┌──────────────────┐ │           │
│ │ [Hapus Data]   │                   │ │ Plat│Pemilik│Fine│ │           │
│ │                │                   │ ├──────────────────┤ │           │
│ ├────────────────┤                   │ │ B 1234│John │Rp50│ │           │
│ │ Statistik      │                   │ │ D 5678│Jane │Rp75│ │           │
│ │ Real-time      │                   │ │ H 9012│Bob  │Rp50│ │           │
│ │ ─────────────  │                   │ └──────────────────┘ │           │
│ │ Total Pelangg: 3                   │                      │           │
│ │ Kendaraan: 25                      │                      │           │
│ │ Total Denda: Rp 180.000            │                      │           │
│ │ Rata-rata: 78 km/h                 │                      │           │
│ │ Maksimal: 95 km/h                  │                      │           │
│ │                │                   │                      │           │
│ ├────────────────┤                   └──────────────────────┘           │
│ │ Status Pemeriksaan (5 Sensor)      │                                  │
│ │ ─────────────────────────────────  │                                  │
│ │                                    │                                  │
│ │ ┌──────────┬──────────┬──────────┐ │                                  │
│ │ │ Sensor 1 │ Sensor 2 │ Sensor 3 │ │                                  │
│ │ ├──────────┼──────────┼──────────┤ │                                  │
│ │ │ [IDLE]   │ [SAFE]   │[VIOLAT]  │ │                                  │
│ │ │ Plat: -  │ B 1234XY │ D 5678AB │ │                                  │
│ │ │ Kec: -   │ 70 km/h  │ 95 km/h  │ │                                  │
│ │ │ Denda: - │ Rp -     │Rp50.000  │ │                                  │
│ │ ├──────────┼──────────┼──────────┤ │                                  │
│ │ │ Sensor 4 │ Sensor 5 │          │ │                                  │
│ │ ├──────────┼──────────┤          │ │                                  │
│ │ │[CHECKING]│ [IDLE]   │          │ │                                  │
│ │ │ H 9012CD │ Plat: -  │          │ │                                  │
│ │ │ 80 km/h  │ Kec: -   │          │ │                                  │
│ │ │ Rp -     │ Denda: - │          │ │                                  │
│ │ └──────────┴──────────┴──────────┘ │                                  │
│ │                                    │                                  │
│ └────────────────┬────────────────────┘                                  │
│                  │                                                       │
└──────────────────┴───────────────────────────────────────────────────────┘
```

---

## Sensor Panel States

### 1. IDLE (Waiting for Car)

```
┌──────────────────┐
│   Sensor 1       │
├──────────────────┤
│ IDLE             │  ← Gray text
│ Plat: -          │
│ Kecepatan: -     │
│ Denda: -         │
└──────────────────┘
```

### 2. CHECKING (Processing Car)

```
┌──────────────────┐
│   Sensor 2       │
├──────────────────┤
│ CHECKING         │  ← Blue background
│ Plat: B 1234 XY  │  ← License plate
│ Kecepatan: 85 km │  ← Current speed
│ Denda: -         │  ← No fine yet
└──────────────────┘
```

### 3. SAFE (Passed Inspection)

```
┌──────────────────┐
│   Sensor 3       │
├──────────────────┤
│ SAFE             │  ← Green background
│ Plat: A 1111 CD  │  ← License plate
│ Kecepatan: 70 km │  ← Speed within limit
│ Denda: -         │  ← No violation
└──────────────────┘
```

### 4. VIOLATION (Speeding Detected)

```
┌──────────────────┐
│   Sensor 4       │
├──────────────────┤
│ VIOLATION        │  ← Red background, bold
│ Plat: D 5678 AB  │  ← License plate
│ Kecepatan: 95 km │  ← Speed over limit
│ Denda: Rp 50.000 │  ← Fine amount
└──────────────────┘
```

---

## Status Transitions

### Car Processing Timeline

```
Queue → Worker → Check Time (100-200ms) → Verdict → Result

Sensor State Transitions:

IDLE
  ↓
  ├─→ [CHECKING] ← Car from queue
  │    ↓ (100-200ms)
  │    ├─→ [SAFE] ← Speed OK → Clear → IDLE (1 sec)
  │    │
  │    └─→ [VIOLATION] ← Speeding → Show fine → IDLE (1 sec)
  ↓
IDLE (ready for next car)
```

---

## Real-Time Display Example

### Scenario: 3 Cars Being Processed

```
Start Time (T=0ms):
┌──────────┬──────────┬──────────┐
│ Sensor 1 │ Sensor 2 │ Sensor 3 │
├──────────┼──────────┼──────────┤
│ CHECKING │ CHECKING │ CHECKING │
│ B 1234XY │ D 5678AB │ H 9012CD │
│ 85 km/h  │ 95 km/h  │ 75 km/h  │
│ -        │ -        │ -        │
└──────────┴──────────┴──────────┘

After 150ms (T=150ms):
┌──────────┬──────────┬──────────┐
│ Sensor 1 │ Sensor 2 │ Sensor 3 │
├──────────┼──────────┼──────────┤
│ SAFE     │ VIOLATION│ SAFE     │ ← Results ready
│ B 1234XY │ D 5678AB │ H 9012CD │
│ 85 km/h  │ 95 km/h  │ 75 km/h  │
│ -        │ Rp 50.000│ -        │
└──────────┴──────────┴──────────┘

After 500ms (T=500ms):
┌──────────┬──────────┬──────────┐
│ Sensor 1 │ Sensor 2 │ Sensor 3 │
├──────────┼──────────┼──────────┤
│ IDLE     │ IDLE     │ IDLE     │ ← Cleared
│ -        │ -        │ -        │
│ -        │ -        │ -        │
│ -        │ -        │ -        │
└──────────┴──────────┴──────────┘
Ready for next batch!
```

---

## Color Reference

```
Status Display Colors:

┌────────────────┬─────────────┬─────────────┐
│   Status       │ Text Color  │ Background  │
├────────────────┼─────────────┼─────────────┤
│ IDLE           │ Gray        │ Default     │
│ CHECKING       │ Blue        │ Light Blue  │
│ SAFE           │ Dark Green  │ Light Green │
│ VIOLATION      │ Dark Red    │ Light Red   │
└────────────────┴─────────────┴─────────────┘

Examples:

IDLE          CHECKING         SAFE           VIOLATION
────────      ────────         ────           ─────────
[Gray]        [Blue Box]       [Green Box]    [Red Box]
```

---

## Information Display Order

### Each Sensor Panel Shows (Top to Bottom):

```
1. STATUS BADGE
   ├─ IDLE
   ├─ CHECKING
   ├─ SAFE
   └─ VIOLATION

2. LICENSE PLATE
   └─ e.g., "B 1234 XY"

3. SPEED (km/h)
   └─ e.g., "85.5 km/h"

4. FINE (Rupiah)
   └─ e.g., "Rp 50,000" or "-"
```

---

## Sensor Grid Layout

### 5 Sensors in 2-Row Grid:

```
Row 1:
┌─────────────────┬─────────────────┬─────────────────┐
│   Sensor 1      │   Sensor 2      │   Sensor 3      │
│                 │                 │                 │
│                 │                 │                 │
│                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘

Row 2:
┌─────────────────┬─────────────────┐
│   Sensor 4      │   Sensor 5      │
│                 │                 │
│                 │                 │
│                 │                 │
└─────────────────┴─────────────────┘
```

---

## Workflow Visualization

### Car Processing with 5 Sensors

```
BATCH FROM SENSOR (10 cars generated every 3 seconds)
    ↓
QUEUE (10 cars waiting)
    ↓
DISTRIBUTE TO 5 WORKERS:

Car 1 ──→ Sensor 1 (100ms) ──→ SAFE ──→ Clear
Car 2 ──→ Sensor 2 (100ms) ──→ VIOLATION ──→ Show Rp 50.000
Car 3 ──→ Sensor 3 (100ms) ──→ SAFE ──→ Clear
Car 4 ──→ Sensor 4 (100ms) ──→ SAFE ──→ Clear
Car 5 ──→ Sensor 5 (100ms) ──→ VIOLATION ──→ Show Rp 50.000

(All 5 run in parallel = 100ms total)

Car 6 ──→ Sensor 1 (100ms) ──→ VIOLATION ──→ Show Rp 75.000
Car 7 ──→ Sensor 2 (100ms) ──→ SAFE ──→ Clear
Car 8 ──→ Sensor 3 (100ms) ──→ SAFE ──→ Clear
Car 9 ──→ Sensor 4 (100ms) ──→ VIOLATION ──→ Show Rp 50.000
Car 10 ─→ Sensor 5 (100ms) ──→ SAFE ──→ Clear

(All 5 run in parallel = 100ms total)

BATCH COMPLETE (200ms total for 10 cars)
vs 1000ms if done sequentially!
```

---

## Dashboard Statistics

```
┌──────────────────────────────┐
│ Left Panel Statistics         │
├──────────────────────────────┤
│ Total Pelanggaran:    3      │  ← From violations file
│ Kendaraan Diproses:   25     │  ← From vehicles file
│ Total Denda (IDR):    Rp... │  ← Sum of all fines
│ Rata-rata Kecepatan:  78 km │  ← Average speed
│ Kecepatan Maksimal:   95 km │  ← Max speed detected
└──────────────────────────────┘
```

---

## GUI Update Cycle

```
┌─ Every 500ms ──────────────────────┐
│                                    │
│  Read: worker_status.json          │
│  ↓                                 │
│  For each Sensor (1-5):            │
│  ├─ Get worker status              │
│  ├─ Update plate/speed             │
│  ├─ Update status color            │
│  ├─ Update fine amount             │
│  └─ Refresh display                │
│  ↓                                 │
│  Update Statistics                 │
│  ↓                                 │
│  Display Ready                     │
│                                    │
└────────────────────────────────────┘
```

---

## Summary

✅ **5 Independent Sensors** - Each monitoring one car
✅ **Real-Time Status** - IDLE/CHECKING/SAFE/VIOLATION
✅ **Live Car Data** - Plate, speed, fine amount
✅ **Color Coding** - Quick visual feedback
✅ **500ms Refresh** - Smooth updates
✅ **Clean Layout** - 2-row grid format

Perfect for monitoring all 5 concurrent workers at a glance!
