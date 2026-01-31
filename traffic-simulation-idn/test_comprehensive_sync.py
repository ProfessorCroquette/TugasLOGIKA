#!/usr/bin/env python3
"""Comprehensive plate-owner region synchronization test"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

# Create a FRESH database instance
owner_db = OwnerDatabase()

# Generate 50 test plates to ensure reliability
print('Comprehensive Plate-Owner Region Synchronization Test')
print('=' * 70)
print('Testing 50 plates...\n')

mismatches = 0
failed_plates = []

for i in range(50):
    plate, region, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
    owner = owner_db.get_or_create_owner(plate)
    
    # Extract province code from plate
    plate_code = plate.split()[0]
    
    # Extract province code from NIK (first 2 digits)
    nik_province = owner.owner_id[:2] if len(owner.owner_id) >= 2 else 'XX'
    
    # Get expected province code for this plate
    plate_info = IndonesianPlateManager.PLATE_DATA.get(plate_code, {})
    expected_province = plate_info.get('province_code', 'XX')
    
    if nik_province != expected_province:
        mismatches += 1
        failed_plates.append({
            'plate': plate,
            'expected': expected_province,
            'actual': nik_province,
            'owner': owner.name
        })

print(f'Results: {50 - mismatches}/50 PASS')
print('=' * 70)

if mismatches == 0:
    print('✓ SUCCESS: All 50 plates are synchronized correctly!')
    print('\nPlate-Owner Region Synchronization is FIXED!')
else:
    print(f'✗ FAILURE: {mismatches} plates failed synchronization')
    print('\nFailed plates:')
    for f in failed_plates:
        print(f"  {f['plate']}: Expected {f['expected']}, got {f['actual']} ({f['owner']})")
