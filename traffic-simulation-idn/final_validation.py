#!/usr/bin/env python3
"""Final comprehensive system validation after plate-owner sync fix"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

print('='*70)
print('FINAL SYSTEM VALIDATION - PLATE-OWNER SYNCHRONIZATION')
print('='*70)

# Test 1: Plate generation
print('\n1. Testing Plate Generation...')
try:
    plate, region, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
    print(f'   ✓ Generated plate: {plate}')
    print(f'     Region: {region}, Sub: {sub_region}')
except Exception as e:
    print(f'   ✗ Error: {e}')
    exit(1)

# Test 2: Province code extraction
print('\n2. Testing Province Code Extraction...')
try:
    plate_code = plate.split()[0]
    province = IndonesianPlateManager.get_province_code_from_plate_code(plate_code)
    print(f'   ✓ Plate code: {plate_code} → Province: {province}')
except Exception as e:
    print(f'   ✗ Error: {e}')
    exit(1)

# Test 3: Owner generation with sync
print('\n3. Testing Owner Generation with Sync...')
try:
    owner_db = OwnerDatabase()
    owner = owner_db.get_or_create_owner(plate)
    nik_province = owner.owner_id[:2]
    print(f'   ✓ Owner: {owner.name}')
    print(f'     NIK: {owner.owner_id}')
    print(f'     Region: {owner.region}')
    if nik_province == province:
        print(f'     Sync: ✓ NIK province {nik_province} matches plate province {province}')
    else:
        print(f'     Sync: ✗ MISMATCH - NIK {nik_province} vs Plate {province}')
        exit(1)
except Exception as e:
    print(f'   ✗ Error: {e}')
    exit(1)

# Test 4: Bulk sync test
print('\n4. Running Bulk Synchronization Test (100 plates)...')
try:
    owner_db = OwnerDatabase()
    mismatches = 0
    
    for i in range(100):
        plate, region, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
        owner = owner_db.get_or_create_owner(plate)
        
        plate_code = plate.split()[0]
        expected_province = IndonesianPlateManager.PLATE_DATA.get(plate_code, {}).get('province_code', 'XX')
        actual_province = owner.owner_id[:2]
        
        if expected_province != actual_province:
            mismatches += 1
    
    if mismatches == 0:
        print(f'   ✓ All 100 plates synchronized correctly!')
    else:
        print(f'   ✗ {mismatches}/100 plates failed')
        exit(1)
        
except Exception as e:
    print(f'   ✗ Error: {e}')
    exit(1)

print('\n' + '='*70)
print('✅ SYSTEM VALIDATION COMPLETE - ALL TESTS PASSED')
print('='*70)
print('\nSummary:')
print('  ✓ Plate generation: Working correctly')
print('  ✓ Province code extraction: Fixed and accurate')
print('  ✓ Owner generation: Synchronized with plate region')
print('  ✓ Bulk test: 100/100 plates synchronized')
print('\nPlate-Owner Region Synchronization: ✅ FIXED AND VERIFIED')
