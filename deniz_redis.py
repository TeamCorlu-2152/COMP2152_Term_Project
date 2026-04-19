# Author: Deniz Can
# Vulnerability: Exposed Redis Database (Critical/Hard Level)
# Target: redis.0x10.cloud (Port 6379)

import socket
import time

def check_redis_vuln():
    target = "redis.0x10.cloud"
    port = 6379
    
    print("=" * 65)
    print("  Advanced Security Scan: Unauthenticated Redis Database")
    print("=" * 65)
    
    print(f"\n[*] Target: {target}")
    print(f"[*] Port:   {port}")
    print("[*] Scanning for exposed database...")
    
    time.sleep(0.15) # Rate limit kuralına uyuyoruz
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print("\n[!!!] CRITICAL VULNERABILITY FOUND [!!!]")
            print(f"-> Port {port} (Redis) is deliberately OPEN on {target}.")
            print("-> RISK: Redis databases do not use authentication by default.")
            print("-> IMPACT: Attackers can connect without a password, dump the entire database, steal user data, or gain Remote Code Execution (RCE) on the server.")
        else:
            print(f"\n[-] Port {port} is closed. Target is secure.")
            
        sock.close()
    except Exception as e:
        print(f"\n[-] Error during scan: {e}")

if __name__ == "__main__":
    check_redis_vuln()