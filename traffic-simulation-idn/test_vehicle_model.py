#!/usr/bin/env python3
"""Test vehicle generation through the data models"""

from data_models.models import Vehicle
from utils.indonesian_plates import IndonesianPlateManager, OwnerDatabase

owner_db = OwnerDatabase()

print('Testing Vehicle model with plate-owner sync...\n')
print('='*70)

# Generate 20 vehicles
mismatches = 0
vehicles_tested = 0

for i in range(20):
    # Generate a plate
    plate, region, sub_region, vehicle_type = IndonesianPlateManager.generate_plate()
    
    # Get owner
    owner = owner_db.get_or_create_owner(plate)
    
    # Create vehicle (mimicking what the system does)
    vehicle = Vehicle(
        vehicle_id=f"vehicle_{i}",
        license_plate=plate,
        vehicle_type=vehicle_type,
        owner_id=owner.owner_id,
        owner_name=owner.name,
        owner_region=owner.region,
        stnk_status=owner.get_stnk_status_display(),
        sim_status=owner.get_sim_status_display(),
        speed=60.0,
        timestamp=owner.registration_date
    )
    
    # Check sync
    plate_code = plate.split()[0]
    expected_province = IndonesianPlateManager.PLATE_DATA.get(plate_code, {}).get('province_code')
    actual_province = owner.owner_id[:2]
    
    vehicles_tested += 1
    
    if actual_province != expected_province:
        mismatches += 1
        print(f'✗ {i+1}. Plate: {plate}, Owner: {owner.name}')
        print(f'   Expected province: {expected_province}, Got: {actual_province}')
    else:
        print(f'✓ {i+1}. Plate: {plate} → NIK province {actual_province}')

print()
print('='*70)
print(f'Results: {vehicles_tested - mismatches}/{vehicles_tested} PASS')
if mismatches == 0:
    print('✓ Vehicle model synchronization: WORKING CORRECTLY')
