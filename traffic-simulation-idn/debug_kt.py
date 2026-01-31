#!/usr/bin/env python3
"""Debug KT and other specific codes"""

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

# Test KT specifically
print('Testing KT (Kalimantan Timur) Synchronization')
print('='*70)

kt_data = IndonesianPlateManager.PLATE_DATA.get('KT', {})
print(f'PLATE_DATA[KT]:')
print(f'  region_name: {kt_data.get("region_name")}')
print(f'  province_code: {kt_data.get("province_code")}')
print()

# Test the method
kt_province = IndonesianPlateManager.get_province_code_from_plate_code('KT')
print(f'get_province_code_from_plate_code("KT"): {kt_province}')
print()

# Generate some KT plates and check owners
owner_db = OwnerDatabase()

print('Testing 10 KT plates:')
print('-'*70)

for i in range(10):
    # Generate a plate with KT code
    plate = f"KT {i+1} A AB"  # Simplified format
    
    # Try to get owner
    try:
        owner = owner_db.get_or_create_owner(plate)
        nik_province = owner.owner_id[:2]
        expected_province = '64'
        
        match = '✓' if nik_province == expected_province else '✗'
        print(f'{i+1}. {plate} → NIK: {owner.owner_id[:2]}... (expected 64) {match}')
        
        if nik_province != expected_province:
            print(f'   MISMATCH! Owner: {owner.name}, Region: {owner.region}')
    except Exception as e:
        print(f'{i+1}. {plate} → ERROR: {e}')
    
    # Clear cache
    if plate in owner_db.owners:
        del owner_db.owners[plate]

print()

# Check if there's an issue with how OwnerDatabase extracts province code
print('='*70)
print('Checking OwnerDatabase.get_or_create_owner() logic:')
print('-'*70)

plate = "KT 1 A AB"
plate_code = plate.split()[0]
print(f'Plate: {plate}')
print(f'Plate code: {plate_code}')
print(f'PLATE_DATA has KT: {"KT" in IndonesianPlateManager.PLATE_DATA}')

if 'KT' in IndonesianPlateManager.PLATE_DATA:
    plate_data = IndonesianPlateManager.PLATE_DATA['KT']
    print(f'Province code from PLATE_DATA: {plate_data.get("province_code")}')

required_province = IndonesianPlateManager.get_province_code_from_plate_code(plate_code)
print(f'Required province from method: {required_province}')
