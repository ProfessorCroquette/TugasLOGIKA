"""Check PLATE_DATA sub-region names"""
from utils.indonesian_plates import IndonesianPlateManager

plate_codes = ['B', 'D', 'F', 'T', 'H', 'A']
for code in plate_codes:
    if code in IndonesianPlateManager.PLATE_DATA:
        data = IndonesianPlateManager.PLATE_DATA[code]
        print(f"{code}: Region={data['region_name']}, Province={data['province_code']}")
        if data.get('sub_codes'):
            sample = list(data['sub_codes'].values())[:5]
            print(f"   Sample sub-regions: {sample}")
            print()
