# QUICK REFERENCE - CORRECT FLOW

## Problem & Solution (1 Minute Summary)

**PROBLEM**: Owner was generated independently, not matching plate region
```
Plate: B (Jakarta, Province 31)
Old Owner NIK: 3205... (Province 32) ❌ WRONG!
```

**SOLUTION**: Generate owner FROM plate, synchronized
```
Plate: B (Jakarta, Province 31)
New Owner NIK: 3174... (Province 31) ✓ CORRECT!
```

---

## 3 New Methods

### 1. Extract Region Info from Plate
```python
from utils.indonesian_plates import IndonesianPlateManager

info = IndonesianPlateManager.extract_region_info_from_plate("B 4123 RK")
# {
#   'region_code': 'B',
#   'province_code': '31',  ← KEY: Use this for NIK generation
#   'region_name': 'DKI Jakarta',
#   'vehicle_type': 'PRIBADI'
# }
```

### 2. Generate Owner FROM Plate (THE KEY ONE!)
```python
owner = IndonesianPlateManager.generate_owner_from_plate("B 4123 RK", "roda_dua")
# VehicleOwner(
#   owner_id='3174056510920071',  ← Starts with '31' from plate!
#   name='Ahmad Gunawan',
#   address='Jl. Kartini No.272, Jakarta Selatan',
#   ...
# )
```

### 3. Generate Address from Region
```python
address = VehicleOwner._generate_address("Jakarta Selatan")
# "Jl. Melati No.1, Jakarta Selatan, DKI Jakarta"
```

---

## Complete Example (Copy & Paste)

```python
from utils.indonesian_plates import IndonesianPlateManager

# Generate plate
plate, region, sub_region, vtype = IndonesianPlateManager.generate_plate()
print(f"Plate: {plate}")

# Generate owner FROM plate (correct flow!)
owner = IndonesianPlateManager.generate_owner_from_plate(plate, "roda_dua")
print(f"Owner: {owner.name}")
print(f"NIK: {owner.owner_id}")
print(f"Address: {owner.address}")

# Validate (optional, but recommended)
region_info = IndonesianPlateManager.extract_region_info_from_plate(plate)
nik_prov = owner.owner_id[:2]
plate_prov = region_info['province_code']

if nik_prov == plate_prov:
    print(f"✓ SYNCHRONIZED ({nik_prov})")
else:
    print(f"✗ NOT SYNCHRONIZED ({nik_prov} != {plate_prov})")
```

---

## NIK Structure (Quick Guide)

```
NIK Format (16 digits): [Province(2)] [City(2)] [District(2)] [Birth(6)] [Seq(4)]

Example: 3174056510920071
├─ 31 = DKI Jakarta (Province)
├─ 74 = Jakarta Selatan (City)
├─ 05 = Kebayoran Baru (District)
├─ 65 = Female, born 25th
├─ 10 = October
├─ 92 = 1992
└─ 0071 = Sequential number

Key: First 2 digits MUST match plate province code!
```

---

## Plate Province Codes (Common Ones)

```python
'B':  '31'  # DKI Jakarta
'D':  '32'  # Jawa Barat
'H':  '33'  # Jawa Tengah
'AB': '34'  # Yogyakarta
'L':  '35'  # Jawa Timur
'A':  '36'  # Banten

'BL': '11'  # Aceh
'BA': '13'  # Sumatera Barat

'RI': '00'  # Government
'CD': '99'  # Diplomatic
'CC': '99'  # Consular
```

---

## Old Way vs New Way

### ❌ OLD WAY (WRONG)
```python
# Generate plate
plate = generate_random_plate()  # "B 4123 RK"

# Generate owner INDEPENDENTLY (not from plate!)
owner = owner_db.get_or_create_owner(plate)  # NIK might start with 32!

# Result: MISMATCHED!
```

### ✓ NEW WAY (CORRECT)
```python
# Generate plate
plate = IndonesianPlateManager.generate_plate()  # "B 4123 RK"

# Generate owner FROM plate (synchronized!)
owner = IndonesianPlateManager.generate_owner_from_plate(plate, "roda_dua")

# Result: SYNCHRONIZED! NIK starts with 31!
```

---

## Test Files

**Run to verify**:
```bash
# Comprehensive test suite
python test_correct_flow.py

# Practical usage example
python example_correct_flow.py

# Backward compatibility check
python test_plate_system.py
```

---

## Integration Checklist

- [ ] Replace `owner_db.get_or_create_owner()` with `generate_owner_from_plate()`
- [ ] Update main.py to use new method
- [ ] Update gui_traffic_simulation.py if needed
- [ ] Test with old test suite (backward compatibility)
- [ ] Run test_correct_flow.py to verify
- [ ] Verify synchronization in actual runs

---

## Key Points to Remember

1. **ALWAYS use `generate_owner_from_plate()`** when generating owner from existing plate
2. **Plate province code MUST match NIK province code** (first 2 digits)
3. **Address is auto-generated** from sub_region
4. **Test synchronization** with simple check: `nik[:2] == province_code`
5. **All 48 plate codes supported** (check PLATE_CODE_TO_PROVINCE)

---

## Documentation Files

1. **test_correct_flow.py** - Full test suite
2. **example_correct_flow.py** - Usage examples
3. **docs/CORRECT_FLOW_EXPLANATION.md** - Detailed docs
4. **CORRECT_FLOW_FIX_COMPLETE.md** - Implementation details
5. **CORRECT_FLOW_IMPLEMENTATION_SUMMARY.md** - Full summary

---

## Need Help?

**For questions about**:
- Plate parsing → See `extract_region_info_from_plate()`
- Owner generation → See `generate_owner_from_plate()`
- Address generation → See `_generate_address()`
- NIK structure → See test files or docs
- Province codes → Check `PLATE_CODE_TO_PROVINCE`
