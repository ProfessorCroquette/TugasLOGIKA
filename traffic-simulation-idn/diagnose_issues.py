#!/usr/bin/env python3
"""Diagnose remaining synchronization issues"""

from utils.indonesian_plates import IndonesianPlateManager

print('Checking all PLATE_DATA entries for province code issues...\n')

issues = []

for plate_code, data in IndonesianPlateManager.PLATE_DATA.items():
    province_code = data.get('province_code', 'MISSING')
    
    # Check for problems:
    # 1. Province code is missing
    # 2. Province code equals plate code (wrong!)
    # 3. Province code is not a 2-digit number
    
    if province_code == 'MISSING':
        issues.append(f'✗ {plate_code}: province_code MISSING')
    elif province_code == plate_code:
        issues.append(f'✗ {plate_code}: province_code = plate_code (should be numeric!)')
    elif not str(province_code).isdigit() or len(str(province_code)) != 2:
        issues.append(f'✗ {plate_code}: province_code = {province_code} (invalid format!)')

if issues:
    print(f'Found {len(issues)} issues:\n')
    for issue in issues:
        print(issue)
else:
    print('✓ No obvious issues found in PLATE_DATA')

# Now test actual method
print('\n\n' + '='*70)
print('Testing get_province_code_from_plate_code() for all codes...\n')

method_issues = []

for plate_code in IndonesianPlateManager.PLATE_DATA.keys():
    expected = IndonesianPlateManager.PLATE_DATA[plate_code].get('province_code')
    actual = IndonesianPlateManager.get_province_code_from_plate_code(plate_code)
    
    if expected != actual:
        method_issues.append(f'✗ {plate_code}: Expected {expected}, got {actual}')

if method_issues:
    print(f'Found {len(method_issues)} method issues:\n')
    for issue in method_issues:
        print(issue)
else:
    print('✓ All plate codes returning correct province codes!')

print('\n' + '='*70)
print(f'Summary: {len(issues)} data issues, {len(method_issues)} method issues')
