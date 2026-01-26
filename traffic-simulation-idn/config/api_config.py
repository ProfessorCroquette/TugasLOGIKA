"""
API Configuration
"""

from config.settings import APP_ENV, RAPID_API_KEY, GEOLOCATION_API_KEY

# API Server
API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 4  # For production
API_RELOAD = APP_ENV == "development"

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Authentication
AUTH_ENABLED = True
TOKEN_EXPIRE_HOURS = 24
SECRET_KEY = "your-secret-key-change-in-production"

# Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 1000
RATE_LIMIT_PERIOD = 3600  # seconds

# External APIs
RAPIDAPI_HOST = "cars-by-api-ninjas.p.rapidapi.com"
RAPIDAPI_ENDPOINT = "https://cars-by-api-ninjas.p.rapidapi.com/v1/cars"
RAPIDAPI_KEY = RAPID_API_KEY

GEOLOCATION_ENDPOINT = "https://nominatim.openstreetmap.org/reverse"

# Cache
API_CACHE_TTL = 3600  # seconds
CACHE_ENABLED = True

# Pagination
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000
DEFAULT_OFFSET = 0
