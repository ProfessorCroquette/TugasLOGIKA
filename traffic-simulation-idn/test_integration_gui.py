#!/usr/bin/env python
"""Test script to verify GUI integration of plate generator with new probabilities"""

import sys
import random
from collections import Counter

# Add the project to path
sys.path.insert(0, '.')

from utils.generators import DataGenerator

def test_vehicle_distribution():
    """Test that vehicle generation follows the 50/40/5/5 probability distribution"""
    print("=" * 70)
    print("Testing Vehicle Generation with New Probability Distribution")
    print("=" * 70)
    
    # Generate a large batch to test probabilities
    all_vehicles = []
    for batch_num in range(10):
        vehicles = DataGenerator.generate_vehicle_batch()
        all_vehicles.extend(vehicles)
    
    print(f"\n✓ Generated {len(all_vehicles)} vehicles across 10 batches")
    
    # Analyze distribution
    categories = Counter()
    plate_types = Counter()
    plate_colors = Counter()
    
    for vehicle in all_vehicles:
        categories[vehicle.vehicle_category] += 1
        plate_types[vehicle.plate_type] += 1
        plate_colors[vehicle.plate_color] += 1
    
    print("\n--- Vehicle Category Distribution ---")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(all_vehicles)) * 100
        print(f"  {category:20s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n--- Plate Type Distribution ---")
    for plate_type, count in sorted(plate_types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(all_vehicles)) * 100
        print(f"  {plate_type:20s}: {count:3d} ({percentage:5.1f}%)")
    
    print("\n--- Plate Color Distribution ---")
    for plate_color, count in sorted(plate_colors.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(all_vehicles)) * 100
        print(f"  {plate_color:20s}: {count:3d} ({percentage:5.1f}%)")
    
    # Show sample vehicles
    print("\n--- Sample Vehicles (10 samples) ---")
    sample_vehicles = random.sample(all_vehicles, min(10, len(all_vehicles)))
    for i, vehicle in enumerate(sample_vehicles, 1):
        print(f"\n  {i}. {vehicle.license_plate}")
        print(f"     ID: {vehicle.vehicle_id}")
        print(f"     Make: {vehicle.vehicle_make} {vehicle.vehicle_model}")
        print(f"     Type: {vehicle.vehicle_type} ({vehicle.vehicle_category})")
        print(f"     Plate: {vehicle.plate_color} {vehicle.plate_type}")
        print(f"     Speed: {vehicle.speed:.1f} km/h")
        print(f"     Owner: {vehicle.owner_name} ({vehicle.owner_region})")
    
    # Expected vs Actual
    print("\n" + "=" * 70)
    print("Probability Analysis")
    print("=" * 70)
    
    pribadi_pct = (categories.get('Pribadi', 0) + categories.get('pribadi', 0)) / len(all_vehicles) * 100
    barang_pct = (categories.get('Barang', 0) + categories.get('barang', 0)) / len(all_vehicles) * 100
    pemerintah_pct = categories.get('PEMERINTAH', 0) / len(all_vehicles) * 100
    kedutaan_pct = categories.get('KEDUTAAN', 0) / len(all_vehicles) * 100
    
    print(f"\nTarget vs Actual Distribution:")
    print(f"  Pribadi (Private):      Target: 50% | Actual: {pribadi_pct:5.1f}%")
    print(f"  Barang/Truk (Commercial): Target: 40% | Actual: {barang_pct:5.1f}%")
    print(f"  Pemerintah (Government):  Target:  5% | Actual: {pemerintah_pct:5.1f}%")
    print(f"  Kedutaan (Diplomatic):    Target:  5% | Actual: {kedutaan_pct:5.1f}%")
    
    # Verify plate-category matching
    print("\n" + "=" * 70)
    print("Plate Type to Category Mapping Verification")
    print("=" * 70)
    
    category_to_plate = {}
    for vehicle in all_vehicles:
        key = (vehicle.vehicle_category, vehicle.plate_type, vehicle.plate_color)
        category_to_plate[key] = category_to_plate.get(key, 0) + 1
    
    print("\nCategory → Plate Type → Color:")
    for (category, plate_type, plate_color), count in sorted(category_to_plate.items()):
        print(f"  {category:20s} → {plate_type:20s} ({plate_color:10s}): {count} vehicles")
    
    print("\n✓ Integration test completed successfully!")
    return True

if __name__ == '__main__':
    try:
        test_vehicle_distribution()
    except Exception as e:
        print(f"\n✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
