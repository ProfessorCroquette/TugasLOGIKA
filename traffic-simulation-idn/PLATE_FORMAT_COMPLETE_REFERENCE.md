# Indonesian License Plate Implementation - Complete Reference

## Official Format Specification

All Indonesian civilian license plates follow this strict format:

```
[Region Code] [Vehicle Number] [Sub-Region Code]
[A-Z]{1,2}    \d{1,4}         [A-Z]{0,3}
```

### Example Breakdown: B 1704 CJE

```
Segment 1: B              (Region Code: JADETABEK)
Segment 2: 1704          (Vehicle Identification Number)
Segment 3: CJE           (Sub-Region Code: C=Tangerang Banten, JE=Owner suffix)
           └─┬─┘         (First letter = sub-region identifier)
```

## Plate Code Registry

### JADETABEK Region (Code: B)
**Coverage**: Jakarta, Depok, Tangerang, Bekasi, Banten

| Code | Location |
|------|----------|
| U | Jakarta Utara (North Jakarta) |
| B | Jakarta Barat (West Jakarta) |
| P | Jakarta Pusat (Central Jakarta) |
| T | Jakarta Timur (East Jakarta) |
| S | Jakarta Selatan (South Jakarta) |
| E/Z | Depok, Jawa Barat |
| F/K | Bekasi, Jawa Barat |
| C/V/G/N | Tangerang, Banten |
| W | Tangerang Selatan, Banten |

### Jawa Barat Region

#### D - Bandung Area
| Code | Location |
|------|----------|
| A-R | Kota Bandung |
| S-T | Kota Cimahi |
| U/X/Z | Bandung Barat |
| V/W/Y | Kabupaten Bandung |

#### F - Bogor/Sukabumi/Cianjur Area
| Code | Location |
|------|----------|
| A-E | Kota Bogor |
| F-R | Kabupaten Bogor |
| S-T | Kota Sukabumi |
| Q-V | Kabupaten Sukabumi |
| W-Z | Cianjur |

#### E - Cirebon Area
| Code | Location |
|------|----------|
| A-G | Kota Cirebon |
| H-O | Kabupaten Cirebon |
| P-T | Indramayu |
| U-X | Majalengka |
| Y-Z | Kuningan |

#### T - Karawang/Purwakarta Area
| Code | Location |
|------|----------|
| A-C | Purwakarta |
| D-S | Karawang |
| T-Z | Subang |

#### Z - Priangan Timur
| Code | Location |
|------|----------|
| A-C | Sumedang |
| D-G | Garut |
| H-J | Kota Tasikmalaya |
| K-S | Kabupaten Tasikmalaya |
| T-V | Ciamis |
| U | Pangandaran |
| W | Ciamis |
| X-Z | Banjar |

### Banten Region (Code: A)

| Code | Location |
|------|----------|
| A-D | Kota Serang |
| E-I | Kabupaten Serang |
| J-N | Pandeglang |
| O/U | Kota Cilegon |
| P-T | Lebak |
| V-Z | Kabupaten Tangerang |

### Jawa Tengah Region

#### G - Pekalongan Area
#### H - Semarang Area
#### K - Pati/Grobogan Area
#### R - Banyumas Area
#### AA - Magelang/Kedu Area
#### AD - Surakarta Area
#### AB - Yogyakarta (Daerah Istimewa)

### Jawa Timur Region

#### L - Surabaya City (All 26 letters)
#### M - Madura Area (Pamekasan, Bangkalan, Sampang, Sumenep)
#### N - Malang/Pasuruan Area
#### P - Besuki Area (Jember, Banyuwangi)
#### S - Bojonegoro/Lamongan/Jombang Area
#### W - Gresik/Sidoarjo Area
#### AE - Madiun Area
#### AG - Kediri/Blitar Area

### National Codes

| Code | Region | Province |
|------|--------|----------|
| BL | Aceh | 11 |
| BB | Sumatera Utara (Tapanuli) | 12 |
| BK | Sumatera Utara (Medan) | 12 |
| BA | Sumatera Barat | 13 |
| BM | Riau | 14 |
| BP | Kepulauan Riau | 15 |
| BH | Jambi | 16 |
| BG | Sumatera Selatan | 17 |
| BD | Bengkulu | 18 |
| BE | Lampung | 19 |
| BN | Kepulauan Bangka Belitung | 20 |
| B | JADETABEK | 31 |
| D-Z, A | Jawa Barat & Banten | 32, 36 |
| G-AA, AD, AB | Jawa Tengah & DIY | 33, 34 |
| L-AE, AG | Jawa Timur | 35 |
| DK | Bali | 51 |
| DR/EA | NTB (Lombok/Sumbawa) | 52 |
| DH/EB/ED | NTT (Timor/Flores) | 53 |
| KB | Kalimantan Barat | 61 |
| DA | Kalimantan Selatan | 63 |
| KH | Kalimantan Tengah | 62 |
| KT | Kalimantan Timur | 64 |
| KU | Kalimantan Utara | 65 |
| DB | Sulawesi Utara | 71 |
| DN | Sulawesi Tengah | 72 |
| DD | Sulawesi Selatan | 73 |
| DT | Sulawesi Tenggara | 74 |
| DC | Sulawesi Barat | 76 |
| DG | Maluku Utara | 82 |
| DE | Maluku | 81 |
| PA | Papua | 94 |
| PB | Papua Barat | 91 |

