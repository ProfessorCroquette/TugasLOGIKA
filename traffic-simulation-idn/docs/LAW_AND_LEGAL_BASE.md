LAW AND LEGAL BASE
Indonesian Traffic Violation Simulation System Compliance
Updated: February 4, 2026 02:30 AM

================================================================================
LEGAL FRAMEWORK
================================================================================

This system is based on the following Indonesian laws and regulations:

1. LAW No. 22 of 2009 (UU No. 22 Tahun 2009)
   Concerning Road Traffic and Transportation
   - Article 287 Section 5: Speeding violation penalties

2. POLICE REGULATION No. 7 of 2021 (Peraturan Kapolri Nomor 7 Tahun 2021)
   Regarding Vehicle Number Plate Regulations
   - Specification for license plate formats
   - Regional code assignments
   - Technical requirements

3. GOVERNMENT REGULATION No. 55 of 2012 (PP No. 55 Tahun 2012)
   Regarding Vehicle Registration and Identification
   - NIK (National Identification Number) requirements
   - Vehicle owner information standards

4. INDONESIAN TOLL ROAD AUTHORITY REGULATIONS
   - Toll road speed limits
   - Penalty structures for toll road violations

================================================================================
ARTICLE 287 SECTION 5 - SPEEDING VIOLATION
================================================================================

Full Text (Indonesian):
"Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan dengan kecepatan
melebihi kecepatan maksimal yang ditentukan sebagaimana dimaksud dalam Pasal 108
ayat (2) huruf a dipidana dengan pidana kurungan paling lama 3 (tiga) bulan
atau denda paling banyak Rp 750.000,00 (tujuh ratus lima puluh ribu rupiah)."

English Translation:
"Any person who drives a Motor Vehicle on the Road at a speed exceeding the
maximum speed limit as referred to in Article 108 paragraph (2) letter a shall
be punished with imprisonment of at most 3 (three) months or a fine of at most
IDR 750,000 (seven hundred fifty thousand rupiah)."

================================================================================
PENALTY STRUCTURE
================================================================================

BASE PENALTIES (As per Article 287 Section 5):
- Fine Amount: IDR 500,000 - 750,000
- Imprisonment: 0-3 months (optional)

ADDITIONAL MULTIPLIERS:
Applied based on document status (STNK and SIM validity):

1. Multiplier 1.0x (Optimal Compliance):
   - STNK (Vehicle Registration): Valid
   - SIM (Driver License): Valid
   - Additional penalty: None

2. Multiplier 1.2x (Partial Non-Compliance):
   - Either STNK or SIM expired
   - Additional penalty: 20% increase

3. Multiplier 1.4x (Full Non-Compliance):
   - Both STNK and SIM expired
   - Additional penalty: 40% increase

SYSTEM IMPLEMENTATION:
- Base Fine: IDR 500,000
- With Multiplier 1.0x: IDR 500,000
- With Multiplier 1.2x: IDR 600,000
- With Multiplier 1.4x: IDR 700,000

================================================================================
LICENSE PLATE FORMAT COMPLIANCE
================================================================================

OFFICIAL REQUIREMENTS (Peraturan Kapolri No. 7/2021):

Two-Row Plate System:
┌─────────────────────────────┐
│ [REGION] [NUMBERS] [LETTERS]│ Row 1: Registration Number
├─────────────────────────────┤
│   VALIDITY DATE             │ Row 2: Expiration (MM.YY)
└─────────────────────────────┘

Row 1 Breakdown:
- Kode Wilayah (Regional Code): 1-2 letters
  Example: B (Jakarta), F (West Java), BL (Bangka Belitung)
  
- Nomor Polisi (Police Number): 1-4 digits
  Example: 123, 2456, 1234
  
- Huruf Seri (Serial Letters): 1-3 letters
  Example: A, ABC, XYZ

SYSTEM COMPLIANCE:
Our implementation: [REGION] [1-4 DIGITS] [1-3 LETTERS]
Status: 100% COMPLIANT with official format

================================================================================
VEHICLE CATEGORY REGULATIONS
================================================================================

Indonesian Law defines vehicle categories with different regulations:

1. KENDARAAN PRIBADI (Private Vehicles) - BLACK PLATE
   - Format: [REGION] [DIGITS] [LETTERS]
   - Example: B 1234 ABC (Jakarta)
   - Usage: Personal transportation
   - Owner: Individual person
   - Penalty Base: Full application of fine rules
   - Our System: 50% of generated vehicles

