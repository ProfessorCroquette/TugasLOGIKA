#!/usr/bin/env python3
"""Comprehensive test to find which plates are still mismatching"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

owner_db = OwnerDatabase()

print('Testing ALL plate codes for synchronization...\n')
print('='*80)

all_codes = sorted(IndonesianPlateManager.PLATE_DATA.keys())
print(f'Testing {len(all_codes)} plate codes...\n')

mismatches = []

for plate_code in all_codes:
    expected_province = IndonesianPlateManager.PLATE_DATA[plate_code].get('province_code')
    
    # Generate a test plate for this code
    test_plate = f"{plate_code} 1 A AB"
    
    # Get owner
    owner = owner_db.get_or_create_owner(test_plate)
    actual_province = owner.owner_id[:2]
    
    status = '✓' if actual_province == expected_province else '✗'
    
    if actual_province != expected_province:
        mismatches.append({
            'code': plate_code,
            'expected': expected_province,
            'actual': actual_province,
            'owner': owner.name,
            'nik': owner.owner_id
        })
    
    print(f'{status} {plate_code}: Expected {expected_province}, Got {actual_province}')
    
    # Clear cache
    if test_plate in owner_db.owners:
        del owner_db.owners[test_plate]

print()
print('='*80)
print(f'Results: {len(all_codes) - len(mismatches)}/{len(all_codes)} PASS')

if mismatches:
    print(f'\n❌ Found {len(mismatches)} mismatches:\n')
    for m in mismatches:
        print(f'  {m["code"]}: Expected {m["expected"]}, got {m["actual"]}')
        print(f'    Owner: {m["owner"]}, NIK: {m["nik"]}')
else:
    print('\n✅ All plate codes synchronized correctly!')
