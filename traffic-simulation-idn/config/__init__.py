"""Configuration modules"""

import os
from datetime import datetime

class Config:
    # Simulation settings
    SIMULATION_INTERVAL = 5  # seconds between batches (reduced for faster violations)
    SPEED_LIMIT = 75  # km/h - standard speed limit for regular roads
    MIN_SPEED_LIMIT = 40  # km/h - minimum safe speed
    MIN_VEHICLES_PER_BATCH = 2  # increased for more violations
    MAX_VEHICLES_PER_BATCH = 100  # increased to max 100 per batch
    
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
    
    # Currency conversion (DEFINE FIRST - used in fine calculations)
    USD_TO_IDR = 15500  # 1 USD = 15,500 IDR
    
    # Fines structure (in USD, converted to IDR in GUI)
    # Maximum fine: Rp 1,250,000
    # Fines are tiered based on severity of violation
    FINES = {
        "SPEED_LOW_MILD": {"min": 30, "max": 39, "fine": 20, "description": "Terlalu lambat (terlalu rendah dari batas minimum)"},  # Rp 310,000
        "SPEED_LOW_SEVERE": {"min": 0, "max": 29, "fine": 35, "description": "Terlalu lambat berat (sangat di bawah batas minimum)"},  # Rp 542,500
        "SPEED_HIGH_LEVEL_1": {"min": 76, "max": 90, "fine": 30, "description": "Melampaui batas kecepatan 1-15 km/h"},  # Rp 465,000
        "SPEED_HIGH_LEVEL_2": {"min": 91, "max": 110, "fine": 50, "description": "Melampaui batas kecepatan 16-35 km/h"},  # Rp 775,000
        "SPEED_HIGH_LEVEL_3": {"min": 111, "max": 130, "fine": 75, "description": "Melampaui batas kecepatan 36+ km/h"}  # Rp 1,162,500 (near max)
    }
    
    # Maximum fine per law
    MAX_FINE_IDR = 1250000  # Rp 1,250,000 - maximum penalty
    MAX_FINE_USD = MAX_FINE_IDR / USD_TO_IDR  # ~USD 80.65
    
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

