#!/usr/bin/env python3
"""
Quick Reference: Indonesian License Plate Format

Format: [Region] [Number] [SubRegion+Owner]
Example: B 1704 CJE

This file serves as a quick lookup guide
"""

# ============================================================================
# OFFICIAL FORMAT
# ============================================================================

OFFICIAL_FORMAT = """
SEGMENT 1: Region Code
  Pattern: [A-Z]{1,2}     (1-2 uppercase letters)
  Example: B, D, DK, KB
  
SEGMENT 2: Vehicle Number
  Pattern: \d{1,4}        (1-4 digits)
  Range:   1 to 9999
  Example: 1, 100, 1704
  
SEGMENT 3: Sub-Region + Owner
  Pattern: [A-Z]{0,3}     (0-3 uppercase letters)
  Format:  [SubLetter][Owner]
  Example: C (sub only), CJE (sub + owner), empty
  
COMPLETE PLATE REGEX: ^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{0,3}$
"""

# ============================================================================
# QUICK REGION CODE REFERENCE
# ============================================================================

QUICK_REGIONS = {
    # JADETABEK Area
    'B': 'JADETABEK (Jakarta, Depok, Tangerang, Bekasi, Banten)',
    
    # Jawa Barat
    'D': 'Jawa Barat - Bandung Area',
    'F': 'Jawa Barat - Bogor/Sukabumi Area',
    'E': 'Jawa Barat - Cirebon Area',
    'T': 'Jawa Barat - Karawang Area',
    'Z': 'Jawa Barat - Priangan Timur',
    'A': 'Banten',
    
    # Jawa Tengah
    'G': 'Jawa Tengah - Pekalongan Area',
    'H': 'Jawa Tengah - Semarang Area',
    'K': 'Jawa Tengah - Pati/Grobogan Area',
    'R': 'Jawa Tengah - Banyumas Area',
    'AA': 'Jawa Tengah - Magelang/Kedu Area',
    'AD': 'Jawa Tengah - Surakarta Area',
    'AB': 'DIY Yogyakarta',
    
    # Jawa Timur
    'L': 'Jawa Timur - Surabaya City',
    'M': 'Jawa Timur - Madura',
    'N': 'Jawa Timur - Malang/Pasuruan',
    'P': 'Jawa Timur - Besuki (Jember, Banyuwangi)',
    'S': 'Jawa Timur - Bojonegoro/Lamongan',
    'W': 'Jawa Timur - Gresik/Sidoarjo',
    'AE': 'Jawa Timur - Madiun Area',
    'AG': 'Jawa Timur - Kediri Area',
    
    # Bali & NTT
    'DK': 'Bali',
    'DR': 'NTB - Lombok',
    'EA': 'NTB - Sumbawa',
    'DH': 'NTT - Timor',
    'EB': 'NTT - Flores',
    'ED': 'NTT - Sumba',
    
    # Kalimantan
    'KB': 'Kalimantan Barat',
    'DA': 'Kalimantan Selatan',
    'KH': 'Kalimantan Tengah',
    'KT': 'Kalimantan Timur',
    'KU': 'Kalimantan Utara',
    
    # Sulawesi
    'DB': 'Sulawesi Utara',
    'DN': 'Sulawesi Tengah',
    'DD': 'Sulawesi Selatan',
    'DT': 'Sulawesi Tenggara',
    'DC': 'Sulawesi Barat',
    'DG': 'Maluku Utara',
    'DE': 'Maluku',
    
    # Papua
    'PA': 'Papua',
    'PB': 'Papua Barat',
    
    # Sumatera
    'BL': 'Aceh',
    'BB': 'Sumatera Utara - Tapanuli',
    'BK': 'Sumatera Utara - Medan',
    'BA': 'Sumatera Barat',
    'BM': 'Riau',
    'BP': 'Kepulauan Riau',
    'BH': 'Jambi',
    'BG': 'Sumatera Selatan',
    'BD': 'Bengkulu',
    'BE': 'Lampung',
    'BN': 'Kepulauan Bangka Belitung',
}

# ============================================================================
# JADETABEK SUB-REGION CODES (Most Common)
# ============================================================================

