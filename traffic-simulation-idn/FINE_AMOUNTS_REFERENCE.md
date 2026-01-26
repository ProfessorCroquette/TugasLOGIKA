# FINE AMOUNTS - QUICK REFERENCE

## System Configuration (config/__init__.py)

```python
# Speed Limits
SPEED_LIMIT = 75 km/h          # Normal speed limit
MIN_SPEED_LIMIT = 40 km/h      # Minimum safe speed

# Currency
USD_TO_IDR = 15500             # Exchange rate

# Maximum Fine
MAX_FINE_IDR = 1,250,000 IDR   # Per Indonesian Law
MAX_FINE_USD = 80.65 USD
```

---

## Fine Structure

### 📉 Driving Too Slowly

| Severity | Speed Range | Fine (USD) | Fine (IDR) | Calculation |
|----------|-------------|-----------|-----------|-------------|
| **MILD** | 30-39 km/h | $20 | Rp 310,000 | 20 × 15,500 |
| **CRITICAL** | 0-29 km/h | $35 | Rp 542,500 | 35 × 15,500 |

### 🏎️ Speeding

| Level | Speed Range | Fine (USD) | Fine (IDR) | Calculation |
|-------|-------------|-----------|-----------|-------------|
| **LEVEL 1** | 76-90 km/h | $30 | Rp 465,000 | 30 × 15,500 |
| **LEVEL 2** | 91-110 km/h | $50 | Rp 775,000 | 50 × 15,500 |
| **LEVEL 3** | 111-130+ km/h | $75 | Rp 1,162,500 | 75 × 15,500 |

### ✅ No Violation

| Range | Status |
|-------|--------|
| **40-75 km/h** | No violation |

---

## Penalty Multiplier

| Condition | Multiplier |
|-----------|-----------|
| Both STNK Active & SIM Valid | 1.0x (base) |
| STNK Non-Active OR SIM Expired | 1.2x |
| Both Non-Active AND Expired | 1.4x |

**Important**: Final amount capped at Rp 1,250,000 (legal maximum)

### Example Calculation

```
Scenario: Speeding at 95 km/h + Expired SIM + Non-Active STNK

Step 1: Determine base fine
  Speed: 95 km/h → LEVEL 2 → Base: $50

Step 2: Apply multiplier
  Conditions: Non-Active STNK (+0.2) + Expired SIM (+0.2)
  Multiplier: 1.0 + 0.2 + 0.2 = 1.4x
  Calculated: $50 × 1.4 = $70

Step 3: Apply cap
  Maximum: Rp 1,250,000 (≈ $80.65)
  Result: $70 × 15,500 = Rp 1,085,000 ✅ (Under cap)

Final Fine: Rp 1,085,000
```

---

## Currency Conversion

| USD | IDR | Calculation |
|-----|-----|------------|
| $20 | Rp 310,000 | 20 × 15,500 |
| $30 | Rp 465,000 | 30 × 15,500 |
| $35 | Rp 542,500 | 35 × 15,500 |
| $50 | Rp 775,000 | 50 × 15,500 |
| $75 | Rp 1,162,500 | 75 × 15,500 |
| $80.65 | Rp 1,250,000 | Max legal limit |

---

## Where These Values Are Used

1. **Config/Settings**: `config/__init__.py` (source of truth)
2. **GUI Display**: `gui_traffic_simulation.py` (shows fines in IDR)
3. **Fine Calculation**: `simulation/analyzer.py` (calculates based on speed)
4. **Database**: `data_files/tickets.json` (stores calculated amounts)
5. **Reports**: Various export formats use these amounts

---

## Compliance

✅ **Legal Basis**: Pasal 287 ayat (5) UU No. 22 Tahun 2009 LLAJ
✅ **Maximum Fine**: Rp 1,250,000 (enforced by system)
✅ **Speed Limits**: 40-75 km/h (normal safe driving range)
✅ **Tiered Structure**: Violations penalized proportionally to severity
✅ **Multipliers**: Additional penalties for registration issues (capped)

---

**Last Updated**: January 26, 2026
**Source**: config/__init__.py
**Status**: ✅ ACCURATE
