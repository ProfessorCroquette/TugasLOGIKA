"""Test improved CSV matching"""
from utils.indonesian_plates import IndonesianPlateManager

test_names = ['Jakarta Selatan', 'Kota Bandung', 'Kota Bogor', 'Kabupaten Tangerang', 'Jakarta Barat']
for name in test_names:
    result = IndonesianPlateManager._get_csv_codes_for_region(name)
    if result:
        print(f"{name:30} -> city={result['city']} dist={result['district']}")
    else:
        print(f"{name:30} -> NOT FOUND")
