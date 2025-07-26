# Quick Start Guide

## For Real Bluetooth Communication

### Prerequisites
- Two devices with Bluetooth capability
- Python 3.8 or 3.9 (recommended for PyBluez compatibility)
- PyBluez library installed

### Setup Steps

1. **Install Python 3.8 or 3.9** on both devices (if you encounter PyBluez issues with newer versions)

2. **Install dependencies**:
   ```bash
   pip install pybluez colorama
   ```

3. **Enable Bluetooth** on both devices and make them discoverable

4. **Run the application**:
   - Device 1: `python bt_chat_server.py`
   - Device 2: `python bt_chat_client.py`

## For Testing/Simulation (Same Computer)

### Quick Test
1. Open two terminal windows
2. Terminal 1: `python chat_simulation.py server`
3. Terminal 2: `python chat_simulation.py client`
4. Start chatting!

### Using Batch Files (Windows)
1. Double-click `run_server.bat` 
2. Double-click `run_client.bat`
3. Start chatting!

## Troubleshooting

### PyBluez Installation Issues
If you get installation errors with PyBluez:

1. **Try older Python version**: Use Python 3.8 or 3.9
2. **Use conda**: `conda install pybluez`
3. **Use simulation for testing**: The TCP simulation works without PyBluez

### Windows-Specific Issues
- Make sure you have Microsoft Visual C++ Build Tools installed
- Try running as administrator
- Ensure Bluetooth drivers are up to date

### Linux-Specific Issues
- Install bluez: `sudo apt-get install bluez bluez-tools`
- Add user to dialout group: `sudo usermod -a -G dialout $USER`
- Restart after group changes

### macOS-Specific Issues
- Grant Bluetooth permissions in System Preferences
- May need to install Xcode Command Line Tools

## Testing Your Setup

Run the system test to check compatibility:
```bash
python test_bluetooth.py
```

This will verify:
- PyBluez installation
- Bluetooth adapter functionality  
- Device discovery capability
- Socket creation

## File Overview

- `bt_chat_server.py` - Real Bluetooth server
- `bt_chat_client.py` - Real Bluetooth client
- `chat_simulation.py` - TCP simulation for testing
- `test_bluetooth.py` - System compatibility test
- `chat_launcher.py` - Unified menu launcher
- `run_server.bat` / `run_client.bat` - Windows shortcuts

## Need Help?

1. Check the README.md for detailed documentation
2. Run `python test_bluetooth.py` to diagnose issues
3. Use the simulation version for testing without hardware requirements
4. Ensure both devices are on the same Bluetooth version/standard
