from utils.indonesian_plates import IndonesianPlateManager

code = 'KT'
print('PLATE_DATA[KT].region_name =', IndonesianPlateManager.PLATE_DATA.get(code, {}).get('region_name'))

owner_region = 'KT'
owner_region_display = owner_region
try:
    val = str(owner_region).upper().strip()
    if val in IndonesianPlateManager.PLATE_DATA:
        owner_region_display = IndonesianPlateManager.PLATE_DATA[val].get('region_name', owner_region)
    else:
        owner_region_display = 'fallback'
except Exception:
    owner_region_display = owner_region

print('Computed owner_region_display =', owner_region_display)
