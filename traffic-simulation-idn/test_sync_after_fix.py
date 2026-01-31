#!/usr/bin/env python3
"""Test plate-owner region synchronization after fix"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

# Create a FRESH database instance (new cache, not using global owner_db)
owner_db = OwnerDatabase()

# Generate 10 test plates and check sync
print('Testing Plate-Owner Region Synchronization (After Fix)')
print('=' * 70)

mismatches = 0
for i in range(10):
    plate, region, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
    owner = owner_db.get_or_create_owner(plate)
    
    # Extract region code from plate
    plate_code = plate.split()[0]
    
    # Extract province code from NIK (first 2 digits)
    nik_province = owner.owner_id[:2] if len(owner.owner_id) >= 2 else 'XX'
    
    # Get expected province code for this plate
    plate_info = IndonesianPlateManager.PLATE_DATA.get(plate_code, {})
    expected_province = plate_info.get('province_code', 'XX')
    
    match = '✓' if nik_province == expected_province else '✗ MISMATCH'
    
    if nik_province != expected_province:
        mismatches += 1
    
    print(f'{i+1}. Plate: {plate}')
    print(f'   Region: {region}, Sub-region: {sub_region}')
    print(f'   Owner: {owner.name}')
    print(f'   NIK: {owner.owner_id[:2]}... (Expected: {expected_province})')
    print(f'   Status: {match}')
    print()

print('=' * 70)
print(f'Total Mismatches: {mismatches}/10')
if mismatches == 0:
    print('✓ All plates are synchronized correctly!')
else:
    print('✗ Still have mismatches - investigation needed')
