#!/usr/bin/env python3
"""Monitor GUI-generated violations to verify region synchronization"""

import json
import time
from pathlib import Path
from utils.indonesian_plates import IndonesianPlateManager

print('Monitoring tickets.json for proper region synchronization...')
print('='*70)

violations_file = Path("data_files/tickets.json")

# Wait for some violations to be generated
start_time = time.time()
last_count = 0

while time.time() - start_time < 30:  # Monitor for 30 seconds
    if violations_file.exists():
        try:
            with open(violations_file, 'r') as f:
                violations = json.load(f) or []
            
            if len(violations) > last_count:
                # Check new violations
                for v in violations[last_count:]:
                    plate = v.get('license_plate', '')
                    owner_id = v.get('owner_id', '')
                    owner_region = v.get('owner_region', '')
                    
                    if plate and owner_id:
                        plate_code = plate.split()[0]
                        expected_province = IndonesianPlateManager.PLATE_DATA.get(plate_code, {}).get('province_code', 'XX')
                        actual_province = owner_id[:2]
                        
                        match = '✓' if actual_province == expected_province else '✗'
                        print(f'{match} {plate:20} | Owner Region: {owner_region:30} | NIK: {owner_id[:2]}... (expected {expected_province})')
                
                last_count = len(violations)
        except Exception as e:
            pass
    
    time.sleep(1)

print()
print('='*70)
print('Monitoring complete')
