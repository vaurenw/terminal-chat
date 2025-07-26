#!/usr/bin/env python3
"""
Bluetooth RFCOMM Chat Application Launcher
A unified launcher for the terminal-based Bluetooth chat application.
"""

import sys
import os
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

def show_menu():
    """Display the main menu"""
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║    Bluetooth RFCOMM Chat Application ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Choose an option:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  1. Start Chat Server (Host a chat room){Style.RESET_ALL}")
    print(f"{Fore.GREEN}  2. Start Chat Client (Join a chat room){Style.RESET_ALL}")
    print(f"{Fore.RED}  3. Exit{Style.RESET_ALL}")
    print()

def show_requirements():
    """Show system requirements and setup instructions"""
    print(f"{Fore.CYAN}System Requirements:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• Python 3.6 or higher{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• PyBluez library (pybluez){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• Bluetooth adapter enabled{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• Bluetooth discoverable mode (for server){Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Setup Instructions:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Make sure Bluetooth is enabled on both devices{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Run the server on one device{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. Run the client on another device{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}4. The client will discover and connect to the server{Style.RESET_ALL}")
    print()

def main():
    """Main function"""
    try:
        # Check if bluetooth module is available
        import bluetooth
    except ImportError:
        print(f"{Fore.RED}Error: PyBluez library not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please install it using: pip install pybluez{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}On Windows, you might need: pip install pybluez-win10{Style.RESET_ALL}")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input(f"{Fore.CYAN}Enter your choice (1-3): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                print(f"{Fore.GREEN}Starting Chat Server...{Style.RESET_ALL}")
                print()
                # Import and run server
                try:
                    from bt_chat_server import BluetoothChatServer
                    server = BluetoothChatServer()
                    server.start_server()
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Server stopped by user.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Server error: {e}{Style.RESET_ALL}")
                    
            elif choice == '2':
                print(f"{Fore.GREEN}Starting Chat Client...{Style.RESET_ALL}")
                print()
                # Import and run client
                try:
                    from bt_chat_client import BluetoothChatClient
                    client = BluetoothChatClient()
                    client.start_client()
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Client stopped by user.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Client error: {e}{Style.RESET_ALL}")
                    
            elif choice == '3':
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
                
            elif choice.lower() == 'help':
                show_requirements()
                
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Application interrupted by user.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
            
        print()  # Add spacing between menu iterations

if __name__ == "__main__":
    main()
