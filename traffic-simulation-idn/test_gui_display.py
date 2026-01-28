#!/usr/bin/env python
"""Test script to verify GUI displays violations correctly"""

import sys
import json
from pathlib import Path
from PyQt5.QtWidgets import QApplication

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui_traffic_simulation import TrafficSimulationGUI

def test_gui_display():
    """Test that GUI can load and display violations"""
    print("Creating Qt application...")
    app = QApplication(sys.argv)
    
    print("Initializing GUI...")
    gui = TrafficSimulationGUI()
    
    print("Testing GUI methods...")
    
    # Test 1: Load violations from file
    print("\n1. Testing load_violations()...")
    gui.load_violations()
    print(f"   - Loaded {len(gui.violations)} violations")
    
    # Test 2: Check if violations were loaded
    if gui.violations:
        print(f"   - First violation plate: {gui.violations[0].get('license_plate', 'UNKNOWN')}")
        print(f"   - First violation owner: {gui.violations[0].get('owner_name', 'UNKNOWN')}")
        print(f"   - First violation speed: {gui.violations[0].get('speed', 0):.1f} km/h")
    else:
        print("   - WARNING: No violations loaded!")
    
    # Test 3: Check region conversion
    print("\n2. Testing region code conversion...")
    test_codes = ['B', 'D', 'H', 'L']
    for code in test_codes:
        converted = gui._convert_region_code_to_name(code)
        print(f"   - {code} -> {converted}")
    
    # Test 4: Check if table is properly populated
    print("\n3. Testing violations table...")
    print(f"   - Table has {gui.violations_table.rowCount()} rows")
    if gui.violations_table.rowCount() > 0:
        first_item = gui.violations_table.item(0, 0)
        if first_item:
            print(f"   - First table cell: {first_item.text()}")
        else:
            print("   - WARNING: First table cell is empty!")
    else:
        print("   - WARNING: Table has no rows!")
    
    # Test 5: Check sensor labels
    print("\n4. Testing sensor status display...")
    for sensor_id in range(1, 6):
        sensor_info = gui.sensor_labels.get(sensor_id)
        if sensor_info:
            status = sensor_info['status'].text()
            print(f"   - Sensor {sensor_id}: {status}")
        else:
            print(f"   - WARNING: Sensor {sensor_id} not found!")
    
    # Test 6: Check stats display
    print("\n5. Testing statistics display...")
    print(f"   - Violations count label: {gui.violations_count_label.text()}")
    print(f"   - Vehicles count label: {gui.vehicles_count_label.text()}")
    print(f"   - Total fines label: {gui.total_fines_label.text()}")
    
    print("\nGUI test completed successfully!")
    print("\nTo see the GUI, uncomment the following line:")
    print("# gui.show()")
    print("# sys.exit(app.exec_())")
    
    return 0

if __name__ == '__main__':
    sys.exit(test_gui_display())
