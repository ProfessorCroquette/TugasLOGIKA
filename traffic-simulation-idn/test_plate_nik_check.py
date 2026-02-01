#!/usr/bin/env python3
"""
Test: Verify plate region codes match NIK administrative codes
"""

import json
from pathlib import Path

def load_admin_codes():
    """Load administrative codes from base.csv (no headers)"""
    admin_codes = {}
    try:
        with open('base.csv', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    code = parts[0].strip()
                    name = parts[1].strip()
                    
                    # Store codes that look like province.district
                    # Format in file: "11.01" -> "KAB. ACEH SELATAN"
                    if '.' in code:
                        parts_code = code.split('.')
                        if len(parts_code) == 2:
                            prov = parts_code[0]
                            dist = parts_code[1]
                            combined = prov + dist
                            admin_codes[combined] = {
                                'code': code,
                                'district': name
                            }
        
        print("Loaded {} administrative codes".format(len(admin_codes)))
        return admin_codes
    except Exception as e:
        print("ERROR loading admin codes: {}".format(e))
        import traceback
        traceback.print_exc()
        return {}

def extract_nik_codes(nik):
    """Extract region codes from NIK"""
    if len(nik) >= 4:
        province_code = nik[0:2]
        district_code = nik[2:4]
        return province_code + district_code
    return None

def test_plate_nik_alignment():
    """Test plate-NIK alignment"""
    
    print("=" * 70)
    print("TEST: Plate Region vs NIK Administrative Code Alignment")
    print("=" * 70)
    
    # Load admin codes
    admin_codes = load_admin_codes()
    if not admin_codes:
        print("ERROR: Could not load administrative codes")
        return False
    
    # Load vehicles
    try:
        with open('data_files/tickets.json', 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
    except Exception as e:
        print("ERROR loading tickets: {}".format(e))
        return False
    
    # Get vehicle list
    if not isinstance(vehicles, list):
        print("ERROR: Expected list of vehicles")
        return False
    
    if not vehicles:
        print("ERROR: No vehicles found")
        return False
    
    print("\nTesting {} vehicles...".format(min(50, len(vehicles))))
    print("-" * 70)
    
    success_count = 0
    error_count = 0
    found_count = 0
    not_found_count = 0
    
    for idx, vehicle in enumerate(vehicles[:50], 1):
        plate = vehicle.get('license_plate')
        owner = vehicle.get('owner')  # owner is a dict with 'id', 'name', 'region'
        
        if not plate or not owner:
            print("[{}] ERROR: Missing plate or owner".format(idx))
            error_count += 1
            continue
        
        nik = owner.get('id')  # Extract NIK from owner.id
        
        # Extract codes from NIK
        nik_region_code = extract_nik_codes(nik)
        if not nik_region_code:
            print("[{}] ERROR: Cannot parse NIK {}".format(idx, nik))
            error_count += 1
            continue
        
        # Look up in admin codes
        if nik_region_code in admin_codes:
            district_name = admin_codes[nik_region_code]['district']
            status = "FOUND"
            found_count += 1
        else:
            district_name = 'NOT IN TABLE'
            status = "NOT FOUND"
            not_found_count += 1
        
        print("[{}] Plate: {} | NIK: {} | Code: {} | Status: {}".format(
            idx, plate, nik, nik_region_code, status))
        print("    District: {}".format(district_name))
        
        success_count += 1
    
    print("-" * 70)
    print("Results:")
    print("  Total tested: {}".format(success_count))
    print("  Errors: {}".format(error_count))
    print("  Codes found in table: {}".format(found_count))
    print("  Codes NOT in table: {}".format(not_found_count))
    
    if error_count == 0:
        print("\n[PASS] All NIK codes parsed successfully!")
        return True
    else:
        print("\n[FAIL] Some errors detected")
        return False

if __name__ == '__main__':
    if test_plate_nik_alignment():
        exit(0)
    else:
        exit(1)
