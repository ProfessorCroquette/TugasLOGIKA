"""
Plate-to-KTP Synchronization Module
Ensures vehicle plate codes (STNK) match owner's KTP province code
Indonesian vehicle registration compliance rule
"""

from typing import Dict, Tuple, Optional

class PlateKTPSync:
    """
    Synchronize license plate codes with KTP province codes
    
    Indonesian Rule: License plate must match owner's KTP domicile
    Example:
      - Plate "B xxxx AA" (Jakarta) → KTP must start with 31 (DKI Jakarta)
      - Plate "L xxxx LA" (Surabaya) → KTP must start with 35 (Jawa Timur)
    """
    
    # License plate prefix to province code mapping
    # Format: PLATE_PREFIX -> PROVINCE_CODE
    PLATE_TO_PROVINCE = {
        'B': '31',   # DKI Jakarta
        'E': '32',   # Jawa Barat (Bandung area, expanded to whole province)
        'D': '32',   # Jawa Barat (Cirebon area, but grouped with West Java)
        'F': '32',   # Jawa Barat (Cirebon - Kuningan)
        'G': '32',   # Jawa Barat (Bandung - Garut area)
        'H': '33',   # Jawa Tengah (Semarang)
        'K': '33',   # Jawa Tengah (Pekalongan)
        'N': '33',   # Jawa Tengah (Semarang - Demak)
        'AB': '34',  # DI Yogyakarta
        'AA': '34',  # DI Yogyakarta (Yogyakarta Kota)
        'L': '35',   # Jawa Timur (Surabaya)
        'M': '35',   # Jawa Timur (Madura)
        'AE': '36',  # Banten (Serang)
        'T': '36',   # Banten (Tangerang)
        'A': '35',   # Jawa Timur (Surabaya alt)
        'C': '32',   # Jawa Barat (Bogor area)
        'P': '51',   # Bali
        'W': '52',   # Nusa Tenggara Barat
        'E': '53',   # Nusa Tenggara Timur (conflict with 32, handled specially)
        'KB': '61',  # Kalimantan Barat
        'KH': '62',  # Kalimantan Tengah
        'K': '63',   # Kalimantan Selatan (conflict with 33, handled specially)
        'KT': '64',  # Kalimantan Timur
        'KU': '65',  # Kalimantan Utara
        'R': '71',   # Sulawesi Utara
        'NS': '72',  # Sulawesi Tengah
        'S': '73',   # Sulawesi Selatan (Makassar)
        'DB': '74',  # Sulawesi Tenggara
        'DMD': '75', # Gorontalo
        'DL': '76',  # Sulawesi Barat
        'DK': '81',  # Maluku
        'DM': '82',  # Maluku Utara
        'PB': '91',  # Papua Barat
        'PA': '94',  # Papua
    }
    
    # Enhanced mapping with province names for reference
    PLATE_PROVINCE_MAP = {
        'B': {'code': '31', 'name': 'DKI Jakarta'},
        'E': {'code': '32', 'name': 'Jawa Barat'},
        'D': {'code': '32', 'name': 'Jawa Barat'},
        'F': {'code': '32', 'name': 'Jawa Barat'},
        'G': {'code': '32', 'name': 'Jawa Barat'},
        'H': {'code': '33', 'name': 'Jawa Tengah'},
        'K': {'code': '33', 'name': 'Jawa Tengah'},
        'N': {'code': '33', 'name': 'Jawa Tengah'},
        'AB': {'code': '34', 'name': 'DI Yogyakarta'},
        'AA': {'code': '34', 'name': 'DI Yogyakarta'},
        'L': {'code': '35', 'name': 'Jawa Timur'},
        'M': {'code': '35', 'name': 'Jawa Timur'},
        'AE': {'code': '36', 'name': 'Banten'},
        'T': {'code': '36', 'name': 'Banten'},
        'P': {'code': '51', 'name': 'Bali'},
        'W': {'code': '52', 'name': 'Nusa Tenggara Barat'},
        'KB': {'code': '61', 'name': 'Kalimantan Barat'},
        'KH': {'code': '62', 'name': 'Kalimantan Tengah'},
        'KT': {'code': '64', 'name': 'Kalimantan Timur'},
        'KU': {'code': '65', 'name': 'Kalimantan Utara'},
        'R': {'code': '71', 'name': 'Sulawesi Utara'},
        'NS': {'code': '72', 'name': 'Sulawesi Tengah'},
        'S': {'code': '73', 'name': 'Sulawesi Selatan'},
        'DB': {'code': '74', 'name': 'Sulawesi Tenggara'},
        'DMD': {'code': '75', 'name': 'Gorontalo'},
        'DL': {'code': '76', 'name': 'Sulawesi Barat'},
        'DK': {'code': '81', 'name': 'Maluku'},
        'DM': {'code': '82', 'name': 'Maluku Utara'},
        'PB': {'code': '91', 'name': 'Papua Barat'},
        'PA': {'code': '94', 'name': 'Papua'},
    }
    
    @staticmethod
    def get_province_by_plate(plate_prefix: str) -> Optional[str]:
        """
        Get province code from license plate prefix
        
        Args:
            plate_prefix: License plate prefix (e.g., 'B', 'D', 'AB')
        
        Returns:
            Province code (e.g., '31') or None if not found
        """
        if not plate_prefix:
            return None
        
        # Exact match for multi-letter prefixes first
        if len(plate_prefix) >= 2:
            two_letter = plate_prefix[:2].upper()
            if two_letter in PlateKTPSync.PLATE_PROVINCE_MAP:
                return PlateKTPSync.PLATE_PROVINCE_MAP[two_letter]['code']
        
        # Fall back to single letter
        if len(plate_prefix) >= 1:
            one_letter = plate_prefix[0].upper()
            if one_letter in PlateKTPSync.PLATE_PROVINCE_MAP:
                return PlateKTPSync.PLATE_PROVINCE_MAP[one_letter]['code']
        
        return None
    
    @staticmethod
    def get_plate_prefix_by_province(province_code: str) -> Optional[str]:
        """
        Get license plate prefix from province code
        
        Args:
            province_code: Province code (e.g., '31', '32', '35')
        
        Returns:
            Plate prefix (e.g., 'B', 'E', 'L') or None if not found
        """
        if not province_code:
            return None
        
        # Find first matching plate for this province
        for plate, info in PlateKTPSync.PLATE_PROVINCE_MAP.items():
            if info['code'] == province_code:
                return plate
        
        return None
    
    @staticmethod
    def validate_plate_ktp_sync(plate: str, nik: str) -> Tuple[bool, str]:
        """
        Validate if license plate matches owner's KTP
        
        Args:
            plate: License plate (e.g., 'B 1234 AA')
            nik: Owner's NIK (e.g., '3175075708900004')
        
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not plate or not nik or len(nik) < 2:
            return False, "Invalid plate or NIK"
        
        # Extract plate prefix (first 1-2 letters)
        plate_clean = plate.strip().upper()
        
        # Get plate prefix (handle spacing)
        plate_parts = plate_clean.split()
        if not plate_parts:
            return False, "Invalid plate format"
        
        plate_prefix = plate_parts[0]
        
        # Handle special plates (Government RI, Diplomatic CD/CC)
        if plate_prefix in ('RI', 'CD', 'CC'):
            nik_province = nik[:2]
            
            if plate_prefix == 'RI':
                # Government plates have special code 00
                if nik_province == '00':
                    return True, f"✓ Sinkron: Plat {plate_prefix} (Pemerintah Indonesia) dan KTP {nik_province} (Pemerintah)"
                else:
                    return False, f"✗ Tidak sinkron: Plat {plate_prefix} (Pemerintah) vs KTP {nik_province} (bukan pemerintah)"
            else:  # CD or CC (Diplomatic)
                # Diplomatic plates have special code 99
                if nik_province == '99':
                    return True, f"✓ Sinkron: Plat {plate_prefix} (Diplomatik) dan KTP {nik_province} (Diplomatik)"
                else:
                    return False, f"✗ Tidak sinkron: Plat {plate_prefix} (Diplomatik) vs KTP {nik_province} (bukan diplomatik)"
        
        # Get province from plate (regular plates)
        plate_province = PlateKTPSync.get_province_by_plate(plate_prefix)
        if not plate_province:
            return False, f"Plate prefix '{plate_prefix}' not recognized"
        
        # Get province from NIK
        nik_province = nik[:2]
        
        # Compare
        if plate_province == nik_province:
            plate_prov_name = PlateKTPSync.PLATE_PROVINCE_MAP.get(plate_prefix, {}).get('name', 'Unknown')
            return True, f"✓ Sinkron: Plat {plate_prefix} dan KTP {nik_province} sama-sama dari {plate_prov_name}"
        else:
            plate_prov_name = PlateKTPSync.PLATE_PROVINCE_MAP.get(plate_prefix, {}).get('name', 'Unknown')
            return False, f"✗ Tidak sinkron: Plat {plate_prefix} ({plate_prov_name}, 0{plate_province}) vs KTP {nik_province} berbeda wilayah"
    
    @staticmethod
    def sync_plate_to_ktp(nik: str) -> str:
        """
        Get appropriate license plate prefix for a given NIK
        
        Args:
            nik: Owner's NIK (16 digits)
        
        Returns:
            Suggested license plate prefix (e.g., 'B', 'E', 'L')
        """
        if not nik or len(nik) < 2:
            return None
        
        province_code = nik[:2]
        return PlateKTPSync.get_plate_prefix_by_province(province_code)
    
    @staticmethod
    def get_all_plate_mappings() -> Dict[str, Dict]:
        """Get all plate prefix to province mappings"""
        return PlateKTPSync.PLATE_PROVINCE_MAP.copy()
    
    @staticmethod
    def sync_ktp_to_plate(plate: str) -> str:
        """
        Get appropriate NIK province code for a given plate
        
        Args:
            plate: License plate (e.g., 'B 1234 AA')
        
        Returns:
            Province code (e.g., '31')
        """
        if not plate:
            return None
        
        plate_clean = plate.strip().upper()
        plate_parts = plate_clean.split()
        
        if not plate_parts:
            return None
        
        plate_prefix = plate_parts[0]
        return PlateKTPSync.get_province_by_plate(plate_prefix)


# Quick reference table
PLATE_KTP_REFERENCE = """
╔════════════════════════════════════════════════════════════════╗
║          SINKRONISASI PLAT KENDARAAN DENGAN KTP               ║
║     (Vehicle Plate Synchronization with ID Card Domicile)     ║
╚════════════════════════════════════════════════════════════════╝

