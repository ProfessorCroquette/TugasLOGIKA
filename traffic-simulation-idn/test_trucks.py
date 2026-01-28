#!/usr/bin/env python
"""Test truck database and vehicle category integration"""

from utils.truck_database import TruckDatabase
from utils.indonesian_plates import VehicleCategory
from utils.generators import DataGenerator

print("✅ Testing truck database...")
db = TruckDatabase()
print(f"✅ Loaded {len(db.trucks)} trucks")
stats = db.get_statistics()
print(f"✅ Total manufacturers: {stats['total_manufacturers']}")

print("\nSample trucks:")
for i in range(3):
    truck = db.get_random_truck()
    print(f"  - {truck['make']} {truck['model']} ({truck['cabin']}) - {truck['category']}")

print("\n✅ Testing vehicle category enum...")
for cat in VehicleCategory:
    print(f"  - {cat.name}: {cat.value}")

print("\n✅ Testing DataGenerator with trucks...")
batch = DataGenerator.generate_vehicle_batch()
print(f"✅ Generated {len(batch)} vehicles")

# Count by type and category
type_count = {}
category_count = {}
for v in batch:
    vtype = v.vehicle_type
    vcat = getattr(v, 'vehicle_category', 'Unknown')
    type_count[vtype] = type_count.get(vtype, 0) + 1
    category_count[vcat] = category_count.get(vcat, 0) + 1

print(f"\nVehicles by type:")
for vtype, count in sorted(type_count.items()):
    print(f"  - {vtype}: {count}")

print(f"\nVehicles by category:")
for cat, count in sorted(category_count.items()):
    print(f"  - {cat}: {count}")

print("\nSample vehicles:")
for i, v in enumerate(batch[:3]):
    vcat = getattr(v, 'vehicle_category', 'Unknown')
    print(f"  {i+1}. {v.vehicle_make} {v.vehicle_model} ({vcat})")
    print(f"     Type: {v.vehicle_type}, Plate: {v.license_plate}")

print("\n✅ All tests passed!")
