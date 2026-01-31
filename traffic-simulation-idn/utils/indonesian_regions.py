"""
Indonesian Regions - Province, Kabupaten/Kota, and Kecamatan mappings
Generated from base.csv file
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

class IndonesianRegions:
    """Parse and manage Indonesian administrative regions"""
    
    _instance = None
    _data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndonesianRegions, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        """Load regions from base.csv"""
        if self._data is not None:
            return
        
        self._data = {
            'provinces': {},  # code -> name
            'kabupatens': {},  # code -> {'name': ..., 'province_code': ...}
            'kecamatan': {},   # code -> {'name': ..., 'kabupaten_code': ..., 'province_code': ...}
        }
        
        # Try to load from base.csv
        csv_path = Path(__file__).parent.parent / 'base.csv'
        
        if csv_path.exists():
            self._load_from_csv(csv_path)
        else:
            self._load_default_provinces()
    
    def _load_from_csv(self, csv_path):
        """Load data from base.csv"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    
                    code, name = row[0].strip(), row[1].strip() if len(row) > 1 else ''
                    parts = code.split('.')
                    
                    if len(parts) == 1:
                        # Province level: 11
                        self._data['provinces'][code] = name
                    
                    elif len(parts) == 2:
                        # Kabupaten/Kota level: 11.01
                        province_code = parts[0]
                        self._data['kabupatens'][code] = {
                            'name': name,
                            'province_code': province_code,
                            'province_name': self._data['provinces'].get(province_code, '')
                        }
                    
                    elif len(parts) == 3:
                        # Kecamatan level: 11.01.01
                        kabupaten_code = f"{parts[0]}.{parts[1]}"
                        province_code = parts[0]
                        
                        kabupaten_data = self._data['kabupatens'].get(kabupaten_code, {})
                        self._data['kecamatan'][code] = {
                            'name': name,
                            'kabupaten_code': kabupaten_code,
                            'province_code': province_code,
                            'kabupaten_name': kabupaten_data.get('name', ''),
                            'province_name': self._data['provinces'].get(province_code, '')
                        }
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self._load_default_provinces()
    
    def _load_default_provinces(self):
        """Load default province data if CSV not available"""
        provinces = {
            '11': 'Aceh', '12': 'Sumatera Utara', '13': 'Sumatera Barat',
            '14': 'Riau', '15': 'Jambi', '16': 'Sumatera Selatan',
            '17': 'Bengkulu', '18': 'Lampung', '19': 'Kepulauan Bangka Belitung',
            '21': 'Kepulauan Riau', '31': 'DKI Jakarta', '32': 'Jawa Barat',
            '33': 'Jawa Tengah', '34': 'DI Yogyakarta', '35': 'Jawa Timur',
            '36': 'Banten', '51': 'Bali', '52': 'Nusa Tenggara Barat',
            '53': 'Nusa Tenggara Timur', '61': 'Kalimantan Barat',
            '62': 'Kalimantan Tengah', '63': 'Kalimantan Selatan',
            '64': 'Kalimantan Timur', '65': 'Kalimantan Utara', '71': 'Sulawesi Utara',
            '72': 'Sulawesi Tengah', '73': 'Sulawesi Selatan', '74': 'Sulawesi Tenggara',
            '75': 'Gorontalo', '76': 'Sulawesi Barat', '81': 'Maluku',
            '82': 'Maluku Utara', '91': 'Papua Barat', '94': 'Papua'
        }
        
        for code, name in provinces.items():
            self._data['provinces'][code] = name
    
    def get_province(self, code: str) -> Optional[str]:
        """Get province name by code"""
        return self._data['provinces'].get(code)
    
    def get_kabupaten(self, code: str) -> Optional[Dict]:
        """Get kabupaten/kota info by code"""
        return self._data['kabupatens'].get(code)
    
    def get_kecamatan(self, code: str) -> Optional[Dict]:
        """Get kecamatan info by code"""
        return self._data['kecamatan'].get(code)
    
    def get_all_provinces(self) -> Dict[str, str]:
        """Get all provinces"""
        return self._data['provinces'].copy()
    
    def get_all_kabupatens(self) -> Dict[str, Dict]:
        """Get all kabupaten/kota"""
        return self._data['kabupatens'].copy()
    
    def get_kabupatens_by_province(self, province_code: str) -> Dict[str, str]:
        """Get all kabupaten/kota in a province"""
        result = {}
        for code, data in self._data['kabupatens'].items():
            if data['province_code'] == province_code:
                result[code] = data['name']
        return result
    
    def get_kecamatan_by_kabupaten(self, kabupaten_code: str) -> Dict[str, str]:
        """Get all kecamatan in a kabupaten"""
        result = {}
        for code, data in self._data['kecamatan'].items():
            if data['kabupaten_code'] == kabupaten_code:
                result[code] = data['name']
        return result


