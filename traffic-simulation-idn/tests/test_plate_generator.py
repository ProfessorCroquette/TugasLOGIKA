"""
Comprehensive test suite for Indonesian License Plate Generator System
Tests all plate types, validations, and specifications
"""

import pytest
from utils.plate_generator import (
    PlatGenerator, PlateType, TruckSubType, TruckClass,
    GovernmentAgency, DiplomaticCountry, TourRoute,
    PlateCharacterValidator, get_plate_generator
)


class TestPlateCharacterValidator:
    """Test character validation rules"""
    
    def test_valid_letters(self):
        """Test that valid letters are accepted"""
        validator = PlateCharacterValidator()
        valid_letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
        
        for letter in valid_letters:
            assert validator.is_valid_letter(letter), f"Letter {letter} should be valid"
    
    def test_forbidden_letters(self):
        """Test that I, O, Q are forbidden"""
        validator = PlateCharacterValidator()
        forbidden = "IOQ"
        
        for letter in forbidden:
            assert not validator.is_valid_letter(letter), f"Letter {letter} should be forbidden"
    
    def test_region_codes_exist(self):
        """Test that region codes database exists"""
        validator = PlateCharacterValidator()
        codes = validator.get_all_region_codes()
        
        # Check important codes
        assert 'B' in codes, "Jakarta code (B) should exist"
        assert 'D' in codes, "Bandung code (D) should exist"
        assert 'L' in codes, "Surabaya code (L) should exist"
    
    def test_region_validation(self):
        """Test region code validation"""
        validator = PlateCharacterValidator()
        
        assert validator.is_valid_region('B'), "B should be valid"
        assert validator.is_valid_region('D'), "D should be valid"
        assert not validator.is_valid_region('ZZ'), "ZZ should be invalid"


class TestPrivatePlateGenerator:
    """Test private vehicle plate generation"""
    
    def test_generate_private_plate_format(self):
        """Test private plate format is correct"""
        gen = PlatGenerator()
        
        for _ in range(10):
            result = gen.generate_private_plate()
            
            assert result['type'] == PlateType.PRIVATE.value
            assert result['color'] == 'Hitam (Tulisan Putih/Silver)'
            assert ' ' in result['plate'], "Plate should have spaces"
            
            parts = result['plate'].split()
            assert len(parts) == 3, f"Plate should have 3 parts, got {len(parts)}"
            
            # Check structure: region number letters
            region_code, number, letters = parts
            assert region_code in PlateCharacterValidator.REGION_CODES
            assert number.isdigit() and 1 <= int(number) <= 9999
            assert all(c in PlateCharacterValidator.VALID_LETTERS for c in letters)
    
    def test_generate_private_plate_specific_region(self):
        """Test generating private plate for specific region"""
        gen = PlatGenerator()
        
        result = gen.generate_private_plate(region_code='B')
        assert result['region_code'] == 'B'
        assert 'Jakarta' in result['region_name']
        assert result['plate'].startswith('B ')
    
    def test_private_plate_uniqueness(self):
        """Test that each generated plate is unique"""
        gen = PlatGenerator()
        plates = set()
        
        for _ in range(100):
            result = gen.generate_private_plate()
            plate = result['plate']
            assert plate not in plates, f"Duplicate plate generated: {plate}"
            plates.add(plate)


class TestCommercialPlateGenerator:
    """Test commercial vehicle plate generation"""
    
    def test_generate_commercial_plate_format(self):
        """Test commercial plate includes NIAGA marker"""
        gen = PlatGenerator()
        
        for _ in range(10):
            result = gen.generate_commercial_plate()
            
            assert result['type'] == PlateType.COMMERCIAL.value
            assert '(NIAGA)' in result['plate']
            assert result['color'] == 'Kuning (Tulisan Hitam)'
    
    def test_commercial_plate_has_required_fields(self):
        """Test commercial plate has all required fields"""
        gen = PlatGenerator()
        result = gen.generate_commercial_plate()
        
        required_fields = ['plate', 'type', 'color', 'region_code', 'region_name', 
                          'number', 'letters', 'category', 'description']
        for field in required_fields:
            assert field in result, f"Missing field: {field}"


