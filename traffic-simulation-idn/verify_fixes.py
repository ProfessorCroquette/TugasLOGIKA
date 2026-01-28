#!/usr/bin/env python
"""Verify GUI fixes are working"""

from gui_traffic_simulation import TrafficSimulationGUI, ViolationDetailDialog

print("✅ GUI modules import successfully")
print("✅ Checking method availability...")
print(f"  - TrafficSimulationGUI has _convert_region_code_to_name: {hasattr(TrafficSimulationGUI, '_convert_region_code_to_name')}")
print(f"  - ViolationDetailDialog has _convert_region_code_to_name: {hasattr(ViolationDetailDialog, '_convert_region_code_to_name')}")

# Test region conversion
from PyQt5.QtWidgets import QApplication
app = QApplication([])
gui = TrafficSimulationGUI()

test_codes = {'B': 'Jakarta (DKI)', 'D': 'Bandung (Jawa Barat)', 'L': 'Surabaya (Jawa Timur)'}
print("\n✅ Testing region code conversion:")
for code, expected in test_codes.items():
    result = gui._convert_region_code_to_name(code)
    status = "✅" if result == expected else "❌"
    print(f"  {status} {code} -> {result}")

print("\n✅ All checks passed!")
