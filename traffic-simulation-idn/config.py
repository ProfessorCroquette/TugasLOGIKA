import os
from datetime import datetime

class Config:
    # Simulation settings
    SIMULATION_INTERVAL = 10  # seconds between batches
    SPEED_LIMIT = 75  # km/h
    MIN_VEHICLES_PER_BATCH = 1
    MAX_VEHICLES_PER_BATCH = 10
    
    # Speed distribution (normal distribution)
    SPEED_MEAN = 65
    SPEED_STD_DEV = 15
    MIN_SPEED = 30
    MAX_SPEED = 140
    
    # Vehicle type distribution (percentages)
    VEHICLE_TYPES = {
        "car": 60,
        "truck": 20,
        "motorcycle": 15,
        "bus": 5
    }
    
    # Fines structure
    FINES = {
        "LEVEL_1": {"min": 76, "max": 90, "fine": 100},
        "LEVEL_2": {"min": 91, "max": 110, "fine": 200},
        "LEVEL_3": {"min": 111, "max": 130, "fine": 500},
        "LEVEL_4": {"min": 131, "max": float('inf'), "fine": 1000}
    }
    
    # Output directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    DATA_DIR = os.path.join(BASE_DIR, "data_files")
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
