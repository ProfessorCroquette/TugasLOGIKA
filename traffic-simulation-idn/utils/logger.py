import logging
import os
from datetime import datetime
from config import Config
from pathlib import Path

def cleanup_old_logs(max_logs=10):
    """
    Delete old log files if count exceeds maximum.
    Keeps the newest log files and removes oldest ones.
    
    Args:
        max_logs (int): Maximum number of log files to keep (default: 10)
    """
    try:
        logs_dir = Path(Config.LOGS_DIR)
        if not logs_dir.exists():
            return
        
        # Get all simulation log files
        log_files = sorted(logs_dir.glob("simulation_*.log"))
        
        # If more than max_logs, delete oldest ones
        if len(log_files) > max_logs:
            num_to_delete = len(log_files) - max_logs
            for log_file in log_files[:num_to_delete]:
                try:
                    log_file.unlink()
                    print(f"[LOG CLEANUP] Deleted old log: {log_file.name}")
                except Exception as e:
                    print(f"[LOG CLEANUP] Failed to delete {log_file.name}: {e}")
            
            print(f"[LOG CLEANUP] Removed {num_to_delete} old log file(s). Keeping latest {max_logs}.")
    
    except Exception as e:
        print(f"[LOG CLEANUP] Error during cleanup: {e}")

def setup_logger():
    """Setup logging configuration with auto-cleanup"""
    Config.setup_directories()
    
    # Clean up old logs before creating new one
    cleanup_old_logs(max_logs=10)
    
    log_file = os.path.join(
        Config.LOGS_DIR, 
        f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logger()
