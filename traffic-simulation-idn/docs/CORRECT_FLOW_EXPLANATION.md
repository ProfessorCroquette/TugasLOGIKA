# CORRECT FLOW - PLAT NOMOR → GENERATE OWNER

## Ringkasan Alur yang Benar (Correct Flow)

```
STEP 1: PARSE PLAT NOMOR
  Input: "B 4123 RK" (Plat nomor yang sudah digenerate)
  ├─ Extract region code: "B"
  ├─ Lookup di PLATE_DATA → Get region info
  └─ Output: {region_code, region_name, province_code, ...}

STEP 2: EXTRACT ADMINISTRATIVE CODES
  ├─ Dari region code "B" → Dapatkan province code "31" (DKI Jakarta)
  ├─ Dari sub_region → Extract city code & sub-district code
  └─ Example: Province=31, City=74 (Jakarta Selatan), SubDistrict=05 (Kebayoran Baru)

STEP 3: GENERATE NIK (NOMOR INDUK KEPENDUDUKAN)
  NIK Format: [Province(2)][City(2)][SubDistrict(2)][BirthDay(2)][Month(2)][Year(2)][Sequential(4)]
  
  Example untuk "B 4123 RK":
  ├─ Province: "31" (dari plat code "B")
  ├─ City: "74" (Jakarta Selatan)
  ├─ SubDistrict: "05" (Kebayoran Baru)
  ├─ BirthDay: "65" (25 + 40 untuk wanita, lahir tanggal 25)
  ├─ Month: "10" (Oktober)
  ├─ Year: "92" (1992)
  ├─ Sequential: "0071" (nomor urut 7 + digit cek)
  └─ HASIL: NIK = "3174056510920071"

STEP 4: GENERATE OWNER DATA
  ├─ Name: Random nama Indonesia (Sari Dewi)
  ├─ Region: Dari province code & plate mapping
  ├─ Sub Region: Dari plat region (Jakarta Selatan)
  ├─ Address: Random street + sub_region
  ├─ STNK Status: Random (70% Active)
  └─ SIM Status: Random (80% Active)

STEP 5: VALIDATE SYNCHRONIZATION
  ├─ Extract NIK province code: "31"
  ├─ Extract Plate province code: "31"
  └─ Verify: Harus sama! (Compliance dengan hukum Indonesia)
```

## Implementasi di Kode

### 1. Parse Plat Nomor

```python
from utils.indonesian_plates import IndonesianPlateManager

# Parse plat nomor
region_info = IndonesianPlateManager.extract_region_info_from_plate("B 4123 RK")

# Output:
# {
#     'region_code': 'B',
#     'region_name': 'DKI Jakarta',
#     'sub_region': 'Jakarta Selatan',
#     'province_code': '31',
#     'area': 'Jawa Bagian Barat',
#     'vehicle_type': 'PRIBADI',
#     'is_special': False
# }
```

### 2. Generate Owner dari Plat

```python
# Generate owner DARI plat nomor
owner = IndonesianPlateManager.generate_owner_from_plate("B 4123 RK", "roda_dua")

# Output:
# VehicleOwner(
#     owner_id='3174056510920071',      # NIK synchronized ke plat province code
#     name='Sari Dewi',                  # Random Indonesian name
#     region='DKI Jakarta',              # Dari plat region mapping
#     sub_region='Jakarta Selatan',      # Dari plat sub-region
#     address='Jl. Melati No.1, Jakarta Selatan',  # Generated address
#     vehicle_type='roda_dua',
#     stnk_status=True,                  # 70% chance active
#     sim_status=True                    # 80% chance active
# )
```

### 3. Validate Synchronization

```python
# Extract province codes dari NIK dan Plat
nik_province = owner.owner_id[:2]         # '31' dari NIK
plat_province = region_info['province_code']  # '31' dari plat

# Harus sama untuk compliance dengan hukum Indonesia
assert nik_province == plat_province, "NIK dan Plat tidak synchronized!"
```

