"""
Indonesian License Plate Management System
Implements complete Indonesian plate nomenclature per official format
Supports both Roda Dua (motorcycles) and Roda Empat atau lebih (4+ wheels)
Format: [RegionCode] [4-digit number] [SubCode] [Owner letters]
Examples:
  - Motor: B 1234 U AB
  - Mobil: B 5678 P ABC
"""

import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum


class VehicleType(Enum):
    """Vehicle classification per Indonesian regulations"""
    RODA_DUA = "Roda Dua (Motor)"
    RODA_EMPAT_LEBIH = "Roda Empat atau lebih (Mobil)"


class VehicleCategory(Enum):
    """Vehicle category per Indonesian License Plate Regulations
    
    Categories determine plate suffix and color:
    - Pribadi: Private vehicles (no suffix, black plate)
    - Umum: Public transport (H suffix, yellow plate)
    - Barang: Commercial goods (K suffix, yellow plate)
    - Pemerintah: Government (no suffix, red plate)
    - Diplomatik: Diplomatic (CD/CC + country code, white plate)
    - Sementara: Temporary/Test (TMP suffix, white plate)
    - Alat Berat: Heavy equipment (BG suffix, white plate)
    """
    PRIBADI = "Pribadi"           # Private: B 1234 ABC
    UMUM = "Umum"                 # Public: B 1234 UD H
    BARANG = "Barang"             # Commercial: B 1234 XY K
    PEMERINTAH = "Pemerintah"     # Government: B 1234 CD
    DIPLOMATIK = "Diplomatik"     # Diplomatic: CD 12 123
    SEMENTARA = "Sementara"       # Temporary: B 1234 TMP
    ALAT_BERAT = "Alat Berat"    # Heavy: L 987 TA BG


