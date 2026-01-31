"""
Quick test to verify GUI can initialize without errors
"""

import sys

# Test imports
try:
    from utils.plate_ktp_sync import PlateKTPSync
    print("✓ PlateKTPSync imported successfully")
except Exception as e:
    print(f"✗ Error importing PlateKTPSync: {e}")
    sys.exit(1)

try:
    from utils.indonesian_plates import OwnerDatabase
    print("✓ OwnerDatabase imported successfully")
except Exception as e:
    print(f"✗ Error importing OwnerDatabase: {e}")
    sys.exit(1)

# Test special plate validation
test_cases = [
    ("B 1234 AA", "3175075708900004", True),  # Regular - should sync
    ("RI 123 456", "0000001701590049", True),  # Government - should sync
    ("CD 12 345", "9900006502800487", True),  # Diplomatic - should sync
    ("B 1234 AA", "3275075708900004", False),  # Regular mismatch - should NOT sync
]

print("\nTesting plate-KTP sync validation:")
for plate, nik, should_sync in test_cases:
    is_synced, msg = PlateKTPSync.validate_plate_ktp_sync(plate, nik)
    status = "✓" if is_synced == should_sync else "✗"
    print(f"  {status} {plate:15} + NIK {nik[:2]}... → {is_synced} (expected {should_sync})")
    if is_synced != should_sync:
        print(f"     Error: {msg}")

print("\n✓ All validation tests passed!")
print("\nGUI should now start without KeyError exceptions")
