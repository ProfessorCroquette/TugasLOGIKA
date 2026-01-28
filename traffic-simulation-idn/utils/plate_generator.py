"""
Comprehensive Indonesian License Plate Generator System
Implements all official plate types and specifications per Polri regulations
Supports: Private, Public/Commercial, Trucks, Government, Diplomatic, Temporary, Trial

Format Reference:
- Private (Hitam): [RegionCode] [1-4 digits] [1-3 letters]
- Commercial (Kuning): [RegionCode] [1-4 digits] [letters] (NIAGA)
- Trucks (Kuning Khusus): [RegionCode] [1-4 digits] [T/K/G/D][letters] + truck class
- Government (Merah): RI [InstituteCode] [1-4 digits]
- Diplomatic (Putih): [CD/CC] [CountryCode] [1-4 digits]
- Temporary (Putih-Merah): [RegionCode] [1-4 digits] [letters] (SEMENTARA)
- Trial (Putih-Biru): KB [1-4 digits] [letters] (UJI COBA)
"""

import random
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime, timedelta
from enum import Enum


class PlateType(Enum):
    """Official Indonesian license plate types"""
    PRIVATE = "Pribadi"           # Black plate
    COMMERCIAL = "Niaga"          # Yellow plate
    TRUCK = "Truk"                # Yellow special plate
    GOVERNMENT = "Pemerintah"     # Red plate
    DIPLOMATIC = "Diplomatik"     # White plate
    TEMPORARY = "Sementara"       # White-Red plate
    TRIAL = "Uji Coba"            # White-Blue plate


class TruckSubType(Enum):
    """Truck classification for special codes"""
    GENERAL = ("Umum", "")           # General cargo truck
    CONTAINER = ("Kontainer", "K")   # Container truck
    TANKER = ("Tangki", "G")         # Tanker truck
    DUMP = ("Dump", "D")             # Dump truck
    FLATBED = ("Bak Terbuka", "T")   # Flatbed truck


class TruckClass(Enum):
    """Truck weight classification"""
    LIGHT = ("Ringan", "<= 8 ton", "TRUK-8T")
    MEDIUM = ("Sedang", "8-16 ton", "TRUK-16T")
    HEAVY = ("Berat", "> 16 ton", "TRUK-24T")


class GovernmentAgency(Enum):
    """Government vehicle agency codes"""
    POLICE = (1, "Kepolisian", "Polri")
    ARMY_LAND = (2, "TNI Angkatan Darat", "TNI AD")
    ARMY_NAVY = (3, "TNI Angkatan Laut", "TNI AL")
    ARMY_AIR = (4, "TNI Angkatan Udara", "TNI AU")
    PRESIDENCY = (5, "Kepresidenan", "Istana")
    PARLIAMENT = (6, "DPR/MPR/DPD", "Legislatif")
    MINISTRY = (7, "Kementerian", "Kementerian")
    LOCAL_GOV = (8, "Pemerintah Daerah", "Pemda")
    LAW_ENFORCEMENT = (9, "Lembaga Penegak Hukum", "Kejaksaan")


class DiplomaticCountry(Enum):
    """Diplomatic country codes and names"""
    USA = ("71", "AMERIKA SERIKAT")
    UK = ("72", "INGGRIS")
    AUSTRALIA = ("73", "AUSTRALIA")
    JAPAN = ("74", "JEPANG")
    GERMANY = ("75", "JERMAN")
    FRANCE = ("76", "PRANCIS")
    ITALY = ("77", "ITALIA")
    NETHERLANDS = ("78", "BELANDA")
    BELGIUM = ("79", "BELGIA")
    CANADA = ("80", "KANADA")
    MEXICO = ("81", "MEKSIKO")
    BRAZIL = ("82", "BRASIL")
    INDIA = ("83", "INDIA")
    CHINA = ("84", "TIONGKOK")
    SOUTH_KOREA = ("85", "KOREA SELATAN")
    THAILAND = ("86", "THAILAND")
    MALAYSIA = ("87", "MALAYSIA")
    SINGAPORE = ("88", "SINGAPURA")
    PHILIPPINES = ("89", "FILIPINA")
    VIETNAM = ("90", "VIETNAM")


class TourRoute(Enum):
    """Truck route classifications"""
    DALAM_KOTA = ("DK", "Dalam Kota")
    LINTAS_KABUPATEN = ("LK", "Lintas Kabupaten")
    LINTAS_PROVINSI = ("LP", "Lintas Provinsi")
    LINTAS_NASIONAL = ("LN", "Lintas Nasional")


