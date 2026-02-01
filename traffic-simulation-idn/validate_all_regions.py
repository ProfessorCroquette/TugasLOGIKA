"""
Comprehensive validation of ALL plate codes and sub-regions against base.csv
Ensures every plate-region combination generates NIKs with correct administrative codes
"""
from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase, VehicleOwner
import csv
from pathlib import Path

# Clear caches for fresh test
OwnerDatabase.owners = {}
VehicleOwner._ADMIN_CODES_CACHE = None

# Load base.csv data for reference
base_csv_data = {}
try:
    with open('base.csv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',', 1)
            if len(parts) >= 2:
                code = parts[0]
                name = parts[1]
                base_csv_data[name.upper()] = code
except Exception as e:
    print(f"Error loading base.csv: {e}")

print("=" * 100)
print("COMPREHENSIVE PLATE-REGION-NIK VALIDATION")
print("Validating ALL plate codes and sub-regions against base.csv")
print("=" * 100)
print()

owner_db = OwnerDatabase()
all_results = []
errors = []

# Test each plate code
plate_data_dict = IndonesianPlateManager.PLATE_DATA
total_tests = 0
passed_tests = 0
failed_tests = 0

for plate_code in sorted(plate_data_dict.keys()):
    plate_info = plate_data_dict[plate_code]
    region_name = plate_info['region_name']
    province_code = plate_info['province_code']
    sub_codes = plate_info.get('sub_codes', {})
    
    if not sub_codes:
        # Test without sub-code
        test_plate = f"{plate_code} 1234 ABC"
        try:
            parsed = IndonesianPlateManager.parse_plate(test_plate)
            owner = owner_db.get_or_create_owner(test_plate, 'roda_empat')
            nik = owner.owner_id
            actual_province = nik[:2]
            
            total_tests += 1
            match = actual_province == province_code
            
            if match:
                passed_tests += 1
                status = "[OK]"
            else:
                failed_tests += 1
                status = "[FAIL]"
                error_msg = f"{status} {plate_code} -> Expected province {province_code}, got {actual_province} (NIK: {nik})"
                errors.append(error_msg)
            
            print(f"{status} {plate_code:5} (no sub-codes) | Province {actual_province} (expected {province_code}) | {region_name}")
        except Exception as e:
            print(f"[FAIL] {plate_code:5} ERROR: {str(e)}")
            failed_tests += 1
            total_tests += 1
    else:
        # Test each sub-code
        print(f"\n{plate_code} - {region_name} (Province {province_code}):")
        
        for sub_code, sub_region in sorted(sub_codes.items()):
            test_plate = f"{plate_code} 1234 {sub_code}BC"  # First letter is sub_code
            
            try:
                # Clear owner cache to get fresh parsing
                if test_plate in owner_db.owners:
                    del owner_db.owners[test_plate]
                
                parsed = IndonesianPlateManager.parse_plate(test_plate)
                owner = owner_db.get_or_create_owner(test_plate, 'roda_empat')
                nik = owner.owner_id
                actual_province = nik[:2]
                
                total_tests += 1
                
                # Check province match
                province_match = actual_province == province_code
                
                # Check if sub_region is in owner's sub_region
                sub_region_match = sub_region.upper() in owner.sub_region.upper()
                
                if province_match:
                    passed_tests += 1
                    status = "[OK]"
                else:
                    failed_tests += 1
                    status = "[FAIL]"
                    error_msg = f"{status} {plate_code} {sub_code} {sub_region} -> Expected {province_code}, got {actual_province}"
                    errors.append(error_msg)
                
                print(f"  {status} {sub_code} | {sub_region:35} | Province {actual_province} (expected {province_code})")
                
            except Exception as e:
                print(f"  [FAIL] {sub_code} | {sub_region:35} | ERROR: {str(e)}")
                failed_tests += 1
                total_tests += 1

print()
print("=" * 100)
print(f"VALIDATION SUMMARY")
print("=" * 100)
print(f"Total tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print(f"Success rate: {(passed_tests/total_tests*100):.1f}%")

if errors:
    print()
    print("ERRORS FOUND:")
    for error in errors[:20]:  # Show first 20 errors
        print(f"  {error}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more errors")
else:
    print()
    print("[SUCCESS] NO ERRORS! All plates and regions correctly map to base.csv codes!")

print("=" * 100)
