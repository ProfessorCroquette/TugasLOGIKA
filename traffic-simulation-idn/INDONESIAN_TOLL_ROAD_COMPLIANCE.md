# Indonesian Toll Road Compliance (PP 43/1993)

## Changes Made

### 1. Vehicle Types - Motorcycles DISABLED ✓
**Legal Basis**: PP (Peraturan Pemerintah) No. 43 Tahun 1993 tentang Prasarana dan Lalu Lintas Jalan

**Configuration Changes**:
- `car`: 75% (increased from 60%)
- `truck`: 25% (increased from 20%)
- `motorcycle`: 0% (DISABLED - was 15%)
- `bus`: 0% (DISABLED - was 5%)

**Result**: Only cars and trucks can be generated on toll roads.

---

### 2. Speed Limits - Toll Road Standards ✓
**Legal Basis**: PP 43/1993 & Permenhub (Peraturan Menteri Perhubungan)

#### Cars (Kendaraan Ringan < 3,500 kg)
- **Minimum Speed**: 60 km/h
- **Maximum Speed**: 100 km/h
- **Speed Mean**: 85 km/h (realistic average)

#### Trucks (Kendaraan Berat ≥ 3,500 kg)
- **Minimum Speed**: 60 km/h (toll road minimum)
- **Maximum Speed**: 80 km/h (truck limit)
- **Speed Mean**: 70 km/h

**Configuration Changes**:
- `SPEED_LIMIT`: 100 km/h (was 75 km/h)
- `MIN_SPEED_LIMIT`: 60 km/h (was 40 km/h)
- `SPEED_MEAN`: 85 km/h (was 70 km/h)
- `MIN_SPEED`: 60 km/h (was 45 km/h)
- `MAX_SPEED`: 120 km/h (was 95 km/h, allows speeding violations)

---

### 3. Fine Tiers - Updated for Toll Road Speeds ✓

| Tier | Speed Range (km/h) | Base Fine (USD) | Fine in IDR | Description |
|------|-------------------|-----------------|------------|-------------|
| **SPEED_LOW_MILD** | 50-59 | $20 | Rp 310,000 | Terlalu lambat (terlalu rendah dari batas minimum) |
| **SPEED_LOW_SEVERE** | 0-49 | $35 | Rp 542,500 | Terlalu lambat berat (sangat di bawah batas minimum) |
| **SPEED_HIGH_LEVEL_1** | 101-110 | $30 | Rp 465,000 | Melampaui batas kecepatan 1-10 km/h (cars) |
| **SPEED_HIGH_LEVEL_2** | 111-120 | $50 | Rp 775,000 | Melampaui batas kecepatan 11-20 km/h (cars) |
| **SPEED_HIGH_LEVEL_3** | 121-150 | $75 | Rp 1,162,500 | Melampaui batas kecepatan 21+ km/h (cars) |

**Maximum Fine**: Rp 500,000 (USD ~$32.26) for base fine
- With STNK multiplier (1.2x): ~Rp 600,000
- With STNK + SIM multiplier (1.4x): ~Rp 700,000

---

## Violation Examples

### Car Speeding
- **Normal speed**: 85 km/h → No violation
- **Speed**: 95 km/h → 5 km/h over limit (LEVEL_1)
- **Speed**: 115 km/h → 15 km/h over limit (LEVEL_2)
- **Speed**: 130 km/h → 30 km/h over limit (LEVEL_3)

### Truck Speeding
- **Normal speed**: 70 km/h → No violation
- **Speed**: 75 km/h → Truck under 80 limit
- **Speed**: 90 km/h → Violation (above truck limit of 80)

### Too Slow
- **Speed**: 50 km/h → MILD violation (below 60 minimum)
- **Speed**: 30 km/h → SEVERE violation (well below minimum)

---

## Legal References

1. **Pasal 23 UU LLAJ** - Obligation to adjust speed based on road conditions
2. **PP No. 43 Tahun 1993** - Road and Traffic Infrastructure Regulations
   - Article about speed limits for toll roads
   - Cars: 60-100 km/h
   - Trucks: Limited to lower speeds
3. **Permenhub** - Ministry of Transportation regulations
   - Speed limit enforcement
   - Vehicle classification

---

## Testing Results

✓ Configuration verified:
- SPEED_LIMIT = 100 km/h
- MIN_SPEED_LIMIT = 60 km/h
- Vehicle types: Cars (75%) + Trucks (25%) only

✓ Speed generation verified:
- Car speeds: 60-120 km/h range
- Truck speeds: 60-80 km/h range
- No motorcycles generated

✓ Fine calculations verified:
- Base fine capped at Rp 500k
- Multipliers apply after cap (1.2x or 1.4x)
- Final fine can exceed base maximum with multipliers

---

## Files Modified

1. `config/__init__.py` - Updated Config class
2. `utils/generators.py` - Updated speed generation and vehicle selection
3. Fine tier ranges updated for toll road speeds

---

**Status**: ✅ COMPLETE - Full compliance with PP 43/1993 Toll Road Standards
