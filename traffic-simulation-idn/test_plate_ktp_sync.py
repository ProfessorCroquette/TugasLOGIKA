#!/usr/bin/env python3
"""
Test Plate-KTP Synchronization
Verify that vehicle plates match owner's KTP province code
"""

from utils.plate_ktp_sync import PlateKTPSync

print("=" * 70)
print("TESTING PLATE-KTP SYNCHRONIZATION")
print("=" * 70)

# Test cases: (plate, nik, expected_valid, description)
test_cases = [
    # Valid synchronizations
    ("B 1234 AA", "3171005708900004", True, "Jakarta plate + Jakarta KTP"),
    ("L 5678 BK", "3575065708900004", True, "Surabaya plate + Jawa Timur KTP"),
    ("E 9012 AB", "3275075708900004", True, "Jawa Barat plate + Jawa Barat KTP"),
    ("H 3456 AC", "3375085708900004", True, "Jawa Tengah plate + Jawa Tengah KTP"),
    ("P 7890 AD", "5175095708900004", True, "Bali plate + Bali KTP"),
    
    # Invalid synchronizations
    ("B 1234 AA", "3275075708900004", False, "Jakarta plate but Jawa Barat KTP (MISMATCH)"),
    ("L 5678 BK", "3171005708900004", False, "Surabaya plate but Jakarta KTP (MISMATCH)"),
    ("E 9012 AB", "3171005708900004", False, "Jawa Barat plate but Jakarta KTP (MISMATCH)"),
]

print("\nTEST RESULTS:")
print("-" * 70)

passed = 0
failed = 0

for plate, nik, expected_valid, description in test_cases:
    is_valid, message = PlateKTPSync.validate_plate_ktp_sync(plate, nik)
    
    status = "✓ PASS" if is_valid == expected_valid else "✗ FAIL"
    if is_valid == expected_valid:
        passed += 1
    else:
        failed += 1
    
    print(f"\n{status}")
    print(f"  Plate: {plate}")
    print(f"  KTP: {nik[:2]}xxxxx... (Province: {nik[:2]})")
    print(f"  Description: {description}")
    print(f"  Result: {message}")

print("\n" + "=" * 70)
print("PROVINCE CODE LOOKUP TESTS")
print("=" * 70)

# Test plate to province lookups
test_plates = ['B', 'E', 'D', 'H', 'L', 'M', 'AA', 'AB', 'P', 'W', 'KB', 'PA']

print("\nPLATE → PROVINCE CODE:")
print("-" * 70)
for plate_prefix in test_plates:
    province = PlateKTPSync.get_province_by_plate(plate_prefix)
    if province:
        plate_info = PlateKTPSync.PLATE_PROVINCE_MAP.get(plate_prefix, {})
        print(f"  {plate_prefix:3} → {province} ({plate_info.get('name', 'Unknown')})")

print("\n" + "=" * 70)
print("PROVINCE CODE TO PLATE LOOKUP")
print("=" * 70)

# Test province to plate lookups
test_provinces = ['31', '32', '33', '34', '35', '36', '51', '73', '81', '94']

print("\nPROVINCE CODE → PLATE PREFIX:")
print("-" * 70)
for province_code in test_provinces:
    plate = PlateKTPSync.get_plate_prefix_by_province(province_code)
    if plate:
        plate_info = PlateKTPSync.PLATE_PROVINCE_MAP.get(plate, {})
        print(f"  {province_code} → {plate:3} ({plate_info.get('name', 'Unknown')})")

print("\n" + "=" * 70)
print("SYNC EXAMPLES")
print("=" * 70)

# Example: Generate appropriate plate for a NIK
example_nik = "3275075708900004"  # Jawa Barat (32)
suggested_plate = PlateKTPSync.sync_plate_to_ktp(example_nik)
print(f"\nFor NIK: {example_nik}")
print(f"  Province code: {example_nik[:2]} (Jawa Barat)")
print(f"  Suggested plate prefix: {suggested_plate}")

# Example: Check what province a plate belongs to
example_plate = "L 5678 BK"
nik_province = PlateKTPSync.sync_ktp_to_plate(example_plate)
print(f"\nFor Plate: {example_plate}")
print(f"  Plate prefix: L")
print(f"  Required NIK province code: {nik_province} (Jawa Timur)")

print("\n" + "=" * 70)
print(f"SUMMARY: {passed} PASSED, {failed} FAILED")
print("=" * 70)
