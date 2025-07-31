#!/usr/bin/env python3
"""
Bluetooth RFCOMM Chat Server
A terminal-based chat application that allows two devices to communicate via Bluetooth.
This is the server component that waits for incoming connections.
"""

import bluetooth
import threading
import sys
import os
from colorama import init, Fore, Style
from encryption import ChatEncryption, get_chat_password

# Initialize colorama for Windows compatibility
init()

class BluetoothChatServer:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.client_info = None
        self.running = False
        self.username = "Server"
        self.encryption = None
        
    def start_server(self):
        """Start the Bluetooth RFCOMM server"""
        # Setup encryption
        password = get_chat_password()
        if password:
            self.encryption = ChatEncryption(password)
            print(f"{Fore.GREEN}🔒 Encryption enabled{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  No encryption - messages will be sent in plaintext{Style.RESET_ALL}")
        
        try:
            # Create a Bluetooth socket using RFCOMM protocol
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            
            # Get local Bluetooth adapter address
            local_addr = bluetooth.read_local_bdaddr()[0]
            print(f"{Fore.CYAN}Starting Bluetooth Chat Server...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Local Bluetooth Address: {local_addr}{Style.RESET_ALL}")
            
            # Bind to any available port
            self.server_socket.bind((local_addr, bluetooth.PORT_ANY))
            port = self.server_socket.getsockname()[1]
            
            # Listen for incoming connections
            self.server_socket.listen(1)
            print(f"{Fore.GREEN}Server listening on port {port}...{Style.RESET_ALL}")
            
            # Make device discoverable
            uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            bluetooth.advertise_service(
                self.server_socket, 
                "BluetoothChatServer",
                service_id=uuid,
                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE]
            )
            
            print(f"{Fore.MAGENTA}Waiting for client connection...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Service UUID: {uuid}{Style.RESET_ALL}")
            
            # Accept incoming connection
            self.client_socket, self.client_info = self.server_socket.accept()
            print(f"{Fore.GREEN}✓ Connected to {self.client_info}{Style.RESET_ALL}")
            
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
                self.stop_server()
                
        except bluetooth.BluetoothError as e:
            print(f"{Fore.RED}Bluetooth Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Make sure Bluetooth is enabled and this device is discoverable.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        finally:
            self.cleanup()
            
    def receive_messages(self):
        """Receive messages from the client"""
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                    
                message = data.decode('utf-8').strip()
                if message.lower() in ['quit', 'exit']:
                    print(f"{Fore.RED}Client disconnected.{Style.RESET_ALL}")
                    self.running = False
                    break
                
                # Decrypt message if encryption is enabled
                if self.encryption and self.encryption.is_encrypted():
                    try:
                        decrypted_message = self.encryption.decrypt_message(message)
                        print(f"{Fore.BLUE}Client: {decrypted_message} {Fore.GREEN}🔒{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Failed to decrypt message from client{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Client (encrypted): {message[:50]}...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.BLUE}Client: {message}{Style.RESET_ALL}")
                
            except bluetooth.BluetoothError:
                print(f"{Fore.RED}Connection lost.{Style.RESET_ALL}")
                self.running = False
                break
            except Exception as e:
                print(f"{Fore.RED}Error receiving message: {e}{Style.RESET_ALL}")
                break
                
    def send_messages(self):
        """Send messages to the client"""
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
                    # Encrypt message if encryption is enabled
                    if self.encryption and self.encryption.is_encrypted():
                        encrypted_message = self.encryption.encrypt_message(message)
                        self.client_socket.send(encrypted_message.encode('utf-8'))
                        print(f"\033[F{Fore.GREEN}{self.username}: {message} {Fore.GREEN}🔒{Style.RESET_ALL}")
                    else:
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
                
    def stop_server(self):
        """Stop the server and close connections"""
        self.running = False
        print(f"\n{Fore.YELLOW}Shutting down server...{Style.RESET_ALL}")
        
    def cleanup(self):
        """Clean up resources"""
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
                
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

def main():
    """Main function"""
    print(f"{Fore.CYAN}████████╗     ██████╗██╗  ██╗ █████╗ ████████╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══██╔══╝    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝{Style.RESET_ALL}")
    print(f"{Fore.CYAN}   ██║       ██║     ███████║███████║   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}   ██║       ██║     ██╔══██║██╔══██║   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}   ██║       ╚██████╗██║  ██║██║  ██║   ██║   {Style.RESET_ALL}")
    print(f"{Fore.CYAN}   ╚═╝        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   {Style.RESET_ALL}")
    print()
    
    server = BluetoothChatServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Server interrupted by user.{Style.RESET_ALL}")
    finally:
        server.cleanup()
        print(f"{Fore.GREEN}Server closed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
