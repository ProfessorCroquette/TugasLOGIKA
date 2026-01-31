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
        """Generate random speed based on vehicle type (Toll Road - PP 43/1993)
        Kendaraan Ringan (Cars): 60-100 km/h (violations: <60 or >100)
        Kendaraan Berat (Trucks/Buses): 60-80 km/h (violations: <60 or >80, but allow 10-20km over)
        Increased violation generation for realistic enforcement data
        """
        # Adjust mean speed based on vehicle type
        if vehicle_type == "truck":
            mean = 70  # Trucks on toll: mean 70, max 80 km/h
            truck_max = 100  # Allow speeding 10-20km over limit for testing
        else:
            mean = 85  # Cars on toll: mean 85, max 100 km/h
            truck_max = 120  # Allow extended speeding range for cars
        
        # Increased violation generation chances (more violations for enforcement data)
        # 15% chance of slow violation (below 60 km minimum)
        # 20% chance of speeding violation (above limit + 10-20km buffer)
        # 65% chance of normal/legal speeds
        random_val = random.random()
        
        if random_val < 0.15:
            # Generate too-slow violation vehicle (below 60 km minimum)
            if vehicle_type == "truck":
                speed = random.uniform(20, 59)  # Below truck minimum of 60
            else:
                speed = random.uniform(20, 59)  # Below car minimum of 60
                
        elif random_val < 0.35:
            # Generate speeding violation (above limit with 10-20km tolerance/differentiation)
            if vehicle_type == "truck":
                # Trucks: 80 km limit, allow 10-20 km over = 90-100 km violation
                speed = random.uniform(85, 100)  # 5-20 km over truck limit
            else:
                # Cars: 100 km limit, allow 10-20 km over = 110-120 km violation
                speed = random.uniform(105, 120)  # 5-20 km over car limit
        else:
            # Generate normal distribution around the mean (legal speeds)
            speed = random.gauss(mean, Config.SPEED_STD_DEV)
        
        # Enforce vehicle-specific speed limits with violation allowance
        if vehicle_type == "truck":
            # Truck speed: 60-80 km/h legal, up to 100 km/h for violations
            speed = max(20, min(speed, truck_max))
        else:
            # Car speed: 60-100 km/h legal, up to 120 km/h for violations
            speed = max(20, min(speed, truck_max))
        
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
            # Select vehicle type by probability - MOTORCYCLES DISABLED (PP 43/1993)
            rand = random.random()
            
            if rand < 0.75:
                # PRIBADI (75%) - Private cars ONLY (motorcycles disabled)
                # No motorcycles on toll roads per PP 43/1993
                vehicle_info = DataGenerator.generate_vehicle_from_cars_db()
                vehicle_class = 'roda_empat'
                is_motorcycle = False  # DISABLED
                
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
        
        # Calculate penalty multiplier (additive, not multiplicative)
        # Base multiplier starts at 1.0 (no penalty)
        penalty_multiplier = 1.0
        
        # Add 20% for each condition
        if stnk_status == 'Non-Active':
            penalty_multiplier += 0.2  # +20% for non-active STNK
        if sim_status == 'Expired':
            penalty_multiplier += 0.2  # +20% for expired SIM
        
        # Cap base fine at maximum (before applying multiplier)
        if base_fine > Config.MAX_FINE_USD:
            base_fine = Config.MAX_FINE_USD
        
        # Calculate total fine: base (capped) × multiplier
        # Total fine can exceed max if multiplier is applied
        total_fine = base_fine * penalty_multiplier
        
        return base_fine, penalty_multiplier, total_fine
