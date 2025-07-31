#!/usr/bin/env python3
"""
Bluetooth Chat Simulation with Encryption
A simulation version of the Bluetooth chat for testing purposes when PyBluez is not available.
This uses standard sockets over localhost to simulate the Bluetooth communication.
"""

import socket
import threading
import sys
from colorama import init, Fore, Style
from encryption import ChatEncryption, get_chat_password

# Initialize colorama for Windows compatibility
init()

class BluetoothChatSimServer:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.client_info = None
        self.running = False
        self.username = "Server"
        self.encryption = None
        
    def start_server(self):
        """Start the simulation server"""
        # Setup encryption
        password = get_chat_password()
        if password:
            self.encryption = ChatEncryption(password)
            print(f"{Fore.GREEN}🔒 Encryption enabled{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  No encryption - messages will be sent in plaintext{Style.RESET_ALL}")
        
        try:
            # Create a TCP socket (simulating Bluetooth RFCOMM)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to localhost
            host = 'localhost'
            port = 12345  # Fixed port for simulation
            self.server_socket.bind((host, port))
            
            print(f"{Fore.CYAN}Starting Bluetooth Chat Server Simulation...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Simulation Address: {host}:{port}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Note: This is a simulation using TCP sockets{Style.RESET_ALL}")
            
            # Listen for incoming connections
            self.server_socket.listen(1)
            print(f"{Fore.GREEN}Server listening on {host}:{port}...{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Waiting for client connection...{Style.RESET_ALL}")
            
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
                
            except socket.error:
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
                    
            except socket.error:
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

class BluetoothChatSimClient:
    def __init__(self):
        self.client_socket = None
        self.running = False
        self.username = "Client"
        self.encryption = None
        
    def connect_to_server(self):
        """Connect to the simulation server"""
        # Setup encryption
        password = get_chat_password()
        if password:
            self.encryption = ChatEncryption(password)
            print(f"{Fore.GREEN}🔒 Encryption enabled{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  No encryption - messages will be sent in plaintext{Style.RESET_ALL}")
        
        try:
            host = 'localhost'
            port = 12345
            
            print(f"{Fore.CYAN}Connecting to simulation server at {host}:{port}...{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Note: This is a simulation using TCP sockets{Style.RESET_ALL}")
            
            # Create a TCP socket (simulating Bluetooth RFCOMM)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
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
                
        except ConnectionRefusedError:
            print(f"{Fore.RED}Connection refused. Make sure the server is running first.{Style.RESET_ALL}")
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
                
                # Decrypt message if encryption is enabled
                if self.encryption and self.encryption.is_encrypted():
                    try:
                        decrypted_message = self.encryption.decrypt_message(message)
                        print(f"{Fore.BLUE}Server: {decrypted_message} {Fore.GREEN}🔒{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Failed to decrypt message from server{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}Server (encrypted): {message[:50]}...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.BLUE}Server: {message}{Style.RESET_ALL}")
                
            except socket.error:
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
                    # Encrypt message if encryption is enabled
                    if self.encryption and self.encryption.is_encrypted():
                        encrypted_message = self.encryption.encrypt_message(message)
                        self.client_socket.send(encrypted_message.encode('utf-8'))
                        print(f"\033[F{Fore.GREEN}{self.username}: {message} {Fore.GREEN}🔒{Style.RESET_ALL}")
                    else:
                        self.client_socket.send(message.encode('utf-8'))
                        print(f"\033[F{Fore.GREEN}{self.username}: {message}{Style.RESET_ALL}")
                    
            except socket.error:
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

def main():
    """Main function"""
    if len(sys.argv) != 2 or sys.argv[1] not in ['server', 'client']:
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║   Bluetooth Chat Simulation         ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        print(f"{Fore.YELLOW}Usage:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  python chat_simulation.py server   # Start as server{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  python chat_simulation.py client   # Start as client{Style.RESET_ALL}")
        print()
        print(f"{Fore.MAGENTA}Note: This is a TCP simulation of Bluetooth RFCOMM with encryption support.{Style.RESET_ALL}")
        return
    
    mode = sys.argv[1]
    
    if mode == 'server':
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║   Bluetooth Chat Simulation Server  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        server = BluetoothChatSimServer()
        try:
            server.start_server()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Server interrupted by user.{Style.RESET_ALL}")
        finally:
            server.cleanup()
            print(f"{Fore.GREEN}Server closed.{Style.RESET_ALL}")
            
    else:  # client
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║   Bluetooth Chat Simulation Client  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        
        client = BluetoothChatSimClient()
        try:
            client.connect_to_server()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Client interrupted by user.{Style.RESET_ALL}")
        finally:
            client.cleanup()
            print(f"{Fore.GREEN}Client closed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
