# Sub-Region Display Feature - Implementation Complete ✅

## Overview
The GUI has been enhanced to display **both main region and sub-region** information for:
1. **Vehicle Information** - Based on license plate code and owner letters
2. **Owner Information** - Based on owner's region code

## Implementation Details

### What are Sub-Regions?
Sub-regions are the administrative divisions within each main region. They are mapped based on:
- **For Vehicle Plates**: The owner code letters (position [2] in the plate)
- **For Owner Region**: The province code stored in owner data

Each plate code (e.g., `BL`, `BB`, `KT`) has a `sub_codes` dictionary that maps:
- Owner code letters → Sub-region names
- Example: `BL` (Aceh) with owner code `L` → `Aceh Besar`

### Example Output

#### Before (Main Region Only)
```
Informasi Kendaraan:
  Plat Nomor: BL 104 LWG
  Wilayah: Aceh
  Tipe Kendaraan: ...
```

#### After (Main Region + Sub-Region)
```
Informasi Kendaraan:
  Plat Nomor: BL 104 LWG
  Wilayah: Aceh
  Sub-Wilayah: Aceh Besar
  Tipe Kendaraan: ...
```

### Updated GUI Sections

#### 1. Vehicle Information Dialog (`Informasi Kendaraan`)
- **New Row Added**: "Sub-Wilayah" showing the sub-region for the vehicle
- Extracted from: Owner code letters in the license plate
- Example: Plate `BP 5954 TB` → Sub-Wilayah: `Kota Tanjung Pinang`

#### 2. Owner Information Dialog (`Data Pemilik`)
- **New Row Added**: "Sub-Wilayah Tempat Tinggal" showing owner's sub-region
- Extracted from: Owner's region code (first available sub-region)
- Provides more detailed location information about the vehicle owner

### Code Changes Made

#### New Methods in `ViolationDetailDialog`

1. **`_get_sub_region_from_plate(plate: str) -> str`**
   - Extracts sub-region from license plate
   - Uses owner code letters to lookup in PLATE_DATA's sub_codes dictionary
   - Returns "-" if not found

2. **`_get_sub_region_from_code(code: str) -> str`**
   - Extracts sub-region from region code (for owner region)
   - Returns first available sub-region from the region's sub_codes
   - Returns "-" if no sub-codes available

#### Updated Dialog Layout
- Row 2: Vehicle Sub-Wilayah
- Row 3: Tipe Kendaraan (shifted down)
- Row 4: Kategori Kendaraan (shifted down)
- Row 3: Owner Sub-Wilayah Tempat Tinggal (in owner section)

### Data Source
All sub-region mappings come from the authoritative `PLATE_DATA` in `utils/indonesian_plates.py`:
- 61 plate codes with complete sub-region mappings
- Each plate code has 20-30 sub-codes mapping to districts/cities
- Example: Aceh (BL) has 22 sub-regions (Kota Banda Aceh, Gayo Lues, Aceh Barat Daya, etc.)

### Test Results

Running test on actual violation data:

```
✓ BP 5954 TB           | Region: Kepulauan Riau        | Sub: Kota Tanjung Pinang
✓ L 735 A              | Region: Jawa Timur            | Sub: Kota Surabaya
✓ BL 104 LWG           | Region: Aceh                  | Sub: Aceh Besar
✓ H 1585 NUP           | Region: Jawa Tengah           | Sub: Demak
✓ KT 0270 TAS          | Region: Kalimantan Timur      | Sub: Mahakam Ulu
✓ B 9748 HWJ           | Region: DKI Jakarta           | Sub: Jakarta Barat
```

### Files Modified
- `gui_traffic_simulation.py`
  - Added `_get_sub_region_from_plate()` method
  - Added `_get_sub_region_from_code()` method
  - Updated `ViolationDetailDialog.init_ui()` to display sub-regions

### Backward Compatibility
✅ All changes are backward compatible:
- Main region display remains unchanged
- Sub-region display is additive (new rows in dialog)
- Falls back to "-" if sub-region cannot be determined
- Existing functionality preserved

## Usage
When clicking on a violation in the traffic simulation GUI:
1. Open violation detail dialog
2. View "Informasi Kendaraan" section to see:
   - Plat Nomor (License Plate)
   - Wilayah (Main Region)
   - **Sub-Wilayah** (Sub-Region) ← NEW
   - Tipe Kendaraan (Vehicle Type)
   - Kategori Kendaraan (Vehicle Category)
3. View "Data Pemilik" section to see:
   - Nama (Owner Name)
   - NIK (National ID)
   - Tempat Tinggal (Owner Region)
   - **Sub-Wilayah Tempat Tinggal** (Owner Sub-Region) ← NEW

---
**Status**: ✅ Complete and Tested
**Date**: January 31, 2026
