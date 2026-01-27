#!/usr/bin/env python3
"""Test fine calculation"""
from utils.generators import DataGenerator

# Test various speeds
speeds_to_test = [30, 50, 60, 80, 100]

print("Testing fine calculations:")
for speed in speeds_to_test:
    base_fine, multiplier, total_fine = DataGenerator.calculate_fine(speed)
    print(f"  Speed {speed} km/h: Base=${base_fine}, Multiplier={multiplier}, Total=${total_fine}")