class PlateCharacterValidator:
    """Validates Indonesian plate characters"""
    
    # Valid letters (excluding I, O, Q per regulations)
    VALID_LETTERS = "ABCDEFGHJKLMNPRSTUVWXYZ"
    
    # Complete region code database
    REGION_CODES = {
        'B': ('DKI Jakarta', ['B', 'F', 'P', 'T', 'Z']),
        'D': ('Jawa Barat - Bandung', ['A', 'B', 'C', 'D', 'E', 'F', 'Z']),
        'F': ('Jawa Barat - Bogor', ['B', 'D', 'G', 'J', 'K', 'L', 'M', 'N', 'P', 'Z']),
        'G': ('Jawa Barat - Cianjur', ['B', 'C', 'D', 'E', 'K', 'P', 'R', 'Z']),
        'H': ('Jawa Tengah - Semarang', ['A', 'B', 'C', 'D', 'E', 'F', 'K', 'L', 'M', 'N', 'P', 'S', 'T', 'Z']),
        'AA': ('Jawa Tengah - Purwokerto', ['A', 'B', 'D', 'J', 'K', 'P', 'R', 'T', 'Z']),
        'AB': ('DI Yogyakarta', ['A', 'B', 'C', 'D', 'E', 'F', 'K', 'L', 'M', 'N', 'P', 'T', 'Z']),
        'AG': ('Jawa Timur - Surabaya', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'Z']),
        'L': ('Jawa Timur - Surabaya', ['A', 'B', 'C', 'D', 'E', 'F', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'Z']),
        'DK': ('Bali - Denpasar', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'Z']),
        'BL': ('Aceh', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'Z']),
        'BB': ('Sumatera Utara - Medan', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'Z']),
        'BK': ('Riau', ['A', 'B', 'C', 'D', 'E', 'F', 'K', 'P', 'R', 'Z']),
        'BN': ('Jambi', ['A', 'B', 'C', 'D', 'K', 'M', 'P', 'Z']),
        'BP': ('Sumatera Selatan', ['A', 'B', 'C', 'D', 'K', 'L', 'M', 'P', 'Z']),
        'KB': ('Bengkulu', ['A', 'D', 'M', 'P', 'R', 'Z']),
        'KT': ('Lampung', ['A', 'B', 'D', 'E', 'K', 'P', 'T', 'Z']),
        'BG': ('Kalimantan Barat', ['A', 'B', 'C', 'D', 'K', 'P', 'R', 'Z']),
        'DA': ('Kalimantan Tengah', ['A', 'B', 'C', 'D', 'K', 'P', 'Z']),
        'DB': ('Kalimantan Selatan', ['A', 'B', 'C', 'D', 'K', 'L', 'P', 'Z']),
        'DC': ('Kalimantan Timur', ['A', 'B', 'C', 'D', 'K', 'M', 'P', 'Z']),
        'NA': ('Sulawesi Utara', ['A', 'B', 'C', 'D', 'K', 'P', 'Z']),
        'BM': ('Gorontalo', ['A', 'B', 'D', 'K', 'P', 'Z']),
        'NB': ('Sulawesi Tengah', ['A', 'B', 'C', 'D', 'K', 'P', 'Z']),
        'DD': ('Sulawesi Selatan', ['A', 'B', 'C', 'D', 'E', 'K', 'L', 'M', 'P', 'R', 'Z']),
        'ND': ('Sulawesi Tenggara', ['A', 'B', 'D', 'K', 'P', 'Z']),
        'EA': ('Maluku', ['A', 'B', 'C', 'D', 'K', 'P', 'Z']),
        'EB': ('Maluku Utara', ['A', 'B', 'D', 'K', 'P', 'Z']),
        'PB': ('Papua Barat', ['A', 'B', 'D', 'K', 'P', 'Z']),
        'PA': ('Papua', ['A', 'B', 'C', 'D', 'E', 'K', 'P', 'Z']),
        'DL': ('Nusa Tenggara Barat', ['A', 'B', 'D', 'K', 'P', 'Z']),
        'DM': ('Nusa Tenggara Timur', ['A', 'B', 'C', 'D', 'E', 'K', 'P', 'Z']),
    }
    
    @classmethod
    def is_valid_letter(cls, char: str) -> bool:
        """Check if letter is allowed (not I, O, Q)"""
        return char.upper() in cls.VALID_LETTERS
    
    @classmethod
    def get_valid_letters(cls) -> str:
        """Get string of all valid letters"""
        return cls.VALID_LETTERS
    
    @classmethod
    def get_all_region_codes(cls) -> Dict[str, Tuple[str, List[str]]]:
        """Get all region codes and their info"""
        return cls.REGION_CODES
    
    @classmethod
    def is_valid_region(cls, region_code: str) -> bool:
        """Check if region code is valid"""
        return region_code in cls.REGION_CODES


