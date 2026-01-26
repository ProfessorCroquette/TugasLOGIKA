"""
GUI Configuration
"""

from config.settings import APP_ENV

# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Theme
DEFAULT_THEME = "dark"  # or "light"
AVAILABLE_THEMES = ["dark", "light"]

# Language
DEFAULT_LANGUAGE = "en"  # or "id" for Indonesian
AVAILABLE_LANGUAGES = ["en", "id"]

# GUI Updates
UPDATE_INTERVAL = 1000  # milliseconds
CHART_UPDATE_INTERVAL = 2000  # milliseconds
TABLE_PAGE_SIZE = 50

# Simulation Controls
DEFAULT_VEHICLE_COUNT = 10
MIN_VEHICLE_COUNT = 1
MAX_VEHICLE_COUNT = 500
DEFAULT_SIMULATION_SPEED = 1.0

# File dialogs
DEFAULT_EXPORT_FORMAT = "csv"
EXPORT_FORMATS = {
    "csv": "CSV Files (*.csv)",
    "pdf": "PDF Files (*.pdf)",
    "excel": "Excel Files (*.xlsx)"
}
