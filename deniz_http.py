# Author: Deniz Can
# Task: Check for Information Disclosure via HTTP Headers
# Target: api.0x10.cloud

import urllib.request
import time

def check_header_leak():
    url = "http://api.0x10.cloud"
    
    print(f"[*] Sending request to {url}...")
    
    # Adding a small delay to respect the server's rate limit
    time.sleep(0.2) 

    try:
        req = urllib.request.urlopen(url, timeout=5)
        headers = dict(req.headers)
        
        # Extracting specific server and backend information
        server_info = headers.get("Server")
        powered_by = headers.get("X-Powered-By")
        
        print("\n--- Extracted Headers ---")
        if server_info: 
            print(f"Server: {server_info}")
        if powered_by: 
            print(f"X-Powered-By: {powered_by}")
             
        # Checking if sensitive info is leaked
        if server_info or powered_by:
            print("\n[!] VULNERABILITY DETECTED: Information Disclosure [!]")
            print("-> Issue: The server is leaking its exact version and technology stack.")
            print("-> Impact: Attackers can use this to search for version-specific exploits.")
        else:
             print("\n[-] Clean: No sensitive headers found.")

    except Exception as e:
        print(f"\n[Error] Connection failed: {e}")

if __name__ == "__main__":
    check_header_leak()