class NIKParser:
    """Enhanced NIK parser using actual Indonesian region codes"""
    
    REGIONS = IndonesianRegions()
    
    # Fallback province codes mapping
    PROVINCE_CODES = {
        '11': 'Aceh', '12': 'Sumatera Utara', '13': 'Sumatera Barat',
        '14': 'Riau', '15': 'Jambi', '16': 'Sumatera Selatan',
        '17': 'Bengkulu', '18': 'Lampung', '19': 'Kepulauan Bangka Belitung',
        '21': 'Kepulauan Riau', '31': 'DKI Jakarta', '32': 'Jawa Barat',
        '33': 'Jawa Tengah', '34': 'DI Yogyakarta', '35': 'Jawa Timur',
        '36': 'Banten', '51': 'Bali', '52': 'Nusa Tenggara Barat',
        '53': 'Nusa Tenggara Timur', '61': 'Kalimantan Barat',
        '62': 'Kalimantan Tengah', '63': 'Kalimantan Selatan',
        '64': 'Kalimantan Timur', '65': 'Kalimantan Utara', '71': 'Sulawesi Utara',
        '72': 'Sulawesi Tengah', '73': 'Sulawesi Selatan', '74': 'Sulawesi Tenggara',
        '75': 'Gorontalo', '76': 'Sulawesi Barat', '81': 'Maluku',
        '82': 'Maluku Utara', '91': 'Papua Barat', '94': 'Papua'
    }
    
    MONTH_NAMES = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    
    @staticmethod
    def parse_nik(nik: str) -> Optional[Dict]:
        """
        Parse NIK into components
        Format: AA BB CC DD MM YY ZZZZ
        AA: Province code
        BB: Kabupaten/Kota code
        CC: Kecamatan code
        DD: Day of birth (female += 40)
        MM: Month of birth
        YY: Year of birth (last 2 digits)
        ZZZZ: Sequential registration number
        """
        
        if not nik or len(nik) != 16 or not nik.isdigit():
            return None
        
        try:
            # Extract components
            province_code = nik[0:2]
            kabupaten_code = nik[2:4]
            kecamatan_code = nik[4:6]
            day_raw = int(nik[6:8])
            month = int(nik[8:10])
            year_short = int(nik[10:12])
            sequential = nik[12:16]
            
            # Determine gender from day field
            is_female = day_raw > 40
            day = day_raw - 40 if is_female else day_raw
            
            # Convert 2-digit year to 4-digit
            if year_short <= 28:
                year = 2000 + year_short
            else:
                year = 1900 + year_short
            
            # Get region information
            province_code_str = province_code
            full_kabupaten_code = f"{province_code}.{kabupaten_code}"
            full_kecamatan_code = f"{province_code}.{kabupaten_code}.{kecamatan_code}"
            
            province_name = NIKParser.REGIONS.get_province(province_code_str)
            if not province_name:
                province_name = NIKParser.PROVINCE_CODES.get(province_code_str, 'Unknown')
            
            kabupaten_data = NIKParser.REGIONS.get_kabupaten(full_kabupaten_code)
            kabupaten_name = kabupaten_data['name'] if kabupaten_data else f"Kabupaten/Kota {kabupaten_code}"
            
            kecamatan_data = NIKParser.REGIONS.get_kecamatan(full_kecamatan_code)
            kecamatan_name = kecamatan_data['name'] if kecamatan_data else f"Kecamatan {kecamatan_code}"
            
            # Validate month
            if month < 1 or month > 12:
                return None
            
            # Validate day
            if day < 1 or day > 31:
                return None
            
            month_name = NIKParser.MONTH_NAMES.get(month, f"Month {month}")
            
            # Calculate age
            from datetime import datetime
            current_year = datetime.now().year
            age = current_year - year
            
            return {
                'nik': nik,
                'nik_formatted': f"{province_code} {kabupaten_code} {kecamatan_code} {nik[6:8]} {nik[8:10]} {nik[10:12]} {sequential}",
                'province_code': province_code_str,
                'province_name': province_name,
                'kabupaten_code': kabupaten_code,
                'kabupaten_name': kabupaten_name,
                'kecamatan_code': kecamatan_code,
                'kecamatan_name': kecamatan_name,
                'birth_day': day,
                'birth_month': month,
                'birth_month_name': month_name,
                'birth_year': year,
                'birth_date': f"{day:02d} {month_name} {year}",
                'day_raw': day_raw,
                'gender': 'Perempuan' if is_female else 'Laki-laki',
                'is_female': is_female,
                'sequential_number': sequential,
                'age': age
            }
        
        except (ValueError, IndexError):
            return None
    
    @staticmethod
    def get_readable_nik_info(nik: str) -> Optional[str]:
        """Get formatted readable NIK information"""
        data = NIKParser.parse_nik(nik)
        if not data:
            return None
        
        info = f"""
NIK: {data['nik_formatted']}

LOKASI ADMINISTRASI:
  Provinsi: {data['province_code']} - {data['province_name']}
  Kabupaten/Kota: {data['kabupaten_code']} - {data['kabupaten_name']}
  Kecamatan: {data['kecamatan_code']} - {data['kecamatan_name']}

DATA PRIBADI:
  Tanggal Lahir: {data['birth_date']}
  Jenis Kelamin: {data['gender']}
  Usia: {data['age']} tahun
  
NOMOR REGISTRASI:
  Nomor Urut: {data['sequential_number']}
"""
        return info
    
    @staticmethod
    def get_summary_nik_info(nik: str) -> Optional[Dict]:
        """Get summary of NIK information"""
        return NIKParser.parse_nik(nik)


# Make it singleton
_instance = IndonesianRegions()