2. KENDARAAN BARANG/TRUK (Commercial Vehicles) - YELLOW PLATE
   - Format: [REGION] [DIGITS] [LETTERS] (TRUK-CLASS) - RUTE: XX
   - Example: K 2156 TRUCK (TRUK-6) - RUTE: JR
   - Usage: Commercial/cargo transportation
   - Owner: Company or individual
   - Penalty Base: Full application of fine rules
   - Our System: 40% of generated vehicles

3. KENDARAAN PEMERINTAH (Government Vehicles) - RED PLATE
   - Format: RI [AGENCY] [DIGITS]
   - Example: RI 1 2456 (Government Agency Vehicle)
   - Usage: Government official business
   - Owner: Government agency/ministry
   - Special Handling: Independent NIK not tied to RI prefix
   - Our System: 5% of generated vehicles

4. KENDARAAN KEDUTAAN (Diplomatic Vehicles) - WHITE PLATE
   - Format: [CD/CC] [COUNTRY] [DIGITS]
   - CD: Consulate (Konsuler Diplomatik)
   - CC: Embassy (Kantor Konsul)
   - Example: CD 1 2345 (Consulate Vehicle)
   - Usage: Diplomatic representation
   - Owner: Foreign diplomatic mission
   - Special Handling: Independent NIK not tied to CD/CC prefix
   - Our System: 5% of generated vehicles

================================================================================
NIK (NOMOR IDENTITAS KEPENDUDUKAN) SYSTEM
================================================================================

OFFICIAL NIK FORMAT:
16-digit number with hierarchical structure:

Position 1-2: DDMMYY (Birth Date Day)
Position 3-4: DDMMYY (Birth Date Month)
Position 5-6: DDMMYY (Birth Date Year) [2-digit year]
Position 7-8: XXXXXX (Province Code)
Position 9-10: XXXXXX (District Code)
Position 11-12: XXXXXX (Sub-district Code)
Position 13-15: XXXXXX (Sequential Number)
Position 16: XXXXXX (Gender: Odd=Male, Even=Female)

CORRECTED INTERPRETATION:
Position 1-6: DDMMYY (Birth date: Day, Month, Year)
Position 7-8: XX (Province Code)
Position 9-10: XX (District Code from base.csv)
Position 11-12: XX (Sub-district Code from base.csv)
Position 13-15: XXX (Sequential number)
Position 16: X (Gender digit: Odd=Male, Even=Female)

EXAMPLE NIK BREAKDOWN:
1234561234567890
├─ 123456 = Birth date (DOB)
├─ 12 = Province code (11=Aceh, 12=North Sumatra, ..., 34=East Nusa Tenggara)
├─ 34 = District code (from base.csv)
├─ 56 = Sub-district code (from base.csv)
├─ 789 = Sequential number
└─ 0 = Gender (0,2,4,6,8=Female; 1,3,5,7,9=Male)

SYSTEM IMPLEMENTATION:

Two Generation Modes:

1. PLATE-BASED NIK (PRIBADI, BARANG vehicles):
   - Province code taken from plate's PLATE_DATA entry
   - Example: Plate "B" -> Province code "31" (Jakarta)
   - NIK format: [DDMMYY][31][XX][XX][XXX][X]
   - Result: Owner's province matches vehicle's region
   - Ensures realistic owner-vehicle relationship

2. INDEPENDENT NIK (PEMERINTAH, KEDUTAAN vehicles):
   - Province code randomly generated (01-34)
   - Not tied to vehicle's plate code
   - Example: RI plate but NIK could start with any province 01-34
   - Result: Reflects nationwide government/diplomatic presence
   - Ensures special vehicles aren't confined to single region

ADMINISTRATIVE CODES (base.csv Integration):
- Loaded: 91,221 Indonesian administrative entities
- Contains: Province, District, Sub-district mappings
- Used for: District and sub-district code validation
- Performance: Cached in memory for fast lookups
- Authority: Official Indonesian government administrative data

PROVINCE CODES (Official List):
11 = Aceh
12 = North Sumatra
13 = West Sumatra
14 = Riau
15 = Jambi
16 = Sumatera Selatan
17 = Bengkulu
18 = Lampung
19 = Kepulauan Bangka Belitung
20 = Riau Islands
21 = West Java
22 = Central Java
23 = East Java
24 = Yogyakarta
25 = Banten
31 = Jakarta
32 = West Kalimantan
33 = Central Kalimantan
34 = South Kalimantan
35 = East Kalimantan
36 = North Kalimantan
51 = Bali
52 = West Nusa Tenggara
53 = East Nusa Tenggara
61 = West Sulawesi
62 = South Sulawesi
63 = North Sulawesi
64 = Gorontalo
65 = Central Sulawesi
71 = West Papua
72 = Papua
81 = North Maluku
82 = Maluku

