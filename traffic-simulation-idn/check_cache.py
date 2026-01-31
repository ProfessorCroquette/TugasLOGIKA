#!/usr/bin/env python3
"""Check if there's a caching issue with the global owner_db"""

import sys
sys.path.insert(0, '.')

# Import the module that might be using old code
from utils.indonesian_plates import owner_db, IndonesianPlateManager

print('Checking global owner_db cache...\n')
print('='*70)

print(f'Global owner_db object: {owner_db}')
print(f'Owners in cache: {len(owner_db.owners)}')
print()

if owner_db.owners:
    print('Cached owners:')
    for plate, owner in list(owner_db.owners.items())[:10]:
        nik_province = owner.owner_id[:2]
        plate_code = plate.split()[0]
        expected = IndonesianPlateManager.PLATE_DATA.get(plate_code, {}).get('province_code')
        match = '✓' if nik_province == expected else '✗'
        print(f'  {plate} → NIK {nik_province}... (expected {expected}) {match}')
    
    if len(owner_db.owners) > 10:
        print(f'  ... and {len(owner_db.owners) - 10} more')
else:
    print('No cached owners')

print()
print('='*70)
print('To fix any caching issues:')
print('1. Restart the Python kernel')
print('2. Or clear the owner cache: owner_db.owners.clear()')
