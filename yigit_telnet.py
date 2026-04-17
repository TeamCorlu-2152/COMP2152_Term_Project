# Author: Yigit Alkoc
# Vulnerability: Cleartext Telnet Service Detected
# Target: telnet.0x10.cloud

import socket
import time

def check_telnet_vulnerability():
    target_host = "telnet.0x10.cloud"
    target_port = 2323

    print(f"[*] Scanning port {target_port} on {target_host}...")
    
    # Adding delay to respect the 10 requests/second rate limit
    time.sleep(0.2) 

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        
        result = sock.connect_ex((target_host, target_port))
        
        if result == 0:
            print("\n[!!!] VULNERABILITY FOUND: Critical Security Risk [!!!]")
            print(f"Status: Port {target_port} (Telnet) is OPEN on {target_host}.")
            print("Risk: Telnet transmits data in cleartext without encryption.")
            print("Attackers sniffing the network can capture usernames and passwords.")
        else:
            print(f"\n[-] Port {target_port} is closed or unreachable. (Code: {result})")
            
        sock.close()

    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_telnet_vulnerability()