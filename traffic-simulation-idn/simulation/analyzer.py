import threading
import queue
from datetime import datetime
from typing import List
from data_models.models import Vehicle, Ticket, TrafficStats
from utils.generators import DataGenerator
from utils.logger import logger
from data_models.storage import DataStorage

class SpeedAnalyzer:
    """Analyzes vehicle speeds and issues tickets"""
    
    def __init__(self, data_queue: queue.Queue):
        """
        Args:
            data_queue: Queue to get vehicle data from sensor
        """
        self.data_queue = data_queue
        self.is_running = False
        self.thread = None
        self.storage = DataStorage()
        self.stats = TrafficStats(
            period_start=datetime.now(),
            period_end=datetime.now()
        )
        self.total_processed = 0
        self.speeding_processed = 0
    
    def start(self):
        """Start the analyzer"""
        self.is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("Speed analyzer started")
    
    def stop(self):
        """Stop the analyzer"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Speed analyzer stopped")
        
        # Save final statistics
        self._update_stats(final=True)
    
    def _run(self):
        """Main analysis loop"""
        while self.is_running:
            try:
                # Get data from queue (with timeout to allow checking is_running)
                try:
                    data = self.data_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Process the vehicle batch
                vehicles = data['vehicles']
                batch_tickets = self._process_batch(vehicles)
                
                # Update statistics
                self._update_stats(batch_tickets, vehicles)
                
                # Save data
                self.storage.save_vehicles(vehicles)
                if batch_tickets:
                    self.storage.save_tickets(batch_tickets)
                
                # Log results
                speeding_count = len([v for v in vehicles if v.ticket_issued])
                logger.info(f"Processed {len(vehicles)} vehicles, {speeding_count} speeding violations")
                
                self.total_processed += len(vehicles)
                self.speeding_processed += speeding_count
                
            except Exception as e:
                logger.error(f"Error in speed analyzer: {e}")
    
    def _process_batch(self, vehicles: List[Vehicle]) -> List[Ticket]:
        """Process a batch of vehicles and issue tickets"""
        tickets = []
        
        for vehicle in vehicles:
            # Check if speeding
            if vehicle.speed > 75:  # Your algorithm threshold
                vehicle.ticket_issued = True
                vehicle.fine_amount = DataGenerator.calculate_fine(vehicle.speed)
                
                # Create ticket
                ticket = Ticket(
                    license_plate=vehicle.license_plate,
                    vehicle_type=vehicle.vehicle_type,
                    speed=vehicle.speed,
                    fine_amount=vehicle.fine_amount,
                    timestamp=vehicle.timestamp
                )
                tickets.append(ticket)
                
                # Log violation
                logger.warning(
                    f"SPEEDING VIOLATION: {vehicle.license_plate} "
                    f"({vehicle.vehicle_type}) - {vehicle.speed} km/h "
                    f"(Fine: ${vehicle.fine_amount})"
                )
        
        return tickets
    
    def _update_stats(self, tickets: List[Ticket] = None, vehicles: List[Vehicle] = None, final: bool = False):
        """Update statistics"""
        if vehicles:
            # Calculate batch statistics
            speeds = [v.speed for v in vehicles]
            self.stats.total_vehicles += len(vehicles)
            self.stats.speeding_count += len([v for v in vehicles if v.ticket_issued])
            self.stats.total_fines += sum(t.fine_amount for t in tickets) if tickets else 0
            
            # Update average speed (weighted)
            if speeds:
                batch_avg = sum(speeds) / len(speeds)
                total_vehicles = self.stats.total_vehicles
                if total_vehicles > 0:
                    # Weighted average calculation
                    self.stats.avg_speed = (
                        (self.stats.avg_speed * (total_vehicles - len(vehicles)) + 
                         batch_avg * len(vehicles)) / total_vehicles
                    )
                
                # Update max speed
                batch_max = max(speeds)
                if batch_max > self.stats.max_speed:
                    self.stats.max_speed = batch_max
        
        if final or (self.stats.total_vehicles > 0 and 
                    (datetime.now() - self.stats.period_start).seconds >= 60):  # Save every minute
            self.stats.period_end = datetime.now()
            self.storage.save_statistics(self.stats)
            self.stats.period_start = datetime.now()  # Reset for next period
    
    def get_stats(self):
        """Get analyzer statistics"""
        return {
            'total_processed': self.total_processed,
            'speeding_processed': self.speeding_processed,
            'current_stats': {
                'total_vehicles': self.stats.total_vehicles,
                'speeding_count': self.stats.speeding_count,
                'total_fines': self.stats.total_fines,
                'avg_speed': round(self.stats.avg_speed, 2),
                'max_speed': round(self.stats.max_speed, 2)
            }
        }
