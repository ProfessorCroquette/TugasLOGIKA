from utils.generators import DataGenerator
from config import Config

print("=== Testing Violation Generation ===\n")

# Test car speeds
print("CARS (60-100 km/h legal limit)")
cars = [DataGenerator.generate_speed('car') for _ in range(50)]
cars_legal = [s for s in cars if 60 <= s <= 100]
cars_slow = [s for s in cars if s < 60]
cars_speeding = [s for s in cars if s > 100]

print(f"  Total: {len(cars)}")
print(f"  Legal (60-100): {len(cars_legal)} ({len(cars_legal)*100//len(cars)}%)")
print(f"  Too slow (<60): {len(cars_slow)} ({len(cars_slow)*100//len(cars)}%)")
print(f"  Speeding (>100): {len(cars_speeding)} ({len(cars_speeding)*100//len(cars)}%)")
print(f"  Speed range: {min(cars):.1f}-{max(cars):.1f} km/h")
if cars_speeding:
    print(f"  Examples speeding: {sorted(cars_speeding)[:5]}")

print("\nTRUCKS (60-80 km/h legal limit)")
trucks = [DataGenerator.generate_speed('truck') for _ in range(50)]
trucks_legal = [s for s in trucks if 60 <= s <= 80]
trucks_slow = [s for s in trucks if s < 60]
trucks_speeding = [s for s in trucks if s > 80]

print(f"  Total: {len(trucks)}")
print(f"  Legal (60-80): {len(trucks_legal)} ({len(trucks_legal)*100//len(trucks)}%)")
print(f"  Too slow (<60): {len(trucks_slow)} ({len(trucks_slow)*100//len(trucks)}%)")
print(f"  Speeding (>80): {len(trucks_speeding)} ({len(trucks_speeding)*100//len(trucks)}%)")
print(f"  Speed range: {min(trucks):.1f}-{max(trucks):.1f} km/h")
if trucks_speeding:
    print(f"  Examples speeding: {sorted(trucks_speeding)[:5]}")
    print(f"  Speeding 10-20km over (90-100): {[s for s in trucks_speeding if 90 <= s <= 100]}")
