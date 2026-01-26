import random
import string
from datetime import datetime
from config import Config
from data_models.models import Vehicle
from .car_database import CarDatabase
from .indonesian_plates import IndonesianPlateManager, owner_db, VehicleOwner

class DataGenerator:
    """Generates random vehicle data using real car database"""
    
    # Load car database once
    car_db = CarDatabase("CARS.md")
    
    @staticmethod
    def generate_license_plate():
        """Generate random license plate (Indonesian format)
        Format: [Region Code] [Number] [Owner Code]
        Example: D 1234 CD (Bandung, number 1234, owner code CD)
        """
        plate, region = IndonesianPlateManager.generate_plate()
        return plate
    
    @staticmethod
    def generate_vehicle_from_cars_db():
        """Generate vehicle using real car database"""
        vehicle = DataGenerator.car_db.get_random_vehicle()
        
        if not vehicle:
            return {
                'make': 'Unknown',
                'model': 'Unknown',
                'type': 'car',
                'support_level': 'Unknown'
            }
        
        return {
            'make': vehicle['make'],
            'model': vehicle['model'],
            'type': vehicle['weight'],  # 'car', 'truck', 'suv'
            'support_level': vehicle['support_level'],
            'package': vehicle['package']
        }
    
    @staticmethod
    def generate_vehicle_type():
        """Generate random vehicle type based on real database distribution"""
        # Get statistics from database
        stats = DataGenerator.car_db.get_statistics()
        type_dist = stats['by_vehicle_type']
        
        types = list(type_dist.keys())
        weights = list(type_dist.values())
        
        return random.choices(types, weights=weights, k=1)[0]
    
    @staticmethod
    def generate_speed(vehicle_type="car"):
        """Generate random speed based on vehicle type"""
        # Adjust mean speed based on vehicle type
        if vehicle_type == "truck":
            mean = 60  # Trucks tend to be slower
        elif vehicle_type == "motorcycle":
            mean = 75  # Motorcycles tend to be faster
        else:
            mean = Config.SPEED_MEAN
        
        # Generate speed with normal distribution
        speed = random.gauss(mean, Config.SPEED_STD_DEV)
        
        # Ensure within bounds
        speed = max(Config.MIN_SPEED, min(speed, Config.MAX_SPEED))
        
        
        return round(speed, 1)
    
    @staticmethod
    def generate_vehicle_batch():
        """Generate a batch of random vehicles using real car database with owner info"""
        num_vehicles = random.randint(
            Config.MIN_VEHICLES_PER_BATCH,
            Config.MAX_VEHICLES_PER_BATCH
        )
        
        vehicles = []
        for i in range(num_vehicles):
            # Get real car from database
            car_info = DataGenerator.generate_vehicle_from_cars_db()
            vehicle_type = car_info['type']
            
            # Generate license plate
            license_plate = DataGenerator.generate_license_plate()
            
            # Get or create owner for this vehicle
            owner = owner_db.get_or_create_owner(license_plate)
            
            vehicle = Vehicle(
                vehicle_id=f"{car_info['make'][:3].upper()}{i+1:04d}",
                license_plate=license_plate,
                vehicle_type=f"{car_info['make']} {car_info['model']}",
                speed=DataGenerator.generate_speed(vehicle_type),
                timestamp=datetime.now(),
                owner_id=owner.owner_id,
                owner_name=owner.name,
                owner_region=owner.region,
                stnk_status='Active' if owner.stnk_status else 'Non-Active',
                sim_status='Active' if owner.sim_status else 'Expired'
            )
            vehicles.append(vehicle)
        
        return vehicles
    
    @staticmethod
    def calculate_fine(speed, stnk_status: str = 'Active', sim_status: str = 'Active'):
        """
        Calculate fine based on speed with penalties for non-active registration
        Based on Article 287 paragraph (5) UU No. 22 Tahun 2009 LLAJ
        Applies to both speeding and driving too slowly
        
        Args:
            speed: Vehicle speed in km/h
            stnk_status: Vehicle registration status ('Active' or 'Non-Active')
            sim_status: Driver license status ('Active' or 'Expired')
        
        Returns:
            Tuple of (base_fine, penalty_multiplier, total_fine, violation_reason)
        """
        # Get base fine
        base_fine = 0.0
        violation_reason = ""
        
        # Check for low-speed violations (driving too slowly)
        if speed < Config.MIN_SPEED_LIMIT:
            if speed < 30:
                base_fine = Config.FINES["SPEED_LOW_SEVERE"]["fine"]
                violation_reason = Config.FINES["SPEED_LOW_SEVERE"]["description"]
            else:
                base_fine = Config.FINES["SPEED_LOW_MILD"]["fine"]
                violation_reason = Config.FINES["SPEED_LOW_MILD"]["description"]
        # Check for high-speed violations (speeding)
        elif speed > Config.SPEED_LIMIT:
            for level, details in Config.FINES.items():
                if "SPEED_HIGH" in level and details["min"] <= speed <= details["max"]:
                    base_fine = details["fine"]
                    violation_reason = details["description"]
                    break
            else:
                # If speed exceeds all levels, use highest tier
                base_fine = Config.FINES["SPEED_HIGH_LEVEL_3"]["fine"]
                violation_reason = Config.FINES["SPEED_HIGH_LEVEL_3"]["description"]
        
        # Calculate penalty multiplier
        # +20% for each condition that applies
        penalty_multiplier = 1.0
        
        # Each expired/non-active status adds 20%
        if stnk_status == 'Non-Active':
            penalty_multiplier += 0.2  # +20% for non-active STNK
        if sim_status == 'Expired':
            penalty_multiplier += 0.2  # +20% for expired SIM
        
        # Calculate total fine
        total_fine = base_fine * penalty_multiplier
        
        # Ensure total fine does not exceed legal maximum
        if total_fine > Config.MAX_FINE_USD:
            total_fine = Config.MAX_FINE_USD
        
        return base_fine, penalty_multiplier, total_fine
