"""Configuration modules"""

import os
from datetime import datetime

class Config:
    # Simulation settings
    SIMULATION_INTERVAL = 3  # seconds between batches (3 seconds for target flow)
    
    # SPEED LIMITS - PP 43/1993 Toll Road Standards
    # Kendaraan Ringan (Cars < 3,500 kg): 60-100 km/h
    # Kendaraan Berat (Trucks/Buses >= 3,500 kg): 60-80 km/h (20 km/h lower than cars)
    SPEED_LIMIT = 100  # km/h - Cars maximum on toll roads
    TRUCK_SPEED_LIMIT = 80  # km/h - Trucks/Buses maximum on toll roads (20 km/h lower)
    MIN_SPEED_LIMIT = 60  # km/h - Minimum safe speed for both (toll road minimum)
    
    MIN_VEHICLES_PER_BATCH = 10  # at least 10 cars per batch
    MAX_VEHICLES_PER_BATCH = 15  # max 15 per batch for consistent violations
    
    # Speed distribution (normal distribution) - PP 43/1993 Toll Road Standards
    SPEED_MEAN = 85  # average speed around 85 km/h (below 100 km/h limit for cars)
    SPEED_STD_DEV = 8  # moderate variation in speeds (realistic)
    MIN_SPEED = 60  # Minimum speed on toll road (both car and truck)
    MAX_SPEED = 120  # Allow speeds above 100 for natural violations (car testing)
    
    # Vehicle type distribution (percentages) - MOTORCYCLES DISABLED
    # Only Cars and Trucks allowed (PP 43/1993 compliance)
    VEHICLE_TYPES = {
        "car": 75,
        "truck": 25,
        "motorcycle": 0,  # DISABLED - Motorcycles not allowed on toll roads
        "bus": 0  # DISABLED - Buses follow truck speed limits
    }
    
    # Currency conversion (DEFINE FIRST - used in fine calculations)
    USD_TO_IDR = 15500  # 1 USD = 15,500 IDR
    
    # Fines structure (in USD, converted to IDR in GUI)
    # Based on PP 43/1993 - Toll Road Speed Limits
    # Cars: 60-100 km/h | Trucks: 40-80 km/h
    # Fines are tiered based on severity of violation
    FINES = {
        "SPEED_LOW_MILD": {"min": 50, "max": 59, "fine": 20, "description": "Terlalu lambat (terlalu rendah dari batas minimum)"},  # Rp 310,000
        "SPEED_LOW_SEVERE": {"min": 0, "max": 49, "fine": 35, "description": "Terlalu lambat berat (sangat di bawah batas minimum)"},  # Rp 542,500
        "SPEED_HIGH_LEVEL_1": {"min": 101, "max": 110, "fine": 30, "description": "Melampaui batas kecepatan 1-10 km/h (cars)"},  # Rp 465,000
        "SPEED_HIGH_LEVEL_2": {"min": 111, "max": 120, "fine": 50, "description": "Melampaui batas kecepatan 11-20 km/h (cars)"},  # Rp 775,000
        "SPEED_HIGH_LEVEL_3": {"min": 121, "max": 150, "fine": 75, "description": "Melampaui batas kecepatan 21+ km/h (cars)"}  # Rp 1,162,500 (near max)
    }
    
    # Maximum fine per law
    MAX_FINE_IDR = 500000  # Rp 500,000 - maximum penalty
    MAX_FINE_USD = MAX_FINE_IDR / USD_TO_IDR  # ~USD 32.26
    
    # Output directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    DATA_DIR = os.path.join(BASE_DIR, "data_files")
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories"""
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)

__all__ = ['Config']

