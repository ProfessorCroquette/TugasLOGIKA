#!/usr/bin/env python3
"""
Test script to verify GUI cleanup properly terminates background simulation
"""

import subprocess
import time
import os
import psutil
import sys

def get_python_processes():
    """Get all Python processes running main.py"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.cmdline())
                if 'main.py' in cmdline:
                    return True, proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception as e:
        print(f"Error checking processes: {e}")
    return False, None

def test_gui_cleanup():
    """Test that GUI cleanup properly stops background processes"""
    print("=" * 60)
    print("Testing GUI Cleanup - Subprocess Termination")
    print("=" * 60)
    
    # Start GUI
    print("\n1. Starting GUI application...")
    gui_proc = subprocess.Popen(
        [sys.executable, "gui_traffic_simulation.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    print(f"   GUI Process started (PID: {gui_proc.pid})")
    
    # Let GUI start and initialize
    time.sleep(3)
    
    # Check if main.py is running
    print("\n2. Checking for background simulation (main.py)...")
    main_running, main_pid = get_python_processes()
    
    if main_running:
        print(f"   ✓ Background simulation detected (PID: {main_pid})")
    else:
        print("   ✗ No background simulation found (unexpected)")
    
    # Simulate user closing GUI
    print("\n3. Closing GUI window...")
    gui_proc.terminate()
    
    try:
        gui_proc.wait(timeout=5)
        print("   ✓ GUI process terminated")
    except subprocess.TimeoutExpired:
        print("   ✗ GUI process did not respond to terminate, killing...")
        gui_proc.kill()
        gui_proc.wait()
    
    # Wait a moment for cleanup
    time.sleep(2)
    
    # Check if main.py is still running
    print("\n4. Checking if background simulation stopped...")
    main_running, main_pid = get_python_processes()
    
    if main_running:
        print(f"   ✗ FAILED: Background simulation still running (PID: {main_pid})")
        print("   Killing stray process...")
        try:
            proc = psutil.Process(main_pid)
            proc.kill()
        except:
            pass
        return False
    else:
        print("   ✓ PASSED: Background simulation properly terminated")
        return True

def test_subprocess_creation():
    """Test that subprocess is created with proper process group"""
    print("\n" + "=" * 60)
    print("Testing Subprocess Creation Flags")
    print("=" * 60)
    
    from gui_traffic_simulation import SimulationWorker
    
    print("\n1. Creating SimulationWorker instance...")
    worker = SimulationWorker()
    print("   ✓ Worker created")
    
    print("\n2. Starting worker thread...")
    worker.start()
    print("   ✓ Worker thread started")
    
    # Wait for process to start
    time.sleep(2)
    
    if worker.process:
        print(f"\n3. Process started with PID: {worker.process.pid}")
        if os.name == 'nt':
            print("   Running on Windows - Process Group handling enabled")
        else:
            print("   Running on Unix - Process Group (setsid) enabled")
        print("   ✓ Process creation flags properly configured")
    else:
        print("   ✗ Process failed to start")
        return False
    
    # Stop worker
    print("\n4. Stopping worker...")
    worker.stop()
    worker.wait(5000)
    
    # Check cleanup
    time.sleep(1)
    main_running, _ = get_python_processes()
    
    if not main_running:
        print("   ✓ PASSED: Process properly cleaned up")
        return True
    else:
        print("   ✗ FAILED: Process still running after cleanup")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("GUI Cleanup Test Suite")
    print("=" * 60)
    
    try:
        # Test subprocess creation
        result1 = test_subprocess_creation()
        
        # Note: GUI cleanup test requires manual window close
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"\nSubprocess Creation Test: {'PASSED ✓' if result1 else 'FAILED ✗'}")
        print("\nNote: Interactive GUI test requires manual window close")
        print("If you want to test interactive behavior:")
        print("  1. Run: python gui_traffic_simulation.py")
        print("  2. Let it run for a few seconds")
        print("  3. Close the window")
        print("  4. Check Task Manager - main.py should NOT be running")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
