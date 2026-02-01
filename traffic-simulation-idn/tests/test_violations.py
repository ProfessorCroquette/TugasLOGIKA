#!/usr/bin/env python3
"""Quick test to verify slow and speeding violations are generated"""

import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from utils.generators import DataGenerator
from simulation.analyzer import SpeedAnalyzer
from data_models.storage import DataStorage
import queue
from datetime import datetime

def test_violations():
    """Generate and analyze violations"""
    print("=" * 70)
    print("TESTING VIOLATION GENERATION")
    print("=" * 70)
    
    # Generate multiple batches
    all_violations = []
    storage = DataStorage()
    
    print("\nGenerating 500 vehicles to test...")
    
    for batch_num in range(5):
        # Generate a batch
        vehicles = DataGenerator.generate_vehicle_batch()
        
        # Analyze with tolerance
        SPEEDING_TOLERANCE = 0.9
        
        slow_vehicles = []
        speeding_vehicles = []
        safe_vehicles = []
        
        for v in vehicles:
            if v.speed < Config.MIN_SPEED_LIMIT:
                slow_vehicles.append(v)
            elif v.speed > (Config.SPEED_LIMIT + SPEEDING_TOLERANCE):
                speeding_vehicles.append(v)
            else:
                safe_vehicles.append(v)
        
        print(f"\nBatch {batch_num + 1}:")
        print(f"  Safe vehicles: {len(safe_vehicles)}")
        print(f"  Speeding vehicles: {len(speeding_vehicles)}")
        print(f"  Slow vehicles: {len(slow_vehicles)}")
        
        # Show sample slow vehicles
        if slow_vehicles:
            print(f"    Sample slow vehicles:")
            for sv in slow_vehicles[:3]:
                print(f"      - {sv.license_plate}: {sv.speed} km/h (Min: {Config.MIN_SPEED_LIMIT})")
        
        # Show sample speeding vehicles
        if speeding_vehicles:
            print(f"    Sample speeding vehicles:")
            for spv in speeding_vehicles[:3]:
                print(f"      - {spv.license_plate}: {spv.speed} km/h (Limit: {Config.SPEED_LIMIT})")
        
        all_violations.extend(slow_vehicles)
        all_violations.extend(speeding_vehicles)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    slow_count = sum(1 for v in all_violations if v.speed < Config.MIN_SPEED_LIMIT)
    speeding_count = sum(1 for v in all_violations if v.speed > (Config.SPEED_LIMIT + 0.9))
    
    print(f"Total slow violations: {slow_count}")
    print(f"Total speeding violations: {speeding_count}")
    print(f"Expected ~8% slow, ~10% speeding out of generated vehicles")
    
    # Check JSON output
    print("\nChecking data_files/tickets.json...")
    tickets_file = Path("data_files/tickets.json")
    if tickets_file.exists():
        with open(tickets_file, 'r') as f:
            try:
                tickets = json.load(f)
                slow_in_json = sum(1 for t in tickets if t.get('speed', 0) < Config.MIN_SPEED_LIMIT)
                speeding_in_json = sum(1 for t in tickets if t.get('speed', 0) > (Config.SPEED_LIMIT + 0.9))
                print(f"  Tickets in JSON: {len(tickets)}")
                print(f"  Slow tickets: {slow_in_json}")
                print(f"  Speeding tickets: {speeding_in_json}")
                
                # Show sample
                if slow_in_json > 0:
                    slow_ticket = next((t for t in tickets if t.get('speed', 0) < Config.MIN_SPEED_LIMIT), None)
                    if slow_ticket:
                        print(f"\n  Sample slow ticket:")
                        print(f"    Plate: {slow_ticket.get('license_plate')}")
                        print(f"    Speed: {slow_ticket.get('speed')} km/h")
                        print(f"    Fine: ${slow_ticket.get('fine_amount')}")
            except json.JSONDecodeError:
                print("  ERROR: tickets.json is empty or malformed")
    else:
        print("  tickets.json does not exist yet")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_violations()
