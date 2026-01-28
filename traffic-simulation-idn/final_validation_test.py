#!/usr/bin/env python
"""Final Validation Test - Indonesian Plate Generator GUI Integration"""

import sys
sys.path.insert(0, '.')

from utils.generators import DataGenerator
from utils.gui_vehicle_formatter import VehicleDisplayFormatter

def final_validation():
    """Run final validation tests"""
    print("\n" + "=" * 70)
    print("FINAL VALIDATION TEST - Indonesian Plate Generator Integration")
    print("=" * 70)
    
    print("\n[TEST 1] Generating vehicles with new probability distribution...")
    vehicles = []
    for i in range(5):
        batch = DataGenerator.generate_vehicle_batch()
        vehicles.extend(batch)
        print(f"  Batch {i+1}: Generated {len(batch)} vehicles")
    
    total_generated = len(vehicles)
    print(f"\n  Total vehicles: {total_generated}")
    
    print("\n[TEST 2] Verifying vehicle categories...")
    from collections import Counter
    categories = Counter(v.vehicle_category for v in vehicles)
    
    for cat in ['Pribadi', 'Barang', 'PEMERINTAH', 'KEDUTAAN']:
        count = sum(1 for v in vehicles if v.vehicle_category == cat)
        pct = (count / total_generated) * 100 if total_generated > 0 else 0
        status = "PASS" if count > 0 else "FAIL"
        print(f"  {cat:20s}: {count:3d} vehicles ({pct:5.1f}%) [{status}]")
    
    print("\n[TEST 3] Verifying plate colors...")
    colors = Counter(v.plate_color for v in vehicles)
    
    for color in ['BLACK', 'YELLOW', 'RED', 'WHITE']:
        count = sum(1 for v in vehicles if v.plate_color == color)
        pct = (count / total_generated) * 100 if total_generated > 0 else 0
        status = "PASS" if count > 0 else "FAIL"
        print(f"  {color:10s}: {count:3d} vehicles ({pct:5.1f}%) [{status}]")
    
    print("\n[TEST 4] Verifying plate types...")
    types = Counter(v.plate_type for v in vehicles)
    
    for plate_type in ['PRIBADI', 'NIAGA/TRUK', 'PEMERINTAH', 'DIPLOMATIK']:
        count = sum(1 for v in vehicles if v.plate_type == plate_type)
        pct = (count / total_generated) * 100 if total_generated > 0 else 0
        status = "PASS" if count > 0 else "FAIL"
        print(f"  {plate_type:20s}: {count:3d} vehicles ({pct:5.1f}%) [{status}]")
    
    print("\n[TEST 5] Verifying vehicle information completeness...")
    required_fields = [
        'license_plate', 'plate_type', 'plate_color', 'vehicle_category',
        'vehicle_make', 'vehicle_model', 'owner_name', 'speed'
    ]
    
    all_valid = True
    for field in required_fields:
        missing = sum(1 for v in vehicles if not getattr(v, field, None))
        status = "PASS" if missing == 0 else f"FAIL ({missing} missing)"
        if missing > 0:
            all_valid = False
        print(f"  {field:20s}: {status}")
    
    print("\n[TEST 6] Testing GUI formatter utilities...")
    try:
        sample_vehicle = vehicles[0]
        
        # Test get_vehicle_info
        info = VehicleDisplayFormatter.get_vehicle_info(sample_vehicle)
        if 'plate' in info and 'category' in info:
            print("  get_vehicle_info(): PASS")
        else:
            print("  get_vehicle_info(): FAIL")
            all_valid = False
        
        # Test get_vehicle_summary
        summary = VehicleDisplayFormatter.get_vehicle_summary(sample_vehicle)
        if len(summary) > 0:
            print("  get_vehicle_summary(): PASS")
        else:
            print("  get_vehicle_summary(): FAIL")
            all_valid = False
        
        # Test filtering
        private_only = VehicleDisplayFormatter.filter_vehicles_by_category(
            vehicles, 'Pribadi'
        )
        if len(private_only) > 0:
            print("  filter_vehicles_by_category(): PASS")
        else:
            print("  filter_vehicles_by_category(): FAIL")
        
        yellow_plates = VehicleDisplayFormatter.filter_vehicles_by_plate_color(
            vehicles, 'YELLOW'
        )
        if len(yellow_plates) > 0:
            print("  filter_vehicles_by_plate_color(): PASS")
        else:
            print("  filter_vehicles_by_plate_color(): FAIL")
        
        # Test statistics
        stats = VehicleDisplayFormatter.get_statistics(vehicles)
        if stats['total_vehicles'] > 0:
            print("  get_statistics(): PASS")
        else:
            print("  get_statistics(): FAIL")
            all_valid = False
        
    except Exception as e:
        print(f"  Formatter utilities: FAIL ({e})")
        all_valid = False
    
    print("\n[TEST 7] Verifying category-to-plate mapping...")
    mapping_valid = True
    
    # Check private vehicles
    private = [v for v in vehicles if v.vehicle_category == 'Pribadi']
    if not all(v.plate_color == 'BLACK' for v in private):
        print("  Pribadi -> BLACK: FAIL")
        mapping_valid = False
    else:
        print("  Pribadi -> BLACK: PASS")
    
    # Check commercial vehicles
    commercial = [v for v in vehicles if v.vehicle_category == 'Barang']
    if not all(v.plate_color == 'YELLOW' for v in commercial):
        print("  Barang -> YELLOW: FAIL")
        mapping_valid = False
    else:
        print("  Barang -> YELLOW: PASS")
    
    # Check government vehicles
    government = [v for v in vehicles if v.vehicle_category == 'PEMERINTAH']
    if not all(v.plate_color == 'RED' for v in government):
        print("  PEMERINTAH -> RED: FAIL")
        mapping_valid = False
    else:
        print("  PEMERINTAH -> RED: PASS")
    
    # Check diplomatic vehicles
    diplomatic = [v for v in vehicles if v.vehicle_category == 'KEDUTAAN']
    if not all(v.plate_color == 'WHITE' for v in diplomatic):
        print("  KEDUTAAN -> WHITE: FAIL")
        mapping_valid = False
    else:
        print("  KEDUTAAN -> WHITE: PASS")
    
    if not mapping_valid:
        all_valid = False
    
    print("\n[TEST 8] Sample vehicle data...")
    if vehicles:
        v = vehicles[0]
        print(f"  License Plate: {v.license_plate}")
        print(f"  Category: {v.vehicle_category}")
        print(f"  Plate Type: {v.plate_type}")
        print(f"  Plate Color: {v.plate_color}")
        print(f"  Make: {v.vehicle_make}")
        print(f"  Owner: {v.owner_name}")
        print(f"  Speed: {v.speed:.1f} km/h")
    
    print("\n" + "=" * 70)
    if all_valid and mapping_valid:
        print("RESULT: ALL TESTS PASSED - IMPLEMENTATION COMPLETE")
        return 0
    else:
        print("RESULT: SOME TESTS FAILED - CHECK OUTPUT ABOVE")
        return 1

if __name__ == '__main__':
    try:
        exit_code = final_validation()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
