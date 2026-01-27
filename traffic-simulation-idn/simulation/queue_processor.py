"""
Queue-based car processor with concurrent sensor workers
Processes cars sequentially but with 5 concurrent sensors for efficiency
"""

import threading
import queue
import time
from datetime import datetime
from typing import List, Dict, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.logger import logger
from data_models.models import Vehicle, Ticket
from utils.generators import DataGenerator
from config import Config


class CarCheckResult:
    """Result of checking a single car"""
    def __init__(self, vehicle: Vehicle, is_violation: bool, 
                 violation_type: str = None, ticket: Ticket = None):
        self.vehicle = vehicle
        self.is_violation = is_violation
        self.violation_type = violation_type
        self.ticket = ticket
        self.check_timestamp = datetime.now()


class QueuedCarProcessor:
    """
    Processes cars from a queue using 5 concurrent sensor workers.
    - Cars are processed one-by-one sequentially
    - But 5 sensors work in parallel for efficiency
    - Each car gets a verdict before moving to next
    """
    
    def __init__(self, num_workers: int = 5):
        """
        Args:
            num_workers: Number of concurrent sensor workers (default: 5)
        """
        self.num_workers = num_workers
        self.car_queue = queue.Queue()  # Queue of vehicles to process
        self.result_queue = queue.Queue()  # Queue of check results
        self.is_running = False
        self.executor = None
        self.worker_threads = []
        
        # Callbacks
        self.on_car_checking = None  # Called when checking starts
        self.on_car_checked = None   # Called when verdict is ready
        self.on_batch_complete = None  # Called when batch is done
        self.on_worker_status = None  # Called when worker status changes
        
        # Stats
        self.total_processed = 0
        self.total_violations = 0
        self.violations_list = []
        self.current_car = None
        
        # Worker tracking - maps worker_id to (vehicle, start_time)
        self.worker_status = {}
        for i in range(num_workers):
            self.worker_status[i] = None
        
        self.lock = threading.Lock()
    
    def start(self):
        """Start the car processor with worker threads"""
        self.is_running = True
        self.executor = ThreadPoolExecutor(max_workers=self.num_workers)
        
        # Start the main processing loop
        main_thread = threading.Thread(target=self._main_loop, daemon=True)
        main_thread.start()
        
        logger.info(f"Car queue processor started with {self.num_workers} concurrent sensors")
    
    def stop(self):
        """Stop the car processor"""
        self.is_running = False
        
        if self.executor:
            self.executor.shutdown(wait=True)
        
        logger.info("Car queue processor stopped")
    
    def add_vehicles(self, vehicles: List[Vehicle]):
        """Add vehicles to the processing queue"""
        for vehicle in vehicles:
            self.car_queue.put(vehicle)
        logger.info(f"Added {len(vehicles)} vehicles to check queue")
    
    def _main_loop(self):
        """Main processing loop that manages queue and callbacks"""
        pending_futures = {}  # Maps future to (worker_id, vehicle)
        batch_start_time = None
        batch_vehicles = []
        worker_counter = 0
        
        while self.is_running:
            try:
                # Try to get next car from queue (non-blocking)
                try:
                    vehicle = self.car_queue.get(timeout=0.5)
                    batch_vehicles.append(vehicle)
                    
                    # Update current car
                    with self.lock:
                        self.current_car = vehicle
                    
                    # Emit checking callback
                    if self.on_car_checking:
                        self.on_car_checking(vehicle)
                    
                    # Submit to worker pool with worker ID tracking
                    worker_id = worker_counter % self.num_workers
                    worker_counter += 1
                    
                    future = self.executor.submit(self._check_car_with_worker, vehicle, worker_id)
                    pending_futures[future] = (worker_id, vehicle)
                    
                    # Update worker status
                    with self.lock:
                        self.worker_status[worker_id] = {
                            'vehicle': vehicle,
                            'start_time': datetime.now(),
                            'status': 'CHECKING'
                        }
                    
                    # Emit worker status callback
                    if self.on_worker_status:
                        self.on_worker_status(worker_id, vehicle, 'CHECKING')
                    
                except queue.Empty:
                    # No more cars in queue right now
                    pass
                
                # Check for completed futures
                if pending_futures:
                    done_futures = [f for f in pending_futures if f.done()]
                    
                    for future in done_futures:
                        try:
                            result, worker_id = future.result()
                            vehicle = pending_futures[future][1]
                            
                            # Update stats
                            with self.lock:
                                self.total_processed += 1
                                if result.is_violation:
                                    self.total_violations += 1
                                    self.violations_list.append(result.ticket)
                                
                                # Clear worker status
                                self.worker_status[worker_id] = None
                            
                            # Emit verdict callback
                            if self.on_car_checked:
                                self.on_car_checked(result)
                            
                            # Emit worker status callback
                            if self.on_worker_status:
                                verdict = 'VIOLATION' if result.is_violation else 'SAFE'
                                self.on_worker_status(worker_id, vehicle, verdict)
                            
                            del pending_futures[future]
                            
                            logger.debug(f"Checked car {vehicle.license_plate}: "
                                       f"{'VIOLATION' if result.is_violation else 'SAFE'}")
                            
                        except Exception as e:
                            logger.error(f"Error processing future: {e}")
                            if future in pending_futures:
                                del pending_futures[future]
                
                # If queue is empty and no pending work, batch is complete
                if self.car_queue.empty() and not pending_futures and batch_vehicles:
                    if self.on_batch_complete:
                        self.on_batch_complete(batch_vehicles, self.violations_list[-len(batch_vehicles):])
                    batch_vehicles = []
                    batch_start_time = None
                
                time.sleep(0.01)  # Small sleep to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Error in main processing loop: {e}")
                time.sleep(0.1)
    
    def _check_car(self, vehicle: Vehicle) -> CarCheckResult:
        """
        Check a single car for violations (runs in worker thread)
        Simulates sensor checking time
        """
        # Simulate sensor checking time (quick - 100-200ms)
        check_time = 0.1 + (hash(vehicle.license_plate) % 100) / 1000
        time.sleep(check_time)
        
        # Check if violating speed limits
        is_speeding = vehicle.speed > Config.SPEED_LIMIT
        is_too_slow = vehicle.speed < Config.MIN_SPEED_LIMIT
        
        if is_speeding or is_too_slow:
            vehicle.ticket_issued = True
            
            # Calculate fine
            base_fine, penalty_multiplier, total_fine = DataGenerator.calculate_fine(
                vehicle.speed,
                stnk_status=vehicle.stnk_status,
                sim_status=vehicle.sim_status
            )
            vehicle.fine_amount = total_fine
            
            # Determine violation type
            if is_speeding:
                violation_type = "SPEEDING"
                speed_note = f"{vehicle.speed:.1f} km/h (Limit: {Config.SPEED_LIMIT} km/h)"
            else:
                violation_type = "TOO SLOW"
                speed_note = f"{vehicle.speed:.1f} km/h (Min: {Config.MIN_SPEED_LIMIT} km/h)"
            
            # Create ticket
            ticket = Ticket(
                license_plate=vehicle.license_plate,
                vehicle_type=vehicle.vehicle_type,
                speed=vehicle.speed,
                fine_amount=total_fine,
                timestamp=vehicle.timestamp,
                owner_id=vehicle.owner_id,
                owner_name=vehicle.owner_name,
                owner_region=vehicle.owner_region,
                stnk_status=vehicle.stnk_status,
                sim_status=vehicle.sim_status,
                base_fine=base_fine,
                penalty_multiplier=penalty_multiplier
            )
            
            return CarCheckResult(
                vehicle=vehicle,
                is_violation=True,
                violation_type=violation_type,
                ticket=ticket
            )
        else:
            return CarCheckResult(
                vehicle=vehicle,
                is_violation=False,
                violation_type="SAFE",
                ticket=None
            )
    
    def _check_car_with_worker(self, vehicle: Vehicle, worker_id: int) -> tuple:
        """
        Check a single car for violations with worker ID tracking
        Returns (CarCheckResult, worker_id)
        """
        result = self._check_car(vehicle)
        return result, worker_id
    
    def get_stats(self) -> Dict:
        """Get current processor statistics"""
        with self.lock:
            return {
                'total_processed': self.total_processed,
                'total_violations': self.total_violations,
                'violation_rate': (self.total_violations / self.total_processed * 100 
                                 if self.total_processed > 0 else 0),
                'current_car': self.current_car,
                'queue_size': self.car_queue.qsize(),
                'num_workers': self.num_workers
            }
