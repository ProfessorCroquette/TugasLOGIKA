"""
Main application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Application
APP_NAME = os.getenv("APP_NAME", "Traffic Simulation Indonesia")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "traffic_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "traffic_simulation")

# Database URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# API Keys
RAPID_API_KEY = os.getenv("RAPID_API_KEY", "")
GEOLOCATION_API_KEY = os.getenv("GEOLOCATION_API_KEY", "")

# Email
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Twilio SMS
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

# Simulation
SIMULATION_SPEED = float(os.getenv("SIMULATION_SPEED", 1.0))
MAX_VEHICLES = int(os.getenv("MAX_VEHICLES", 500))
VIOLATION_CHECK_INTERVAL = int(os.getenv("VIOLATION_CHECK_INTERVAL", 5))

# Paths
LOGS_DIR = BASE_DIR / "outputs" / "logs"
REPORTS_DIR = BASE_DIR / "outputs" / "reports"
BACKUPS_DIR = BASE_DIR / "outputs" / "backups"
DATA_DIR = BASE_DIR / "data"

# Create directories if they don't exist
for directory in [LOGS_DIR, REPORTS_DIR, BACKUPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
