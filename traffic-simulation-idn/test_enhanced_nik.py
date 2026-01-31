#!/usr/bin/env python3
"""Test the enhanced Indonesian regions and NIK parser"""

from utils.indonesian_regions import NIKParser

# Test cases
test_niks = [
    "3275075708900004",  # Maluku Utara, Female, 17 Aug 1990
    "1234567812051989",  # Female, birthday 38-12-2005 (invalid but test)
    "3179031234567890",  # Jawa Timur, Male
]

print("=" * 60)
print("TESTING ENHANCED NIK PARSER WITH REGION DATA")
print("=" * 60)

for nik in test_niks:
    print(f"\nTesting NIK: {nik}")
    print("-" * 60)
    
    data = NIKParser.parse_nik(nik)
    
    if data:
        print(f"  ✓ Parsing successful!")
        print(f"  Province: {data['province_code']} - {data['province_name']}")
        print(f"  Kabupaten: {data['kabupaten_code']} - {data['kabupaten_name']}")
        print(f"  Kecamatan: {data['kecamatan_code']} - {data['kecamatan_name']}")
        print(f"  Birthdate: {data['birth_date']}")
        print(f"  Gender: {data['gender']}")
        print(f"  Age: {data['age']} years")
        print(f"  Sequential: {data['sequential_number']}")
    else:
        print(f"  ✗ Invalid NIK format")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
