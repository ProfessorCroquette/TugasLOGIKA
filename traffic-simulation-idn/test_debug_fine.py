#!/usr/bin/env python3
"""Debug fine calculation"""
from config import Config

# Test speed 80 (should be LEVEL_1)
speed = 80
print(f"Testing speed {speed} km/h")
print(f"SPEED_LIMIT: {Config.SPEED_LIMIT}")
print(f"speed > SPEED_LIMIT: {speed > Config.SPEED_LIMIT}")

# Check the fines dict
print(f"\nFINES structure:")
for level, details in Config.FINES.items():
    if "SPEED_HIGH" in level:
        print(f"  {level}: min={details.get('min')}, max={details.get('max')}, fine={details.get('fine')}")

# Now test manually
base_fine = 0.0
for level, details in Config.FINES.items():
    if "SPEED_HIGH" in level and details["min"] <= speed <= details["max"]:
        base_fine = details["fine"]
        print(f"\nFound match: {level}, fine={base_fine}")
        break
else:
    print(f"\nNo match found, using highest")
    base_fine = Config.FINES["SPEED_HIGH_LEVEL_3"]["fine"]

print(f"Final base_fine: {base_fine}")
