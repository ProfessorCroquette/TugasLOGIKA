#!/usr/bin/env python3
"""
Test script untuk memvalidasi CORRECT FLOW:
- PLAT NOMOR -> Parse -> Generate OWNER dari PLAT
"""

from utils.indonesian_plates import IndonesianPlateManager, VehicleType

print("=" * 80)
print("TEST: CORRECT FLOW - GENERATE VEHICLE FROM PLATE NUMBER")
print("=" * 80)

# Test data
test_plates = [
    ("B 4123 RK", "roda_dua", "Jakarta Selatan"),
    ("D 5678 ABC", "roda_empat", "Bandung"),
    ("H 123 K", "roda_dua", "Semarang"),
    ("AB 9876 XY", "roda_empat", "Yogyakarta"),
    ("L 456 U", "roda_dua", "Surabaya"),
    ("RI 1 234", "roda_empat", "Pemerintah Indonesia"),
    ("CD 12 345", "roda_empat", "Diplomatik"),
]

for plate_num, vehicle_type, expected_region in test_plates:
    print(f"\n{'-' * 80}")
    print(f"PLAT NOMOR: {plate_num}")
    print(f"VEHICLE TYPE: {vehicle_type}")
    print(f"{'-' * 80}")
    
    # STEP 1: Extract region info dari plat
    print("\n[STEP 1] PARSE PLAT NOMOR - Extract region information")
    region_info = IndonesianPlateManager.extract_region_info_from_plate(plate_num)
    
    if region_info:
        print(f"  OK Region Code: {region_info['region_code']}")
        print(f"  OK Region Name: {region_info['region_name']}")
        print(f"  OK Sub Region: {region_info['sub_region']}")
        print(f"  OK Province Code: {region_info['province_code']}")
        print(f"  OK Vehicle Type: {region_info.get('vehicle_type', 'PRIBADI')}")
        
        # STEP 2: Generate owner dari plat
        print("\n[STEP 2] GENERATE OWNER FROM PLATE")
        owner = IndonesianPlateManager.generate_owner_from_plate(plate_num, vehicle_type)
        
        if owner:
            print(f"  OK Owner ID (NIK): {owner.owner_id}")
            print(f"  OK Name: {owner.name}")
            print(f"  OK Region: {owner.region}")
            print(f"  OK Sub Region: {owner.sub_region}")
            print(f"  OK Address: {owner.address}")
            print(f"  OK Vehicle Type: {owner.vehicle_type}")
            print(f"  OK STNK Status: {'Active' if owner.stnk_status else 'Expired'}")
            print(f"  OK SIM Status: {'Active' if owner.sim_status else 'Expired'}")
            
            # STEP 3: Validate synchronization
            print("\n[STEP 3] VALIDATE PLATE-OWNER SYNCHRONIZATION")
            nik_province = owner.owner_id[:2]
            plat_province = region_info['province_code']
            
            if nik_province == plat_province:
                print(f"  [OK] SYNCHRONIZED: NIK province ({nik_province}) == Plate province ({plat_province})")
            else:
                print(f"  [ERROR] NOT SYNCHRONIZED: NIK province ({nik_province}) != Plate province ({plat_province})")
                
        else:
            print(f"  [ERROR] Could not generate owner")
    else:
        print(f"  [ERROR] Could not parse plate")

print(f"\n{'=' * 80}")
print("TEST COMPLETE")
print(f"{'=' * 80}")

# Additional test: Generate new plate and owner from scratch
print("\n\n" + "=" * 80)
print("ADDITIONAL TEST: Generate new PLATE + OWNER (synchronized)")
print("=" * 80)

for i in range(3):
    print(f"\n{'-' * 80}")
    print(f"GENERATION #{i+1}")
    print(f"{'-' * 80}")
    
    # Generate random plate
    plate, region_name, sub_region, vehicle_type_display = IndonesianPlateManager.generate_plate(
        VehicleType.RODA_DUA if i % 2 == 0 else VehicleType.RODA_EMPAT_LEBIH
    )
    
    print(f"\nGenerated Plate: {plate}")
    print(f"Vehicle Type: {vehicle_type_display}")
    
    # Generate owner dari plate
    vehicle_type = 'roda_dua' if 'Motor' in vehicle_type_display else 'roda_empat'
    owner = IndonesianPlateManager.generate_owner_from_plate(plate, vehicle_type)
    
    if owner:
        print(f"\nOwner Information:")
        print(f"  NIK: {owner.owner_id}")
        print(f"  Name: {owner.name}")
        print(f"  Region: {owner.region}")
        print(f"  Sub-Region: {owner.sub_region}")
        print(f"  Address: {owner.address}")
        
        # Validate
        region_info = IndonesianPlateManager.extract_region_info_from_plate(plate)
        if region_info:
            nik_province = owner.owner_id[:2]
            plat_province = region_info['province_code']
            
            if nik_province == plat_province:
                print(f"\n[OK] SYNCHRONIZED: NIK province == Plate province ({nik_province})")
            else:
                print(f"\n[ERROR] NOT SYNCHRONIZED: NIK province ({nik_province}) != Plate province ({plat_province})")

print("\n" + "=" * 80)
print("ALL TESTS COMPLETED")
print("=" * 80)

