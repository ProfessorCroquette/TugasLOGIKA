import time
import threading
import queue
from datetime import datetime
from utils.generators import DataGenerator
from utils.logger import logger
from data_models.models import Vehicle

class TrafficSensor:
    """Simulates traffic sensor generating vehicle data"""
    
    def __init__(self, data_queue: queue.Queue, interval: int = 10):
        """
        Args:
            data_queue: Queue to put generated vehicle data
            interval: Seconds between data generation batches
        """
        self.data_queue = data_queue
        self.interval = interval
        self.is_running = False
        self.thread = None
        self.vehicles_generated = 0
    
    def start(self):
        """Start the sensor simulation"""
        self.is_running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(f"Traffic sensor started (interval: {self.interval}s)")
    
    def stop(self):
        """Stop the sensor simulation"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Traffic sensor stopped")
    
    def _run(self):
        """Main simulation loop"""
        while self.is_running:
            try:
                # Generate a batch of vehicles
                vehicles = DataGenerator.generate_vehicle_batch()
                self.vehicles_generated += len(vehicles)
                
                # Put data in queue
                self.data_queue.put({
                    'timestamp': datetime.now(),
                    'vehicles': vehicles,
                    'batch_size': len(vehicles)
                })
                
                logger.info(f"Generated {len(vehicles)} vehicles. Total: {self.vehicles_generated}")
                
                # Wait for next interval
                time.sleep(self.interval)
                
            except Exception as e:
                logger.error(f"Error in traffic sensor: {e}")
                time.sleep(1)  # Prevent tight loop on error
    
    def get_stats(self):
        """Get sensor statistics"""
        return {
            'vehicles_generated': self.vehicles_generated,
            'interval': self.interval,
            'is_running': self.is_running
        }