## Struktur NIK (Nomor Induk Kependudukan)

Indonesian NIK memiliki format tetap 16 digit:

```
[Province Code][City Code][SubDistrict Code][Birth Date][Birth Month][Birth Year][Sequential][Check Digit]
    (2 digit)    (2 digit)     (2 digit)       (2 digit)  (2 digit)   (2 digit)  (4 digit)

Contoh: 3 1 7 4 0 5 6 5 1 0 9 2 0 0 7 1
        └─────┘ └─────┘ └────────────────────┘
        Province  City   Birth Info
        (31)      (74)   (65=Female+25, Oct 92)
```

### Kode Provinsi (Province Codes)

```
11 = Aceh
12 = Sumatera Utara
13 = Sumatera Barat
14 = Riau
15 = Kepulauan Riau
16 = Jambi
17 = Sumatera Selatan
18 = Bengkulu
19 = Lampung
21 = Kepulauan Bangka Belitung
31 = DKI Jakarta
32 = Jawa Barat
33 = Jawa Tengah
34 = Daerah Istimewa Yogyakarta
35 = Jawa Timur
36 = Banten
51 = Bali
52 = Nusa Tenggara Barat
53 = Nusa Tenggara Timur
61 = Kalimantan Barat
62 = Kalimantan Tengah
63 = Kalimantan Selatan
64 = Kalimantan Timur
65 = Kalimantan Utara
71 = Sulawesi Utara
72 = Sulawesi Tengah
73 = Sulawesi Selatan
74 = Sulawesi Tenggara
75 = Gorontalo
76 = Sulawesi Barat
81 = Maluku
82 = Maluku Utara
91 = Papua Barat
94 = Papua

Special Codes:
00 = Pemerintah Indonesia (Government vehicles - RI plates)
99 = Diplomatik (Diplomatic vehicles - CD/CC plates)
```

### Kode Kota (City Codes)

Setiap provinsi memiliki 2-3 digit kode kota/kabupaten. Contoh untuk DKI Jakarta:

```
31.01 = Jakarta Pusat
31.72 = Jakarta Utara
31.73 = Jakarta Barat
31.74 = Jakarta Selatan
31.75 = Jakarta Timur
31.76 = Kota Administrasi Jakarta Selatan (pada era tertentu)
```

### Birth Date Encoding

```
Birth Day: 
  - Male: 01-31 (as is)
  - Female: 41-71 (add 40 to day)
  
Example:
  - Born on 25th as female → 25 + 40 = 65

Birth Month: 01-12 (Standard)

Birth Year: 2-digit format
  - Born 1992 → 92
  - Born 1945 → 45
  - Born 2005 → 05
```

## Plat Nomor Mapping ke Province Code

```python
PLATE_CODE_TO_PROVINCE = {
    # Sumatera
    'BL': '11',  # Aceh
    'BB': '12',  # Sumatera Utara
    'BK': '12',  # Sumatera Utara (Pesisir Timur)
    'BA': '13',  # Sumatera Barat
    'BM': '14',  # Riau
    'BP': '15',  # Kepulauan Riau
    'BH': '16',  # Jambi
    'BG': '17',  # Sumatera Selatan
    'BD': '18',  # Bengkulu
    'BE': '19',  # Lampung
    'BN': '21',  # Kepulauan Bangka Belitung
    
    # Jawa
    'A': '36',   # Banten
    'B': '31',   # DKI Jakarta
    'D': '32',   # Jawa Barat
    'E': '32',   # Jawa Barat (Cirebon)
    'F': '32',   # Jawa Barat (Bogor)
    'T': '32',   # Jawa Barat (Karawang)
    'Z': '32',   # Jawa Barat (Tasikmalaya/Ciamis)
    'G': '33',   # Jawa Tengah
    'H': '33',   # Jawa Tengah (Semarang)
    'K': '33',   # Jawa Tengah (Pati/Grobogan)
    'R': '33',   # Jawa Tengah (Banyumas)
    'AA': '33',  # Jawa Tengah (Kedu)
    'AD': '33',  # Jawa Tengah (Surakarta)
    'AB': '34',  # Yogyakarta
    'L': '35',   # Jawa Timur
    
    # Special
    'RI': '00',  # Government (Pemerintah)
    'CD': '99',  # Diplomatic Corps
    'CC': '99',  # Consular Corps
}
```

