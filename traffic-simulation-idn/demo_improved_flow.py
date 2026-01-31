"""
Demonstrate the new improved flow of synchronized vehicle generation

Flow:
1. Parse PLATE → Extract region and sub_region
2. Extract administrative codes from region/sub_region → NIK digits 3-6  
3. Use province code from plate → NIK digits 1-2
4. Randomize: birthday, gender, sequential number
"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

print("\n" + "="*80)
print("NEW IMPROVED FLOW - SYNCHRONIZED VEHICLE GENERATION")
print("="*80 + "\n")

# Example: Generate vehicle with plate B (Jakarta)
plate = "B 1234 UA"
print(f"1️⃣  PARSE PLATE")
print(f"   Input: {plate}")

# Parse plate
plate_info = IndonesianPlateManager.parse_plate(plate)
if plate_info:
    print(f"   Region: {plate_info['region_name']}")
    print(f"   Sub-region: {plate_info['sub_region']}")
    print()

# Generate owner from parsed plate
db = OwnerDatabase()
owner = db.get_or_create_owner(plate)

print(f"2️⃣  GENERATE OWNER WITH SYNCHRONIZED NIK")
print(f"   NIK: {owner.owner_id}")

# Parse the NIK to show the structure
nik = owner.owner_id
print(f"\n   NIK Structure: {nik}")
print(f"   ├─ Digits 1-2 (Province):    {nik[0:2]} ← From PLATE (B = 31 for Jakarta)")
print(f"   ├─ Digits 3-4 (District):    {nik[2:4]} ← From region ({plate_info['region_name']})")
print(f"   ├─ Digits 5-6 (Subdistrict): {nik[4:6]} ← From sub_region ({plate_info['sub_region']})")
print(f"   ├─ Digits 7-8 (Birth day):   {nik[6:8]} ← RANDOMIZED")
print(f"   ├─ Digits 9-10 (Birth month): {nik[8:10]} ← RANDOMIZED")
print(f"   ├─ Digits 11-12 (Birth year): {nik[10:12]} ← RANDOMIZED")
print(f"   └─ Digits 13-16 (Sequential): {nik[12:16]} ← RANDOMIZED")
print()

print(f"3️⃣  VERIFICATION")
print(f"   Name: {owner.name}")
print(f"   Region: {owner.region}")
print(f"   Sub-region: {owner.sub_region}")
print()

# Verify sync
from utils.plate_ktp_sync import PlateKTPSync
is_sync, msg = PlateKTPSync.validate_plate_ktp_sync(plate, owner.owner_id)
status = "✓ SINKRON (SYNCHRONIZED)" if is_sync else "✗ TIDAK SINKRON"
print(f"   Plate-KTP Sync Status: {status}")
print(f"   Message: {msg}")

print("\n" + "="*80)
print("FLOW SUMMARY:")
print("="*80)
print("""
✓ PARSE PLATE             → Extract region/sub_region
✓ MAP REGION TO CODES     → Get district/subdistrict codes  
✓ BUILD NIK STRUCTURE     → Combine all codes + randomized data
✓ ENSURE SYNCHRONIZATION  → Province code matches plate domicile

Result: Plates and KTP are perfectly aligned! 🎯
""")
print("="*80 + "\n")