class TestTruckPlateGenerator:
    """Test truck vehicle plate generation"""
    
    def test_generate_truck_plate_general(self):
        """Test general truck plate format"""
        gen = PlatGenerator()
        
        result = gen.generate_truck_plate(
            truck_type=TruckSubType.GENERAL,
            truck_class=TruckClass.MEDIUM
        )
        
        assert result['type'] == PlateType.TRUCK.value
        assert 'TRUK-' in result['plate']
        assert 'RUTE:' in result['plate']
    
    def test_generate_truck_plate_container(self):
        """Test container truck plate has K code"""
        gen = PlatGenerator()
        
        result = gen.generate_truck_plate(
            truck_type=TruckSubType.CONTAINER,
            truck_class=TruckClass.HEAVY
        )
        
        assert 'K' in result['plate']
        assert result['truck_subtype'] == 'Kontainer'
    
    def test_generate_truck_plate_tanker(self):
        """Test tanker truck plate has G code"""
        gen = PlatGenerator()
        
        result = gen.generate_truck_plate(
            truck_type=TruckSubType.TANKER,
            truck_class=TruckClass.LIGHT
        )
        
        assert 'G' in result['plate']
        assert result['truck_subtype'] == 'Tangki'
    
    def test_generate_truck_plate_dump(self):
        """Test dump truck plate has D code"""
        gen = PlatGenerator()
        
        result = gen.generate_truck_plate(
            truck_type=TruckSubType.DUMP,
            truck_class=TruckClass.HEAVY
        )
        
        assert 'D' in result['plate']
        assert result['truck_subtype'] == 'Dump'
    
    def test_truck_plate_weight_class(self):
        """Test truck plate includes weight classification"""
        gen = PlatGenerator()
        
        # Light truck
        result_light = gen.generate_truck_plate(truck_class=TruckClass.LIGHT)
        assert 'TRUK-8T' in result_light['plate']
        
        # Medium truck
        result_medium = gen.generate_truck_plate(truck_class=TruckClass.MEDIUM)
        assert 'TRUK-16T' in result_medium['plate']
        
        # Heavy truck
        result_heavy = gen.generate_truck_plate(truck_class=TruckClass.HEAVY)
        assert 'TRUK-24T' in result_heavy['plate']
    
    def test_truck_plate_route_info(self):
        """Test truck plate includes route information"""
        gen = PlatGenerator()
        
        for route in list(TourRoute):
            result = gen.generate_truck_plate(
                truck_class=TruckClass.HEAVY,
                route=route
            )
            route_code = route.value[0]
            assert route_code in result['plate'] or route_code in result['route_code']


class TestGovernmentPlateGenerator:
    """Test government vehicle plate generation"""
    
    def test_generate_government_plate_format(self):
        """Test government plate format"""
        gen = PlatGenerator()
        
        result = gen.generate_government_plate()
        
        assert result['type'] == PlateType.GOVERNMENT.value
        assert result['color'] == 'Merah (Tulisan Putih)'
        assert result['plate'].startswith('RI ')
    
    def test_government_plate_police(self):
        """Test police vehicle plate"""
        gen = PlatGenerator()
        
        result = gen.generate_government_plate(GovernmentAgency.POLICE)
        
        assert result['agency_code'] == 1
        assert 'Kepolisian' in result['agency_name'] or 'Polri' in result['agency_short']
    
    def test_government_plate_military(self):
        """Test military vehicle plate"""
        gen = PlatGenerator()
        
        # Army Land
        result = gen.generate_government_plate(GovernmentAgency.ARMY_LAND)
        assert result['agency_code'] == 2
        assert 'TNI' in result['agency_name']
        
        # Army Navy
        result = gen.generate_government_plate(GovernmentAgency.ARMY_NAVY)
        assert result['agency_code'] == 3
        
        # Army Air
        result = gen.generate_government_plate(GovernmentAgency.ARMY_AIR)
        assert result['agency_code'] == 4
    
    def test_government_plate_presidency(self):
        """Test presidency vehicle plate"""
        gen = PlatGenerator()
        
        result = gen.generate_government_plate(GovernmentAgency.PRESIDENCY)
        
        assert result['agency_code'] == 5
        assert 'Kepresidenan' in result['agency_name']


class TestDiplomaticPlateGenerator:
    """Test diplomatic vehicle plate generation"""
    
    def test_generate_diplomatic_plate_format(self):
        """Test diplomatic plate format"""
        gen = PlatGenerator()
        
        result = gen.generate_diplomatic_plate()
        
        assert result['type'] == PlateType.DIPLOMATIC.value
        assert result['color'] == 'Putih (Tulisan Hitam)'
        assert result['plate'].startswith('CD ')
    
    def test_diplomatic_plate_corps(self):
        """Test Corps Diplomatic plate"""
        gen = PlatGenerator()
        
        result = gen.generate_diplomatic_plate(is_consular=False)
        
        assert result['plate'].startswith('CD ')
        assert result['diplomatic_type'] == 'Corps Diplomatic'
    
    def test_diplomatic_plate_consular(self):
        """Test Consular Corps plate"""
        gen = PlatGenerator()
        
        result = gen.generate_diplomatic_plate(is_consular=True)
        
        assert result['plate'].startswith('CC ')
        assert result['diplomatic_type'] == 'Consular Corps'
    
    def test_diplomatic_plate_countries(self):
        """Test diplomatic plates for different countries"""
        gen = PlatGenerator()
        
        # USA
        result_usa = gen.generate_diplomatic_plate(DiplomaticCountry.USA)
        assert 'AMERIKA' in result_usa['country_name']
        assert '71' in result_usa['plate']
        
        # Japan
        result_japan = gen.generate_diplomatic_plate(DiplomaticCountry.JAPAN)
        assert 'JEPANG' in result_japan['country_name']
        assert '74' in result_japan['plate']


