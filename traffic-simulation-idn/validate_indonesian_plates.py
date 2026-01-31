#!/usr/bin/env python3
"""
Validate Indonesian license plates against official format
Ensures all plates follow: [A-Z]{1,2} \d{1,4} [A-Z]{0,3}
"""

import re
import json
from pathlib import Path
from typing import Dict, Tuple, List

class IndonesianPlateValidator:
    """Validates Indonesian license plates against official format"""
    
    # Official plate format regex
    # Segment 1: 1-2 letters (region code)
    # Segment 2: 1-4 digits (vehicle number)
    # Segment 3: 0-3 letters (sub-region code)
    PLATE_PATTERN = r'^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{0,3}$'
    
    def __init__(self):
        """Initialize validator with indonesian_regions.json data"""
        self.regions_file = Path("data/regions/indonesian_regions.json")
        self.valid_region_codes = set()
        self.valid_sub_codes = {}
        self._load_region_data()
    
    def _load_region_data(self):
        """Load valid region and sub-region codes from JSON"""
        try:
            if self.regions_file.exists():
                with open(self.regions_file, 'r') as f:
                    data = json.load(f)
                
                for region_code, region_data in data.items():
                    self.valid_region_codes.add(region_code)
                    
                    # Extract sub-codes
                    if isinstance(region_data, list) and len(region_data) > 1:
                        sub_codes = region_data[1]
                        if isinstance(sub_codes, dict):
                            self.valid_sub_codes[region_code] = set(sub_codes.keys())
        except Exception as e:
            print(f"Warning: Could not load region data: {e}")
    
    def validate_format(self, plate: str) -> Tuple[bool, str]:
        """
        Validate plate format against official regex
        
        Args:
            plate: Plate string to validate
            
        Returns:
            (is_valid, error_message)
        """
        if not plate:
            return False, "Plate cannot be empty"
        
        # Remove extra whitespace
        plate = plate.strip()
        
        # Check regex match
        if not re.match(self.PLATE_PATTERN, plate):
            return False, f"Invalid format. Expected: [A-Z]{{1,2}} \\d{{1,4}} [A-Z]{{0,3}}"
        
        return True, "Format is valid"
    
    def validate_segments(self, plate: str) -> Tuple[bool, Dict]:
        """
        Validate each segment of the plate
        
        Returns:
            (is_valid, details_dict)
        """
        is_valid, error = self.validate_format(plate)
        if not is_valid:
            return False, {
                'valid': False,
                'error': error,
                'segments': {}
            }
        
        parts = plate.split()
        region_code = parts[0]
        number = parts[1]
        sub_code = parts[2] if len(parts) > 2 else ""
        
        details = {
            'valid': True,
            'segments': {
                'region_code': {
                    'value': region_code,
                    'length': len(region_code),
                    'valid': len(region_code) in (1, 2) and region_code.isupper()
                },
                'vehicle_number': {
                    'value': number,
                    'numeric_value': int(number),
                    'valid': 1 <= int(number) <= 9999 and number.isdigit()
                },
                'sub_region_code': {
                    'value': sub_code,
                    'length': len(sub_code),
                    'valid': 0 <= len(sub_code) <= 3 and (not sub_code or sub_code.isupper())
                }
            },
            'errors': []
        }
        
        # Check region code validity
        if region_code not in self.valid_region_codes:
            details['errors'].append(f"Region code '{region_code}' not found in registry")
        
        # Check sub-code validity
        if sub_code and region_code in self.valid_sub_codes:
            first_letter = sub_code[0]
            if first_letter not in self.valid_sub_codes[region_code]:
                details['errors'].append(
                    f"Sub-region code '{first_letter}' not valid for region '{region_code}'"
                )
        
        details['valid'] = len(details['errors']) == 0
        return details['valid'], details
    
    def validate_complete(self, plate: str) -> Tuple[bool, Dict]:
        """
        Complete validation with all checks
        
        Returns:
            (is_valid, complete_details)
        """
        is_valid, details = self.validate_segments(plate)
        
        if is_valid:
            parts = plate.split()
            region_code = parts[0]
            
            # Add human-readable info
            if region_code in self.valid_region_codes:
                # Find region name from JSON
                try:
                    with open(self.regions_file, 'r') as f:
                        data = json.load(f)
                        if region_code in data:
                            region_data = data[region_code]
                            details['region_name'] = region_data[0] if isinstance(region_data, list) else "Unknown"
                except:
                    details['region_name'] = "Unknown"
        
        return is_valid, details
    
    def get_region_info(self, region_code: str) -> Dict:
        """Get information about a region code"""
        if not region_code.upper() in self.valid_region_codes:
            return {'error': f"Region code '{region_code}' not found"}
        
        try:
            with open(self.regions_file, 'r') as f:
                data = json.load(f)
                region_data = data[region_code.upper()]
                
                return {
                    'region_code': region_code.upper(),
                    'region_name': region_data[0] if isinstance(region_data, list) else "Unknown",
                    'sub_regions': region_data[1] if isinstance(region_data, list) and len(region_data) > 1 else {}
                }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_example_plate(self, region_code: str) -> str:
        """Generate example plate for a region"""
        import random
        
        region_code = region_code.upper()
        if region_code not in self.valid_region_codes:
            return f"Invalid region code: {region_code}"
        
        try:
            with open(self.regions_file, 'r') as f:
                data = json.load(f)
                region_data = data[region_code]
                
                # Get random sub-code
                sub_codes = region_data[1] if isinstance(region_data, list) and len(region_data) > 1 else {}
                sub_code = random.choice(list(sub_codes.keys())) if sub_codes else ""
                
                # Generate random number (1-9999)
                number = random.randint(1, 9999)
                
                # Generate owner code (1-3 letters)
                owner_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(1, 3)))
                
                plate = f"{region_code} {number} {sub_code}{owner_code}"
                return plate
        except Exception as e:
            return f"Error generating plate: {e}"