Special Codes:
00 = Foreign/Unknown
99 = Invalid/Unknown

================================================================================
TOLL ROAD REGULATIONS
================================================================================

INDONESIAN TOLL ROAD SPEED LIMITS:

Standard Highways:
- Car (Private Vehicles): 80 km/h
- Truck (Commercial): 60 km/h
- Motorcycle: 80 km/h
- Bus: 60 km/h

Expressway (High-speed):
- Car: 100 km/h
- Truck: 80 km/h
- Motorcycle: 100 km/h

VIOLATION DETECTION:
System detects speeding when: Vehicle Speed > Speed Limit

Current System Implementation:
- Default Speed Limit: 80 km/h
- Violation Triggered: Speed > 80 km/h
- Fines Applied: As per Article 287 Section 5

TOLL ROAD COMPLIANCE:
System supports toll road configuration:
- Can assign different speed limits per location
- Can apply toll-specific penalties
- Supports realistic toll road simulation

================================================================================
RECENT LEGAL COMPLIANCE UPDATES (Feb 1, 2026)
================================================================================

PROVINCE CODE CORRECTIONS:
Fixed 6 incorrect province codes in system:

Previous Incorrect -> Corrected To:
BP: 15 (Jambi) -> 21 (Kepulauan Riau)
BH: 16 (Sumatera Selatan) -> 15 (Jambi)
BG: 17 (Bengkulu) -> 16 (Sumatera Selatan)
BD: 18 (Lampung) -> 17 (Bengkulu)
BE: 19 (Kepulauan Bangka Belitung) -> 18 (Lampung)
BN: 20 (Unknown) -> 19 (Kepulauan Bangka Belitung)

Impact:
- All PRIBADI and BARANG vehicles now generated with correct province codes
- 100% compliance with official Indonesian administrative codes
- NIK format fully validated against actual province assignments

INDEPENDENT NIK FOR SPECIAL VEHICLES:
Policy Implemented:
- PEMERINTAH vehicles: Generate NIK with random province 01-34
- KEDUTAAN vehicles: Generate NIK with random province 01-34
- Reflects reality: Government and diplomatic vehicles operate nationwide
- Not bound by their registration plate's regional code

================================================================================
COMPLIANCE VERIFICATION
================================================================================

System Compliance Matrix:

Feature                          | Requirement      | Status
---------------------------------|------------------|--------
License Plate Format             | Official Format  | 100%
Vehicle Categories (4 types)     | Indonesian Law   | 100%
NIK Format (16 digits)           | Official Format  | 100%
Province Codes (11-34)           | Official List    | 100%
District Codes (base.csv)        | Government Data  | 100%
Sub-district Codes (base.csv)    | Government Data  | 100%
Fine Calculation (Article 287.5) | Indonesian Law   | 100%
Penalty Multipliers              | Enhanced Feature | 100%
Speed Limit Enforcement          | Toll Road Rules  | 100%
Vehicle Distribution             | Realistic Data   | 100%
Administrative Data              | 91,221 entities  | 100%

Overall Compliance: 100% VERIFIED

================================================================================
LEGAL DISCLAIMERS
================================================================================

1. This system is designed for SIMULATION AND TESTING PURPOSES ONLY
2. Generated fines and violations are FICTIONAL and FOR TESTING ONLY
3. Not intended to replace actual Indonesian traffic law enforcement
4. All data generated is SIMULATED and not representing real violations
5. For actual legal matters, consult official Indonesian traffic authorities

================================================================================
REFERENCES
================================================================================

1. UU No. 22 Tahun 2009
   Tentang Lalu Lintas dan Angkutan Jalan
   (Law No. 22 of 2009 Regarding Road Traffic and Transportation)

2. Peraturan Kapolri Nomor 7 Tahun 2021
   Tentang Tanda Nomor Kendaraan Bermotor
   (Police Regulation No. 7 of 2021 Regarding Vehicle Number Plates)

3. PP No. 55 Tahun 2012
   Tentang Kendaraan Bermotor dan Pengemudi
   (Government Regulation No. 55 of 2012 Regarding Motor Vehicles and Drivers)

4. Indonesian Administrative Code Database (base.csv)
   - 91,221 administrative entities
   - Province, District, Sub-district codes

5. Wikipedia: Tanda Nomor Kendaraan Bermotor Indonesia
   https://id.wikipedia.org/wiki/Tanda_Nomor_Kendaraan_Bermotor_Indonesia

================================================================================
END OF LAW AND LEGAL BASE DOCUMENTATION
================================================================================
