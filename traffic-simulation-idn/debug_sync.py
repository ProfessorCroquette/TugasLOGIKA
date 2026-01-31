#!/usr/bin/env python3
"""Detailed debug test for plate-owner synchronization"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

# Create database instance
owner_db = OwnerDatabase()

print('=== DETAILED SYNC DEBUG TEST ===\n')

# Test with specific problematic plates
test_cases = [
    'BM 735 Y FM',  # Riau plate but got 31 in NIK
    'T 34 P UX',    # Jawa Barat plate but got 36 in NIK
]

for plate in test_cases:
    print(f'Testing: {plate}')
    print('-' * 60)
    
    # Extract plate code
    plate_code = plate.split()[0]
    print(f'  Plate Code: {plate_code}')
    
    # Get expected province code
    if plate_code in IndonesianPlateManager.PLATE_DATA:
        plate_data = IndonesianPlateManager.PLATE_DATA[plate_code]
        expected_province = plate_data.get('province_code', 'XX')
        region_name = plate_data.get('region_name', '?')
        print(f'  Expected Province Code: {expected_province}')
        print(f'  Region: {region_name}')
        print(f'  Sub-codes available: {len(plate_data.get("sub_codes", {}))}')
    else:
        print(f'  ERROR: Plate code {plate_code} not found in PLATE_DATA')
        expected_province = 'XX'
    
    # Generate owner multiple times to see if issue is random or deterministic
    print(f'\n  Generated Owners (5 attempts):')
    for attempt in range(5):
        owner = owner_db.get_or_create_owner(plate)
        actual_province = owner.owner_id[:2]
        match = '✓' if actual_province == expected_province else '✗'
        print(f'    {attempt+1}. {owner.name}: NIK {owner.owner_id} ({actual_province}) {match}')
    
    # Clear from cache to get new generation
    if plate in owner_db.owners:
        del owner_db.owners[plate]
    
    print()