class TestTemporaryPlateGenerator:
    """Test temporary vehicle plate generation"""
    
    def test_generate_temporary_plate_format(self):
        """Test temporary plate format"""
        gen = PlatGenerator()
        
        result = gen.generate_temporary_plate()
        
        assert result['type'] == PlateType.TEMPORARY.value
        assert result['color'] == 'Putih-Merah (Tulisan Hitam)'
        assert '(SEMENTARA)' in result['plate']
        assert 'EXP:' in result['plate']
    
    def test_temporary_plate_expiry(self):
        """Test temporary plate has expiry date"""
        gen = PlatGenerator()
        
        result = gen.generate_temporary_plate(valid_days=90)
        
        assert result['valid_days'] == 90
        assert 'EXP:' in result['plate']
        assert result['expiry_date'] is not None


class TestTrialPlateGenerator:
    """Test trial/dealer vehicle plate generation"""
    
    def test_generate_trial_plate_format(self):
        """Test trial plate format"""
        gen = PlatGenerator()
        
        result = gen.generate_trial_plate()
        
        assert result['type'] == PlateType.TRIAL.value
        assert result['color'] == 'Putih-Biru (Tulisan Hitam)'
        assert result['plate'].startswith('KB ')
        assert '(UJI COBA)' in result['plate']
        assert 'EXP:' in result['plate']
    
    def test_trial_plate_expiry(self):
        """Test trial plate expiry"""
        gen = PlatGenerator()
        
        result = gen.generate_trial_plate(valid_days=180)
        
        assert result['valid_days'] == 180
        assert result['expiry_date'] is not None


class TestRandomPlateGeneration:
    """Test random plate generation"""
    
    def test_generate_random_plate(self):
        """Test generating random plates"""
        gen = PlatGenerator()
        
        for _ in range(50):
            result = gen.generate_random_plate()
            assert 'plate' in result
            assert 'type' in result
            assert 'color' in result
    
    def test_generate_random_plate_with_type(self):
        """Test generating random plates of specific type"""
        gen = PlatGenerator()
        
        for plate_type in PlateType:
            result = gen.generate_random_plate(plate_type=plate_type)
            assert result['type'] == plate_type.value


class TestPlateValidation:
    """Test plate validation"""
    
    def test_validate_valid_plates(self):
        """Test validation of valid plates"""
        gen = PlatGenerator()
        
        # Generate valid plates and validate them
        private = gen.generate_private_plate()
        validation = gen.validate_plate(private['plate'])
        assert validation['valid'], f"Valid plate failed validation: {private['plate']}"
    
    def test_validate_forbidden_letters(self):
        """Test that plates with I, O, Q fail validation"""
        gen = PlatGenerator()
        
        invalid_plates = [
            "B 1234 IOQ",
            "D 5678 AIO",
        ]
        
        for plate in invalid_plates:
            validation = gen.validate_plate(plate)
            assert not validation['valid'], f"Plate with forbidden letters should fail: {plate}"
    
    def test_validate_empty_plate(self):
        """Test validation of empty plate"""
        gen = PlatGenerator()
        
        validation = gen.validate_plate("")
        assert not validation['valid']
    
    def test_identify_plate_type(self):
        """Test that validation identifies plate type correctly"""
        gen = PlatGenerator()
        
        # Government plate
        validation = gen.validate_plate("RI 1 1234")
        assert validation['plate_type'] == 'Government'
        
        # Diplomatic plate
        validation = gen.validate_plate("CD 71 123")
        assert validation['plate_type'] == 'Diplomatic'
        
        # Trial plate
        validation = gen.validate_plate("KB 1234 AB")
        assert validation['plate_type'] == 'Trial'


class TestSessionTracking:
    """Test session tracking of generated plates"""
    
    def test_plate_uniqueness_tracking(self):
        """Test that generator tracks unique plates"""
        gen = PlatGenerator()
        
        for _ in range(20):
            result = gen.generate_private_plate()
            plate = result['plate']
            
            # Should be in generated set
            assert not gen.is_plate_unique(plate), "Recently generated plate should not be unique"
    
    def test_generated_count(self):
        """Test counting generated plates"""
        gen = PlatGenerator()
        initial_count = gen.get_generated_plates_count()
        
        gen.generate_private_plate()
        assert gen.get_generated_plates_count() == initial_count + 1
        
        gen.generate_commercial_plate()
        assert gen.get_generated_plates_count() == initial_count + 2
    
    def test_clear_session(self):
        """Test clearing session data"""
        gen = PlatGenerator()
        
        gen.generate_private_plate()
        assert gen.get_generated_plates_count() > 0
        
        gen.clear_session()
        assert gen.get_generated_plates_count() == 0


class TestGlobalGenerator:
    """Test global generator instance"""
    
    def test_global_generator_instance(self):
        """Test that global generator returns same instance"""
        gen1 = get_plate_generator()
        gen2 = get_plate_generator()
        
        assert gen1 is gen2, "Global generator should return same instance"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
