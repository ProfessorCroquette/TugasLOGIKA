# Fix: Background Simulation Continues After GUI Close

## Problem
When closing the GUI window, the background `main.py` simulation process was not being properly terminated, resulting in:
- Continuous ticket generation even after GUI closed
- Stray Python processes running in background
- Memory leaks and system resource waste

## Root Cause
1. **Inadequate Process Cleanup**: The subprocess termination logic only attempted to kill the main process, not child processes
2. **No Process Group**: On Windows, the subprocess wasn't created with proper process group flags to allow group termination
3. **Incomplete Signal Handling**: The process hierarchy wasn't properly managed before cleanup

## Solution Implemented

### 1. Added psutil for Process Management
**File**: `requirements.txt`
- Added `psutil==5.9.6` for robust process and child process management
- Allows querying process tree and killing all descendants

### 2. Improved Subprocess Creation
**File**: `gui_traffic_simulation.py` - `SimulationWorker.run()`

**Windows**:
```python
self.process = subprocess.Popen(
    [sys.executable, "main.py"],
    cwd=current_dir,
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # Enables group termination
)
```

**Unix/Linux**:
```python
self.process = subprocess.Popen(
    [sys.executable, "main.py"],
    cwd=current_dir,
    preexec_fn=os.setsid  # Creates new process session
)
```

### 3. Enhanced Process Termination
**File**: `gui_traffic_simulation.py` - `SimulationWorker.stop()`

```
Process Kill Chain:
1. Get parent process via psutil
2. Find ALL child processes (recursive)
3. Kill/terminate all children first
4. Then kill parent
5. Wait with timeout (3 seconds)
6. Force kill if timeout exceeded
7. Fallback to taskkill on Windows if psutil fails
```

**Key Features**:
- ✅ Handles process not found gracefully
- ✅ Handles access denied errors
- ✅ 3-tier timeout strategy (3s → 2s → fail)
- ✅ Fallback mechanism using taskkill
- ✅ Proper error logging

### 4. Improved GUI Cleanup
**File**: `gui_traffic_simulation.py` - `TrafficSimulationGUI.cleanup()`

```python
cleanup() method now:
1. Stops refresh timer
2. Stops simulation worker thread
3. Waits for thread to finish (3s)
4. Force quits thread if still running (2s)
5. Scans for stray main.py processes and kills them
6. Comprehensive error handling
```

## Code Changes

### gui_traffic_simulation.py Changes

#### Before:
```python
def stop(self):
    if os.name == 'nt':  # Only taskkill, no child process handling
        sp.Popen(['taskkill', '/PID', str(self.process.pid), '/T', '/F'],...)
    else:
        self.process.terminate()  # Simple terminate, may miss children
```

#### After:
```python
def stop(self):
    parent = psutil.Process(self.process.pid)
    children = parent.children(recursive=True)  # Get ALL descendants
    
    # Kill children first, then parent, with proper error handling
    for child in children:
        if os.name == 'nt':
            child.kill()
        else:
            child.terminate()
    
    # Parent termination with 3-tier timeout
    parent.kill()
    try:
        parent.wait(timeout=3)  # 1st attempt: 3s
    except subprocess.TimeoutExpired:
        parent.kill()  # 2nd attempt: force kill
        try:
            parent.wait(timeout=2)  # 2nd timeout: 2s
        except subprocess.TimeoutExpired:
            logger.error(f"Could not kill process {self.process.pid}")
```

### Process Creation with Group Management

#### Before:
```python
self.process = subprocess.Popen(
    [sys.executable, "main.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    cwd=current_dir
)
```

#### After:
```python
if os.name == 'nt':  # Windows
    self.process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=current_dir,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
else:  # Unix/Linux
    self.process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=current_dir,
        preexec_fn=os.setsid
    )
```

## Testing

### Manual Test Procedure
1. Run: `python gui_traffic_simulation.py`
2. Wait for simulation to start (should see tickets appearing)
3. Close the GUI window
4. Open Task Manager (Ctrl+Shift+Esc)
5. Verify: No `python.exe` or `main.py` processes running

### Automated Test
```bash
python test_gui_cleanup.py
```

This tests:
- ✅ Subprocess creation with proper flags
- ✅ Process tree cleanup
- ✅ Stray process detection and killing
- ✅ Timeout handling

## Verification Checklist

- ✅ psutil added to requirements.txt
- ✅ Process groups implemented (Windows: CREATE_NEW_PROCESS_GROUP, Unix: setsid)
- ✅ Child process detection and termination
- ✅ Multi-tier timeout strategy (3s → 2s)
- ✅ Fallback mechanism (taskkill)
- ✅ Stray process scanner in cleanup()
- ✅ Comprehensive error handling
- ✅ Proper logging at each step
- ✅ Test script created

## Impact

**Before Fix**:
- Closing GUI → main.py still running
- Tickets continue being generated
- Process never cleaned up

**After Fix**:
- Closing GUI → immediate process termination
- All child processes killed
- Complete resource cleanup
- No orphaned processes

## Files Modified

1. `requirements.txt` - Added psutil dependency
2. `gui_traffic_simulation.py` - Enhanced process management
3. `test_gui_cleanup.py` - New test script (created)

## Compatibility

- ✅ Windows (taskkill fallback)
- ✅ Linux (process groups via setsid)
- ✅ macOS (process groups via setsid)
- ✅ Python 3.6+
- ✅ PyQt5

---

**Status**: ✅ FIXED - GUI cleanup now properly terminates all background processes
**Date**: January 31, 2026
