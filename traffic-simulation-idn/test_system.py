#!/usr/bin/env python
"""
Test script to validate the traffic simulation system
Run this to check if all components are working correctly
"""

import os
import sys
import json
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from config import Config
        from data_models.models import Vehicle, Ticket, TrafficStats
        from data_models.storage import DataStorage
        from utils.generators import DataGenerator
        from utils.logger import logger
        from simulation.sensor import TrafficSensor
        from simulation.analyzer import SpeedAnalyzer
        from dashboard.display import Dashboard
        print("✅ All imports successful\n")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}\n")
        return False

def test_config():
    """Test configuration"""
    print("🔍 Testing configuration...")
    try:
        from config import Config
        
        # Check key settings
        assert Config.SPEED_LIMIT == 75, "Speed limit not set correctly"
        assert Config.SIMULATION_INTERVAL == 10, "Simulation interval not set correctly"
        assert len(Config.VEHICLE_TYPES) > 0, "Vehicle types not defined"
        assert len(Config.FINES) == 4, "Fines not properly configured"
        
        print("✅ Configuration OK")
        print(f"   Speed Limit: {Config.SPEED_LIMIT} km/h")
        print(f"   Simulation Interval: {Config.SIMULATION_INTERVAL}s")
        print(f"   Vehicle Types: {list(Config.VEHICLE_TYPES.keys())}")
        print(f"   Fine Levels: {list(Config.FINES.keys())}\n")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}\n")
        return False

def test_directories():
    """Test directory creation"""
    print("🔍 Testing directories...")
    try:
        from config import Config
        Config.setup_directories()
        
        # Check if directories exist
        assert os.path.exists(Config.LOGS_DIR), f"Logs directory not created: {Config.LOGS_DIR}"
        assert os.path.exists(Config.DATA_DIR), f"Data directory not created: {Config.DATA_DIR}"
        
        print("✅ Directories created successfully")
        print(f"   Logs: {Config.LOGS_DIR}")
        print(f"   Data: {Config.DATA_DIR}\n")
        return True
    except Exception as e:
        print(f"❌ Directory error: {e}\n")
        return False

def test_data_generation():
    """Test data generation"""
    print("🔍 Testing data generation...")
    try:
        from utils.generators import DataGenerator
        
        # Generate sample data
        plate = DataGenerator.generate_license_plate()
        vehicle_type = DataGenerator.generate_vehicle_type()
        speed = DataGenerator.generate_speed(vehicle_type)
        fine = DataGenerator.calculate_fine(speed)
        
        # Validate
        assert len(plate.split()) == 2, "Invalid license plate format"
        assert vehicle_type in ["car", "truck", "motorcycle", "bus"], "Invalid vehicle type"
        assert 30 <= speed <= 140, f"Speed out of bounds: {speed}"
        assert fine >= 0, "Invalid fine amount"
        
        print("✅ Data generation OK")
        print(f"   Sample Plate: {plate}")
        print(f"   Sample Type: {vehicle_type}")
        print(f"   Sample Speed: {speed} km/h")
        print(f"   Sample Fine: ${fine}\n")
        return True
    except Exception as e:
        print(f"❌ Data generation error: {e}\n")
        return False

def test_models():
    """Test data models"""
    print("🔍 Testing data models...")
    try:
        from datetime import datetime
        from data_models.models import Vehicle, Ticket, TrafficStats
        
        # Create vehicle
        vehicle = Vehicle(
            vehicle_id="TEST-001",
            license_plate="ABC 123",
            vehicle_type="car",
            speed=85.5,
            timestamp=datetime.now()
        )
        assert vehicle.vehicle_id == "TEST-001"
        assert vehicle.fine_amount == 0.0
        
        # Create ticket
        ticket = Ticket(
            license_plate="ABC 123",
            vehicle_type="car",
            speed=85.5,
            fine_amount=200.0
        )
        assert ticket.license_plate == "ABC 123"
        assert ticket.fine_amount == 200.0
        
        # Create stats
        stats = TrafficStats(
            period_start=datetime.now(),
            period_end=datetime.now(),
            total_vehicles=10,
            speeding_count=2
        )
        assert stats.total_vehicles == 10
        assert stats.speeding_count == 2
        
        print("✅ Models OK")
        print(f"   Vehicle: {vehicle.vehicle_id} - {vehicle.license_plate}")
        print(f"   Ticket: {ticket.license_plate} - Fine: ${ticket.fine_amount}")
        print(f"   Stats: {stats.total_vehicles} vehicles, {stats.speeding_count} speeding\n")
        return True
    except Exception as e:
        print(f"❌ Models error: {e}\n")
        return False

def test_storage():
    """Test storage system"""
    print("🔍 Testing storage...")
    try:
        from datetime import datetime
        from data_models.storage import DataStorage
        from data_models.models import Vehicle, Ticket, TrafficStats
        
        storage = DataStorage()
        
        # Create test data
        vehicle = Vehicle(
            vehicle_id="TEST-001",
            license_plate="ABC 123",
            vehicle_type="car",
            speed=85.5,
            timestamp=datetime.now()
        )
        
        ticket = Ticket(
            license_plate="ABC 123",
            vehicle_type="car",
            speed=85.5,
            fine_amount=200.0
        )
        
        # Save data
        storage.save_vehicles([vehicle])
        storage.save_tickets([ticket])
        
        stats = TrafficStats(
            period_start=datetime.now(),
            period_end=datetime.now(),
            total_vehicles=1,
            speeding_count=1,
            total_fines=200.0
        )
        storage.save_statistics(stats)
        
        # Verify saved
        vehicles = storage.get_all_vehicles()
        tickets = storage.get_all_tickets()
        
        assert len(vehicles) > 0, "Vehicles not saved"
        assert len(tickets) > 0, "Tickets not saved"
        
        print("✅ Storage OK")
        print(f"   Vehicles saved: {len(vehicles)}")
        print(f"   Tickets saved: {len(tickets)}")
        print(f"   Files:")
        print(f"     - {storage.traffic_file}")
        print(f"     - {storage.tickets_file}")
        print(f"     - {storage.stats_file}\n")
        return True
    except Exception as e:
        print(f"❌ Storage error: {e}\n")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("   TRAFFIC SIMULATION SYSTEM - VALIDATION TEST")
    print("=" * 60 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Directories": test_directories(),
        "Data Generation": test_data_generation(),
        "Models": test_models(),
        "Storage": test_storage(),
    }
    
    # Summary
    print("=" * 60)
    print("   TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nRun the simulation with:")
        print("   python main.py\n")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
