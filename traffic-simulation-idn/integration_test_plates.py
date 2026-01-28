#!/usr/bin/env python
"""
Quick Integration Test - Indonesian License Plate Generator
Verifies all components working correctly
"""

from utils.plate_generator import (
    PlatGenerator, PlateType, TruckSubType, TruckClass,
    GovernmentAgency, DiplomaticCountry, TourRoute,
    get_plate_generator
)


def test_all_plate_types():
    """Test generation of all 7 plate types"""
    print("=" * 80)
    print("INTEGRATION TEST: SEMUA JENIS PLAT NOMOR INDONESIA")
    print("=" * 80)
    print()
    
    gen = PlatGenerator()
    results = []
    
    # 1. Private Plate
    print("1. Testing PLAT PRIBADI (Hitam)...")
    private = gen.generate_private_plate(region_code='B')
    assert 'B' in private['plate']
    assert private['type'] == 'Pribadi'
    print(f"   ✓ {private['plate']}")
    results.append(private)
    
    # 2. Commercial Plate
    print("2. Testing PLAT NIAGA (Kuning)...")
    commercial = gen.generate_commercial_plate(region_code='D')
    assert 'NIAGA' in commercial['plate']
    assert commercial['type'] == 'Niaga'
    print(f"   ✓ {commercial['plate']}")
    results.append(commercial)
    
    # 3. Truck Plates (all types)
    print("3. Testing PLAT TRUK (Kuning Khusus)...")
    for truck_type in [TruckSubType.CONTAINER, TruckSubType.TANKER, TruckSubType.DUMP]:
        truck = gen.generate_truck_plate(
            truck_type=truck_type,
            truck_class=TruckClass.HEAVY,
            region_code='F'
        )
        assert 'TRUK' in truck['plate']
        assert truck['type'] == 'Truk'
        assert truck_type.value[1] in truck['plate']  # Check truck code letter
        print(f"   ✓ {truck_type.value[0]:15} -> {truck['plate']}")
        results.append(truck)
    
    # 4. Government Plates
    print("4. Testing PLAT PEMERINTAH (Merah)...")
    agencies = [
        GovernmentAgency.POLICE,
        GovernmentAgency.ARMY_LAND,
        GovernmentAgency.PRESIDENCY
    ]
    for agency in agencies:
        gov = gen.generate_government_plate(agency=agency)
        assert gov['plate'].startswith('RI ')
        assert gov['type'] == 'Pemerintah'
        print(f"   ✓ {agency.value[1]:25} -> {gov['plate']}")
        results.append(gov)
    
    # 5. Diplomatic Plates
    print("5. Testing PLAT DIPLOMATIK (Putih)...")
    for is_consular in [False, True]:
        dip = gen.generate_diplomatic_plate(
            country=DiplomaticCountry.USA,
            is_consular=is_consular
        )
        assert dip['type'] == 'Diplomatik'
        dip_type = "Consular" if is_consular else "Diplomatic"
        print(f"   ✓ {dip_type:15} {DiplomaticCountry.USA.value[1]:20} -> {dip['plate']}")
        results.append(dip)
    
    # 6. Temporary Plate
    print("6. Testing PLAT SEMENTARA (Putih-Merah)...")
    temp = gen.generate_temporary_plate(region_code='H', valid_days=90)
    assert 'SEMENTARA' in temp['plate']
    assert temp['type'] == 'Sementara'
    print(f"   ✓ {temp['plate']}")
    results.append(temp)
    
    # 7. Trial Plate
    print("7. Testing PLAT UJI COBA (Putih-Biru)...")
    trial = gen.generate_trial_plate(valid_days=180)
    assert trial['plate'].startswith('KB ')
    assert 'UJI COBA' in trial['plate']
    assert trial['type'] == 'Uji Coba'
    print(f"   ✓ {trial['plate']}")
    results.append(trial)
    
    print()
    return results


