#!/usr/bin/env python3
"""Test sub-region extraction with actual plates"""

import sys
import json
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from pathlib import Path
from utils.indonesian_plates import IndonesianPlateManager

# Read actual tickets
tickets_file = Path("data_files/tickets.json")

if tickets_file.exists():
    with open(tickets_file, 'r') as f:
        tickets = json.load(f) or []
    
    print("Testing Sub-Region Extraction from Actual Plates")
    print("=" * 100)
    
    for ticket in tickets[:15]:
        plate = ticket.get('license_plate', '')
        if plate:
            parts = plate.split()
            plate_code = parts[0].upper()
            owner_code = parts[2].upper() if len(parts) > 2 else '?'
            
            sub_region = '-'
            try:
                if plate_code in IndonesianPlateManager.PLATE_DATA:
                    plate_info = IndonesianPlateManager.PLATE_DATA[plate_code]
                    region_name = plate_info.get('region_name', '?')
                    sub_codes = plate_info.get('sub_codes', {})
                    
                    # Try first letter
                    if owner_code and owner_code[0] in sub_codes:
                        sub_region = sub_codes[owner_code[0]]
                    elif owner_code in sub_codes:
                        sub_region = sub_codes[owner_code]
                    
                    print(f"✓ {plate:20} | Region: {region_name:35} | Owner Code: {owner_code:5} | Sub: {sub_region}")
                else:
                    print(f"? {plate:20} | Plate code '{plate_code}' not in PLATE_DATA")
            except Exception as e:
                print(f"✗ {plate:20} | Error: {e}")
else:
    print("No tickets.json found. Run GUI first to generate violations.")
