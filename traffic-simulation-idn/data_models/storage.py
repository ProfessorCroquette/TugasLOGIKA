import json
import csv
import os
from datetime import datetime
from typing import List
from data_models.models import Vehicle, Ticket, TrafficStats
from config import Config
from utils.logger import logger

class DataStorage:
    """Handles data storage to files"""
    
    def __init__(self):
        Config.setup_directories()
        self.traffic_file = os.path.join(Config.DATA_DIR, "traffic_data.json")
        self.tickets_file = os.path.join(Config.DATA_DIR, "tickets.json")
        self.stats_file = os.path.join(Config.DATA_DIR, "statistics.csv")
        
        # Initialize files if they don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize data files"""
        if not os.path.exists(self.traffic_file):
            with open(self.traffic_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'total_vehicles', 'speeding_count',
                    'total_fines', 'avg_speed', 'max_speed'
                ])
    
    def save_vehicles(self, vehicles: List[Vehicle]):
        """Save vehicle data to JSON file"""
        try:
            # Convert vehicles to dictionary
            vehicles_data = []
            for v in vehicles:
                vehicle_dict = {
                    'vehicle_id': v.vehicle_id,
                    'license_plate': v.license_plate,
                    'vehicle_type': v.vehicle_type,
                    'speed': v.speed,
                    'timestamp': v.timestamp.isoformat(),
                    'location': v.location,
                    'ticket_issued': v.ticket_issued,
                    'fine_amount': v.fine_amount
                }
                vehicles_data.append(vehicle_dict)
            
            # Read existing data
            with open(self.traffic_file, 'r') as f:
                existing_data = json.load(f)
            
            # Append new data
            existing_data.extend(vehicles_data)
            
            # Write back
            with open(self.traffic_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            logger.info(f"Saved {len(vehicles)} vehicles to {self.traffic_file}")
            
        except Exception as e:
            logger.error(f"Error saving vehicles: {e}")
    
    def save_tickets(self, tickets: List[Ticket]):
        """Save tickets to JSON file"""
        try:
            tickets_data = []
            for t in tickets:
                ticket_dict = {
                    'ticket_id': t.ticket_id,
                    'license_plate': t.license_plate,
                    'vehicle_type': t.vehicle_type,
                    'speed': t.speed,
                    'speed_limit': t.speed_limit,
                    'fine_amount': t.fine_amount,
                    'timestamp': t.timestamp.isoformat(),
                    'location': t.location,
                    'status': t.status
                }
                tickets_data.append(ticket_dict)
            
            # Read existing data
            with open(self.tickets_file, 'r') as f:
                existing_data = json.load(f)
            
            # Append new data
            existing_data.extend(tickets_data)
            
            # Write back
            with open(self.tickets_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            logger.info(f"Saved {len(tickets)} tickets to {self.tickets_file}")
            
        except Exception as e:
            logger.error(f"Error saving tickets: {e}")
    
    def save_statistics(self, stats: TrafficStats):
        """Save statistics to CSV file"""
        try:
            with open(self.stats_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    stats.period_end.isoformat(),
                    stats.total_vehicles,
                    stats.speeding_count,
                    stats.total_fines,
                    round(stats.avg_speed, 2),
                    round(stats.max_speed, 2)
                ])
            
            logger.info(f"Saved statistics for period ending {stats.period_end}")
            
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
    
    def get_all_tickets(self):
        """Retrieve all tickets"""
        try:
            with open(self.tickets_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def get_all_vehicles(self):
        """Retrieve all vehicles"""
        try:
            with open(self.traffic_file, 'r') as f:
                return json.load(f)
        except:
            return []