def test_validator():
    """Test the validator with various plates"""
    validator = IndonesianPlateValidator()
    
    test_plates = [
        "B 1704 CJE",      # Valid JADETABEK
        "D 100 ABC",       # Valid Bandung
        "B 1 U",           # Valid Jakarta Utara (minimal)
        "L 9999 Z",        # Valid Surabaya
        "DK 123 A",        # Valid Bali
        "B1704CJE",        # Invalid (no spaces)
        "B 1704",          # Invalid (no sub-code)
        "BB 12345 ABC",    # Invalid (number too large)
        "2 100 ABC",       # Invalid (digit in region)
        "B 0 ABC",         # Invalid (number < 1)
    ]
    
    print("=" * 80)
    print("Indonesian License Plate Validator - Test Results")
    print("=" * 80)
    
    for plate in test_plates:
        is_valid, details = validator.validate_complete(plate)
        print(f"\nPlate: {plate}")
        print(f"Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
        
        if 'region_name' in details:
            print(f"Region: {details['region_name']}")
        
        if 'errors' in details and details['errors']:
            for error in details['errors']:
                print(f"  Error: {error}")
    
    # Show region info
    print("\n" + "=" * 80)
    print("Sample Region Information")
    print("=" * 80)
    
    for code in ['B', 'D', 'DK', 'L']:
        info = validator.get_region_info(code)
        print(f"\nRegion Code: {code}")
        print(f"Region Name: {info.get('region_name', 'Unknown')}")
        print(f"Sample Sub-regions: {list(info.get('sub_regions', {}).keys())[:5]}")
    
    # Show example plates
    print("\n" + "=" * 80)
    print("Example Generated Plates")
    print("=" * 80)
    
    for code in ['B', 'D', 'F', 'DK', 'L']:
        plate = validator.generate_example_plate(code)
        print(f"{code}: {plate}")


if __name__ == "__main__":
    test_validator()
