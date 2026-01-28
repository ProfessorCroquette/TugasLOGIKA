#!/usr/bin/env python
"""Test random digit plate generation"""

from utils.indonesian_plates import IndonesianPlateManager, VehicleType

print("✅ Testing random digit plate generation...\n")

print("Motorcycles (Roda Dua) - 1-2 letter owner codes:")
for i in range(6):
    plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_DUA)
    print(f"  {i+1}. {plate} -> {region} / {sub}")

print("\nCars (Roda Empat) - 2-3 letter owner codes:")
for i in range(6):
    plate, region, sub, vtype = IndonesianPlateManager.generate_plate(VehicleType.RODA_EMPAT_LEBIH)
    print(f"  {i+1}. {plate} -> {region} / {sub}")

print("\n✅ Analysis of number digits distribution:")
digit_count = {2: 0, 3: 0, 4: 0}
for _ in range(300):
    plate, _, _, _ = IndonesianPlateManager.generate_plate()
    number = plate.split()[1]
    num_digits = len(number)
    digit_count[num_digits] += 1

total = sum(digit_count.values())
for digits, count in sorted(digit_count.items()):
    percentage = (count / total) * 100
    print(f"  {digits}-digit numbers: {count} ({percentage:.1f}%)")

print("\n✅ Test completed!")
