#!/usr/bin/env python3
"""
Comprehensive Report: Plate-NIK Alignment Analysis
Tests the alignment between:
1. Plate region codes
2. NIK administrative codes
3. Owner region information
"""

import json
from pathlib import Path

def load_admin_codes():
    """Load administrative codes from base.csv"""
    admin_codes = {}
    with open('base.csv', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                code = parts[0].strip()
                name = parts[1].strip()
                
                if '.' in code:
                    code_parts = code.split('.')
                    if len(code_parts) == 2:
                        prov = code_parts[0]
                        dist = code_parts[1]
                        combined = prov + dist
                        admin_codes[combined] = {
                            'code': code,
                            'district': name
                        }
    
    return admin_codes

def extract_nik_province(nik):
    """Extract province code from NIK"""
    if len(nik) >= 2:
        return nik[0:2]
    return None

def extract_nik_district(nik):
    """Extract district code from NIK"""
    if len(nik) >= 4:
        return nik[2:4]
    return None

def is_special_plate(plate):
    """Check if plate is special (diplomatic, government, etc)"""
    plate_upper = plate.upper().strip()
    special_prefixes = ('CC', 'CD', 'RI')
    return any(plate_upper.startswith(p) for p in special_prefixes)

def analyze_alignment():
    """Analyze plate-NIK alignment"""
    
    print("=" * 80)
    print("PLATE-NIK ALIGNMENT ANALYSIS")
    print("=" * 80)
    
    # Load data
    admin_codes = load_admin_codes()
    print("\nLoaded {} administrative codes".format(len(admin_codes)))
    
    try:
        with open('data_files/tickets.json', 'r', encoding='utf-8') as f:
            vehicles = json.load(f)
    except Exception as e:
        print("ERROR: Could not load tickets: {}".format(e))
        return False
    
    if not isinstance(vehicles, list):
        vehicles = []
    
    print("Analyzing {} vehicles".format(len(vehicles)))
    print("-" * 80)
    
    regular_plates = []
    special_plates = []
    
    for vehicle in vehicles:
        plate = vehicle.get('license_plate', '')
        owner = vehicle.get('owner', {})
        nik = owner.get('id', '')
        owner_region = owner.get('region', '')
        
        plate_data = {
            'plate': plate,
            'nik': nik,
            'owner_region': owner_region,
            'is_special': is_special_plate(plate)
        }
        
        if plate_data['is_special']:
            special_plates.append(plate_data)
        else:
            regular_plates.append(plate_data)
    
    print("\nPLATE STATISTICS:")
    print("  Regular plates: {}".format(len(regular_plates)))
    print("  Special plates: {} (CC, CD, RI)".format(len(special_plates)))
    print("  Total: {}".format(len(vehicles)))
    
    # Analyze regular plates
    print("\n" + "=" * 80)
    print("REGULAR PLATES ANALYSIS (Non-diplomatic)")
    print("=" * 80)
    
    found_in_admin = 0
    not_found_in_admin = 0
    details_regular = []
    
    for plate_data in regular_plates[:100]:  # Test first 100 or all available
        nik = plate_data['nik']
        owner_region = plate_data['owner_region']
        
        prov_code = extract_nik_province(nik)
        dist_code = extract_nik_district(nik)
        
        if prov_code and dist_code:
            combined = prov_code + dist_code
            
            if combined in admin_codes:
                found_in_admin += 1
                status = 'FOUND'
                admin_name = admin_codes[combined]['district']
            else:
                not_found_in_admin += 1
                status = 'NOT FOUND'
                admin_name = '-'
            
            details_regular.append({
                'plate': plate_data['plate'],
                'nik': nik,
                'code': combined,
                'owner_region': owner_region,
                'admin_name': admin_name,
                'status': status
            })
    
    print("\nResults for regular plates (first 100):")
    print("  Found in admin table: {}".format(found_in_admin))
    print("  NOT found in admin table: {}".format(not_found_in_admin))
    
    if not_found_in_admin > 0:
        print("\nMissing codes in regular plates:")
        not_found_codes = set()
        for d in details_regular:
            if d['status'] == 'NOT FOUND':
                not_found_codes.add(d['code'])
        
        for code in sorted(not_found_codes)[:10]:
            print("  - {}".format(code))
    
    # Analyze special plates
    print("\n" + "=" * 80)
    print("SPECIAL PLATES ANALYSIS (Diplomatic/Government)")
    print("=" * 80)
    
    special_found = 0
    special_not_found = 0
    details_special = []
    
    for plate_data in special_plates[:100]:  # Test first 100
        nik = plate_data['nik']
        owner_region = plate_data['owner_region']
        
        prov_code = extract_nik_province(nik)
        dist_code = extract_nik_district(nik)
        
        if prov_code and dist_code:
            combined = prov_code + dist_code
            
            if combined in admin_codes:
                special_found += 1
                status = 'FOUND'
                admin_name = admin_codes[combined]['district']
            else:
                special_not_found += 1
                status = 'NOT FOUND'
                admin_name = '-'
            
            details_special.append({
                'plate': plate_data['plate'],
                'nik': nik,
                'code': combined,
                'owner_region': owner_region,
                'admin_name': admin_name,
                'status': status
            })
    
    print("\nResults for special plates (first 100):")
    print("  Found in admin table: {}".format(special_found))
    print("  NOT found in admin table: {}".format(special_not_found))
    
    # Show samples
    print("\n" + "=" * 80)
    print("SAMPLE ALIGNMENT DETAILS")
    print("=" * 80)
    
    print("\nRegular Plate Samples:")
    for d in details_regular[:5]:
        print("\n  Plate: {} | Owner: {}".format(d['plate'], d['owner_region']))
        print("    NIK: {} | Code: {}".format(d['nik'], d['code']))
        print("    Admin District: {} | Status: {}".format(d['admin_name'], d['status']))
    
    print("\nSpecial Plate Samples:")
    for d in details_special[:5]:
        print("\n  Plate: {} | Owner: {}".format(d['plate'], d['owner_region']))
        print("    NIK: {} | Code: {}".format(d['nik'], d['code']))
        print("    Admin District: {} | Status: {}".format(d['admin_name'], d['status']))
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_regular = len(regular_plates)
    total_special = len(special_plates)
    total = total_regular + total_special
    
    regular_alignment = 100 * found_in_admin / len(details_regular) if details_regular else 0
    special_alignment = 100 * special_found / len(details_special) if details_special else 0
    
    print("\nRegular Plates (Non-diplomatic):")
    print("  Alignment rate: {:.1f}% ({}/{})".format(regular_alignment, found_in_admin, len(details_regular)))
    print("  Status: {}".format("PASS" if regular_alignment >= 90 else "NEEDS REVIEW"))
    
    print("\nSpecial Plates (Diplomatic/Government):")
    print("  Alignment rate: {:.1f}% ({}/{})".format(special_alignment, special_found, len(details_special)))
    print("  Note: Special plates may use independent NIK codes")
    
    print("\nConclusion:")
    if regular_alignment >= 90:
        print("  [PASS] Regular plates have good NIK alignment (>=90%)")
    else:
        print("  [REVIEW] Regular plates need alignment review (<90%)")
    
    return True

if __name__ == '__main__':
    analyze_alignment()
