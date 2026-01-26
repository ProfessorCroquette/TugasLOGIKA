import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Vehicle:
    """Represents a detected vehicle"""
    vehicle_id: str
    license_plate: str
    vehicle_type: str
    speed: float
    timestamp: datetime
    location: str = "Highway-Sensor-001"
    ticket_issued: bool = False
    fine_amount: float = 0.0
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.vehicle_id:
            self.vehicle_id = str(uuid.uuid4())[:8]

@dataclass
class Ticket:
    """Represents a speeding ticket"""
    ticket_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    license_plate: str = ""
    vehicle_type: str = ""
    speed: float = 0.0
    speed_limit: float = 75.0
    fine_amount: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    location: str = "Highway-Sensor-001"
    status: str = "PENDING"
    
    def __str__(self):
        return f"Ticket {self.ticket_id[:8]} - {self.license_plate}: {self.speed} km/h (Fine: ${self.fine_amount})"

@dataclass
class TrafficStats:
    """Statistics for a time period"""
    period_start: datetime
    period_end: datetime
    total_vehicles: int = 0
    speeding_count: int = 0
    total_fines: float = 0.0
    avg_speed: float = 0.0
    max_speed: float = 0.0
    vehicle_type_distribution: dict = field(default_factory=dict)
