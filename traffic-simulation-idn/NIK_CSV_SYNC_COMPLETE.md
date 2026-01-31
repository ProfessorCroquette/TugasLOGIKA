# Update: NIK-Plate Region Sync dengan CSV Administrative Codes

## Changes Made

### 1. NIK Generation dengan CSV Administrative Codes ✅
**File:** `utils/indonesian_plates.py`

#### New Method: `generate_nik_from_plate(plate_region_code, sub_region=None)`
```python
# Format 16-digit NIK:
Province(2) + City(2) + District(2) + BirthDay(2) + Month(2) + Year(2) + Sequential(4)
```

**How it works:**
1. Takes plate region code (e.g., 'B' for Jakarta)
2. Gets province code from PLATE_DATA mapping (e.g., 'B' → '31' for DKI Jakarta)
3. If sub_region provided, searches CSV for administrative codes:
   - Searches base.csv for matching region name (e.g., "JAKARTA SELATAN")
   - Extracts city code from CSV (e.g., '31.74' → city='74')
   - Picks random district from that city (e.g., '01' for Tebet)
4. Generates complete NIK with:
   - Birth day (1-28, +40 for female)
   - Birth month (1-12)
   - Birth year (50-99)
   - Sequential number (1-9999)

#### New Method: `_get_csv_codes_for_region(sub_region)`
Extracts administrative codes from base.csv for a region:
- Searches for "KOTA" or "KAB" entries matching sub_region name
- Returns city code and random district code
- Example: "Jakarta Selatan" → {'city': '74', 'district': '03', 'full': '31.74.03'}

### 2. GUI Updates ✅
**File:** `gui_traffic_simulation.py`

**Removed:**
- ✅ Sinkronisasi Plat-KTP status section
- ✅ "Lihat Detail NIK" button
- ✅ NIK detail dialog (`_show_nik_details()` method)
- ✅ Unused imports: `NIKParser`, `PlateKTPSync`

**Result:**
- NIK displayed as simple text in owner section
- No synchronization status shown
- Cleaner, simpler dialog

### 3. Owner Generation Integration ✅
**Updated:** `OwnerDatabase.get_or_create_owner()`
- Passes `sub_region` to `generate_random_owner()`
- Works with CSV administrative codes for proper NIK generation
- Maintains backward compatibility

## NIK Format Examples

### Jakarta Selatan (Region Code: B)
```
31.74.01 (Jakarta Selatan, Tebet)
  ├─ 31 = DKI Jakarta (Province)
  ├─ 74 = Jakarta Selatan (City)
  └─ 01 = Tebet (District)
  
Generated NIK: 3174DDMMYYXXXX
Example: 3174021105642543
  ├─ Province: 31 (DKI Jakarta)
  ├─ City: 74 (Jakarta Selatan)
  ├─ District: 01 (Tebet)
  ├─ Day: 02
  ├─ Month: 11
  ├─ Year: 06
  └─ Sequential: 2543
```

### Bandung (Region Code: D)
```
32.71.01 (Bandung, Cidadap)
Generated NIK: 3271DDMMYYXXXX
```

### Surabaya (Region Code: T)
```
35.78.01 (Surabaya, Sawahan)
Generated NIK: 3578DDMMYYXXXX
```

## CSV Data Structure

The base.csv file uses hierarchical administrative codes:

```
31,DKI JAKARTA                              (Province)
31.71,KOTA ADM. JAKARTA PUSAT              (City)
31.71.01,Gambir                             (District)
31.71.01.1001,Gambir                        (Sub-district)

31.74,KOTA ADM. JAKARTA SELATAN
31.74.01,Tebet
31.74.01.1001,Tebet Timur
31.74.01.1002,Tebet Barat
...
31.74.07,Kebayoran Baru
31.74.07.1001,Melawai
31.74.07.1002,Gunung
31.74.07.1003,Kramat Pela
...
```

## Test Results

```
✅ NIK Generation:
   - Jakarta (B): Province 31, City codes from CSV
   - Bandung (D): Province 32, City codes from CSV
   - All with proper district codes

✅ Owner Generation:
   - Works without address field
   - NIK matches plate region via CSV codes

✅ Complete Flow:
   - Generate plate → Parse → Extract region → Load CSV codes → Generate NIK ✓
   - Owner created with 16-digit synchronized NIK ✓
```

## System Flow

```
Plate Generated (e.g., "B 4123 RK")
    ↓
Parse Plate → Extract "Jakarta Selatan"
    ↓
Search CSV for "JAKARTA SELATAN"
    ↓
Find: 31.74 (DKI Jakarta, Jakarta Selatan)
    ↓
Generate complete NIK:
  - Province: 31
  - City: 74
  - District: Random (01-30)
  - Birth: Day, Month, Year
  - Sequential: 1-9999
    ↓
Create VehicleOwner with 16-digit NIK ✓
```

## Compliance

✅ Proper administrative hierarchy from Indonesian government database
✅ NIK format matches Indonesian KTP standard (16 digits)
✅ Region codes from base.csv (official administrative codes)
✅ Gender encoding in birth day (>40 = female)
✅ No address storage/display (simplified system)

## Files Modified

1. `utils/indonesian_plates.py`
   - Added: `generate_nik_from_plate()` method
   - Added: `_get_csv_codes_for_region()` method
   - Updated: `get_or_create_owner()` documentation

2. `gui_traffic_simulation.py`
   - Removed: KTP-Plate sync status section
   - Removed: "Lihat Detail NIK" button
   - Removed: NIK detail dialog method
   - Removed: Unused imports
   - Simplified: Owner information display

3. `test_simplified_flow.py`
   - Updated: Test assertions for 16-digit NIK format

## Backward Compatibility

✅ Existing code still works
✅ `generate_random_owner()` method unchanged
✅ Owner database operations unchanged
✅ All violation generation still works

---
**Status:** ✅ COMPLETE - NIK generation now properly synchronized with CSV administrative codes
**Date:** January 31, 2026