JADETABEK_CODES = {
    'U': 'Jakarta Utara',
    'B': 'Jakarta Barat',
    'P': 'Jakarta Pusat',
    'T': 'Jakarta Timur',
    'S': 'Jakarta Selatan',
    'E': 'Depok, Jawa Barat',
    'Z': 'Depok, Jawa Barat',
    'F': 'Bekasi, Jawa Barat',
    'K': 'Bekasi, Jawa Barat',
    'C': 'Tangerang, Banten',
    'V': 'Tangerang, Banten',
    'G': 'Tangerang, Banten',
    'N': 'Tangerang, Banten',
    'W': 'Tangerang Selatan, Banten',
}

# ============================================================================
# VALIDATION RULES
# ============================================================================

VALIDATION_RULES = """
1. FORMAT VALIDATION
   - Must match regex: ^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{0,3}$
   - Single space between segments
   - No special characters
   - Uppercase letters only

2. REGION CODE VALIDATION
   - Must be in official registry (33 codes total)
   - Can be 1 or 2 letters
   - Valid examples: B, D, DK, KB, BK

3. VEHICLE NUMBER VALIDATION
   - Must be numeric (0-9 only)
   - Range: 1 to 9999
   - Can be 1, 2, 3, or 4 digits
   - Leading zeros optional for display

4. SUB-REGION VALIDATION
   - Optional (can be 0 letters)
   - Maximum 3 letters
   - First letter must be valid for that region
   - All uppercase

5. EXAMPLES OF VALID PLATES
   B 1704 CJE       ✓ Full format with owner code
   B 1 U            ✓ Minimal format
   D 100 ABC        ✓ Jawa Barat plate
   L 9999 Z         ✓ Surabaya (maximum number)
   DK 123 A         ✓ Bali plate

6. EXAMPLES OF INVALID PLATES
   B1704CJE         ✗ Missing spaces
   B 1704           ✗ Missing sub-region
   B 0 ABC          ✗ Number too small (must be >= 1)
   BB 12345 ABC     ✗ Number too large (max 9999)
   2 100 ABC        ✗ Invalid region (digit in code)
   B ABC 100        ✗ Wrong segment order
"""

# ============================================================================
# COMMON PATTERNS
# ============================================================================

PATTERNS = {
    'Motorcycle (Motor)': {
        'format': '[Region] [1-4 digits] [SubCode][1-2 owner letters]',
        'example': 'B 1234 UAB',
        'notes': 'Typically 1-2 digit numbers and 1-2 letter owner codes',
    },
    'Car (Mobil)': {
        'format': '[Region] [1-4 digits] [SubCode][2-3 owner letters]',
        'example': 'B 5678 PABC',
        'notes': 'Typically higher numbers and 2-3 letter owner codes',
    },
    'Minimal': {
        'format': '[Region] [1 digit] [SubCode]',
        'example': 'B 1 U',
        'notes': 'Rare but valid - single digit vehicles',
    },
    'Maximum': {
        'format': '[Region] [4 digits] [SubCode][3 owner letters]',
        'example': 'L 9999 ZABC',
        'notes': 'Maximum allowed digits and letters',
    },
}

# ============================================================================
# QUICK LOOKUP
# ============================================================================

def get_region_name(code):
    """Get region name from code"""
    return QUICK_REGIONS.get(code, 'Unknown Region')

def is_valid_region_code(code):
    """Check if region code is valid"""
    return code in QUICK_REGIONS

def is_valid_number(num):
    """Check if vehicle number is valid"""
    try:
        n = int(num)
        return 1 <= n <= 9999
    except:
        return False

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("INDONESIAN LICENSE PLATE FORMAT - QUICK REFERENCE")
    print("=" * 70)
    print()
    
    print("OFFICIAL FORMAT:")
    print(OFFICIAL_FORMAT)
    print()
    
    print("VALIDATION RULES:")
    print(VALIDATION_RULES)
    print()
    
    print("JADETABEK SUB-REGION CODES (Region B):")
    for code, name in sorted(JADETABEK_CODES.items()):
        print(f"  {code}: {name}")
    print()
    
    print("QUICK REGION LOOKUP:")
    for code in ['B', 'D', 'DK', 'KB', 'L', 'AE']:
        print(f"  {code}: {get_region_name(code)}")
    print()
    
    print("COMMON PATTERNS:")
    for pattern_type, details in PATTERNS.items():
        print(f"  {pattern_type}:")
        print(f"    Format: {details['format']}")
        print(f"    Example: {details['example']}")
        print(f"    Notes: {details['notes']}")
        print()

print("\n✅ Indonesian Plate Format Quick Reference Ready")
print("   Use validate_indonesian_plates.py for full validation")
print("   See INDONESIAN_PLATE_FORMAT.md for complete documentation")
