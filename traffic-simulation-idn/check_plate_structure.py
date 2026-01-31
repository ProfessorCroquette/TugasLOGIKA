#!/usr/bin/env python3
"""Check plate structure by reading actual violation data"""

import sys
import json
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from pathlib import Path

# Read actual tickets to see the plate structure
tickets_file = Path("data_files/tickets.json")

if tickets_file.exists():
    with open(tickets_file, 'r') as f:
        tickets = json.load(f) or []
    
    print("Sample plates from actual violation data:")
    print("=" * 80)
    
    seen_plates = set()
    for ticket in tickets[:20]:
        plate = ticket.get('license_plate', '')
        if plate and plate not in seen_plates:
            parts = plate.split()
            seen_plates.add(plate)
            
            print(f"Plate: {plate}")
            print(f"  Parts breakdown:")
            for i, part in enumerate(parts):
                print(f"    [{i}] = '{part}'")
            print()
            
            if len(seen_plates) >= 10:
                break
else:
    print("No tickets.json found. Run the GUI first to generate some violations.")
