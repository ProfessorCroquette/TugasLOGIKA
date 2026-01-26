import random
import string
from datetime import datetime
from config import Config
from data_models.models import Vehicle

class DataGenerator:
    """Generates random vehicle data"""
    
    @staticmethod
    def generate_license_plate():
        """Generate random license plate"""
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"{letters} {numbers}"
    
    @staticmethod
    def generate_vehicle_type():
        """Generate random vehicle type based on distribution"""
        types = list(Config.VEHICLE_TYPES.keys())
        weights = list(Config.VEHICLE_TYPES.values())
        return random.choices(types, weights=weights, k=1)[0]
    
    @staticmethod
    def generate_speed(vehicle_type=""):
        """Generate random speed based on vehicle type"""
        # Adjust mean speed based on vehicle type
        if vehicle_type == "truck":
            mean = 60  # Trucks tend to be slower
        elif vehicle_type == "motorcycle":
            mean = 70  # Motorcycles tend to be faster
        else:
            mean = Config.SPEED_MEAN
        
        # Generate speed with normal distribution
        speed = random.gauss(mean, Config.SPEED_STD_DEV)
        
        # Ensure within bounds
        speed = max(Config.MIN_SPEED, min(speed, Config.MAX_SPEED))
        
        return round(speed, 1)
    
    @staticmethod
    def generate_vehicle_batch():
        """Generate a batch of random vehicles"""
        num_vehicles = random.randint(
            Config.MIN_VEHICLES_PER_BATCH,
            Config.MAX_VEHICLES_PER_BATCH
        )
        
        vehicles = []
        for i in range(num_vehicles):
            vehicle_type = DataGenerator.generate_vehicle_type()
            vehicle = Vehicle(
                vehicle_id=f"{vehicle_type.upper()}-{i+1:03d}",
                license_plate=DataGenerator.generate_license_plate(),
                vehicle_type=vehicle_type,
                speed=DataGenerator.generate_speed(vehicle_type),
                timestamp=datetime.now()
            )
            vehicles.append(vehicle)
        
        return vehicles
    
    @staticmethod
    def calculate_fine(speed):
        """Calculate fine based on speed"""
        if speed <= Config.SPEED_LIMIT:
            return 0.0
        
        for level, details in Config.FINES.items():
            if details["min"] <= speed <= details["max"]:
                return details["fine"]
        
        return Config.FINES["LEVEL_4"]["fine"]  # Default to highest fine
