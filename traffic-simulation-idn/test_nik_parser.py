#!/usr/bin/env python3
"""Quick test of NIK parser integration"""

from utils.nik_parser import NIKParser

# Test examples
test_niks = [
    "3275075708900004",  # Female from user example
    "1234567812051989",  # Male example (if valid)
]

print("=" * 60)
print("NIK PARSER TEST")
print("=" * 60)

for nik in test_niks:
    print(f"\nTesting NIK: {nik}")
    result = NIKParser.parse_nik(nik)
    
    if result:
        print(f"  ✓ Status: VALID")
        print(f"  ✓ Formatted: {result['nik_formatted']}")
        print(f"  ✓ Province: {result['province_name']}")
        print(f"  ✓ Gender: {result['gender']}")
        print(f"  ✓ Birth Date: {result['birth_date']}")
        print(f"  ✓ Age Category: {NIKParser.get_age_category(result['birth_year'])}")
    else:
        print(f"  ✗ Status: INVALID")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
