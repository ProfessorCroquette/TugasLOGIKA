#!/usr/bin/env python3
"""Validate license plate format"""
import re
from utils.indonesian_plates import IndonesianPlateManager

# Indonesian plate format: [1-2 letters] [4 digits] [1-3 letters]
plate_pattern = r'^[A-Z]{1,2} \d{4} [A-Z]{1,3}$'

print("Validating 20 generated license plates:")
all_valid = True
for i in range(20):
    plate, region = IndonesianPlateManager.generate_plate()
    is_valid = bool(re.match(plate_pattern, plate))
    status = "✓" if is_valid else "✗"
    print(f"  {status} {plate} - {region}")
    if not is_valid:
        all_valid = False

print(f"\nAll plates valid: {'YES' if all_valid else 'NO'}")
