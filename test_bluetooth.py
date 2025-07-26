#!/usr/bin/env python3
"""
Bluetooth Test Script
Test basic Bluetooth functionality and system compatibility.
"""

import sys
from colorama import init, Fore, Style

# Initialize colorama
init()

def test_bluetooth_import():
    """Test if PyBluez can be imported"""
    print(f"{Fore.CYAN}Testing PyBluez import...{Style.RESET_ALL}")
    try:
        import bluetooth
        print(f"{Fore.GREEN}✓ PyBluez imported successfully{Style.RESET_ALL}")
        return True
    except ImportError as e:
        print(f"{Fore.RED}✗ Failed to import PyBluez: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Try installing with: pip install pybluez{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}On Windows, try: pip install pybluez-win10{Style.RESET_ALL}")
        return False

def test_local_bluetooth():
    """Test local Bluetooth adapter"""
    print(f"{Fore.CYAN}Testing local Bluetooth adapter...{Style.RESET_ALL}")
    try:
        import bluetooth
        local_addr = bluetooth.read_local_bdaddr()[0]
        print(f"{Fore.GREEN}✓ Local Bluetooth address: {local_addr}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Cannot access Bluetooth adapter: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Make sure Bluetooth is enabled{Style.RESET_ALL}")
        return False

def test_device_discovery():
    """Test Bluetooth device discovery"""
    print(f"{Fore.CYAN}Testing device discovery (this may take a few seconds)...{Style.RESET_ALL}")
    try:
        import bluetooth
        devices = bluetooth.discover_devices(duration=5, lookup_names=True)
        print(f"{Fore.GREEN}✓ Discovery completed. Found {len(devices)} device(s){Style.RESET_ALL}")
        
        if devices:
            print(f"{Fore.CYAN}Nearby devices:{Style.RESET_ALL}")
            for addr, name in devices:
                print(f"  {Fore.YELLOW}{name} ({addr}){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No devices found (this is normal if no other Bluetooth devices are nearby){Style.RESET_ALL}")
            
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Device discovery failed: {e}{Style.RESET_ALL}")
        return False

def test_socket_creation():
    """Test RFCOMM socket creation"""
    print(f"{Fore.CYAN}Testing RFCOMM socket creation...{Style.RESET_ALL}")
    try:
        import bluetooth
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.close()
        print(f"{Fore.GREEN}✓ RFCOMM socket created successfully{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Socket creation failed: {e}{Style.RESET_ALL}")
        return False

def main():
    """Run all tests"""
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     Bluetooth System Test            ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    tests = [
        ("PyBluez Import", test_bluetooth_import),
        ("Local Bluetooth Adapter", test_local_bluetooth),
        ("RFCOMM Socket Creation", test_socket_creation),
        ("Device Discovery", test_device_discovery),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{Fore.MAGENTA}Running {test_name} test...{Style.RESET_ALL}")
        if test_func():
            passed += 1
        print()
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║             Test Results              ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    
    if passed == total:
        print(f"{Fore.GREEN}All tests passed! ({passed}/{total}){Style.RESET_ALL}")
        print(f"{Fore.GREEN}Your system is ready to run the Bluetooth chat application.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Passed: {passed}/{total} tests{Style.RESET_ALL}")
        print(f"{Fore.RED}Some tests failed. Please check the error messages above.{Style.RESET_ALL}")
        
    print(f"\n{Fore.CYAN}System Information:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Python version: {sys.version}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Platform: {sys.platform}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
