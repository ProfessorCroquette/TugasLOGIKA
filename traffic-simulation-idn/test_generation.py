#!/usr/bin/env python3
"""Test vehicle batch generation"""
from utils.generators import DataGenerator

batch = DataGenerator.generate_vehicle_batch()
print(f"Generated {len(batch)} vehicles")
if batch:
    v = batch[0]
    print(f"First vehicle: {v.vehicle_id}")
    print(f"  Type: {v.vehicle_type}")
    print(f"  Plate: {v.license_plate}")
    print(f"  Speed: {v.speed} km/h")
