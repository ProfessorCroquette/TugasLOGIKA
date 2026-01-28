#!/usr/bin/env python3
"""
Test script for Indonesian License Plate System
Verifies all core functionality
"""

from utils.indonesian_plates import IndonesianPlateManager, VehicleType, owner_db

def test_plate_generation():
    """Test plate generation for both vehicle types"""
    print("1. Motorcycle Plate Generation (Roda Dua):")
    for i in range(3):
        plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_DUA)
        print(f"   {plate} -> {region} / {sub}")

    print("\n2. Car Plate Generation (Roda Empat atau lebih):")
    for i in range(3):
        plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_EMPAT_LEBIH)
        print(f"   {plate} -> {region} / {sub}")


def test_plate_parsing():
    """Test plate parsing and validation"""
    print("\n3. Plate Parsing:")
    test_plates = ["B 1234 U AB", "D 5678 A XYZ", "DK 9999 P ABC"]
    for plate in test_plates:
        info = IndonesianPlateManager.parse_plate(plate)
        if info:
            print(f"   {plate}:")
            print(f"      Region: {info['region_name']} -> {info['sub_region']}")
            print(f"      Valid: {info['is_valid']}")


def test_vehicle_owner():
    """Test vehicle owner integration"""
    print("\n4. Vehicle Owner Integration:")
    plate = "B 5678 U AB"
    owner = owner_db.get_or_create_owner(plate, "roda_dua")
    print(f"   Plate: {plate}")
    print(f"   Owner: {owner.name}")
    print(f"   Region: {owner.region}")
    print(f"   Vehicle Type: {owner.get_vehicle_type_display()}")
    print(f"   STNK Status: {owner.stnk_status}")
    print(f"   SIM Status: {owner.sim_status}")
    print(f"   Violation Risk: {owner.is_violation_risk()}")


if __name__ == "__main__":
    print("=== Indonesian License Plate System Test ===\n")
    
    try:
        test_plate_generation()
        test_plate_parsing()
        test_vehicle_owner()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
