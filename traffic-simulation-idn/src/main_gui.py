#!/usr/bin/env python
"""
GUI Entry Point
Traffic Simulation Indonesia PyQt5 Application
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.qt_app import TrafficSimulationApp


def main():
    """Main entry point for GUI"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        app = TrafficSimulationApp(sys.argv)
        sys.exit(app.run())
    except ImportError as e:
        print(f"Error: PyQt5 not installed. Install with: pip install PyQt5")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
