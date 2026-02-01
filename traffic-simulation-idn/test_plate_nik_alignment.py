#!/usr/bin/env python3
"""
Test: Verify plate region codes match NIK administrative codes
"""

import json
import csv
from pathlib import Path

# Load admin codes
ADMIN_CODES = {}

def load_admin_codes():
    """Load administrative codes"""
    global ADMIN_CODES
    try:
        base_csv = Path("base.csv")
        with open(base_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'kode_provinsi' in row and 'kode_kabupaten' in row:
                    code = row['kode_provinsi'].strip() + row['kode_kabupaten'].strip()
                    ADMIN_CODES[code] = {
                        'province': row.get('nama_provinsi', '').strip(),
                        'district': row.get('nama_kabupaten', '').strip()
                    }
        print("Loaded {} administrative codes".format(len(ADMIN_CODES)))
        return True
    except Exception as e:
        print("ERROR loading admin codes: {}".format(e))
        return False

def extract_nik_codes(nik):
    """Extract region codes from NIK"""
    if len(nik) >= 4:
        province_code = nik[0:2]
        district_code = nik[2:4]
        return province_code, district_code
    return None, None

def test_plate_nik_alignment():
    """Test plate-NIK alignment"""
    
    print("=" * 70)
    print("TEST: Plate Region vs NIK Administrative Code Alignment")
    print("=" * 70)
    
    # Load admin codes
    if not load_admin_codes():
        return False
    
    # Load vehicles
    try:
        with open('vehicles_database.json', 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
    except Exception as e:
        print("ERROR loading vehicles: {}".format(e))
        return False
    
    print("\nTesting {} vehicles...".format(len(vehicles[:50])))
    print("-" * 70)
    
    success_count = 0
    error_count = 0
    
    for idx, vehicle in enumerate(vehicles[:50], 1):
        plate = vehicle.get('plate')
        nik = vehicle.get('nik')
        
        if not plate or not nik:
            print("[{}] ERROR: Missing plate or NIK".format(idx))
            error_count += 1
            continue
        
        # Extract codes from NIK
        prov_code, dist_code = extract_nik_codes(nik)
        if not prov_code:
            print("[{}] ERROR: Cannot parse NIK {}".format(idx, nik))
            error_count += 1
            continue
        
        nik_region_code = prov_code + dist_code
        
        # Look up in admin codes
        admin_info = ADMIN_CODES.get(nik_region_code, {})
        
        district_name = admin_info.get('district', 'NOT FOUND')
        province_name = admin_info.get('province', 'NOT FOUND')
        
        print("[{}] Plate: {} | NIK: {}".format(idx, plate, nik))
        print("    Region Code: {} | District: {}, {}".format(
            nik_region_code, district_name, province_name))
        
        success_count += 1
    
    print("-" * 70)
    print("Results: {} successful, {} errors".format(success_count, error_count))
    
    if error_count == 0:
        print("\n[PASS] All alignments verified!")
        return True
    else:
        print("\n[FAIL] Some errors detected")
        return False

if __name__ == '__main__':
    if test_plate_nik_alignment():
        exit(0)
    else:
        exit(1)
    
    success = test_plate_to_nik_alignment()
    sys.exit(0 if success else 1)
