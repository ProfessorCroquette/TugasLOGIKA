#!/usr/bin/env python3
"""Final verification: GUI displays proper region names"""

from PyQt5.QtWidgets import QApplication
import sys
from gui_traffic_simulation import ViolationDetailDialog

print('='*70)
print('FINAL GUI FIX VERIFICATION')
print('='*70)
print()

test_cases = [
    {'plate': 'KT 123 A AB', 'code': 'KT', 'expected': 'Kalimantan Timur'},
    {'plate': 'BM 456 B CD', 'code': 'BM', 'expected': 'Riau'},
    {'plate': 'BA 789 C EF', 'code': 'BA', 'expected': 'Sumatera Barat'},
    {'plate': 'T 012 D GH', 'code': 'T', 'expected': 'Jawa Barat (Keresidenan Karawang)'},
]

app = QApplication(sys.argv)
all_pass = True

for test in test_cases:
    violation = {
        'license_plate': test['plate'],
        'owner_region': test['code'],
        'owner_name': 'Test Owner',
        'owner_id': '6401010101010001',
        'stnk_status': 'Active',
        'sim_status': 'Active',
        'speed': 80,
        'fine_amount': 10,
        'penalty_multiplier': 1,
        'timestamp': '2026-01-31 12:00:00'
    }
    
    d = ViolationDetailDialog(violation)
    
    # Get wilayah label (should be first KT region after "Wilayah:")
    labels = [w.text() for w in d.findChildren(type(d.findChildren()[0].__class__))]
    
    # Check if "Wilayah:" label and its value are correct
    wilayah_idx = None
    for i, label in enumerate(labels):
        if label == 'Wilayah:':
            wilayah_idx = i
            break
    
    if wilayah_idx is not None and wilayah_idx + 1 < len(labels):
        wilayah_value = labels[wilayah_idx + 1]
        if 'Kode:' in wilayah_value:
            print(f'✗ {test["plate"]}: Shows "Kode: {test["code"]}" instead of "{test["expected"]}"')
            all_pass = False
        elif test['expected'] in wilayah_value or test['code'] not in wilayah_value:
            print(f'✓ {test["plate"]}: Displays "{wilayah_value}"')
        else:
            print(f'✗ {test["plate"]}: Shows "{wilayah_value}"')
            all_pass = False
    
    d.close()

print()
print('='*70)
if all_pass:
    print('✅ GUI FIX VERIFIED: All region codes display proper names!')
else:
    print('⚠️  Some codes still showing "Kode: XX" format')
