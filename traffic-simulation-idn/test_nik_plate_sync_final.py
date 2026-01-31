"""
Final test to verify NIK-Plate synchronization with CSV administrative codes
"""

import sys, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

def test_nik_plate_sync():
    """Test NIK-Plate synchronization"""
    
    test_cases = [
        ('B 1234 AA', '31'),  # DKI Jakarta
        ('D 5678 BC', '32'),  # Jawa Barat - Bandung
        ('F 2345 DE', '32'),  # Jawa Barat - Bogor
        ('H 3456 HI', '33'),  # Jawa Tengah
        ('T 9876 FG', '36'),  # Jawa Timur
        ('AG 7890 JK', '35'),  # Jawa Timur - Kediri
        ('A 1111 LM', '35'),  # Banten
    ]
    
    db = OwnerDatabase()
    
    print("=" * 90)
    print("NIK-PLATE SYNCHRONIZATION TEST WITH CSV ADMINISTRATIVE CODES")
    print("=" * 90)
    
    passed = 0
    failed = 0
    
    for plate, expected_province in test_cases:
        owner = db.get_or_create_owner(plate)
        nik = owner.owner_id
        
        # Extract components
        nik_province = nik[:2]
        nik_city = nik[2:4]
        nik_district = nik[4:6]
        nik_day = nik[6:8]
        nik_month = nik[8:10]
        nik_year = nik[10:12]
        nik_seq = nik[12:16]
        
        # Check synchronization
        prov_match = nik_province == expected_province
        
        status = "OK" if prov_match else "FAIL"
        print(f"\n{status} | Plate={plate}")
        print(f"    NIK: {nik}")
        print(f"    Province: Expected={expected_province}, Got={nik_province}, Match={prov_match}")
        print(f"    City Code: {nik_city}")
        print(f"    District Code: {nik_district}")
        print(f"    Birth: {nik_day}/{nik_month}/{nik_year}")
        print(f"    Sequential: {nik_seq}")
        
        if prov_match:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 90)
    print(f"RESULTS: {passed} Passed, {failed} Failed")
    print("=" * 90)
    
    if failed == 0:
        print("SUCCESS: All NIKs are synchronized with plate regions!")
    else:
        print(f"FAILURE: {failed} NIKs are not synchronized")
    
    return failed == 0


if __name__ == '__main__':
    success = test_nik_plate_sync()
    sys.exit(0 if success else 1)
