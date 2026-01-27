"""
Indonesian License Plate and Vehicle Owner Database
Handles plate nomenclature, region mapping, and owner information
"""

import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path

class IndonesianPlateManager:
    """Manages Indonesian license plate generation and parsing"""
    
    # Indonesian plate format: [Region Code] [Number] [Letter Code]
    # Example: D 1234 CD = Bandung, number 1234, owner code CD
    
    # Cached regions data loaded from JSON
    _REGION_CODES = None
    _REGION_CODES_FLAT = None
    
    # Common Indonesian owner code suffixes
    OWNER_CODE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    @classmethod
    def _load_regions_data(cls) -> Dict:
        """Load regions data from JSON file"""
        if cls._REGION_CODES is not None:
            return cls._REGION_CODES
        
        try:
            # Try to load from data/regions/indonesian_regions.json
            json_path = Path(__file__).parent.parent / 'data' / 'regions' / 'indonesian_regions.json'
            
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    cls._REGION_CODES = json.load(f)
                print(f"[REGIONS] Loaded comprehensive regions data from {json_path}")
                return cls._REGION_CODES
            else:
                print(f"[REGIONS] Warning: regions.json not found at {json_path}")
                raise FileNotFoundError(f"Indonesian regions file not found: {json_path}")
        except Exception as e:
            print(f"[REGIONS] Error loading regions data: {e}")
            # Fallback to minimal hardcoded regions
            cls._REGION_CODES = {
                'B': ['JADETABEK', {'U': 'Jakarta Utara', 'B': 'Jakarta Barat', 'P': 'Jakarta Pusat', 'T': 'Jakarta Timur', 'S': 'Jakarta Selatan'}],
                'D': ['Jawa Barat', {'A': 'Bandung, Jawa Barat', 'B': 'Bandung, Jawa Barat'}],
                'H': ['Jawa Tengah', {'A': 'Semarang, Jawa Tengah'}],
                'L': ['Surabaya, Jawa Timur'],
                'AB': ['Daerah Istimewa Yogyakarta', {'A': 'Yogyakarta'}],
                'DK': ['Bali', {'A': 'Denpasar, Bali'}],
            }
            print("[REGIONS] Using minimal fallback regions data")
            return cls._REGION_CODES
    
    @classmethod
    def _get_all_region_codes_flat(cls) -> Dict[str, str]:
        """Get flattened region codes from nested structure"""
        if cls._REGION_CODES_FLAT is not None:
            return cls._REGION_CODES_FLAT
        
        regions = cls._load_regions_data()
        flat_codes = {}
        
        for region_code, region_data in regions.items():
            if isinstance(region_data, list):
                if len(region_data) == 2 and isinstance(region_data[1], dict):
                    # Has sub-codes
                    for sub_code, location in region_data[1].items():
                        full_code = f"{region_code}{sub_code}"
                        flat_codes[full_code] = location
                        # Also add primary code as fallback
                        if region_code not in flat_codes:
                            flat_codes[region_code] = region_data[0] if isinstance(region_data[0], str) else location
                else:
                    # No sub-codes, just province name
                    flat_codes[region_code] = region_data[0] if isinstance(region_data[0], str) else 'Unknown'
            else:
                flat_codes[region_code] = region_data
        
        cls._REGION_CODES_FLAT = flat_codes
        return cls._REGION_CODES_FLAT
    
    @staticmethod
    def generate_plate() -> Tuple[str, str]:
        """
        Generate Indonesian license plate
        Returns: (plate_number, region_location)
        Example: ('D 1234 CD', 'Bandung, Jawa Barat')
        """
        # Get random region code from comprehensive data
        flat_codes = IndonesianPlateManager._get_all_region_codes_flat()
        
        # Filter to only use 1-2 character region codes (proper format)
        valid_codes = {k: v for k, v in flat_codes.items() if len(k) <= 2}
        
        if not valid_codes:
            valid_codes = flat_codes  # Fallback if no valid codes
        
        region_code = random.choice(list(valid_codes.keys()))
        region_location = valid_codes[region_code]
        
        # Generate 4-digit number
        number = random.randint(1000, 9999)
        
        # Generate 2-letter owner code (last 2 letters typically represent owner initials area)
        owner_code = ''.join(random.choices(IndonesianPlateManager.OWNER_CODE_LETTERS, k=2))
        
        plate = f"{region_code} {number} {owner_code}"
        
        return plate, region_location
    
    @staticmethod
    def parse_plate(plate: str) -> Dict:
        """
        Parse Indonesian license plate
        Example: 'D 1234 CD' -> {region_code: 'D', region: 'Bandung...', number: '1234', owner_code: 'CD'}
        """
        parts = plate.split()
        if len(parts) != 3:
            return None
        
        region_code = parts[0]
        number = parts[1]
        owner_code = parts[2]
        
        # Try to find region from comprehensive data
        flat_codes = IndonesianPlateManager._get_all_region_codes_flat()
        region = flat_codes.get(region_code, 'Unknown')
        
        return {
            'plate': plate,
            'region_code': region_code,
            'region': region,
            'number': number,
            'owner_code': owner_code
        }
    
    @staticmethod
    def get_region_from_code(code: str) -> str:
        """Get region location from plate code"""
        flat_codes = IndonesianPlateManager._get_all_region_codes_flat()
        return flat_codes.get(code, 'Unknown Region')