class IndonesianPlateManager:
    """Manages Indonesian license plate generation following official nomenclature"""
    
    OWNER_CODE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Complete Indonesian plate data per official regulations
    PLATE_DATA = {
        'BL': {
            'region_name': 'Aceh',
            'area': 'Sumatra Bagian Utara',
            'sub_codes': {
                'A': 'Kota Banda Aceh', 'B': 'Gayo Lues', 'C': 'Aceh Barat Daya',
                'D': 'Aceh Timur', 'E': 'Aceh Barat', 'F': 'Kota Langsa',
                'G': 'Aceh Tengah', 'H': 'Aceh Tenggara', 'I': 'Kota Subulussalam',
                'J': 'Kota Banda Aceh', 'K': 'Aceh Utara', 'L': 'Aceh Besar',
                'M': 'Kota Sabang', 'N': 'Kota Lhokseumawe', 'O': 'Pidie Jaya',
                'P': 'Pidie', 'Q': 'Aceh Utara', 'R': 'Aceh Singkil',
                'S': 'Simeulue', 'T': 'Aceh Selatan', 'U': 'Aceh Tamiang',
                'V': 'Nagan Raya', 'W': 'Aceh Jaya', 'Y': 'Bener Meriah', 'Z': 'Bireuen'
            }
        },
        'BB': {
            'region_name': 'Sumatera Utara Barat (Tapanuli)',
            'area': 'Sumatra Bagian Utara',
            'sub_codes': {
                'A': 'Kota Sibolga', 'B': 'Tapanuli Utara', 'C': 'Samosir',
                'D': 'Humbang Hasundutan', 'E': 'Toba', 'F': 'Kota Padang Sidempuan',
                'G': 'Tapanuli Selatan', 'H': 'Kota Padang Sidempuan', 'J': 'Padang Lawas Utara',
                'K': 'Padang Lawas', 'L': 'Kota Sibolga', 'M': 'Tapanuli Tengah',
                'N': 'Kota Sibolga', 'Q': 'Nias Utara', 'R': 'Mandailing Natal',
                'T': 'Kota Gunungsitoli', 'U': 'Nias Barat', 'V': 'Nias',
                'W': 'Nias Selatan', 'Y': 'Dairi', 'Z': 'Pakpak Bharat'
            }
        },
        'B': {
            'region_name': 'DKI Jakarta',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'B': 'Jakarta Barat', 'P': 'Jakarta Pusat', 'S': 'Jakarta Selatan',
                'D': 'Jakarta Selatan', 'R': 'Jakarta Timur', 'T': 'Jakarta Timur',
                'U': 'Jakarta Utara', 'H': 'Jakarta Barat', 'E': 'Kota Depok',
                'Z': 'Kota Depok', 'F': 'Kabupaten Bekasi', 'Y': 'Kabupaten Bekasi',
                'K': 'Kota Bekasi', 'J': 'Kabupaten Tangerang', 'C': 'Kota Tangerang',
                'V': 'Kota Tangerang', 'N': 'Kota Tangerang Selatan', 'W': 'Kota Tangerang Selatan'
            }
        },
        'D': {
            'region_name': 'Kota Bandung',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Kota Bandung', 'B': 'Kota Bandung', 'C': 'Kota Bandung',
                'S': 'Kota Cimahi', 'T': 'Kota Cimahi', 'U': 'Bandung Barat',
                'X': 'Bandung Barat', 'V': 'Kabupaten Bandung', 'W': 'Kabupaten Bandung',
                'Y': 'Kabupaten Bandung', 'Z': 'Kabupaten Bandung'
            }
        },
        'H': {
            'region_name': 'Kota Semarang',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Kota Semarang', 'B': 'Kota Salatiga', 'C': 'Kabupaten Semarang',
                'D': 'Kendal', 'E': 'Demak', 'F': 'Kota Semarang'
            }
        },
        'AB': {
            'region_name': 'Yogyakarta',
            'area': 'DI Yogyakarta',
            'sub_codes': {
                'A': 'Kota Yogyakarta', 'B': 'Bantul', 'C': 'Kulon Progo',
                'D': 'Gunungkidul', 'E': 'Sleman', 'F': 'Kota Yogyakarta',
                'G': 'Bantul', 'H': 'Kota Yogyakarta', 'I': 'Kota Yogyakarta',
                'J': 'Bantul', 'K': 'Bantul', 'L': 'Kulon Progo',
                'M': 'Gunungkidul', 'N': 'Sleman', 'O': 'Kulon Progo',
                'P': 'Kulon Progo', 'Q': 'Sleman', 'R': 'Gunungkidul',
                'S': 'Kota Yogyakarta', 'T': 'Bantul', 'U': 'Sleman',
                'V': 'Kulon Progo', 'W': 'Gunungkidul', 'X': 'Sleman',
                'Y': 'Sleman', 'Z': 'Sleman'
            }
        },
        'L': {
            'region_name': 'Kota Surabaya',
            'area': 'Jawa Timur',
            'sub_codes': {
                c: 'Kota Surabaya' for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            }
        },
        'DK': {
            'region_name': 'Bali',
            'area': 'Bali',
            'sub_codes': {
                'A': 'Kota Denpasar', 'B': 'Kota Denpasar', 'C': 'Kota Denpasar',
                'D': 'Kota Denpasar', 'E': 'Kota Denpasar', 'F': 'Badung',
                'G': 'Tabanan', 'H': 'Tabanan', 'I': 'Kota Denpasar',
                'J': 'Badung', 'K': 'Gianyar', 'L': 'Gianyar',
                'M': 'Klungkung', 'N': 'Klungkung', 'O': 'Badung',
                'P': 'Bangli', 'Q': 'Kota Denpasar', 'R': 'Bangli',
                'S': 'Karangasem', 'T': 'Karangasem', 'U': 'Buleleng',
                'V': 'Buleleng', 'W': 'Jembrana', 'X': 'Kota Denpasar',
                'Y': 'Kota Denpasar', 'Z': 'Jembrana'
            }
        }
    }
    
    @classmethod
    def generate_plate(
        cls,
        vehicle_type: VehicleType = VehicleType.RODA_DUA
    ) -> Tuple[str, str, str, str]:
        """
        Generate Indonesian license plate following official nomenclature.
        
        Format: [RegionCode] [1-4 digit number] [SubCode] [Owner letters]
        Examples:
        - Motor: B 1 U AB, B 12 U AB, B 123 U AB, B 1234 U AB
        - Mobil: B 5 P ABC, B 56 P ABC, B 567 P ABC, B 5678 P ABC
        
        Args:
            vehicle_type: VehicleType enum value
            
        Returns:
            (plate_string, region_name, sub_region, vehicle_type_display)
        """
        region_code = random.choice(list(cls.PLATE_DATA.keys()))
        region_data = cls.PLATE_DATA[region_code]
        sub_code = random.choice(list(region_data['sub_codes'].keys()))
        sub_region = region_data['sub_codes'][sub_code]
        
        # Randomly choose 1, 2, 3, or 4 digit number
        num_digits = random.choice([1, 2, 3, 4])
        max_number = (10 ** num_digits) - 1
        number = f"{random.randint(0, max_number):0{num_digits}d}"
        
        if vehicle_type == VehicleType.RODA_DUA:
            owner_code = ''.join(random.choices(cls.OWNER_CODE_LETTERS, k=random.randint(1, 2)))
        else:
            owner_code = ''.join(random.choices(cls.OWNER_CODE_LETTERS, k=random.randint(2, 3)))
        
        plate = f"{region_code} {number} {sub_code} {owner_code}"
        return plate, region_data['region_name'], sub_region, vehicle_type.value
    
    @classmethod
    def parse_plate(cls, plate: str) -> Optional[Dict]:
        """Parse Indonesian license plate (handles multiple formats)
        
        Formats supported:
        - New Private: [RegionCode] [1-4 digits] [1-3 letters]
        - New Commercial: [RegionCode] [1-4 digits] [1-3 letters] (NIAGA)
        - New Truck: [RegionCode] [1-4 digits] [T/K/G/D][1-3 letters] (TRUK-XXX) - RUTE: XX
        - New Government: RI [Agency] [1-4 digits]
        - New Diplomatic: CD/CC [CountryCode] [1-4 digits]
        - Old format: [RegionCode] [4-digit] [SubCode] [Owner letters]
        """
        try:
            # Remove extra information in parentheses for parsing
            base_plate = plate.split('(')[0].strip()
            parts = base_plate.split()
            
            if len(parts) < 2:
                return None
            
            region_code = parts[0]
            
            # Handle government plates (RI prefix)
            if region_code == 'RI':
                return {
                    'plate': plate,
                    'region_code': 'RI',
                    'region_name': 'Pemerintah Indonesia',
                    'sub_region': 'Pemerintah Indonesia',
                    'is_valid': True,
                    'format': 'government'
                }
            
            # Handle diplomatic plates (CD/CC prefix)
            if region_code in ('CD', 'CC'):
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'region_name': 'Diplomatik',
                    'sub_region': 'Diplomatik',
                    'is_valid': True,
                    'format': 'diplomatic'
                }
            
            # Check if region code exists in PLATE_DATA
            if region_code not in cls.PLATE_DATA:
                return None
            
            region_data = cls.PLATE_DATA[region_code]
            region_name = region_data['region_name']
            
            # Handle new formats with 3 parts: [RegionCode] [1-4 digits] [1-3 letters]
            if len(parts) == 3:
                number = parts[1]
                letters = parts[2]
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'number': number,
                    'letters': letters,
                    'region_name': region_name,
                    'sub_region': region_name,
                    'area': region_data.get('area', 'Unknown'),
                    'is_valid': True,
                    'format': 'new'
                }
            
            # Handle old format with 4+ parts: [RegionCode] [4-digit] [SubCode] [Owner letters]
            elif len(parts) >= 4:
                number = parts[1]
                sub_code = parts[2]
                owner_code = parts[3]
                
                # Check if sub_code exists
                if sub_code not in region_data['sub_codes']:
                    return None
                
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'number': number,
                    'sub_code': sub_code,
                    'owner_code': owner_code,
                    'region_name': region_name,
                    'sub_region': region_data['sub_codes'][sub_code],
                    'area': region_data['area'],
                    'is_valid': True,
                    'format': 'old'
                }
            
            return None
        except Exception:
            return None
    
    @classmethod
    def validate_plate(cls, plate: str) -> Dict:
        """Validate plate and return information"""
        parsed = cls.parse_plate(plate)
        
        if not parsed:
            return {
                'valid': False,
                'error': 'Invalid plate format',
                'suggestion': 'Format: [RegionCode] [4digits] [SubCode] [Letters]'
            }
        
        return {
            'valid': True,
            'plate': parsed['plate'],
            'region_code': parsed['region_code'],
            'region_name': parsed['region_name'],
            'sub_region': parsed['sub_region'],
            'area': parsed['area'],
        }
    
    @classmethod
    def _load_regions_data(cls) -> Dict:
        """Load regions data - returns PLATE_DATA"""
        return cls.PLATE_DATA
    
    @classmethod
    def _get_all_region_codes_flat(cls) -> Dict[str, str]:
        """Get flattened region codes for backwards compatibility"""
        flat = {}
        for region_code, region_data in cls.PLATE_DATA.items():
            for sub_code, location in region_data['sub_codes'].items():
                full_code = f"{region_code}{sub_code}"
                flat[full_code] = location
            flat[region_code] = region_data['region_name']
        return flat
    
    @staticmethod
    def generate_plate_legacy() -> Tuple[str, str]:
        """Legacy method for backwards compatibility"""
        plate, region_name, sub_region, _ = IndonesianPlateManager.generate_plate()
        return plate, sub_region
    
    @staticmethod
    def parse_plate_legacy(plate: str) -> Optional[Dict]:
        """Legacy method for backwards compatibility"""
        return IndonesianPlateManager.parse_plate(plate)


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
    
    def __init__(
        self,
        owner_id: str,
        name: str,
        region: str,
        sub_region: str,
        stnk_status: bool,
        sim_status: bool,
        vehicle_type: str = 'roda_dua'
    ):
        """
        Args:
            owner_id: Personal ID number (NIK/KTP)
            name: Owner's full name
            region: Region/City of residence
            sub_region: Specific sub-region
            stnk_status: True = Active (Surat Tanda Nomor Kendaraan)
            sim_status: True = Active (Surat Izin Mengemudi)
            vehicle_type: 'roda_dua' or 'roda_empat'
        """
        self.owner_id = owner_id
        self.name = name
        self.region = region
        self.sub_region = sub_region
        self.stnk_status = stnk_status
        self.sim_status = sim_status
        self.vehicle_type = vehicle_type
        self.stnk_expiry = self._generate_stnk_expiry(stnk_status)
        self.sim_expiry = self._generate_sim_expiry(sim_status)
        self.registration_date = datetime.now() - timedelta(days=random.randint(30, 365*3))
    
    @staticmethod
    def generate_random_owner(region: str, sub_region: str, vehicle_type: str = 'roda_dua') -> 'VehicleOwner':
        """Generate a random vehicle owner with valid NIK"""
        province_code = f"{random.randint(1, 34):02d}"
        district_code = f"{random.randint(1, 99):02d}"
        subdistrict_code = f"{random.randint(1, 99):02d}"
        
        birth_day = random.randint(1, 28)
        is_female = random.random() < 0.5
        if is_female:
            birth_day += 40
        birth_date = f"{birth_day:02d}"
        
        birth_month = f"{random.randint(1, 12):02d}"
        birth_year = f"{random.randint(50, 99):02d}"
        sequential_number = f"{random.randint(1, 9999):04d}"
        owner_id = f"{province_code}{district_code}{subdistrict_code}{birth_date}{birth_month}{birth_year}{sequential_number}"
        
        first_name = random.choice(VehicleOwner.INDONESIAN_FIRST_NAMES)
        last_name = random.choice(VehicleOwner.INDONESIAN_LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        stnk_status = random.random() < 0.7
        sim_status = random.random() < 0.8
        
        return VehicleOwner(owner_id, name, region, sub_region, stnk_status, sim_status, vehicle_type)
    
    @staticmethod
    def _generate_stnk_expiry(is_active: bool) -> datetime:
        if is_active:
            days = random.randint(30, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            days = -random.randint(30, 730)
            return datetime.now() + timedelta(days=days)
    
    @staticmethod
    def _generate_sim_expiry(is_active: bool) -> datetime:
        if is_active:
            days = random.randint(30, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            days = -random.randint(30, 1095)
            return datetime.now() + timedelta(days=days)
    
    def get_vehicle_type_display(self) -> str:
        """Get vehicle type display"""
        if self.vehicle_type == 'roda_dua':
            return 'Roda Dua (Motor)'
        else:
            return 'Roda Empat atau lebih (Mobil)'
    
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
        """Check if owner has inactive STNK or SIM"""
        return not self.stnk_status or not self.sim_status
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'owner_id': self.owner_id,
            'name': self.name,
            'region': self.region,
            'sub_region': self.sub_region,
            'vehicle_type': self.get_vehicle_type_display(),
            'stnk_status': 'Active' if self.stnk_status else 'Non-Active',
            'stnk_expiry': self.stnk_expiry.strftime('%Y-%m-%d'),
            'sim_status': 'Active' if self.sim_status else 'Expired',
            'sim_expiry': self.sim_expiry.strftime('%Y-%m-%d'),
            'registration_date': self.registration_date.strftime('%Y-%m-%d'),
            'is_violation_risk': self.is_violation_risk()
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
    
    def get_or_create_owner(self, plate: str, vehicle_type: str = 'roda_dua') -> VehicleOwner:
        """Get existing owner or create a new one
        
        Extracts region information from plate number to generate owner from correct region.
        Handles both old and new plate formats.
        """
        if plate in self.owners:
            return self.owners[plate]
        
        # Parse plate to get region information
        plate_info = IndonesianPlateManager.parse_plate(plate)
        if plate_info:
            region = plate_info['region_name']
            sub_region = plate_info['sub_region']
        else:
            # Fallback: Try to extract region code from plate
            parts = plate.split()
            if parts and parts[0] in IndonesianPlateManager.PLATE_DATA:
                region_data = IndonesianPlateManager.PLATE_DATA[parts[0]]
                region = region_data['region_name']
                sub_region = region_data.get('area', region)
            else:
                region = 'Jakarta'  # Default fallback
                sub_region = 'DKI Jakarta'
        
        # Create new owner
        owner = VehicleOwner.generate_random_owner(region, sub_region, vehicle_type)
        self.owners[plate] = owner
        
        return owner
    
    def save_to_file(self, filepath: str) -> None:
        """Save database to JSON file"""
        data = {plate: owner.to_dict() for plate, owner in self.owners.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filepath: str) -> None:
        """Load database from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for plate, owner_data in data.items():
                vehicle_type = 'roda_dua' if 'Roda Dua' in owner_data.get('vehicle_type', '') else 'roda_empat'
                owner = VehicleOwner(
                    owner_id=owner_data['owner_id'],
                    name=owner_data['name'],
                    region=owner_data['region'],
                    sub_region=owner_data.get('sub_region', ''),
                    stnk_status=owner_data['stnk_status'] == 'Active',
                    sim_status=owner_data['sim_status'] == 'Active',
                    vehicle_type=vehicle_type
                )
                self.owners[plate] = owner
        except FileNotFoundError:
            pass


# Global database instance
owner_db = OwnerDatabase()
