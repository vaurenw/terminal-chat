#!/usr/bin/env python3
"""
Bluetooth RFCOMM Chat Client
A terminal-based chat application that allows two devices to communicate via Bluetooth.
This is the client component that connects to a server.
"""

import bluetooth
import threading
import sys
import time
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

class BluetoothChatClient:
    def __init__(self):
        self.client_socket = None
        self.running = False
        self.username = "Client"
        
    def discover_devices(self):
        """Discover nearby Bluetooth devices"""
        print(f"{Fore.CYAN}Discovering nearby Bluetooth devices...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This may take a few seconds...{Style.RESET_ALL}")
        
        try:
            nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            
            if not nearby_devices:
                print(f"{Fore.RED}No Bluetooth devices found.{Style.RESET_ALL}")
                return []
                
            print(f"{Fore.GREEN}Found {len(nearby_devices)} device(s):{Style.RESET_ALL}")
            for i, (addr, name) in enumerate(nearby_devices):
                print(f"{Fore.CYAN}  {i+1}. {name} ({addr}){Style.RESET_ALL}")
                
            return nearby_devices
            
        except bluetooth.BluetoothError as e:
            print(f"{Fore.RED}Error discovering devices: {e}{Style.RESET_ALL}")
            return []
            
    def find_chat_service(self, target_addr):
        """Find the chat service on the target device"""
        print(f"{Fore.CYAN}Searching for chat service on {target_addr}...{Style.RESET_ALL}")
        
        try:
            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            service_matches = bluetooth.find_service(uuid=uuid, address=target_addr)
            
            if len(service_matches) == 0:
                print(f"{Fore.RED}No chat service found on {target_addr}{Style.RESET_ALL}")
                return None
                
            first_match = service_matches[0]
            port = first_match["port"]
            name = first_match["name"]
            host = first_match["host"]
            
            print(f"{Fore.GREEN}Found service '{name}' on {host}:{port}{Style.RESET_ALL}")
            return port
            
        except bluetooth.BluetoothError as e:
            print(f"{Fore.RED}Error finding service: {e}{Style.RESET_ALL}")
            return None
            
    def connect_to_server(self, server_addr, port):
        """Connect to the chat server"""
        try:
            print(f"{Fore.CYAN}Connecting to {server_addr}:{port}...{Style.RESET_ALL}")
            
            # Create a Bluetooth socket using RFCOMM protocol
            self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.client_socket.connect((server_addr, port))
            
            print(f"{Fore.GREEN}✓ Connected to server!{Style.RESET_ALL}")
            self.running = True
            
            # Start threads for sending and receiving messages
            receive_thread = threading.Thread(target=self.receive_messages)
            send_thread = threading.Thread(target=self.send_messages)
            
            receive_thread.daemon = True
            send_thread.daemon = True
            
            receive_thread.start()
            send_thread.start()
            
            print(f"{Fore.GREEN}Chat started! Type your messages below.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Type 'quit' or 'exit' to close the connection.{Style.RESET_ALL}")
            print("-" * 50)
            
            # Keep main thread alive
            try:
                while self.running:
                    threading.Event().wait(1)
            except KeyboardInterrupt:
                self.disconnect()
                
        except bluetooth.BluetoothError as e:
            print(f"{Fore.RED}Connection failed: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        finally:
            self.cleanup()
            
    def receive_messages(self):
        """Receive messages from the server"""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                    
                message = data.decode('utf-8').strip()
                if message.lower() in ['quit', 'exit']:
                    print(f"{Fore.RED}Server disconnected.{Style.RESET_ALL}")
                    self.running = False
                    break
                    
                print(f"{Fore.BLUE}Server: {message}{Style.RESET_ALL}")
                
            except bluetooth.BluetoothError:
                print(f"{Fore.RED}Connection lost.{Style.RESET_ALL}")
                self.running = False
                break
            except Exception as e:
                print(f"{Fore.RED}Error receiving message: {e}{Style.RESET_ALL}")
                break
                
    def send_messages(self):
        """Send messages to the server"""
        while self.running:
            try:
                message = input()
                if not self.running:
                    break
                    
                if message.lower() in ['quit', 'exit']:
                    self.client_socket.send(message.encode('utf-8'))
                    self.running = False
                    break
                    
                if message.strip():  # Only send non-empty messages
                    self.client_socket.send(message.encode('utf-8'))
                    print(f"\033[F{Fore.GREEN}{self.username}: {message}{Style.RESET_ALL}")
                    
            except bluetooth.BluetoothError:
                print(f"{Fore.RED}Connection lost.{Style.RESET_ALL}")
                self.running = False
                break
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")
                break
                
    def disconnect(self):
        """Disconnect from the server"""
        self.running = False
        print(f"\n{Fore.YELLOW}Disconnecting from server...{Style.RESET_ALL}")
        
    def cleanup(self):
        """Clean up resources"""
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
                
    def start_client(self):
        """Start the client and connect to a server"""
        # Discover devices
        devices = self.discover_devices()
        if not devices:
            return
            
        # Let user choose a device
        print()
        while True:
            try:
                choice = input(f"{Fore.CYAN}Enter device number to connect to (1-{len(devices)}): {Style.RESET_ALL}")
                device_index = int(choice) - 1
                if 0 <= device_index < len(devices):
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and {len(devices)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
                return
                
        target_addr, target_name = devices[device_index]
        print(f"{Fore.CYAN}Selected: {target_name} ({target_addr}){Style.RESET_ALL}")
        
        # Find chat service on the selected device
        port = self.find_chat_service(target_addr)
        if port is None:
            return
            
        # Connect to the server
        self.connect_to_server(target_addr, port)

def main():
    """Main function"""
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     Bluetooth RFCOMM Chat Client     ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    
    client = BluetoothChatClient()
    
    try:
        client.start_client()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Client interrupted by user.{Style.RESET_ALL}")
    finally:
        client.cleanup()
        print(f"{Fore.GREEN}Client closed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
