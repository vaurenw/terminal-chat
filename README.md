# Bluetooth RFCOMM Terminal Chat Application

A terminal-based chat application that allows two devices to communicate via Bluetooth using the RFCOMM protocol.

## System Requirements

- Python 3.6 or higher
- Bluetooth adapter on both devices
- Windows, Linux, or macOS
- PyBluez library

## Installation

1. **Clone or download** the project files to both devices
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note for Windows users**: PyBluez may have compatibility issues with newer Python versions. If you encounter installation problems:
   
   ### Alternative Installation Methods:
   - Try using Python 3.8 or 3.9 instead of newer versions
   - Use conda: `conda install pybluez colorama`
   - For testing purposes, use the simulation version (see Testing section below)

3. **Enable Bluetooth** on both devices
4. **Make devices discoverable** (especially the server device)

## Testing Without Bluetooth

If you're having trouble with PyBluez installation, you can test the chat functionality using the simulation version:

```bash
# Terminal 1 (Server)
python chat_simulation.py server

# Terminal 2 (Client)
python chat_simulation.py client
```

This uses TCP sockets over localhost to simulate the Bluetooth communication, allowing you to test the chat interface and functionality.

## Usage

**On the first device (Server):**
```bash
python bt_chat_server.py
```

**On the second device (Client):**
```bash
python bt_chat_client.py
```

## How It Works

1. **Server Setup**: One device runs as a server, creating a Bluetooth service and waiting for connections
2. **Device Discovery**: The client discovers nearby Bluetooth devices
3. **Service Discovery**: The client searches for the chat service on the selected device
4. **Connection**: The client connects to the server using RFCOMM protocol
5. **Chat**: Both devices can send and receive messages in real-time

## File Structure

```
terminal-chat/
├── bt_chat_server.py    # Server component
├── bt_chat_client.py    # Client component  
├── chat_simulation.py   # TCP simulation for testing
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Commands

While chatting, you can use these commands:
- **Type any message** and press Enter to send
- **`quit`** or **`exit`**: Close the chat connection
- **Ctrl+C**: Force quit the application

## Troubleshooting

### Common Issues

1. **"Import bluetooth could not be resolved"**
   - Install PyBluez: `pip install pybluez`
   - Try using Python 3.8-3.9 instead of newer versions
   - Use conda: `conda install pybluez`
   - For testing, use the simulation: `python chat_simulation.py server|client`

2. **"No Bluetooth devices found"**
   - Ensure Bluetooth is enabled on both devices
   - Make sure the server device is discoverable
   - Try running device discovery longer (increase duration in code)

3. **"Connection failed"**
   - Check if both devices are paired (not always required)
   - Ensure the server is running before starting the client
   - Verify Bluetooth permissions on your OS

4. **"No chat service found"**
   - Make sure the server is running and listening
   - Check firewall/security settings that might block Bluetooth

### Platform-Specific Notes

- **Windows**: May require additional Bluetooth drivers or PyBluez-win10
- **Linux**: May require `bluez` and `bluez-tools` packages
- **macOS**: Generally works out of the box with PyBluez

## Technical Details

- **Protocol**: RFCOMM (Radio Frequency Communication)
- **Service UUID**: `94f39d29-7d6d-437d-973b-fba39e49d4ee`
- **Port**: Dynamically assigned by the system
- **Encoding**: UTF-8 for message transmission
- **Threading**: Separate threads for sending and receiving messages

## Security Notes

- This is a basic implementation for demonstration purposes
- Messages are transmitted in plain text over Bluetooth
- For production use, consider adding encryption and authentication
- Be cautious when accepting connections from unknown devices

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

