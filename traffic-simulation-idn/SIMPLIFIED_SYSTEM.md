# Simplified Owner Generation System

## Overview
The owner generation system has been simplified to focus on **NIK generation from plate numbers only**. No address generation, no dialog display.

## Key Changes

### What Was Removed
- ❌ Complex address generation method `_generate_address()`
- ❌ STREET_NAMES constant (20 Indonesian street names)
- ❌ Address storage in VehicleOwner class
- ❌ Extensive docstrings explaining complex flow
- ❌ Multiple region extraction methods

### What Was Kept
- ✅ Simple NIK generation: `generate_nik_from_plate(plate_region_code)`
- ✅ Owner generation with minimal fields
- ✅ Existing administrative code lookup (for accuracy)
- ✅ Document status validation (STNK, SIM)

## How It Works

### 1. Plate Parsing
```python
parsed = IndonesianPlateManager.parse_plate("B 4123 RK")
# Result: {'region_code': 'B', 'region_name': 'Jakarta Selatan', ...}
```

### 2. NIK Generation from Plate
```python
nik = IndonesianPlateManager.generate_nik_from_plate('B')
# Returns: "3183660869991" (14 digits)
# Format: Province(2) + City(2) + BirthDay(2) + Month(2) + Year(2) + Sequential(4)
```

### 3. Owner Creation
```python
owner = VehicleOwner.generate_random_owner(
    region='DKI Jakarta',
    sub_region='Jakarta Selatan',
    vehicle_type='roda_empat',
    required_province_code='31'  # From plate region code B
)
# Result: VehicleOwner with NIK, name, region, vehicle_type ONLY
# NO ADDRESS FIELD
```

## NIK Format
```
[Province(2)][City(2)][BirthDay(2)][Month(2)][Year(2)][Sequential(4)]
Example: 31 71 03 28 01 7003  -> 3171032801700003
         ├─ 31 = DKI Jakarta
         ├─ 71 = Jakarta Selatan (city code)
         ├─ 03 = Birth day 3 (28+40 for female)
         ├─ 28 = February
         ├─ 01 = Year 2001
         └─ 7003 = Sequential number
```

## VehicleOwner Structure
```python
VehicleOwner:
  - owner_id: str (14-digit NIK)
  - name: str (Indonesian name)
  - region: str (Province name)
  - sub_region: str (City/Kabupaten name)
  - vehicle_type: str ('roda_dua' or 'roda_empat')
  - stnk_status: bool (Active/Expired)
  - sim_status: bool (Active/Expired)
  # NO ADDRESS FIELD
```

## Usage in Violations
Owner details are only shown in violation/pelanggaran records:
```python
violation = {
    'plate': 'B 4123 RK',
    'owner_name': 'Sari Nugroho',
    'owner_nik': '3171032801700381',
    'violation_type': 'speeding',
    'location': 'Jakarta Selatan',
    ...
}
```

## Special Plates (RI, Diplomatik)
For government and diplomatic plates, NIK is completely random:
```python
owner = VehicleOwner.generate_random_owner(
    region='Pemerintah Indonesia',
    sub_region='Pemerintah Indonesia',
    is_special_plate=True  # Generates random NIK
)
```

## Test Results
All tests passed:
- ✅ NIK generation from different plate regions
- ✅ Owner generation without address
- ✅ Complete flow: Plate → Parse → NIK → Owner
- ✅ Special plates work correctly

## Performance
- No database lookups needed for address
- No string processing for address generation
- Direct NIK generation from plate code
- **Much faster** than previous implementation

## Migration Notes
If code previously accessed `owner.address`, it needs to be removed:
```python
# OLD CODE (will fail)
print(owner.address)

# NEW CODE
print(owner.name, owner.region)
```

All address information should be removed from display logic.
