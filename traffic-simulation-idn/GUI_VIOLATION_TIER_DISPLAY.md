# GUI Violation Tier Display Guide

## Two Ways to See Violation Tiers

### 1. **Hover Over Violation Type in Main Table** (Quick View)

**Location:** Main violations table, "Jenis Pelanggaran" column

**Before:** 
```
Plat Nomor | Pemilik    | Jenis Pelanggaran | Kecepatan | Denda (IDR) | Status STNK | Detail
B 1234 ABC | John Doe   | SPEEDING          | 125.5     | Rp 480,000  | Active     | Lihat
```

**After (Hover):**
```
Plat Nomor | Pemilik    | Jenis Pelanggaran | Kecepatan | Denda (IDR) | Status STNK | Detail
B 1234 ABC | John Doe   | SPEEDING ◄── Kategori: Melampaui batas kecepatan 21+ km/h
           | John Doe   |          │          | 125.5     | Rp 480,000  | Active     | Lihat
           |            |          └─ TOOLTIP appears on hover
```

**What you'll see:**
- Hover your mouse over any red "SPEEDING" or orange "TERLALU LAMBAT" text
- A yellow tooltip appears showing the category
- Examples:
  - "Kategori: Melampaui batas kecepatan 21+ km/h"
  - "Kategori: Terlalu lambat berat (sangat di bawah batas minimum)"
  - "Kategori: Melampaui batas kecepatan 11-20 km/h"

---

### 2. **Click "Lihat" Button for Detailed View** (Full Details)

**Location:** Detail dialog, "Perhitungan Denda" section (top)

**Step 1:** Click the "Lihat" button on any violation row
**Step 2:** A dialog opens with vehicle and violation details
**Step 3:** Scroll down to "Perhitungan Denda" section

**Before:**
```
┌──────────────────────────────────────────────┐
│ Perhitungan Denda                            │
├──────────────────────────────────────────────┤
│ Denda Dasar:        $32.00 / Rp 496,000      │
│ Pengali Penalti:    1.2x (STNK Tidak Aktif)  │
│ Total Denda:        $38.40 / Rp 595,200      │
└──────────────────────────────────────────────┘
```

**After (NEW):**
```
┌──────────────────────────────────────────────────────────────┐
│ Perhitungan Denda                                            │
├──────────────────────────────────────────────────────────────┤
│ Kategori Pelanggaran:  Melampaui batas kecepatan 21+ km/h    │ ← NEW!
│ Denda Dasar:           $32.00 / Rp 496,000                   │
│ Pengali Penalti:       1.2x (STNK Tidak Aktif +20%)          │
│ Total Denda:           $38.40 / Rp 595,200                   │
└──────────────────────────────────────────────────────────────┘
```

---

## Violation Categories Displayed

When you hover or see the detail dialog, you'll see one of these five categories:

### **Too Slow Violations (Orange):**
1. **"Terlalu lambat berat (sangat di bawah batas minimum)"**
   - Speed: 0-49 km/h
   - Fine: $32 / Rp 500,000

2. **"Terlalu lambat (terlalu rendah dari batas minimum)"**
   - Speed: 50-59 km/h  
   - Fine: $20 / Rp 310,000

### **Speeding Violations (Dark Red):**
3. **"Melampaui batas kecepatan 1-10 km/h (cars)"**
   - Speed: 101-110 km/h
   - Fine: $21 / Rp 320,000

4. **"Melampaui batas kecepatan 11-20 km/h (cars)"**
   - Speed: 111-120 km/h
   - Fine: $32 / Rp 497,000

5. **"Melampaui batas kecepatan 21+ km/h (cars)"**
   - Speed: 121+ km/h
   - Fine: $32 / Rp 500,000

---

## Complete Example Walkthrough

### Example 1: Speeding Violation (High Level)

**You see in main table:**
```
License Plate: B 1234 ABC
Owner: John Doe
Type: SPEEDING (dark red text)
Speed: 125.5 km/h
Fine: Rp 480,000
Status: Active
```

**You hover over "SPEEDING":**
```
Tooltip: "Kategori: Melampaui batas kecepatan 21+ km/h"
```

**You click "Lihat":**
```
Vehicle Information:
├─ Plat Nomor: B 1234 ABC
├─ Jenis: Kendaraan Pribadi
└─ Kategori: Mobil

Owner Information:
├─ Nama: John Doe
└─ Region: Jakarta Timur

Registration Status:
├─ STNK: Active ✓
└─ SIM: Active ✓

Violation Details:
├─ Kecepatan Terdeteksi: 125.5 km/h
├─ Batas Kecepatan: 75 km/h
└─ Kelebihan: +50.5 km/h

Perhitungan Denda:
├─ Kategori Pelanggaran: Melampaui batas kecepatan 21+ km/h     ← HERE!
├─ Denda Dasar: $32.00 / Rp 496,000
├─ Pengali Penalti: 1.0x (No penalty)
└─ Total Denda: $32.00 / Rp 496,000
```

---

### Example 2: Slow Violation with Penalty

**You see in main table:**
```
License Plate: B 5678 DEF
Owner: Jane Smith
Type: TERLALU LAMBAT (orange text)
Speed: 35.2 km/h
Fine: Rp 496,000
Status: Non-Active (red)
```

**You hover over "TERLALU LAMBAT":**
```
Tooltip: "Kategori: Terlalu lambat berat (sangat di bawah batas minimum)"
```

**You click "Lihat":**
```
...
Registration Status:
├─ STNK: Non-Active ⚠️
└─ SIM: Active ✓

...
Perhitungan Denda:
├─ Kategori Pelanggaran: Terlalu lambat berat (sangat di bawah batas minimum)  ← HERE!
├─ Denda Dasar: $32.00 / Rp 496,000
├─ Pengali Penalti: 1.2x (STNK Tidak Aktif +20%)
└─ Total Denda: $38.40 / Rp 595,200
```

---

## What This Means for Users

✓ **Transparency:** Users can see exactly which tier their violation falls into
✓ **Learning:** Helps drivers understand the exact nature of their violation
✓ **Accountability:** Clear categorization based on exact speed reading
✓ **Fairness:** Consistent tier application based on speed ranges
✓ **Tracking:** Administrators can analyze violations by category

---

## Tips for Testing

1. **Generate violations at different speeds:**
   - 35 km/h → Should show "Terlalu lambat berat"
   - 55 km/h → Should show "Terlalu lambat"
   - 105 km/h → Should show "Melampaui 1-10 km/h"
   - 115 km/h → Should show "Melampaui 11-20 km/h"
   - 125 km/h → Should show "Melampaui 21+ km/h"

2. **Verify tooltip appears:**
   - Hover over violation type for 1 second
   - Tooltip should appear in yellow

3. **Check detail dialog:**
   - Click "Lihat" button
   - Scroll to "Perhitungan Denda" section
   - Top line should show the category

4. **Check data file:**
   - Open `data_files/tickets.json`
   - Each ticket should have `"violation_reason"` field
   - Value should match what's shown in GUI

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tooltip doesn't appear | Move mouse away and back to violation type. Wait 1 second. |
| Category not shown in detail | Violation may be from old data. Re-run simulation. |
| tickets.json missing field | Old tickets don't have field. New violations will include it. |
| Wrong category shown | Check speed reading. Category is auto-selected by speed range. |

---

## Summary

The violation tier system is now fully visible in the GUI! You can see the exact violation category in two ways:
1. **Quick view:** Hover over violation type in main table
2. **Full view:** Click "Lihat" and check the detail dialog

Both locations clearly display which of the 5 tiers was assigned. 🎯