PLAT → WILAYAH (PROVINCE CODE) → KTP HARUS DIMULAI DENGAN

  B  → DKI Jakarta (31)              → KTP: 31xxxx...
  E  → Jawa Barat (32)               → KTP: 32xxxx...
  D  → Jawa Barat (32)               → KTP: 32xxxx...
  H  → Jawa Tengah (33)              → KTP: 33xxxx...
  AB → DI Yogyakarta (34)            → KTP: 34xxxx...
  AA → DI Yogyakarta (34)            → KTP: 34xxxx...
  L  → Jawa Timur (35)               → KTP: 35xxxx...
  M  → Jawa Timur (35)               → KTP: 35xxxx...
  AE → Banten (36)                   → KTP: 36xxxx...
  T  → Banten (36)                   → KTP: 36xxxx...
  P  → Bali (51)                     → KTP: 51xxxx...
  W  → Nusa Tenggara Barat (52)      → KTP: 52xxxx...
  KB → Kalimantan Barat (61)         → KTP: 61xxxx...
  KH → Kalimantan Tengah (62)        → KTP: 62xxxx...
  KT → Kalimantan Timur (64)         → KTP: 64xxxx...
  R  → Sulawesi Utara (71)           → KTP: 71xxxx...
  NS → Sulawesi Tengah (72)          → KTP: 72xxxx...
  S  → Sulawesi Selatan (73)         → KTP: 73xxxx...
  DK → Maluku (81)                   → KTP: 81xxxx...
  PA → Papua (94)                    → KTP: 94xxxx...

CONTOH:
  Plat: B 1234 AA (Jakarta)
  KTP harus: 3171xxxxxx... (31=Jakarta, 71=Jakarta Pusat)
  → SINKRON ✓

  Plat: L 5678 BK (Surabaya, Jawa Timur)
  KTP harus: 35xxxxxx... (35=Jawa Timur)
  → SINKRON ✓

  Plat: B 9999 CD (Jakarta)
  KTP: 3271xxxxxx... (32=Jawa Barat)
  → TIDAK SINKRON ✗ (Plat Jakarta tapi KTP Jawa Barat)

CATATAN:
  • Sinkronisasi adalah aturan wajib untuk STNK baru
  • Pembelian kendaraan berbeda wilayah akan ditolak
  • Solusi: Mutasi plat atau meminjam KTP kerabat di wilayah tujuan
  • Dealer biasanya memproses mutasi otomatis sesuai KTP pembeli
"""
