"""Truck database for realistic heavy vehicle models"""

import random
from typing import Dict, List

class TruckDatabase:
    """Manage truck models and their specifications"""
    
    def __init__(self):
        self.trucks = self._load_trucks()
    
    def _load_trucks(self) -> List[Dict]:
        """Load truck database"""
        return [
            # DAF Trucks
            {"manufacturer": "DAF", "model": "XF105", "cabin": "Space Cab Plus", "category": "Barang (K)", "engine": "360-510 hp", "year": 2012},
            {"manufacturer": "DAF", "model": "XF Euro 6", "cabin": "Space Aero", "category": "Barang (K)", "engine": "370-530 hp", "year": 2014},
            {"manufacturer": "DAF", "model": "XG", "cabin": "Space", "category": "Barang (K)", "engine": "367-530 hp", "year": 2021},
            {"manufacturer": "DAF", "model": "XD", "cabin": "Day Cab", "category": "Barang (K)", "engine": "299-449 hp", "year": 2023},
            {"manufacturer": "DAF", "model": "XF Electric", "cabin": "Sleeper High", "category": "Barang (K)", "engine": "415 hp", "year": 2025},
            
            # Iveco Trucks
            {"manufacturer": "Iveco", "model": "Stralis", "cabin": "Active Space", "category": "Barang (K)", "engine": "310-560 hp", "year": 2012},
            {"manufacturer": "Iveco", "model": "Stralis Hi-Way", "cabin": "Hi-Way", "category": "Barang (K)", "engine": "310-560 hp", "year": 2013},
            {"manufacturer": "Iveco", "model": "S-Way", "cabin": "Active Space", "category": "Barang (K)", "engine": "460-580 hp", "year": 2024},
            
            # MAN Trucks
            {"manufacturer": "MAN", "model": "TGX TG1", "cabin": "XL", "category": "Barang (K)", "engine": "320-680 hp", "year": 2012},
            {"manufacturer": "MAN", "model": "TGX TG2", "cabin": "Standard", "category": "Barang (K)", "engine": "330-640 hp", "year": 2019},
            {"manufacturer": "MAN", "model": "TGX TG3", "cabin": "GM", "category": "Barang (K)", "engine": "330-640 hp", "year": 2023},
            
            # Mercedes-Benz Trucks
            {"manufacturer": "Mercedes-Benz", "model": "Actros MP3", "cabin": "Low Roof Sleeper", "category": "Barang (K)", "engine": "320-598 hp", "year": 2012},
            {"manufacturer": "Mercedes-Benz", "model": "Actros MP4", "cabin": "BigSpace", "category": "Barang (K)", "engine": "421-625 hp", "year": 2015},
            
            # Renault Trucks
            {"manufacturer": "Renault", "model": "Magnum", "cabin": "Excellence", "category": "Barang (K)", "engine": "440-520 hp", "year": 2012},
            {"manufacturer": "Renault", "model": "Premium", "cabin": "High Roof", "category": "Barang (K)", "engine": "380-460 hp", "year": 2012},
            {"manufacturer": "Renault", "model": "T-Range", "cabin": "High Sleeper", "category": "Barang (K)", "engine": "380-520 hp", "year": 2019},
            {"manufacturer": "Renault", "model": "E-Tech T Electric", "cabin": "Sleeper", "category": "Barang (K)", "engine": "450-666 hp", "year": 2024},
            
            # Scania Trucks
            {"manufacturer": "Scania", "model": "R 2009", "cabin": "Topline", "category": "Barang (K)", "engine": "360-730 hp", "year": 2012},
            {"manufacturer": "Scania", "model": "Streamline", "cabin": "Standard", "category": "Barang (K)", "engine": "370-730 hp", "year": 2013},
            {"manufacturer": "Scania", "model": "R 2016", "cabin": "High Roof", "category": "Barang (K)", "engine": "370-770 hp", "year": 2017},
            {"manufacturer": "Scania", "model": "S", "cabin": "High Roof", "category": "Barang (K)", "engine": "540-610 hp", "year": 2024},
            {"manufacturer": "Scania", "model": "S Electric", "cabin": "High Roof", "category": "Barang (K)", "engine": "540-610 hp", "year": 2024},
            
            # Volvo Trucks
            {"manufacturer": "Volvo", "model": "FH Series 3", "cabin": "Globetrotter", "category": "Barang (K)", "engine": "420-750 hp", "year": 2012},
            {"manufacturer": "Volvo", "model": "FH Series 4", "cabin": "Standard", "category": "Barang (K)", "engine": "420-750 hp", "year": 2013},
            {"manufacturer": "Volvo", "model": "FH Series 5", "cabin": "Sleeper", "category": "Barang (K)", "engine": "420-750 hp", "year": 2024},
            {"manufacturer": "Volvo", "model": "FH Series 6", "cabin": "Globetrotter XL", "category": "Barang (K)", "engine": "420-780 hp", "year": 2024},
        ]
    
    def get_random_truck(self) -> Dict:
        """Get a random truck model"""
        if not self.trucks:
            return {
                'make': 'Unknown',
                'model': 'Unknown',
                'cabin': 'Standard',
                'category': 'Barang (K)',
                'engine': 'Unknown'
            }
        
        truck = random.choice(self.trucks)
        return {
            'make': truck['manufacturer'],
            'model': truck['model'],
            'cabin': truck['cabin'],
            'category': truck['category'],
            'engine': truck['engine']
        }
    
    def get_truck_for_plate(self) -> Dict:
        """Get truck info formatted for display"""
        truck = self.get_random_truck()
        return {
            'make': truck['make'],
            'model': truck['model'],
            'category': truck['category']  # 'Barang (K)' for commercial goods
        }
    
    def get_trucks_by_manufacturer(self, manufacturer: str) -> List[Dict]:
        """Get all trucks by manufacturer"""
        return [t for t in self.trucks if t['manufacturer'].lower() == manufacturer.lower()]
    
    def get_all_manufacturers(self) -> List[str]:
        """Get all truck manufacturers"""
        return sorted(list(set(t['manufacturer'] for t in self.trucks)))
    
    def get_statistics(self) -> Dict:
        """Get truck database statistics"""
        manufacturers = {}
        for truck in self.trucks:
            mfg = truck['manufacturer']
            manufacturers[mfg] = manufacturers.get(mfg, 0) + 1
        
        return {
            'total_trucks': len(self.trucks),
            'total_manufacturers': len(set(t['manufacturer'] for t in self.trucks)),
            'by_manufacturer': manufacturers,
            'manufacturers': self.get_all_manufacturers()
        }


if __name__ == "__main__":
    # Test the database
    db = TruckDatabase()
    
    print("\n[*] Truck Database Statistics")
    print("=" * 60)
    
    stats = db.get_statistics()
    print(f"Total Trucks: {stats['total_trucks']}")
    print(f"Total Manufacturers: {stats['total_manufacturers']}")
    
    print(f"\nTrucks by Manufacturer:")
    for mfg, count in sorted(stats['by_manufacturer'].items()):
        print(f"  {mfg}: {count}")
    
    # Get random truck
    print(f"\n[*] Random Truck Examples:")
    for i in range(3):
        truck = db.get_random_truck()
        print(f"  {truck['make']} {truck['model']} - {truck['cabin']} - Category: {truck['category']}")
