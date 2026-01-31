#!/usr/bin/env python3
"""Test plate-owner region synchronization"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

# Create database instance
owner_db = OwnerDatabase()

# Generate 10 test plates and check sync
print('Testing Plate-Owner Region Synchronization')
print('=' * 70)

mismatches = 0
mismatched_plates = []

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
        mismatched_plates.append({
            'plate': plate,
            'plate_code': plate_code,
            'expected_province': expected_province,
            'actual_province': nik_province,
            'owner': owner.name
        })
    
    print(f'{i+1}. Plate: {plate}')
    print(f'   Region: {region}, Sub-region: {sub_region}')
    print(f'   Owner: {owner.name}')
    print(f'   NIK: {owner.owner_id[:2]}... (Expected: {expected_province})')
    print(f'   Status: {match}')
    print()

print('=' * 70)
print(f'Total Mismatches: {mismatches}/10')

if mismatches > 0:
    print('\nMismatched plates:')
    for m in mismatched_plates:
        print(f"  - {m['plate']}: Expected {m['expected_province']}, got {m['actual_province']} in NIK")
        print(f"    Owner: {m['owner']}")
else:
    print('✓ All plates are synchronized correctly!')
