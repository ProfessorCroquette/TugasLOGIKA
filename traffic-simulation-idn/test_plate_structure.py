#!/usr/bin/env python3
"""Test actual plate structure"""

import sys
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from utils.indonesian_plates import IndonesianPlateManager

# Check actual plate generation
print("Testing Actual Plate Generation and Structure")
print("=" * 80)

# Generate a few plates from different regions
for code in ['BL', 'BB', 'BK', 'BA', 'KT']:
    if code in IndonesianPlateManager.PLATE_DATA:
        plate = IndonesianPlateManager.generate_plate(code)
        parts = plate.split()
        
        print(f"Code: {code}")
        print(f"  Generated plate: {plate}")
        print(f"  Parts: {parts}")
        print(f"  Part 0 (region code): '{parts[0]}'")
        print(f"  Part 1 (4 digits): '{parts[1]}'")
        print(f"  Part 2 (sub-code?): '{parts[2] if len(parts) > 2 else 'N/A'}'")
        print(f"  Part 3 (owner code?): '{parts[3] if len(parts) > 3 else 'N/A'}'")
        print()

print("=" * 80)
print("Checking PLATE_DATA structure")
print("=" * 80)

plate_info = IndonesianPlateManager.PLATE_DATA['BL']
print(f"BL sub_codes keys: {list(plate_info.get('sub_codes', {}).keys())[:10]}")
