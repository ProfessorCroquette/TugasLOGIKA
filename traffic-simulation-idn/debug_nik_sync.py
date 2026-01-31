"""
Debug script to check NIK-Plate synchronization issues
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

def test_plate_to_nik_sync():
    """Test if NIK regions match plate regions"""
    
    test_plates = [
        'B 1234 AA',    # Jakarta Selatan
        'D 5678 BC',    # Bandung
        'F 2345 DE',    # Bogor
        'T 9876 FG',    # Surabaya
        'H 3456 HI',    # Semarang
        'AG 7890 JK',   # Yogyakarta
        'A 1111 LM',    # Banten
        'RI 1234 NOP',  # Government
        'CD 5678 QRS',  # Diplomatic
    ]
    
    db = OwnerDatabase()
    
    print("=" * 80)
    print("PLATE TO NIK SYNCHRONIZATION TEST")
    print("=" * 80)
    
    for plate in test_plates:
        print(f"\n{'='*80}")
        print(f"PLATE: {plate}")
        
        # Parse plate
        parsed = IndonesianPlateManager.parse_plate(plate)
        if parsed:
            print(f"  Region Name: {parsed['region_name']}")
            print(f"  Sub Region: {parsed.get('sub_region', 'N/A')}")
            print(f"  Region Code: {parsed['region_code']}")
        
        # Get province code from plate
        province_code = IndonesianPlateManager.get_province_code_from_plate_code(parsed['region_code'] if parsed else 'B')
        print(f"  Province Code from Plate: {province_code}")
        
        # Generate owner (which generates NIK)
        owner = db.get_or_create_owner(plate, 'roda_empat')
        nik = owner.owner_id
        
        print(f"\n  Generated Owner:")
        print(f"    NIK: {nik}")
        print(f"    NIK Province Code: {nik[:2]}")
        print(f"    NIK City Code: {nik[2:4]}")
        print(f"    NIK District Code: {nik[4:6]}")
        print(f"    NIK Birth Day: {nik[6:8]}")
        print(f"    NIK Birth Month: {nik[8:10]}")
        print(f"    NIK Birth Year: {nik[10:12]}")
        print(f"    NIK Sequential: {nik[12:16]}")
        
        # Check synchronization
        print(f"\n  Synchronization Check:")
        print(f"    Plate Province: {province_code}")
        print(f"    NIK Province: {nik[:2]}")
        print(f"    Match: {' YES' if province_code == nik[:2] else ' NO'}")
        
        # Try to find CSV codes
        if parsed:
            csv_codes = IndonesianPlateManager._get_csv_codes_for_region(parsed.get('sub_region', ''))
            if csv_codes:
                print(f"\n  CSV Administrative Codes Found:")
                print(f"    Full Code: {csv_codes['full']}")
                print(f"    City: {csv_codes['city']}")
                print(f"    District: {csv_codes['district']}")
                print(f"    NIK City Match: {' YES' if csv_codes['city'] == nik[2:4] else ' NO'}")
            else:
                print(f"\n  CSV Administrative Codes: NOT FOUND for '{parsed.get('sub_region', '')}'")
                print(f"    Using random city/district codes (NOT SYNCHRONIZED)")
    
    print("\n" + "=" * 80)


def debug_csv_matching():
    """Debug CSV matching to find why some regions aren't matching"""
    
    print("\n" + "=" * 80)
    print("CSV REGION MATCHING DEBUG")
    print("=" * 80)
    
    test_regions = [
        'Jakarta Selatan',
        'JAKARTA SELATAN',
        'Bandung',
        'BANDUNG',
        'Jakarta',
        'JAKARTA',
    ]
    
    for region in test_regions:
        print(f"\nSearching CSV for: '{region}'")
        csv_codes = IndonesianPlateManager._get_csv_codes_for_region(region)
        if csv_codes:
            print(f"  FOUND: {csv_codes}")
        else:
            print(f"  NOT FOUND")


if __name__ == '__main__':
    debug_csv_matching()
    test_plate_to_nik_sync()
