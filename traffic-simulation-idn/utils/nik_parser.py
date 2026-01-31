"""
Indonesian NIK (Nomor Induk Kependudukan) Parser and Decoder
Provides functions to parse and display readable NIK information
Based on Indonesian national ID format specifications
"""

from typing import Dict, Optional

# Indonesian Province Codes (1-34)
PROVINCE_CODES = {
    1: "Aceh", 2: "Sumatera Utara", 3: "Sumatera Barat", 4: "Riau",
    5: "Jambi", 6: "Sumatera Selatan", 7: "Bengkulu", 8: "Lampung",
    9: "Kepulauan Bangka Belitung", 10: "Kepulauan Riau",
    11: "DKI Jakarta", 12: "Jawa Barat", 13: "Jawa Tengah",
    14: "D.I. Yogyakarta", 15: "Jawa Timur", 16: "Banten",
    17: "Bali", 18: "Nusa Tenggara Barat", 19: "Nusa Tenggara Timur",
    20: "Kalimantan Barat", 21: "Kalimantan Tengah", 22: "Kalimantan Selatan",
    23: "Kalimantan Timur", 24: "Kalimantan Utara",
    25: "Sulawesi Utara", 26: "Sulawesi Tengah", 27: "Sulawesi Selatan",
    28: "Sulawesi Tenggara", 29: "Gorontalo", 30: "Sulawesi Barat",
    31: "Maluku", 32: "Maluku Utara", 33: "Papua Barat",
    34: "Papua"
}


class NIKParser:
    """Parser for Indonesian NIK (Nomor Induk Kependudukan)"""
    
    @staticmethod
    def parse_nik(nik: str) -> Optional[Dict]:
        """
        Parse NIK into its components
        
        NIK Format: AA BB CC DD MM YY ZZZZ (16 digits)
        Where:
            AA = Province code (01-34)
            BB = District/City code (01-99)
            CC = Subdistrict code (01-99)
            DD = Birth day (01-31 for males, 41-71 for females)
            MM = Birth month (01-12)
            YY = Birth year (last 2 digits, 00-99)
            ZZZZ = Sequential number (0001-9999)
        
        Args:
            nik: NIK string (16 digits)
            
        Returns:
            Dictionary with parsed components or None if invalid
        """
        # Validate format
        if not nik or len(nik) != 16:
            return None
        
        if not nik.isdigit():
            return None
        
        try:
            # Extract components
            province_code = int(nik[0:2])
            district_code = int(nik[2:4])
            subdistrict_code = int(nik[4:6])
            birth_day_code = int(nik[6:8])
            birth_month = int(nik[8:10])
            birth_year = int(nik[10:12])
            sequential = int(nik[12:16])
            
            # Determine gender and actual birth day
            is_female = birth_day_code > 40
            if is_female:
                actual_birth_day = birth_day_code - 40
            else:
                actual_birth_day = birth_day_code
            
            # Get province name
            province_name = PROVINCE_CODES.get(province_code, "Unknown Province")
            
            # Convert 2-digit year to 4-digit year
            # Assume 00-99 maps to 1900-1999 for older records, 2000-2099 for newer
            if birth_year <= 30:
                full_year = 2000 + birth_year
            else:
                full_year = 1900 + birth_year
            
            # Format birth date
            birth_date_str = f"{actual_birth_day:02d}-{birth_month:02d}-{full_year}"
            
            # Get month name
            month_names = {
                1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
                5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
                9: "September", 10: "Oktober", 11: "November", 12: "Desember"
            }
            month_name = month_names.get(birth_month, f"Bulan {birth_month} (Invalid)")
            
            # Validate month
            if birth_month < 1 or birth_month > 12:
                month_name = f"Invalid Month ({birth_month})"
            
            return {
                'nik': nik,
                'nik_formatted': f"{nik[0:2]} {nik[2:4]} {nik[4:6]} {nik[6:8]} {nik[8:10]} {nik[10:12]} {nik[12:16]}",
                'province_code': f"{province_code:02d}",
                'province_name': province_name,
                'district_code': f"{district_code:02d}",
                'subdistrict_code': f"{subdistrict_code:02d}",
                'birth_day': actual_birth_day,
                'birth_month': birth_month,
                'birth_month_name': month_name,
                'birth_year': full_year,
                'birth_date': birth_date_str,
                'gender': 'Perempuan (Female)' if is_female else 'Laki-laki (Male)',
                'is_female': is_female,
                'sequential_number': sequential
            }
        
        except (ValueError, IndexError):
            return None
    
    @staticmethod
    def get_readable_nik_info(nik: str) -> str:
        """
        Get a readable text description of NIK information
        
        Args:
            nik: NIK string (16 digits)
            
        Returns:
            Formatted text description
        """
        parsed = NIKParser.parse_nik(nik)
        
        if not parsed:
            return f"NIK: {nik}\nFormat: Invalid"
        
        # Format as readable text
        info = f"""
NIK (Nomor Induk Kependudukan): {parsed['nik']}
Format: {parsed['nik_formatted']}

IDENTITAS PEMILIK:
  Province: {parsed['province_code']} - {parsed['province_name']}
  District: {parsed['district_code']}
  Subdistrict: {parsed['subdistrict_code']}

TANGGAL LAHIR (Birth Date):
  Tanggal: {parsed['birth_day']} {parsed['birth_month_name']} {parsed['birth_year']}
  Format: {parsed['birth_date']}
  Jenis Kelamin (Gender): {parsed['gender']}

NOMOR URUT PENDAFTARAN (Sequential):
  Nomor: {parsed['sequential_number']:04d}
"""
        return info
    
    @staticmethod
    def get_summary_nik_info(nik: str) -> Dict[str, str]:
        """
        Get summary of NIK information for GUI display
        
        Args:
            nik: NIK string (16 digits)
            
        Returns:
            Dictionary with display-ready information
        """
        parsed = NIKParser.parse_nik(nik)
        
        if not parsed:
            return {
                'nik': nik,
                'province': 'Unknown',
                'gender': 'Unknown',
                'birth_date': 'Unknown',
                'age_category': 'Unknown'
            }
        
        return {
            'nik': parsed['nik_formatted'],
            'province': parsed['province_name'],
            'gender': 'Perempuan' if parsed['is_female'] else 'Laki-laki',
            'birth_date': parsed['birth_date'],
            'age_category': NIKParser.get_age_category(parsed['birth_year']),
            'sequential': f"Pendaftar ke-{parsed['sequential_number']:04d}"
        }
    
    @staticmethod
    def get_age_category(birth_year: int) -> str:
        """
        Get age category based on birth year
        
        Args:
            birth_year: Birth year (4 digits)
            
        Returns:
            Age category string
        """
        from datetime import datetime
        current_year = datetime.now().year
        age = current_year - birth_year
        
        if age < 18:
            return f"{age} tahun (Anak-anak)"
        elif age < 30:
            return f"{age} tahun (Muda)"
        elif age < 45:
            return f"{age} tahun (Dewasa Muda)"
        elif age < 60:
            return f"{age} tahun (Dewasa)"
        else:
            return f"{age} tahun (Senior)"


if __name__ == "__main__":
    # Example usage
    test_niks = [
        "3275075708900004",  # Example from user request
        "0857519332844595",  # Female example
        "1234567890123456"   # Random example
    ]
    
    for nik in test_niks:
        print(NIKParser.get_readable_nik_info(nik))
        print("-" * 60)