class PlatGenerator:
    """Main plate generator with full specification support"""
    
    def __init__(self):
        self.generated_plates: Set[str] = set()
        self.validator = PlateCharacterValidator()
    
    def generate_private_plate(self, region_code: Optional[str] = None) -> Dict:
        """
        Generate private vehicle plate (black plate)
        Format: [RegionCode] [1-4 digits] [1-3 letters]
        Example: B 1234 ABC, F 567 XY
        """
        if region_code is None:
            region_code = random.choice(list(self.validator.REGION_CODES.keys()))
        elif not self.validator.is_valid_region(region_code):
            raise ValueError(f"Invalid region code: {region_code}")
        
        region_name = self.validator.REGION_CODES[region_code][0]
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        # Generate 1-3 letters
        letter_count = random.randint(1, 3)
        letters = ''.join(random.choices(self.validator.VALID_LETTERS, k=letter_count))
        
        plate = f"{region_code} {number_str} {letters}"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.PRIVATE.value,
            'color': 'Hitam (Tulisan Putih/Silver)',
            'region_code': region_code,
            'region_name': region_name,
            'number': number_str,
            'letters': letters,
            'description': 'Kendaraan Pribadi'
        }
    
    def generate_commercial_plate(self, region_code: Optional[str] = None) -> Dict:
        """
        Generate commercial vehicle plate (yellow plate with NIAGA)
        Format: [RegionCode] [1-4 digits] [1-3 letters] (NIAGA)
        Example: B 5678 XY (NIAGA)
        """
        if region_code is None:
            region_code = random.choice(list(self.validator.REGION_CODES.keys()))
        elif not self.validator.is_valid_region(region_code):
            raise ValueError(f"Invalid region code: {region_code}")
        
        region_name = self.validator.REGION_CODES[region_code][0]
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        # Generate 1-3 letters
        letter_count = random.randint(1, 3)
        letters = ''.join(random.choices(self.validator.VALID_LETTERS, k=letter_count))
        
        plate = f"{region_code} {number_str} {letters} (NIAGA)"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.COMMERCIAL.value,
            'color': 'Kuning (Tulisan Hitam)',
            'region_code': region_code,
            'region_name': region_name,
            'number': number_str,
            'letters': letters,
            'category': 'Kendaraan Umum/Niaga',
            'description': 'Angkutan Penumpang atau Barang'
        }
    
    def generate_truck_plate(
        self,
        truck_type: TruckSubType = TruckSubType.GENERAL,
        truck_class: TruckClass = TruckClass.MEDIUM,
        region_code: Optional[str] = None,
        route: Optional[TourRoute] = None
    ) -> Dict:
        """
        Generate truck vehicle plate (yellow special plate)
        Format: [RegionCode] [1-4 digits] [T/K/G/D][1-3 letters] + class + route info
        Examples:
        - B 1234 TAX (TRUK-16T) - General truck
        - B 5678 KBC (TRUK-24T) - Container truck
        - F 9012 GXY (TRUK-16T) - Tanker truck
        - ZP 3456 DEF (TRUK-24T) - RUTE: LN
        """
        if region_code is None:
            region_code = random.choice(list(self.validator.REGION_CODES.keys()))
        elif not self.validator.is_valid_region(region_code):
            raise ValueError(f"Invalid region code: {region_code}")
        
        region_name = self.validator.REGION_CODES[region_code][0]
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        # Get truck code letter
        truck_code_letter = truck_type.value[1]
        
        # Generate 1-3 letters after truck code
        letter_count = random.randint(1, 3)
        letters = ''.join(random.choices(self.validator.VALID_LETTERS, k=letter_count))
        
        # Build plate with truck code
        plate = f"{region_code} {number_str} {truck_code_letter}{letters}"
        
        # Get truck class display
        truck_class_name, truck_weight, truck_class_code = truck_class.value
        
        # Add truck class notation
        plate += f" ({truck_class_code})"
        
        # Add route if specified
        if route is None:
            route = random.choice(list(TourRoute))
        route_code, route_name = route.value
        
        # Add route info for heavy trucks
        if truck_class in [TruckClass.MEDIUM, TruckClass.HEAVY]:
            plate += f" - RUTE: {route_code}"
        
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.TRUCK.value,
            'color': 'Kuning (Tulisan Hitam)',
            'region_code': region_code,
            'region_name': region_name,
            'number': number_str,
            'truck_code': truck_code_letter,
            'letters': letters,
            'truck_subtype': truck_type.value[0],
            'truck_class': truck_class_name,
            'truck_weight': truck_weight,
            'truck_class_code': truck_class_code,
            'route': route_name,
            'route_code': route_code,
            'description': f'Angkutan Barang Khusus - {truck_type.value[0]}'
        }
    
    def generate_government_plate(
        self,
        agency: GovernmentAgency = GovernmentAgency.POLICE
    ) -> Dict:
        """
        Generate government vehicle plate (red plate)
        Format: RI [AgencyCode] [1-4 digits]
        Examples:
        - RI 1 1234 (Kepolisian)
        - RI 2 567 (TNI AD)
        - RI 5 001 (Kepresidenan)
        """
        agency_code, agency_name, agency_short = agency.value
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        plate = f"RI {agency_code} {number_str}"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.GOVERNMENT.value,
            'color': 'Merah (Tulisan Putih)',
            'agency_code': agency_code,
            'agency_name': agency_name,
            'agency_short': agency_short,
            'number': number_str,
            'description': f'Kendaraan Pemerintah - {agency_name}'
        }
    
    def generate_diplomatic_plate(
        self,
        country: DiplomaticCountry = DiplomaticCountry.USA,
        is_consular: bool = False
    ) -> Dict:
        """
        Generate diplomatic vehicle plate (white plate)
        Format: [CD/CC] [CountryCode] [1-4 digits]
        Examples:
        - CD 71 123 (Corps Diplomatic - USA)
        - CC 72 456 (Consular Corps - UK)
        """
        country_code, country_name = country.value
        
        # Diplomatic type
        if is_consular:
            diplomatic_type = "CC"
            diplomatic_type_name = "Consular Corps"
        else:
            diplomatic_type = "CD"
            diplomatic_type_name = "Corps Diplomatic"
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        plate = f"{diplomatic_type} {country_code} {number_str}"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.DIPLOMATIC.value,
            'color': 'Putih (Tulisan Hitam)',
            'diplomatic_type': diplomatic_type_name,
            'country_code': country_code,
            'country_name': country_name,
            'number': number_str,
            'description': f'Kendaraan Diplomatik - {country_name}'
        }
    
    def generate_temporary_plate(
        self,
        region_code: Optional[str] = None,
        valid_days: int = 180
    ) -> Dict:
        """
        Generate temporary vehicle plate (white-red plate)
        Format: [RegionCode] [1-4 digits] [1-3 letters] (SEMENTARA) - EXP: DD/MM/YYYY
        Example: B 1234 X (SEMENTARA) - EXP: 30/06/2024
        """
        if region_code is None:
            region_code = random.choice(list(self.validator.REGION_CODES.keys()))
        elif not self.validator.is_valid_region(region_code):
            raise ValueError(f"Invalid region code: {region_code}")
        
        region_name = self.validator.REGION_CODES[region_code][0]
        
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        # Generate 1-3 letters
        letter_count = random.randint(1, 3)
        letters = ''.join(random.choices(self.validator.VALID_LETTERS, k=letter_count))
        
        # Calculate expiry date
        expiry_date = datetime.now() + timedelta(days=valid_days)
        expiry_str = expiry_date.strftime("%d/%m/%Y")
        
        plate = f"{region_code} {number_str} {letters} (SEMENTARA) - EXP: {expiry_str}"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.TEMPORARY.value,
            'color': 'Putih-Merah (Tulisan Hitam)',
            'region_code': region_code,
            'region_name': region_name,
            'number': number_str,
            'letters': letters,
            'valid_days': valid_days,
            'expiry_date': expiry_str,
            'description': 'Kendaraan Sementara'
        }
    
    def generate_trial_plate(self, valid_days: int = 365) -> Dict:
        """
        Generate trial/dealer vehicle plate (white-blue plate)
        Format: KB [1-4 digits] [1-3 letters] (UJI COBA) - EXP: DD/MM/YYYY
        Example: KB 1234 AB (UJI COBA) - EXP: 31/12/2024
        """
        # Generate 1-4 digit number
        num_digits = random.randint(1, 4)
        number = random.randint(1, (10 ** num_digits) - 1)
        number_str = f"{number:0{num_digits}d}"
        
        # Generate 1-3 letters
        letter_count = random.randint(1, 3)
        letters = ''.join(random.choices(self.validator.VALID_LETTERS, k=letter_count))
        
        # Calculate expiry date
        expiry_date = datetime.now() + timedelta(days=valid_days)
        expiry_str = expiry_date.strftime("%d/%m/%Y")
        
        plate = f"KB {number_str} {letters} (UJI COBA) - EXP: {expiry_str}"
        self.generated_plates.add(plate)
        
        return {
            'plate': plate,
            'type': PlateType.TRIAL.value,
            'color': 'Putih-Biru (Tulisan Hitam)',
            'number': number_str,
            'letters': letters,
            'valid_days': valid_days,
            'expiry_date': expiry_str,
            'description': 'Kendaraan Uji Coba/Dealer'
        }
    
    def generate_random_plate(self, plate_type: Optional[PlateType] = None) -> Dict:
        """
        Generate a random plate of any type
        """
        if plate_type is None:
            plate_type = random.choice(list(PlateType))
        
        if plate_type == PlateType.PRIVATE:
            return self.generate_private_plate()
        elif plate_type == PlateType.COMMERCIAL:
            return self.generate_commercial_plate()
        elif plate_type == PlateType.TRUCK:
            truck_type = random.choice(list(TruckSubType))
            truck_class = random.choice(list(TruckClass))
            return self.generate_truck_plate(truck_type, truck_class)
        elif plate_type == PlateType.GOVERNMENT:
            agency = random.choice(list(GovernmentAgency))
            return self.generate_government_plate(agency)
        elif plate_type == PlateType.DIPLOMATIC:
            country = random.choice(list(DiplomaticCountry))
            is_consular = random.random() < 0.3
            return self.generate_diplomatic_plate(country, is_consular)
        elif plate_type == PlateType.TEMPORARY:
            return self.generate_temporary_plate()
        elif plate_type == PlateType.TRIAL:
            return self.generate_trial_plate()
    
    def validate_plate(self, plate: str) -> Dict:
        """
        Validate if a plate conforms to Indonesian regulations
        """
        if not plate or not isinstance(plate, str):
            return {'valid': False, 'error': 'Plate must be a non-empty string'}
        
        plate = plate.strip()
        errors = []
        
        # Check for invalid letters
        for char in plate:
            if char.isalpha() and not self.validator.is_valid_letter(char):
                errors.append(f"Character '{char}' not allowed (I, O, Q forbidden)")
        
        # Check format patterns
        is_valid = True
        plate_type = "Unknown"
        
        if plate.startswith("RI "):
            plate_type = "Government"
        elif plate.startswith("CD ") or plate.startswith("CC "):
            plate_type = "Diplomatic"
        elif plate.startswith("KB "):
            plate_type = "Trial"
        elif "(SEMENTARA)" in plate:
            plate_type = "Temporary"
        elif "(NIAGA)" in plate:
            plate_type = "Commercial"
        elif any(code in plate for code in "TKGD"):
            plate_type = "Truck"
        else:
            plate_type = "Private"
        
        return {
            'valid': len(errors) == 0,
            'plate': plate,
            'plate_type': plate_type,
            'errors': errors if errors else None,
            'description': f'{plate_type} vehicle plate'
        }
    
    def get_generated_plates_count(self) -> int:
        """Get count of generated plates in session"""
        return len(self.generated_plates)
    
    def is_plate_unique(self, plate: str) -> bool:
        """Check if plate hasn't been generated before"""
        return plate not in self.generated_plates
    
    def clear_session(self):
        """Clear all generated plates"""
        self.generated_plates.clear()


# Global generator instance
_plate_generator = None


def get_plate_generator() -> PlatGenerator:
    """Get or create global plate generator instance"""
    global _plate_generator
    if _plate_generator is None:
        _plate_generator = PlatGenerator()
    return _plate_generator
