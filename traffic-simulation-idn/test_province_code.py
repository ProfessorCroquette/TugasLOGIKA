#!/usr/bin/env python3
"""Test get_province_code_from_plate_code"""

from utils.indonesian_plates import IndonesianPlateManager

test_codes = ['BM', 'T', 'AA', 'D', 'L', 'BB', 'BA']

print('Testing get_province_code_from_plate_code():')
print('=' * 50)

for code in test_codes:
    if code in IndonesianPlateManager.PLATE_DATA:
        plate_data = IndonesianPlateManager.PLATE_DATA[code]
        province_from_data = plate_data.get('province_code', '??')
        
        # Try the method
        province_from_method = IndonesianPlateManager.get_province_code_from_plate_code(code)
        
        match = '✓' if province_from_data == province_from_method else '✗ MISMATCH'
        print(f'{code}: Data={province_from_data}, Method={province_from_method} {match}')
    else:
        print(f'{code}: NOT IN PLATE_DATA')
