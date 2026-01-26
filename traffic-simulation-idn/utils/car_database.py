#!/usr/bin/env python
"""
Vehicle Database Parser - Extracts vehicle data from CARS.md
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

class CarDatabase:
    """Parse and manage vehicle data from CARS.md"""
    
    def __init__(self, cars_md_path: str = "CARS.md"):
        self.cars_md_path = Path(cars_md_path)
        self.vehicles = []
        self.manufacturers = set()
        
        if self.cars_md_path.exists():
            self.parse_cars_md()
    
    def parse_cars_md(self):
        """Parse CARS.md and extract vehicle information"""
        with open(self.cars_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the table data (between first | and last |)
        lines = content.split('\n')
        
        # Find the table start
        table_start = None
        for i, line in enumerate(lines):
            if line.startswith('|Make|Model|Package|Support'):
                table_start = i + 2  # Skip header and separator
                break
        
        if not table_start:
            return
        
        # Parse each vehicle row
        for line in lines[table_start:]:
            if not line.startswith('|'):
                break
            
            # Parse: |Make|Model|Package|Support|
            parts = [p.strip() for p in line.split('|')[1:-1]]
            
            if len(parts) >= 3:
                make = parts[0]
                model = parts[1]
                package = parts[2]
                support = parts[3] if len(parts) > 3 else "Unknown"
                
                # Skip section headers
                if make in ['Make', '---']:
                    continue
                
                self.manufacturers.add(make)
                
                vehicle = {
                    'make': make,
                    'model': model,
                    'package': package,
                    'support_level': self._parse_support_level(support),
                    'weight': self._get_vehicle_weight(make, model)
                }
                
                self.vehicles.append(vehicle)
    
    def _parse_support_level(self, support_str: str) -> str:
        """Extract support level from support column"""
        support_str = support_str.lower()
        
        if 'upstream' in support_str:
            return 'Upstream'
        elif 'community' in support_str:
            return 'Community'
        elif 'custom' in support_str:
            return 'Custom'
        elif 'dashcam' in support_str:
            return 'Dashcam'
        else:
            return 'Not compatible'
    
    def _get_vehicle_weight(self, make: str, model: str) -> str:
        """Assign weight category based on make and model"""
        # Trucks and large vehicles
        heavy = ['truck', 'pickup', 'f-150', 'silverado', 'ram', 'sierra', 'tundra', 
                'highlander', 'sequoia', 'expedition', 'explorer', 'tahoe', 'suburban']
        
        # Cars
        cars = ['civic', 'accord', 'camry', 'corolla', 'prius', 'elantra', 'sonata', 
               'altima', 'maxima', 'jetta', 'passat', 'golf', 'a3', 'a4', 'a6']
        
        # Motorcycles (not in CARS.md but for reference)
        # motorcycles = []
        
        model_lower = model.lower()
        
        for vehicle in heavy:
            if vehicle in model_lower:
                return 'truck'
        
        for vehicle in cars:
            if vehicle in model_lower:
                return 'car'
        
        # Default to SUV/crossover for most models
        return 'suv'
    
    def get_random_vehicle(self) -> Dict:
        """Get a random vehicle from database"""
        import random
        if not self.vehicles:
            return None
        return random.choice(self.vehicles)
    
    def get_vehicles_by_make(self, make: str) -> List[Dict]:
        """Get all vehicles by manufacturer"""
        return [v for v in self.vehicles if v['make'].lower() == make.lower()]
    
    def get_vehicles_by_support(self, support_level: str) -> List[Dict]:
        """Get all vehicles by support level"""
        return [v for v in self.vehicles if v['support_level'] == support_level]
    
    def get_all_makes(self) -> List[str]:
        """Get all manufacturers"""
        return sorted(list(self.manufacturers))
    
    def export_json(self, output_path: str = "vehicles_database.json"):
        """Export vehicle database to JSON"""
        output = {
            'total_vehicles': len(self.vehicles),
            'total_manufacturers': len(self.manufacturers),
            'manufacturers': sorted(list(self.manufacturers)),
            'vehicles': self.vehicles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        support_counts = {}
        weight_counts = {}
        
        for vehicle in self.vehicles:
            # Count by support level
            support = vehicle['support_level']
            support_counts[support] = support_counts.get(support, 0) + 1
            
            # Count by weight
            weight = vehicle['weight']
            weight_counts[weight] = weight_counts.get(weight, 0) + 1
        
        return {
            'total_vehicles': len(self.vehicles),
            'total_manufacturers': len(self.manufacturers),
            'by_support_level': support_counts,
            'by_vehicle_type': weight_counts,
            'manufacturers': sorted(list(self.manufacturers))
        }


if __name__ == "__main__":
    # Test the database
    db = CarDatabase("CARS.md")
    
    print("\n[*] Vehicle Database Statistics")
    print("=" * 60)
    
    stats = db.get_statistics()
    print(f"Total Vehicles: {stats['total_vehicles']}")
    print(f"Total Manufacturers: {stats['total_manufacturers']}")
    
    print(f"\nVehicles by Support Level:")
    for level, count in sorted(stats['by_support_level'].items()):
        print(f"  {level}: {count}")
    
    print(f"\nVehicles by Type:")
    for vtype, count in sorted(stats['by_vehicle_type'].items()):
        print(f"  {vtype}: {count}")
    
    print(f"\nManufacturers ({len(stats['manufacturers'])}):")
    for make in stats['manufacturers'][:10]:
        print(f"  - {make}")
    if len(stats['manufacturers']) > 10:
        print(f"  ... and {len(stats['manufacturers']) - 10} more")
    
    # Export to JSON
    db.export_json()
    print(f"\n[+] Database exported to vehicles_database.json")
