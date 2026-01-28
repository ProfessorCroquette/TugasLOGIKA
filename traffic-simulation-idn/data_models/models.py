import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

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
    owner_id: str = ""
    owner_name: str = ""
    owner_region: str = ""
    stnk_status: str = ""
    sim_status: str = ""
    vehicle_make: str = ""
    vehicle_model: str = ""
    vehicle_category: str = "Pribadi"  # Pribadi, Barang, Umum, Pemerintah, etc.
    plate_type: str = "PRIBADI"  # PRIBADI, NIAGA/TRUK, PEMERINTAH, DIPLOMATIK
    plate_color: str = "BLACK"  # BLACK, YELLOW, RED, WHITE
    
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
    vehicle_make: str = ""
    vehicle_model: str = ""
    vehicle_category: str = "Pribadi"
    plate_type: str = "PRIBADI"
    plate_color: str = "BLACK"
    speed: float = 0.0
    speed_limit: float = 75.0
    fine_amount: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    location: str = "Highway-Sensor-001"
    status: str = "PENDING"
    owner_id: str = ""
    owner_name: str = ""
    owner_region: str = ""
    stnk_status: str = ""
    sim_status: str = ""
    base_fine: float = 0.0
    penalty_multiplier: float = 1.0
    
    def __str__(self):
        return f"Ticket {self.ticket_id[:8]} - {self.license_plate}: {self.speed} km/h (Fine: ${self.fine_amount})"
    
    def get_violation_details(self) -> Dict[str, Any]:
        """Get detailed violation information"""
        return {
            'ticket_id': self.ticket_id,
            'license_plate': self.license_plate,
            'owner': {
                'id': self.owner_id,
                'name': self.owner_name,
                'region': self.owner_region,
            },
            'violation': {
                'speed': self.speed,
                'speed_limit': self.speed_limit,
                'excess': round(self.speed - self.speed_limit, 1),
            },
            'registration': {
                'stnk_status': self.stnk_status,
                'sim_status': self.sim_status,
            },
            'fine': {
                'base_fine': self.base_fine,
                'penalty_multiplier': self.penalty_multiplier,
                'total_fine': self.fine_amount,
                'timestamp': self.timestamp.isoformat(),
            }
        }

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
