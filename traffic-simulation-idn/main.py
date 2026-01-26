import queue
import threading
import time
import signal
import sys
from simulation.sensor import TrafficSensor
from simulation.analyzer import SpeedAnalyzer
from dashboard.display import Dashboard
from utils.logger import logger
from config import Config

class SpeedingTicketSimulator:
    """Main application controller"""
    
    def __init__(self):
        # Setup configuration
        Config.setup_directories()
        
        # Create data queue for communication (increased to 500 for more data)
        self.data_queue = queue.Queue(maxsize=500)
        
        # Initialize components
        self.sensor = TrafficSensor(self.data_queue, Config.SIMULATION_INTERVAL)
        self.analyzer = SpeedAnalyzer(self.data_queue)
        self.dashboard = Dashboard(self.sensor, self.analyzer)
        
        self.is_running = False
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # On Windows, also register for other signals
        if sys.platform == 'win32':
            # Windows doesn't have SIGUSR1 or other Unix signals
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {signum}, stopping gracefully...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the simulation"""
        logger.info("Starting Speeding Ticket Simulation...")
        self.is_running = True
        
        try:
            # Start components
            self.sensor.start()
            self.analyzer.start()
            
            # Start dashboard in separate thread
            dashboard_thread = threading.Thread(
                target=self.dashboard.run,
                daemon=True
            )
            dashboard_thread.start()
            
            # Main control loop
            self._control_loop()
            
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logger.error(f"Error in simulation: {e}")
            self.stop()
    
    def _control_loop(self):
        """Handle user input"""
        import sys
        import select
        
        print("\n[STARTED] Simulation Started! Press 'q' to quit.")
        
        while self.is_running:
            # Check for user input (non-blocking)
            if sys.platform == "win32":
                # Windows implementation
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    self._handle_keypress(key)
            else:
                # Unix/Linux/Mac implementation
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1).lower()
                    self._handle_keypress(key)
            
            time.sleep(0.1)
    
    def _handle_keypress(self, key):
        """Handle keyboard input"""
        if key == 'q':
            print("\nQuitting simulation...")
            self.stop()
        elif key == 'p':
            # Toggle sensor
            if self.sensor.is_running:
                self.sensor.stop()
                print("\nSensor PAUSED")
            else:
                self.sensor.start()
                print("\nSensor RESUMED")
        elif key == 'r':
            print("\nStatistics reset feature would be implemented here")
        elif key == 'h':
            print("\nHelp: q=quit, p=pause/resume, r=reset, h=help")
    
    def stop(self):
        """Stop the simulation"""
        logger.info("Stopping simulation...")
        self.is_running = False
        
        # Stop components
        self.sensor.stop()
        self.analyzer.stop()
        
        # Display final statistics
        self._display_final_stats()
        
        logger.info("Simulation stopped.")
        print("\nSimulation complete. Check logs/ and data_files/ for results.")
    
    def _display_final_stats(self):
        """Display final statistics"""
        analyzer_stats = self.analyzer.get_stats()
        stats = analyzer_stats['current_stats']
        
        print("\n" + "=" * 70)
        print("                   FINAL SIMULATION STATISTICS")
        print("=" * 70)
        print(f"Total Vehicles Processed: {analyzer_stats['total_processed']}")
        print(f"Speeding Violations: {analyzer_stats['speeding_processed']}")
        print(f"Total Fines Issued: ${stats['total_fines']}")
        print(f"Average Speed: {stats['avg_speed']} km/h")
        print(f"Maximum Speed Recorded: {stats['max_speed']} km/h")
        
        if analyzer_stats['total_processed'] > 0:
            violation_rate = (analyzer_stats['speeding_processed'] / 
                            analyzer_stats['total_processed'] * 100)
            print(f"Violation Rate: {violation_rate:.1f}%")
        print("=" * 70)

def main():
    """Application entry point"""
    import sys
    
    print("[*] SPEEDING TICKET SIMULATION SYSTEM")
    print("=" * 50)
    print("1. Traffic sensor generating random vehicles")
    print("2. Speed analyzer issuing tickets for violations")
    print("3. Real-time dashboard showing statistics")
    print("=" * 50)
    
    # Check for command-line duration argument
    duration_min = None
    if len(sys.argv) > 1:
        try:
            duration_min = int(sys.argv[1])
            print(f"Simulation will run for {duration_min} minutes")
        except ValueError:
            print("Invalid duration. Running continuous simulation.")
    
    if duration_min is None:
        print("Simulation will run until stopped (GUI will stop it)")
    
    # Create and run simulator
    simulator = SpeedingTicketSimulator()
    
    # Set up timed stop if duration specified
    if duration_min:
        def stop_after_duration():
            time.sleep(duration_min * 60)
            print(f"\n{duration_min} minutes elapsed. Stopping simulation...")
            simulator.stop()
        
        timer_thread = threading.Thread(target=stop_after_duration, daemon=True)
        timer_thread.start()
    
    # Start simulation
    simulator.start()

if __name__ == "__main__":
    main()
