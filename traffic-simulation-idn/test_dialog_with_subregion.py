#!/usr/bin/env python3
"""Test the updated GUI dialog with sub-region display"""

import sys
import json
sys.path.insert(0, str(__file__).rsplit('\\', 1)[0])

from pathlib import Path
from utils.indonesian_plates import IndonesianPlateManager

# Simulate the GUI methods
def get_region_from_plate(plate: str) -> str:
    """Get main region from license plate"""
    if not plate:
        return 'Tidak Diketahui'
    
    parts = plate.split()
    if parts:
        code = parts[0].upper()
        try:
            if code in IndonesianPlateManager.PLATE_DATA:
                return IndonesianPlateManager.PLATE_DATA[code].get('region_name', f'Kode: {code}')
        except Exception:
            pass
    return 'Tidak Diketahui'

def get_sub_region_from_plate(plate: str) -> str:
    """Get sub-region from license plate based on owner code"""
    if not plate:
        return '-'
    
    parts = plate.split()
    if len(parts) < 3:
        return '-'
    
    plate_code = parts[0].upper()
    owner_code = parts[2].upper()
    
    try:
        if plate_code in IndonesianPlateManager.PLATE_DATA:
            plate_info = IndonesianPlateManager.PLATE_DATA[plate_code]
            sub_codes = plate_info.get('sub_codes', {})
            
            # Try first letter of owner code
            if owner_code and owner_code[0] in sub_codes:
                return sub_codes[owner_code[0]]
            
            # Try full owner code
            if owner_code in sub_codes:
                return sub_codes[owner_code]
    except Exception:
        pass
    
    return '-'

def get_sub_region_from_code(code: str) -> str:
    """Get sub-region from region code (for owner region)"""
    if not code or code == '-':
        return '-'
    
    code = str(code).upper().strip()
    
    try:
        if code in IndonesianPlateManager.PLATE_DATA:
            plate_info = IndonesianPlateManager.PLATE_DATA[code]
            sub_codes = plate_info.get('sub_codes', {})
            if sub_codes:
                # Return first available sub-region as representative
                first_sub = next(iter(sub_codes.values()), '-')
                return first_sub
    except Exception:
        pass
    
    return '-'

# Read actual tickets and display dialog-like output
tickets_file = Path("data_files/tickets.json")

if tickets_file.exists():
    with open(tickets_file, 'r') as f:
        tickets = json.load(f) or []
    
    print("\nSimulated ViolationDetailDialog Output (with Sub-Region Support)")
    print("=" * 100)
    
    for i, ticket in enumerate(tickets[:5]):
        plate = ticket.get('license_plate', '')
        owner_region = ticket.get('owner_region', '-')
        
        print(f"\n--- Violation #{i+1} ---")
        print(f"Informasi Kendaraan:")
        print(f"  Plat Nomor: {plate}")
        region = get_region_from_plate(plate)
        print(f"  Wilayah: {region}")
        sub_region = get_sub_region_from_plate(plate)
        print(f"  Sub-Wilayah: {sub_region}")
        
        print(f"Data Pemilik:")
        owner_region_name = IndonesianPlateManager.PLATE_DATA.get(owner_region, {}).get('region_name', owner_region) if owner_region in IndonesianPlateManager.PLATE_DATA else owner_region
        print(f"  Tempat Tinggal: {owner_region_name}")
        owner_sub_region = get_sub_region_from_code(owner_region)
        print(f"  Sub-Wilayah Tempat Tinggal: {owner_sub_region}")
else:
    print("No tickets.json found. Run GUI first to generate violations.")