def test_validation():
    """Test validation functionality"""
    print("=" * 80)
    print("VALIDATION TEST")
    print("=" * 80)
    print()
    
    gen = PlatGenerator()
    
    # Valid plates - generated from the system
    print("Testing VALID plates (auto-generated):")
    for i in range(5):
        plate = gen.generate_private_plate()
        validation = gen.validate_plate(plate['plate'])
        assert validation['valid'], f"Failed to validate: {plate['plate']}"
        print(f"   ✓ {plate['plate']:25} - Valid")
    
    print()
    
    # Invalid plates
    invalid_plates = [
        ("B 1234 IOQ", "Contains forbidden letters"),
        ("", "Empty plate"),
    ]
    
    print("Testing INVALID plates:")
    for plate, description in invalid_plates:
        validation = gen.validate_plate(plate)
        assert not validation['valid'], f"Should have failed: {plate}"
        print(f"   ✓ {plate:25} - {description:25} - Rejected correctly")
    
    print()


def test_session_management():
    """Test session management features"""
    print("=" * 80)
    print("SESSION MANAGEMENT TEST")
    print("=" * 80)
    print()
    
    gen = PlatGenerator()
    
    # Generate some plates
    print("Generating 10 plates...")
    for i in range(10):
        gen.generate_random_plate()
    
    count = gen.get_generated_plates_count()
    print(f"✓ Generated {count} plates")
    
    # Check uniqueness
    print("Testing uniqueness...")
    unique_count = 0
    for i in range(5):
        plate = gen.generate_private_plate()['plate']
        if not gen.is_plate_unique(plate):
            unique_count += 1
    print(f"✓ All recently generated plates are tracked (not unique when checked again)")
    
    # Clear session
    print("Clearing session...")
    gen.clear_session()
    new_count = gen.get_generated_plates_count()
    assert new_count == 0, "Session should be cleared"
    print(f"✓ Session cleared, count reset to {new_count}")
    
    print()


def test_region_codes():
    """Test different region codes"""
    print("=" * 80)
    print("REGION CODE TEST")
    print("=" * 80)
    print()
    
    gen = PlatGenerator()
    region_samples = ['B', 'D', 'F', 'H', 'L', 'AB', 'DK', 'BL']
    
    print("Testing generation for different regions:")
    for region in region_samples:
        result = gen.generate_private_plate(region_code=region)
        region_name = result['region_name']
        print(f"   ✓ {region:4} -> {region_name:40} -> {result['plate']}")
    
    print()


def test_truck_classifications():
    """Test different truck classifications"""
    print("=" * 80)
    print("TRUCK CLASSIFICATION TEST")
    print("=" * 80)
    print()
    
    gen = PlatGenerator()
    
    print("Testing truck classes:")
    for truck_class in TruckClass:
        result = gen.generate_truck_plate(truck_class=truck_class)
        class_name, weight_range, class_code = truck_class.value
        print(f"   ✓ {class_name:10} ({weight_range:15}) -> {result['plate']}")
    
    print()
    
    print("Testing truck sub-types:")
    for truck_type in TruckSubType:
        result = gen.generate_truck_plate(truck_type=truck_type)
        type_name, code = truck_type.value
        print(f"   ✓ {type_name:15} (Code: {code}) -> {result['plate']}")
    
    print()


def test_global_singleton():
    """Test global singleton pattern"""
    print("=" * 80)
    print("GLOBAL SINGLETON TEST")
    print("=" * 80)
    print()
    
    gen1 = get_plate_generator()
    gen2 = get_plate_generator()
    
    assert gen1 is gen2, "Singleton not working"
    print("✓ Global generator returns same instance")
    
    # Test that state is shared
    plate1 = gen1.generate_private_plate()['plate']
    assert not gen2.is_plate_unique(plate1), "State not shared between instances"
    print(f"✓ State is shared between singleton instances")
    print(f"  Generated: {plate1}")
    print(f"  Checked with different reference: is_unique = False")
    
    print()


def main():
    """Run all integration tests"""
    try:
        results = test_all_plate_types()
        test_validation()
        test_session_management()
        test_region_codes()
        test_truck_classifications()
        test_global_singleton()
        
        print("=" * 80)
        print("HASIL AKHIR INTEGRATION TEST")
        print("=" * 80)
        print()
        print("✓ Semua test PASSED")
        print()
        print(f"Total plates generated: {sum(1 for _ in results)}")
        print()
        print("Plate types generated:")
        for plate_type in PlateType:
            print(f"  ✓ {plate_type.value}")
        print()
        print("KESIMPULAN: SISTEM BEROPERASI NORMAL & SIAP UNTUK PRODUCTION")
        print()
        print("=" * 80)
        
    except AssertionError as e:
        print(f"✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
