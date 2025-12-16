#!/usr/bin/env python3
"""
Utility script to clean up wireless interfaces after roguehostapd crashes
This helps restore normal NetworkManager functionality on CachyOS and similar systems
"""

import subprocess
import sys
import argparse


def run_command(cmd, ignore_errors=True):
    """Run a shell command and optionally ignore errors"""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            check=not ignore_errors
        )
        if result.stdout:
            print(f"  {result.stdout.strip()}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            print(f"  Error: {e.stderr.strip()}")
        return False


def cleanup_interface(interface):
    """Clean up a wireless interface and restore it to managed mode"""
    print(f"[*] Cleaning up interface: {interface}")
    
    # Kill any remaining hostapd processes
    print("[*] Killing any hostapd processes...")
    run_command(['pkill', '-9', 'hostapd'])
    
    # Bring interface down
    print("[*] Bringing interface down...")
    run_command(['ip', 'link', 'set', interface, 'down'])
    
    # Set back to managed mode
    print("[*] Setting interface to managed mode...")
    if run_command(['iw', 'dev', interface, 'set', 'type', 'managed']):
        print("[✓] Interface set to managed mode")
    else:
        print("[!] Warning: Could not set managed mode")
    
    # Bring interface back up
    print("[*] Bringing interface back up...")
    run_command(['ip', 'link', 'set', interface, 'up'])
    
    # Unblock WiFi (in case rfkill was used)
    print("[*] Unblocking WiFi with rfkill...")
    run_command(['rfkill', 'unblock', 'wifi'])
    run_command(['rfkill', 'unblock', 'all'])
    
    print("[*] Done!")


def restart_network_manager():
    """Restart NetworkManager service"""
    print("[*] Restarting NetworkManager...")
    if run_command(['systemctl', 'restart', 'NetworkManager'], ignore_errors=False):
        print("[✓] NetworkManager restarted successfully")
    else:
        print("[!] Failed to restart NetworkManager")
        print("[!] You may need to run this script with sudo")


def list_wireless_interfaces():
    """List all wireless interfaces"""
    print("[*] Detecting wireless interfaces...")
    result = subprocess.run(
        ['iw', 'dev'],
        capture_output=True,
        text=True
    )
    
    interfaces = []
    for line in result.stdout.split('\n'):
        if 'Interface' in line:
            iface = line.split()[-1]
            interfaces.append(iface)
    
    return interfaces


def main():
    parser = argparse.ArgumentParser(
        description="Clean up wireless interfaces after roguehostapd crash"
    )
    parser.add_argument(
        '-i', '--interface',
        help="Specific interface to clean up (e.g., wlan0)"
    )
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help="Clean up all wireless interfaces"
    )
    parser.add_argument(
        '--no-restart',
        action='store_true',
        help="Don't restart NetworkManager"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RogueHostapd Interface Cleanup Utility")
    print("=" * 60)
    
    # Check if running as root
    if subprocess.run(['id', '-u'], capture_output=True, text=True).stdout.strip() != '0':
        print("[!] Warning: Not running as root. Some operations may fail.")
        print("[!] Consider running with: sudo python3 cleanup_interface.py")
        print()
    
    if args.interface:
        # Clean up specific interface
        cleanup_interface(args.interface)
    elif args.all:
        # Clean up all wireless interfaces
        interfaces = list_wireless_interfaces()
        if interfaces:
            print(f"[*] Found {len(interfaces)} wireless interface(s): {', '.join(interfaces)}")
            for iface in interfaces:
                cleanup_interface(iface)
        else:
            print("[!] No wireless interfaces found")
    else:
        # Auto-detect and clean up
        interfaces = list_wireless_interfaces()
        if not interfaces:
            print("[!] No wireless interfaces found")
            return 1
        
        if len(interfaces) == 1:
            cleanup_interface(interfaces[0])
        else:
            print(f"[*] Found multiple interfaces: {', '.join(interfaces)}")
            print("[*] Please specify which interface to clean up:")
            print(f"    python3 cleanup_interface.py -i <interface>")
            print(f"    or use -a to clean all interfaces")
            return 1
    
    # Restart NetworkManager unless told not to
    if not args.no_restart:
        print()
        restart_network_manager()
    
    print()
    print("[✓] Cleanup complete!")
    print("[*] Your WiFi connection should now work normally.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
