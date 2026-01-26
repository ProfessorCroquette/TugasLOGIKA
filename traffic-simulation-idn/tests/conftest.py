"""
Pytest configuration and fixtures
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


@pytest.fixture
def app():
    """Create application fixture"""
    from src.core.application import Application
    app = Application()
    yield app
    # Cleanup
    app.cleanup()


@pytest.fixture
def db_session():
    """Create database session fixture"""
    from src.database.session import SessionLocal
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_vehicle():
    """Sample vehicle data"""
    return {
        "plate": "B1234ABC",
        "type": "sedan",
        "brand": "Toyota",
        "model": "Camry",
        "year": 2020
    }


@pytest.fixture
def sample_owner():
    """Sample owner data"""
    return {
        "name": "Budi Santoso",
        "email": "budi@example.com",
        "phone": "08123456789",
        "nik": "3141234567890123"
    }


@pytest.fixture
def sample_violation():
    """Sample violation data"""
    return {
        "vehicle_id": 1,
        "type": "speed",
        "speed": 75,
        "speed_limit": 60,
        "location": "Jalan Sudirman"
    }
