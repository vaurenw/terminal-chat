```
████████╗     ██████╗██╗  ██╗ █████╗ ████████╗
╚══██╔══╝    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
   ██║       ██║     ███████║███████║   ██║   
   ██║       ██║     ██╔══██║██╔══██║   ██║   
   ██║       ╚██████╗██║  ██║██║  ██║   ██║   
   ╚═╝        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
```

Terminal-based chat application for Bluetooth communication with optional encryption.

## Install

```bash
pip install -r requirements.txt
```

## Usage

**Server:**
```bash
python bt_chat_server.py
```

**Client:**
```bash
python bt_chat_client.py
```

**Test without Bluetooth:**
```bash
python chat_simulation.py server
python chat_simulation.py client
```

## Features

- Bluetooth RFCOMM communication
- AES-256 encryption (optional)
- Real-time messaging
- Device discovery
- Terminal interface

## Requirements

- Python 3.6+
- Bluetooth adapter
- PyBluez, colorama, cryptography

