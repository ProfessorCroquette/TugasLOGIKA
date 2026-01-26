import os
import time
from datetime import datetime
from utils.logger import logger

class Dashboard:
    """Console-based dashboard for monitoring"""
    
    def __init__(self, sensor, analyzer, update_interval=5):
        self.sensor = sensor
        self.analyzer = analyzer
        self.update_interval = update_interval
        self.is_running = False
        self.start_time = datetime.now()
    
    def display_header(self):
        """Display dashboard header"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 70)
        print("              TRAFFIC SPEEDING TICKET SIMULATION DASHBOARD")
        print("=" * 70)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Runtime: {self._get_runtime()}")
        print("-" * 70)
    
    def display_sensor_stats(self, sensor_stats):
        """Display sensor statistics"""
        print("\n📡 TRAFFIC SENSOR")
        print(f"   Status: {'RUNNING' if sensor_stats['is_running'] else 'STOPPED'}")
        print(f"   Vehicles Generated: {sensor_stats['vehicles_generated']}")
        print(f"   Interval: {sensor_stats['interval']} seconds")
        print("-" * 70)
    
    def display_analyzer_stats(self, analyzer_stats):
        """Display analyzer statistics"""
        stats = analyzer_stats['current_stats']
        print("\n⚡ SPEED ANALYZER")
        print(f"   Vehicles Processed: {analyzer_stats['total_processed']}")
        print(f"   Speeding Violations: {analyzer_stats['speeding_processed']}")
        print(f"   Total Fines: ${stats['total_fines']}")
        print(f"   Average Speed: {stats['avg_speed']} km/h")
        print(f"   Maximum Speed: {stats['max_speed']} km/h")
        print("-" * 70)
    
    def display_speed_distribution(self, analyzer_stats):
        """Display simple speed distribution"""
        print("\n📊 SPEED DISTRIBUTION (Last Batch)")
        # This is a simplified version - in real implementation, 
        # you'd track actual distribution
        total = analyzer_stats['total_processed']
        speeding = analyzer_stats['speeding_processed']
        if total > 0:
            compliant = total - speeding
            print(f"   Within Limit (≤75 km/h): {compliant} ({compliant/total*100:.1f}%)")
            print(f"   Speeding (>75 km/h): {speeding} ({speeding/total*100:.1f}%)")
            
            # Simple bar chart
            compliant_bar = "█" * int(compliant/total * 20)
            speeding_bar = "█" * int(speeding/total * 20)
            print(f"   [ {compliant_bar}{speeding_bar} ]")
        print("-" * 70)
    
    def display_recent_violations(self, limit=5):
        """Display recent violations"""
        print("\n🚨 RECENT SPEEDING TICKETS")
        
        try:
            from data_models.storage import DataStorage
            storage = DataStorage()
            tickets = storage.get_all_tickets()
            
            if tickets:
                # Get most recent tickets
                recent_tickets = sorted(
                    tickets, 
                    key=lambda x: x['timestamp'], 
                    reverse=True
                )[:limit]
                
                for i, ticket in enumerate(recent_tickets, 1):
                    time_str = datetime.fromisoformat(ticket['timestamp']).strftime('%H:%M:%S')
                    print(f"   {i}. [{time_str}] {ticket['license_plate']}: "
                          f"{ticket['speed']} km/h - Fine: ${ticket['fine_amount']}")
            else:
                print("   No tickets issued yet.")
        except:
            print("   Loading ticket data...")
        
        print("-" * 70)
    
    def display_controls(self):
        """Display control instructions"""
        print("\n🎮 CONTROLS")
        print("   Press 'q' to quit simulation")
        print("   Press 'p' to pause/resume sensor")
        print("   Press 'r' to reset statistics")
        print("=" * 70)
    
    def _get_runtime(self):
        """Calculate runtime duration"""
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update(self):
        """Update and display the dashboard"""
        try:
            self.display_header()
            
            sensor_stats = self.sensor.get_stats()
            analyzer_stats = self.analyzer.get_stats()
            
            self.display_sensor_stats(sensor_stats)
            self.display_analyzer_stats(analyzer_stats)
            self.display_speed_distribution(analyzer_stats)
            self.display_recent_violations()
            self.display_controls()
            
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
    
    def run(self):
        """Run the dashboard update loop"""
        self.is_running = True
        
        try:
            while self.is_running:
                self.update()
                time.sleep(self.update_interval)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the dashboard"""
        self.is_running = False
        print("\nDashboard stopped.")
