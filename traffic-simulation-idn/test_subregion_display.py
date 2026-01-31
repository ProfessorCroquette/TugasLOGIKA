#!/usr/bin/env python3
"""Test sub-region display functionality"""

import sys
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from utils.indonesian_plates import IndonesianPlateManager

# Test extracting sub-regions from different plates
test_plates = [
    'BL A 1234 AB',  # Aceh - should show first sub-code
    'BB C 5678 XY',  # Sumatera Utara Barat - Samosir
    'BK M 9999 CD',  # Sumatera Utara Timur - Deli Serdang
    'BA A 1111 EF',  # Sumatera Barat
    'KT M 2222 GH',  # Kalimantan Timur
]

print("Testing Sub-Region Extraction from Plates")
print("=" * 80)

for plate in test_plates:
    parts = plate.split()
    plate_code = parts[0].upper()
    sub_code = parts[2].upper()
    
    if plate_code in IndonesianPlateManager.PLATE_DATA:
        plate_info = IndonesianPlateManager.PLATE_DATA[plate_code]
        region_name = plate_info.get('region_name', '?')
        sub_codes = plate_info.get('sub_codes', {})
        
        if sub_code in sub_codes:
            sub_region = sub_codes[sub_code]
            print(f"✓ Plate: {plate:20} | Region: {region_name:35} | Sub: {sub_region}")
        else:
            print(f"? Plate: {plate:20} | Region: {region_name:35} | Sub-code '{sub_code}' not found")
    else:
        print(f"✗ Plate code '{plate_code}' not found in PLATE_DATA")

print()
print("=" * 80)
print("Testing Region Code to Sub-Region Mapping")
print("=" * 80)

# Test a few region codes to get their first sub-region
test_codes = ['BL', 'BB', 'BK', 'BA', 'KT']

for code in test_codes:
    if code in IndonesianPlateManager.PLATE_DATA:
        plate_info = IndonesianPlateManager.PLATE_DATA[code]
        region_name = plate_info.get('region_name', '?')
        sub_codes = plate_info.get('sub_codes', {})
        
        if sub_codes:
            first_sub = next(iter(sub_codes.values()))
            print(f"✓ Code: {code:5} | Region: {region_name:35} | First Sub: {first_sub}")
        else:
            print(f"- Code: {code:5} | Region: {region_name:35} | No sub-codes")
    else:
        print(f"✗ Code '{code}' not found in PLATE_DATA")

print()
print("Test complete!")
