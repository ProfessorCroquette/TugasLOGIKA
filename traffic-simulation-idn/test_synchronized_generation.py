"""
Test script to verify plate-KTP synchronized vehicle generation

Indonesian Compliance Test:
When generating vehicles, plates and KTP must be perfectly synchronized.
Example: Plate B (Jakarta, 31) must generate NIK starting with 31xxxxx
"""

import sys
sys.path.insert(0, '.')

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase
from utils.plate_ktp_sync import PlateKTPSync

def test_synchronized_generation():
    """Test that generated vehicles have synchronized plate-KTP codes"""
    
    print("=" * 70)
    print("TEST: Synchronized Vehicle Generation (Plate-KTP Sync)")
    print("=" * 70)
    print()
    
    owner_db = OwnerDatabase()
    test_cases = [
        ('B', '31', 'DKI Jakarta'),
        ('D', '32', 'Jawa Barat'),
        ('H', '33', 'Jawa Tengah'),
        ('AB', '34', 'DI Yogyakarta'),
        ('L', '35', 'Jawa Timur'),
        ('P', '51', 'Bali'),
    ]
    
    all_passed = True
    
    for plate_code, expected_province, region_name in test_cases:
        print(f"Testing Plate Code: {plate_code}")
        print(f"  Expected Province Code: {expected_province} ({region_name})")
        
        # Get province code from plate using IndonesianPlateManager
        actual_province = IndonesianPlateManager.get_province_code_from_plate_code(plate_code)
        
        if actual_province == expected_province:
            print(f"  ✓ Province mapping correct: {plate_code} → {actual_province}")
        else:
            print(f"  ✗ FAILED - Province mapping incorrect!")
            print(f"    Expected: {expected_province}, Got: {actual_province}")
            all_passed = False
            continue
        
        # Generate a vehicle with this plate code
        # Create a sample plate like "B 1234 UA"
        sample_plate = f"{plate_code} 1234 UA"
        owner = owner_db.get_or_create_owner(sample_plate, 'roda_dua')
        
        # Extract province code from generated NIK (first 2 digits)
        nik_province = owner.owner_id[:2]
        
        print(f"  Generated NIK: {owner.owner_id}")
        print(f"  NIK Province Code: {nik_province}")
        
        # Verify synchronization
        if nik_province == expected_province:
            print(f"  ✓ SYNCHRONIZED: Plate {plate_code} + NIK {nik_province} → MATCH ✓")
            
            # Double-check with PlateKTPSync
            is_sync, msg = PlateKTPSync.validate_plate_ktp_sync(sample_plate, owner.owner_id)
            if is_sync:
                print(f"  ✓ PlateKTPSync validation: {msg}")
            else:
                print(f"  ✗ PlateKTPSync validation FAILED: {msg}")
                all_passed = False
        else:
            print(f"  ✗ NOT SYNCHRONIZED: Plate {plate_code} ({expected_province}) + NIK {nik_province} → MISMATCH ✗")
            all_passed = False
        
        print()
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Synchronized Generation Working!")
        print("  Plates and KTP province codes are perfectly synchronized")
    else:
        print("✗ SOME TESTS FAILED - Check synchronization logic")
    print("=" * 70)
    
    return all_passed


def test_multiple_vehicles():
    """Test generation of multiple vehicles to ensure consistency"""
    
    print()
    print("=" * 70)
    print("TEST: Multiple Vehicle Generation (Consistency Check)")
    print("=" * 70)
    print()
    
    owner_db = OwnerDatabase()
    sync_count = 0
    total_count = 10
    
    plates = ['B 1111 UA', 'D 2222 UD', 'H 3333 UH', 'L 4444 UL', 'P 5555 UP',
              'B 6666 UB', 'D 7777 UD', 'H 8888 UH', 'L 9999 UL', 'AB 1010 UAA']
    
    print(f"Generating {len(plates)} vehicles...\n")
    
    for plate in plates:
        owner = owner_db.get_or_create_owner(plate, 'roda_dua')
        plate_code = plate.split()[0]
        
        # Check if synchronized
        is_sync, msg = PlateKTPSync.validate_plate_ktp_sync(plate, owner.owner_id)
        
        status = "✓ SINKRON" if is_sync else "✗ TIDAK SINKRON"
        print(f"Plate: {plate:15} | NIK: {owner.owner_id} | {status}")
        
        if is_sync:
            sync_count += 1
    
    print()
    print("=" * 70)
    print(f"Results: {sync_count}/{total_count} vehicles are synchronized")
    if sync_count == total_count:
        print("✓ ALL VEHICLES SYNCHRONIZED - Implementation Successful!")
    else:
        print(f"✗ {total_count - sync_count} vehicles NOT synchronized")
    print("=" * 70)
    
    return sync_count == total_count


if __name__ == '__main__':
    test1_passed = test_synchronized_generation()
    test2_passed = test_multiple_vehicles()
    
    print()
    if test1_passed and test2_passed:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("Vehicle generation is properly synchronized!")
        sys.exit(0)
    else:
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        sys.exit(1)
