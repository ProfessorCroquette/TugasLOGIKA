import logging
import os
from datetime import datetime
from config import Config

def setup_logger():
    """Setup logging configuration"""
    Config.setup_directories()
    
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
