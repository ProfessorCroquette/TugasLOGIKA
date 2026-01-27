#!/usr/bin/env python3
"""Test license plate generation"""
from utils.indonesian_plates import IndonesianPlateManager

print("Generating 10 license plates:")
for i in range(10):
    plate, region = IndonesianPlateManager.generate_plate()
    print(f"  {plate} - {region}")