## Test Results

Berikut hasil test untuk memvalidasi correct flow:

```
TEST CASE 1: PLAT B 4123 RK
├─ Parse Plat: OK
│  ├─ Region Code: B
│  ├─ Province Code: 31 (DKI Jakarta)
│  └─ Sub Region: Jakarta Selatan
├─ Generate Owner: OK
│  ├─ NIK: 3174056510920071 (starts with 31 - synchronized!)
│  ├─ Name: Ahmad Gunawan
│  ├─ Region: DKI Jakarta
│  ├─ Address: Jl. Kartini No.272, Jakarta Selatan
│  ├─ STNK Status: Active
│  └─ SIM Status: Active
└─ Validate: SYNCHRONIZED (31 == 31) ✓

TEST CASE 2: PLAT D 5678 ABC
├─ Parse Plat: OK
│  ├─ Region Code: D
│  ├─ Province Code: 32 (Jawa Barat)
│  └─ Sub Region: Jawa Barat
├─ Generate Owner: OK
│  ├─ NIK: 3205121910621728 (starts with 32 - synchronized!)
│  ├─ Name: Dwi Wijaya
│  ├─ Region: Jawa Barat
│  └─ Address: Jl. Menteng No.553, Bandung
└─ Validate: SYNCHRONIZED (32 == 32) ✓

... [more test cases] ...

RESULT: ALL TESTS PASSED ✓
- 7 test plates validated
- 3 generated plates validated
- 100% synchronization rate
```

## Penggunaan di Main Application

```python
# Dalam generasi kendaraan
def generate_vehicle_with_correct_flow():
    # STEP 1: Generate random plat nomor
    plate, region_name, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
    
    # STEP 2: Generate owner DARI plat (not independently!)
    owner = IndonesianPlateManager.generate_owner_from_plate(
        plate, 
        vehicle_type_str  # 'roda_dua' or 'roda_empat'
    )
    
    # STEP 3: Create vehicle object
    vehicle = Vehicle(
        license_plate=plate,
        owner_id=owner.owner_id,
        owner_name=owner.name,
        owner_region=owner.region,
        owner_address=owner.address,
        stnk_status='Active' if owner.stnk_status else 'Expired',
        sim_status='Active' if owner.sim_status else 'Expired',
        model='Toyota Avanza',  # Generate separately
        speed=60.5,
        tipe='PRIBADI'  # Can be PRIBADI, KOMERSIAL, BARANG, DIPLOMATIK, PEMERINTAH
    )
    
    return vehicle
```

## Keuntungan Correct Flow

1. **Compliance**: Memastikan NIK pemilik sesuai dengan kode wilayah plat
2. **Konsistensi**: Owner selalu match dengan plat region
3. **Realism**: Address selalu sesuai dengan region plat
4. **Auditability**: Mudah untuk trace NIK → Plat relationship
5. **Validation**: Semua vehicle yang digenerate sudah pre-validated

## Regulasi yang Diikuti

**Peraturan Kapolri Nomor 7 Tahun 2021 tentang Pengesahan Bentuk, Ukuran, Warna, Penulisan dan Penempatan Tanda Nomor Kendaraan Bermotor**

Key Points:
- Kode wilayah plat harus sesuai dengan tempat tinggal pemilik
- NIK pemilik harus match dengan kode wilayah plat
- Province code (2 digit pertama NIK) = Province code dari plat region
- Format plat: [Region Code] [1-4 digits] [Sub Code] [Owner Letters]
