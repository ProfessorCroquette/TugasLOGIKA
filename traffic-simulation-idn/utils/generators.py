import random
import string
from datetime import datetime
from config import Config
from data_models.models import Vehicle
from .car_database import CarDatabase
from .motorcycle_database import MotorcycleDatabase
from .truck_database import TruckDatabase
from .indonesian_plates import IndonesianPlateManager, owner_db, VehicleOwner, VehicleType, VehicleCategory
from .plate_generator import (
    get_plate_generator, TruckSubType, TruckClass,
    GovernmentAgency, DiplomaticCountry
)

class DataGenerator:
    """Generates random vehicle data using real car, motorcycle, and truck databases"""
    
    # Load databases once
    car_db = CarDatabase("CARS.md")
    motorcycle_db = MotorcycleDatabase("model.csv")
    truck_db = TruckDatabase()
    
    @staticmethod
    def generate_license_plate(vehicle_type: str = 'car'):
        """Generate random license plate following Indonesian nomenclature
        Format: [Region Code] [4-digit number] [Sub Code] [Owner letters]
        Examples:
        - Motor: B 1234 U AB
        - Mobil: B 5678 P ABC
        
        Args:
            vehicle_type: 'motorcycle' or 'car'
        
        Returns:
            plate string (e.g., "B 1234 U AB")
        """
        vehicle_enum = VehicleType.RODA_DUA if vehicle_type == 'motorcycle' else VehicleType.RODA_EMPAT_LEBIH
        plate, region_name, sub_region, vehicle_display = IndonesianPlateManager.generate_plate(vehicle_enum)
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
    def generate_motorcycle_from_db():
        """Generate motorcycle using real motorcycle database"""
        motorcycle = DataGenerator.motorcycle_db.get_random_motorcycle()
        
        return {
            'make': motorcycle['make'],
            'model': motorcycle['model'],
            'type': 'motorcycle',
            'support_level': 'Sport'
        }
    
    @staticmethod
    def generate_truck_from_db():
        """Generate truck using real truck database"""
        truck = DataGenerator.truck_db.get_random_truck()
        
        return {
            'make': truck['make'],
            'model': truck['model'],
            'type': 'truck',
            'cabin': truck['cabin'],
            'category': truck['category']
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
        """Generate random speed based on vehicle type
        Includes a small chance of generating very slow or very fast speeds for violation diversity
        """
        # Adjust mean speed based on vehicle type
        if vehicle_type == "truck":
            mean = 60  # Trucks tend to be slower
        elif vehicle_type == "motorcycle":
            mean = 72  # Motorcycles tend to be faster but capped at 75
        else:
            mean = Config.SPEED_MEAN
        
        # 8% chance of generating a distinctly slow vehicle (< 40 km/h) for too-slow violations
        # 10% chance of generating a distinctly fast vehicle (> 80 km/h) for speeding violations
        random_val = random.random()
        
        if random_val < 0.08:
            # Generate too-slow violation vehicle (20-39 km/h)
            speed = random.uniform(20, 39)
        elif random_val < 0.18:
            # Generate speeding vehicle (80-130 km/h)
            speed = random.uniform(80, 130)
        else:
            # Generate normal distribution around the mean
            speed = random.gauss(mean, Config.SPEED_STD_DEV)
        
        # Ensure within bounds (but allow full range to allow too-slow violations)
        # For slow violations: allow down to 20 km/h, up to 130 km/h max
        speed = max(20, min(speed, Config.MAX_SPEED))
        
        return round(speed, 1)
    
    @staticmethod
    def generate_vehicle_batch():
        """Generate a batch of random vehicles with probability distribution:
        50% Pribadi (cars/motorcycles) - Private plate (BLACK)
        40% Barang/Truk/Angkutan Umum (commercial) - Truck plate (YELLOW)
        5% Pemerintah (government) - Government plate (RED)
        5% Kedutaan (diplomatic) - Diplomatic plate (WHITE)
        """
        num_vehicles = random.randint(
            Config.MIN_VEHICLES_PER_BATCH,
            Config.MAX_VEHICLES_PER_BATCH
        )
        
        vehicles = []
        plate_gen = get_plate_generator()
        
        for i in range(num_vehicles):
            # Select vehicle type by probability
            rand = random.random()
            
            if rand < 0.50:
                # PRIBADI (50%) - Private cars and motorcycles
                is_motorcycle = random.random() < 0.15  # 15% motorcycles within pribadi
                
                if is_motorcycle:
                    vehicle_info = DataGenerator.generate_motorcycle_from_db()
                    vehicle_class = 'roda_dua'
                else:
                    vehicle_info = DataGenerator.generate_vehicle_from_cars_db()
                    vehicle_class = 'roda_empat'
                
                vehicle_category = VehicleCategory.PRIBADI.value
                plate_color = 'BLACK'
                plate_type = 'PRIBADI'
                
                # Generate private plate
                region_code = random.choice(['B', 'D', 'F', 'H', 'L', 'AB', 'AG', 'AA', 'BL', 'BP', 'KB', 'KT', 'DK'])
                plate_data = plate_gen.generate_private_plate(region_code)
                license_plate = plate_data['plate']
                
            elif rand < 0.90:
                # BARANG/TRUK/ANGKUTAN UMUM (40%) - Commercial vehicles
                vehicle_info = DataGenerator.generate_truck_from_db()
                vehicle_class = 'roda_empat'
                vehicle_category = VehicleCategory.BARANG.value
                plate_color = 'YELLOW'
                plate_type = 'NIAGA/TRUK'
                
                # Generate truck plate with random specifications
                truck_type = random.choice([
                    TruckSubType.GENERAL,
                    TruckSubType.CONTAINER,
                    TruckSubType.TANKER,
                    TruckSubType.DUMP,
                    TruckSubType.FLATBED
                ])
                truck_class = random.choice([
                    TruckClass.LIGHT,
                    TruckClass.MEDIUM,
                    TruckClass.HEAVY
                ])
                region_code = random.choice(['B', 'D', 'F', 'H', 'L', 'AB', 'BL'])
                
                plate_data = plate_gen.generate_truck_plate(
                    region_code=region_code,
                    truck_type=truck_type,
                    truck_class=truck_class
                )
                license_plate = plate_data['plate']
                
            elif rand < 0.95:
                # PEMERINTAH (5%) - Government vehicles
                vehicle_info = DataGenerator.generate_vehicle_from_cars_db()
                vehicle_class = 'roda_empat'
                vehicle_category = 'PEMERINTAH'
                plate_color = 'RED'
                plate_type = 'PEMERINTAH'
                
                # Generate government plate
                agency = random.choice([
                    GovernmentAgency.POLICE,
                    GovernmentAgency.ARMY_LAND,
                    GovernmentAgency.ARMY_NAVY,
                    GovernmentAgency.ARMY_AIR,
                    GovernmentAgency.PRESIDENCY,
                    GovernmentAgency.PARLIAMENT
                ])
                
                plate_data = plate_gen.generate_government_plate(agency)
                license_plate = plate_data['plate']
                
            else:
                # KEDUTAAN (5%) - Diplomatic vehicles
                vehicle_info = DataGenerator.generate_vehicle_from_cars_db()
                vehicle_class = 'roda_empat'
                vehicle_category = 'KEDUTAAN'
                plate_color = 'WHITE'
                plate_type = 'DIPLOMATIK'
                
                # Generate diplomatic plate
                country = random.choice([
                    DiplomaticCountry.USA,
                    DiplomaticCountry.CHINA,
                    DiplomaticCountry.JAPAN,
                    DiplomaticCountry.SOUTH_KOREA,
                    DiplomaticCountry.SINGAPORE,
                    DiplomaticCountry.MALAYSIA,
                    DiplomaticCountry.THAILAND,
                    DiplomaticCountry.VIETNAM,
                    DiplomaticCountry.PHILIPPINES,
                    DiplomaticCountry.INDIA
                ])
                is_consular = random.random() < 0.3
                
                plate_data = plate_gen.generate_diplomatic_plate(country, is_consular)
                license_plate = plate_data['plate']
            
            vehicle_type = vehicle_info['type']
            
            # Get or create owner for this vehicle
            owner = owner_db.get_or_create_owner(license_plate, vehicle_class)
            
            vehicle = Vehicle(
                vehicle_id=f"{vehicle_info['make'][:3].upper()}{i+1:04d}",
                license_plate=license_plate,
                vehicle_type=vehicle_class,  # 'roda_dua' or 'roda_empat'
                speed=DataGenerator.generate_speed(vehicle_type),
                timestamp=datetime.now(),
                owner_id=owner.owner_id,
                owner_name=owner.name,
                owner_region=owner.region,
                stnk_status='Active' if owner.stnk_status else 'Non-Active',
                sim_status='Active' if owner.sim_status else 'Expired',
                vehicle_make=vehicle_info.get('make', ''),
                vehicle_model=vehicle_info.get('model', ''),
            )
            # Add vehicle category and plate info for display
            vehicle.vehicle_category = vehicle_category
            vehicle.plate_type = plate_type
            vehicle.plate_color = plate_color
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