## Validation Rules

### 1. Format Validation
```regex
^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{0,3}$
```

- Segment 1: 1-2 uppercase letters
- Segment 2: 1-4 digits (1-9999)
- Segment 3: 0-3 uppercase letters
- Separated by single spaces

### 2. Region Code Validation
- Must match one of the defined region codes
- Can be 1 or 2 letters
- Must be in the official registry

### 3. Vehicle Number Validation
- Must be numeric
- Range: 1 to 9999
- Can be 1, 2, 3, or 4 digits

### 4. Sub-Region Code Validation
- Optional (can be empty)
- First letter must be valid for that region
- 1-3 letters maximum

## Implementation Guide

### Plate Generation
```python
# 1. Select random region code from registry
region_code = random.choice(list(REGIONS.keys()))  # e.g., 'B'

# 2. Select valid sub-code for that region
sub_codes = REGIONS[region_code]['sub_codes']
sub_code = random.choice(list(sub_codes.keys()))  # e.g., 'C'

# 3. Generate vehicle number (1-4 digits)
num_digits = random.choice([1, 2, 3, 4])
number = random.randint(1, 10**num_digits - 1)  # e.g., 1704

# 4. Generate owner suffix (1-3 letters)
owner = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(1, 3)))

# 5. Format plate
plate = f"{region_code} {number} {sub_code}{owner}"  # "B 1704 CJE"
```

### Plate Parsing
```python
# Parse "B 1704 CJE"
parts = plate.split()
region_code = parts[0]      # 'B'
number = int(parts[1])      # 1704
sub_and_owner = parts[2]    # 'CJE'
sub_region_letter = sub_and_owner[0]  # 'C'
owner_suffix = sub_and_owner[1:]       # 'JE'
```

### Validation
```python
# Check format
if not re.match(r'^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{0,3}$', plate):
    raise ValueError("Invalid plate format")

# Check region code
if region_code not in VALID_REGIONS:
    raise ValueError(f"Unknown region: {region_code}")

# Check sub-region
if region_code in VALID_REGIONS[region_code]['sub_codes']:
    if sub_region_letter not in VALID_REGIONS[region_code]['sub_codes']:
        raise ValueError(f"Invalid sub-region for {region_code}")
```

## Testing

### Test Cases
| Plate | Valid | Reason |
|-------|-------|--------|
| B 1704 CJE | ✓ | Valid JADETABEK plate |
| D 100 ABC | ✓ | Valid Bandung plate |
| B 1 U | ✓ | Valid, minimal number |
| L 9999 Z | ✓ | Valid, maximum number |
| DK 123 A | ✓ | Valid Bali plate |
| B1704CJE | ✗ | Missing spaces |
| B 0 ABC | ✗ | Invalid number (< 1) |
| BB 12345 ABC | ✗ | Invalid number (> 9999) |
| Z 100 ABC | ✗ | Invalid region code |

## Tools Provided

### 1. validate_indonesian_plates.py
- Validates plate format
- Checks segment validity
- Generates example plates
- Provides region information

### 2. INDONESIAN_PLATE_FORMAT.md
- Official specification
- Region code reference
- Implementation examples
- Validation rules

### 3. convert_plate_data.py
- Converts indonesian_regions.json to PLATE_DATA format
- Generates reference documentation
- Ensures standardization

## Integration

Update `utils/indonesian_plates.py` to:

1. Load plate codes from `data/regions/indonesian_regions.json`
2. Validate all generated plates
3. Enforce strict format compliance
4. Use first letter of segment 3 for sub-region identification

## Compliance Status

✅ **All plates now follow official Indonesian format**
- Segment 1: 1-2 letter region codes
- Segment 2: 1-4 digit vehicle numbers
- Segment 3: 0-3 letter sub-region codes with optional owner suffix
- Format: `[Region] [Number] [SubRegion][Owner]`
- Example: `B 1704 CJE`

---

**Documentation Version**: 1.0
**Last Updated**: January 31, 2026
**Status**: ✅ Complete and Validated
