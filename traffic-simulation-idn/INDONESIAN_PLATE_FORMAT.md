# Indonesian License Plate Format (Official Standard)

## Format Specification

Indonesian civilian license plates follow a 3-segment structure:

### Segment 1: Region Code
- **Pattern**: `[A-Z]{1,2}` (1-2 letters)
- **Meaning**: Province or combined area (JADETABEK)
- **Examples**:
  - `B` = JADETABEK (Jakarta, Depok, Tangerang, Bekasi)
  - `D` = Jawa Barat (Bandung area)
  - `F` = Jawa Barat (Bogor area)
  - `L` = Surabaya, Jawa Timur
  - `DK` = Bali
  - `KB` = Kalimantan Barat

### Segment 2: Vehicle Number
- **Pattern**: `\d{1,4}` (1-4 digits)
- **Range**: 1 to 9999
- **Meaning**: Vehicle identification/sequential number
- **Examples**:
  - `1`, `12`, `123`, `1234`
  - `1704` in "B 1704 CJE"

### Segment 3: Sub-Region Code
- **Pattern**: `[A-Z]{0,3}` (0-3 letters, optional)
- **Meaning**: Identifies specific city/regency/district
- **First Letter**: Identifies the sub-region
- **Usage**: Only the first letter is significant for identification
- **Examples**:
  - `C` in "CJE" = Tangerang, Banten (from plate code B)
  - `U` in "UAE" = Jakarta Utara (from plate code B)
  - `A` in "ABC" = Bandung (from plate code D)

## Complete Example Analysis

**Plate: B 1704 CJE**

| Segment | Value | Meaning |
|---------|-------|---------|
| 1 | B | JADETABEK Area (Jakarta region) |
| 2 | 1704 | Vehicle ID number 1704 |
| 3 | C* | Tangerang, Banten (*first letter C identifies the city) |

The full plate format in regex: `^[A-Z]{1,2} \d{1,4} [A-Z]{0,3}$`

**Spacing**: `RegionCode SPACE Number SPACE SubCode`

## Plate Code Reference by Region

### JADETABEK Region (Code: B)
- `U` = Jakarta Utara
- `B` = Jakarta Barat
- `P` = Jakarta Pusat (Central)
- `T` = Jakarta Timur (East)
- `S` = Jakarta Selatan (South)
- `E` = Depok, Jawa Barat
- `Z` = Depok, Jawa Barat
- `F` = Bekasi, Jawa Barat
- `K` = Bekasi, Jawa Barat
- `C` = Tangerang, Banten
- `V` = Tangerang, Banten
- `G` = Tangerang, Banten
- `N` = Tangerang, Banten
- `W` = Tangerang Selatan, Banten

### Jawa Barat Codes
- **D** = Bandung Area (City Bandung, Cimahi, Kab. Bandung, Kab. Bandung Barat)
- **F** = Bogor Area (City Bogor, Kab. Bogor, Sukabumi, Cianjur)
- **E** = Cirebon Area
- **T** = Karawang/Purwakarta Area
- **Z** = Priangan Timur (Garut, Tasikmalaya, Ciamis, Banjar)

### Jawa Tengah Codes
- **G** = Pekalongan Area
- **H** = Semarang Area
- **K** = Pati/Grobogan Area
- **R** = Banyumas Area
- **AA** = Magelang/Kedu Area
- **AD** = Surakarta Area
- **AB** = Yogyakarta Special Region

### Jawa Timur Codes
- **L** = Surabaya City
- **M** = Madura (Pamekasan, Bangkalan, Sampang, Sumenep)
- **N** = Malang/Pasuruan Area
- **P** = Besuki Area (Jember, Banyuwangi)
- **S** = Bojonegoro/Lamongan/Jombang Area
- **W** = Gresik/Sidoarjo Area
- **AE** = Madiun Area
- **AG** = Kediri Area

### Bali (Code: DK)
Sub-regions: Denpasar, Badung, Tabanan, Gianyar, Klungkung, Bangli, Karangasem, Buleleng, Jembrana

### Kalimantan
- **KB** = Kalimantan Barat
- **DA** = Kalimantan Selatan
- **KH** = Kalimantan Tengah
- **KT** = Kalimantan Timur
- **KU** = Kalimantan Utara

### Sulawesi & Maluku
- **DB** = Sulawesi Utara
- **DN** = Sulawesi Tengah
- **DD** = Sulawesi Selatan
- **DT** = Sulawesi Tenggara
- **DE** = Maluku

### Sumatera
- **BL** = Aceh
- **BB** = Sumatera Utara (Tapanuli)
- **BK** = Sumatera Utara (Medan)
- **BA** = Sumatera Barat
- **BM** = Riau
- **BP** = Kepulauan Riau
- **BH** = Jambi
- **BG** = Sumatera Selatan
- **BD** = Bengkulu
- **BE** = Lampung
- **BN** = Kepulauan Bangka Belitung

## Validation Rules

1. **Segment 1**: Must be 1-2 uppercase letters matching defined region codes
2. **Segment 2**: Must be 1-4 digits, value 1-9999
3. **Segment 3**: Must be 0-3 uppercase letters (can be empty but usually present)
4. **Spacing**: Single space between segments
5. **Sub-region First Letter**: Must match valid code for that region

## Special Cases

- **Government Plates**: Start with `RI` (Republik Indonesia)
- **Diplomatic Plates**: Start with `CD` or `CC` (Consulate/Embassy)
- **Motorcycle vs Car**: Same format, no distinction in plate itself

## Implementation

The system should:
1. Generate plates from defined region codes
2. Select random valid sub-region codes for that region
3. Generate 1-4 random digits
4. Optionally add 1-3 letter owner codes
5. Format as: `{region} {number} {sub_code} {owner_code}`

---

**Source**: Official Indonesian Ministry of Transportation Regulation
**Last Updated**: January 31, 2026