class VehicleOwner:
    """Represents a vehicle owner with registration details"""
    
    INDONESIAN_FIRST_NAMES = [
        'Budi', 'Siti', 'Ahmad', 'Rina', 'Suryanto', 'Dewi', 'Hendra', 'Putri',
        'Bambang', 'Indra', 'Nurhayati', 'Wawan', 'Sari', 'Totok', 'Retno',
        'Yudi', 'Maya', 'Kusuma', 'Handoko', 'Lestari', 'Adi', 'Diana',
        'Prayogo', 'Fitri', 'Rendi', 'Ayu', 'Wahyu', 'Nisak', 'Haryo'
    ]
    
    INDONESIAN_LAST_NAMES = [
        'Wijaya', 'Santoso', 'Rahman', 'Setiawan', 'Gunawan', 'Hartono',
        'Kusuma', 'Hermawan', 'Pratama', 'Sugiono', 'Prasetyo', 'Wibowo',
        'Nugroho', 'Cahyono', 'Sumarlin', 'Hermansyah', 'Bambang',
        'Prabowo', 'Sumargo', 'Indrawan'
    ]
    
    # ID types (KTP, Paspor, SIM)
    ID_TYPES = ['KTP', 'Paspor', 'SIM']
    
    def __init__(self, owner_id: str, name: str, region: str, stnk_status: bool, sim_status: bool):
        """
        Args:
            owner_id: Personal ID number (NIK/KTP)
            name: Owner's full name
            region: Region/City of residence
            stnk_status: True = Active, False = Non-active (STNK = Surat Tanda Nomor Kendaraan)
            sim_status: True = Active, False = Expired/Dead (SIM = Surat Izin Mengemudi)
        """
        self.owner_id = owner_id
        self.name = name
        self.region = region
        self.stnk_status = stnk_status  # Vehicle registration status
        self.sim_status = sim_status    # Driving license status
        self.stnk_expiry = self._generate_stnk_expiry(stnk_status)
        self.sim_expiry = self._generate_sim_expiry(sim_status)
    
    @staticmethod
    def generate_random_owner(region: str) -> 'VehicleOwner':
        """Generate a random vehicle owner"""
        # Generate proper Indonesian NIK (16 digits)
        # Format: AA BB CC DD MM YY ZZZZ
        # AA = Province code (01-34)
        # BB = District/City code (01-99)
        # CC = Subdistrict code (01-99)
        # DD = Birth date (01-31, or +40 for females)
        # MM = Birth month (01-12)
        # YY = Birth year (2 digits)
        # ZZZZ = Sequential number (0001-9999)
        
        province_code = f"{random.randint(1, 34):02d}"  # 01-34
        district_code = f"{random.randint(1, 99):02d}"  # 01-99
        subdistrict_code = f"{random.randint(1, 99):02d}"  # 01-99
        
        # Generate birth date
        birth_day = random.randint(1, 28)  # Use 1-28 to avoid month-specific issues
        is_female = random.random() < 0.5
        if is_female:
            birth_day += 40  # Females have +40 added to birth day
        birth_date = f"{birth_day:02d}"
        
        birth_month = f"{random.randint(1, 12):02d}"
        birth_year = f"{random.randint(50, 99):02d}"  # Birth years from 1950-1999
        
        sequential_number = f"{random.randint(1, 9999):04d}"
        
        owner_id = f"{province_code}{district_code}{subdistrict_code}{birth_date}{birth_month}{birth_year}{sequential_number}"
        
        # Generate random name
        first_name = random.choice(VehicleOwner.INDONESIAN_FIRST_NAMES)
        last_name = random.choice(VehicleOwner.INDONESIAN_LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # 70% chance STNK is active, 30% non-active
        stnk_status = random.random() < 0.7
        
        # 80% chance SIM is active, 20% expired
        sim_status = random.random() < 0.8
        
        return VehicleOwner(owner_id, name, region, stnk_status, sim_status)
    
    @staticmethod
    def _generate_stnk_expiry(is_active: bool) -> datetime:
        """Generate STNK expiry date"""
        if is_active:
            # Valid for 1-5 years
            days = random.randint(365, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            # Expired 1 month to 2 years ago
            days = -random.randint(30, 730)
            return datetime.now() + timedelta(days=days)
    
    @staticmethod
    def _generate_sim_expiry(is_active: bool) -> datetime:
        """Generate SIM expiry date"""
        if is_active:
            # Valid for 1-5 years
            days = random.randint(365, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            # Expired 1 month to 3 years ago
            days = -random.randint(30, 1095)
            return datetime.now() + timedelta(days=days)
    
    def get_stnk_status_display(self) -> str:
        """Get STNK status display"""
        if self.stnk_status:
            return f"Active (Expires: {self.stnk_expiry.strftime('%Y-%m-%d')})"
        else:
            return f"Non-Active (Expired: {self.stnk_expiry.strftime('%Y-%m-%d')})"
    
    def get_sim_status_display(self) -> str:
        """Get SIM status display"""
        if self.sim_status:
            return f"Active (Expires: {self.sim_expiry.strftime('%Y-%m-%d')})"
        else:
            return f"Expired (Expired: {self.sim_expiry.strftime('%Y-%m-%d')})"
    
    def is_violation_risk(self) -> bool:
        """Check if owner has inactive STNK or SIM (risk factors for violations)"""
        return not self.stnk_status or not self.sim_status
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'owner_id': self.owner_id,
            'name': self.name,
            'region': self.region,
            'stnk_status': 'Active' if self.stnk_status else 'Non-Active',
            'stnk_expiry': self.stnk_expiry.isoformat(),
            'sim_status': 'Active' if self.sim_status else 'Expired',
            'sim_expiry': self.sim_expiry.isoformat(),
        }


class OwnerDatabase:
    """Database for storing vehicle owners by license plate"""
    
    def __init__(self):
        self.owners: Dict[str, VehicleOwner] = {}
    
    def register_vehicle(self, plate: str, owner: VehicleOwner) -> None:
        """Register a vehicle with its owner"""
        self.owners[plate] = owner
    
    def get_owner(self, plate: str) -> Optional[VehicleOwner]:
        """Get owner by plate number"""
        return self.owners.get(plate)
    
    def get_or_create_owner(self, plate: str) -> VehicleOwner:
        """Get existing owner or create a new one"""
        if plate in self.owners:
            return self.owners[plate]
        
        # Parse plate to get region
        plate_info = IndonesianPlateManager.parse_plate(plate)
        region = plate_info['region'] if plate_info else 'Unknown'
        
        # Create new owner
        owner = VehicleOwner.generate_random_owner(region)
        self.owners[plate] = owner
        
        return owner
    
    def save_to_file(self, filepath: str) -> None:
        """Save database to JSON file"""
        data = {
            plate: owner.to_dict() 
            for plate, owner in self.owners.items()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filepath: str) -> None:
        """Load database from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Reconstruct owner objects
            for plate, owner_data in data.items():
                owner = VehicleOwner(
                    owner_id=owner_data['owner_id'],
                    name=owner_data['name'],
                    region=owner_data['region'],
                    stnk_status=owner_data['stnk_status'] == 'Active',
                    sim_status=owner_data['sim_status'] == 'Active'
                )
                self.owners[plate] = owner
        except FileNotFoundError:
            pass  # Database doesn't exist yet


# Global database instance
owner_db = OwnerDatabase()
