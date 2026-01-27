"""Motorcycle database loader for realistic motorcycle models"""

import csv
import random
from pathlib import Path


class MotorcycleDatabase:
    """Load and manage motorcycle models from CSV"""
    
    def __init__(self, csv_file="model.csv"):
        self.models = []
        self.manufacturers = {
            1: "Honda",
            2: "Suzuki",
            3: "Yamaha",
            4: "Kawasaki",
            5: "Harley-Davidson",
            6: "BMW",
            7: "KTM",
            8: "Ducati",
            9: "Triumph",
            10: "Royal Enfield"
        }
        self.load_models(csv_file)
    
    def load_models(self, csv_file):
        """Load motorcycle models from CSV file"""
        csv_path = Path(csv_file)
        
        if not csv_path.exists():
            print(f"Warning: {csv_file} not found, using defaults")
            self.models = [
                ("Honda", "CB500X"),
                ("Suzuki", "GSX-R600"),
                ("Yamaha", "YZF-R6"),
                ("Kawasaki", "Ninja 400"),
                ("Harley-Davidson", "Street 500")
            ]
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        mfg_id = int(row[0])
                        model_name = row[1].strip()
                        
                        manufacturer = self.manufacturers.get(mfg_id, f"Manufacturer {mfg_id}")
                        self.models.append((manufacturer, model_name))
            
            print(f"Loaded {len(self.models)} motorcycle models from {csv_file}")
        except Exception as e:
            print(f"Error loading motorcycle database: {e}")
            self.models = []
    
    def get_random_motorcycle(self):
        """Get a random motorcycle model"""
        if not self.models:
            return {
                'make': 'Unknown',
                'model': 'Unknown'
            }
        
        make, model = random.choice(self.models)
        return {
            'make': make,
            'model': model
        }
    
    def get_motorcycle_for_plate(self):
        """Get motorcycle info formatted for display"""
        moto = self.get_random_motorcycle()
        return f"{moto['make']} {moto['model']}"
