#!/usr/bin/env python3
"""Detailed inspection - check if issue is in administrative codes"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

owner_db = OwnerDatabase()

print('Testing if administrative code selection causes issues...\n')
print('='*70)

# Test generating multiple owners for the same plate to see variance
test_plates = ['KT 1 A AB', 'KT 2 B BC', 'BM 1 A AB', 'BA 1 A AB', 'T 1 A AB']

for plate in test_plates:
    plate_code = plate.split()[0]
    expected_province = IndonesianPlateManager.PLATE_DATA.get(plate_code, {}).get('province_code')
    
    print(f'\nPlate: {plate}')
    print(f'Expected Province: {expected_province}')
    print('Generated owners (10 attempts):')
    print('-'*70)
    
    mismatches_for_plate = 0
    
    for i in range(10):
        owner = owner_db.get_or_create_owner(plate)
        nik = owner.owner_id
        nik_province = nik[:2]
        
        match = '✓' if nik_province == expected_province else '✗'
        
        if nik_province != expected_province:
            mismatches_for_plate += 1
        
        print(f'  {i+1}. {owner.name:20} NIK: {nik} Province: {nik_province} {match}')
        
        # Clear cache for next generation
        if plate in owner_db.owners:
            del owner_db.owners[plate]
    
    if mismatches_for_plate > 0:
        print(f'\n⚠️  {mismatches_for_plate}/10 mismatches for {plate_code}!')
    else:
        print(f'\n✓ All 10 correct for {plate_code}')
