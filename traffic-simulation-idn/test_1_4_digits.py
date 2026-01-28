#!/usr/bin/env python
"""Test 1-4 digit plate generation"""

from utils.indonesian_plates import IndonesianPlateManager, VehicleType

print("✅ Testing 1-4 digit plate generation...\n")

print("Motorcycles (Roda Dua) - 1-2 letter owner codes:")
for i in range(8):
    plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_DUA)
    print(f"  {i+1}. {plate} -> {region} / {sub}")

print("\nCars (Roda Empat) - 2-3 letter owner codes:")
for i in range(8):
    plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_EMPAT_LEBIH)
    print(f"  {i+1}. {plate} -> {region} / {sub}")

print("\n✅ Analysis of number digits distribution:")
digit_count = {1: 0, 2: 0, 3: 0, 4: 0}
for _ in range(400):
    plate, _, _, _ = IndonesianPlateManager.generate_plate()
    number = plate.split()[1]
    num_digits = len(number)
    digit_count[num_digits] += 1

total = sum(digit_count.values())
for digits in sorted(digit_count.keys()):
    count = digit_count[digits]
    percentage = (count / total) * 100
    print(f"  {digits}-digit numbers: {count} ({percentage:.1f}%)")

print("\n✅ Test completed!")
