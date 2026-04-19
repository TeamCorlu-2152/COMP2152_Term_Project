# Authors: Yigit Alkoc & Deniz Can (Bonus Effort)
# Vulnerability: Anonymous FTP Login Allowed
# Target: ftp.0x10.cloud (Port 2121)

import ftplib
import time

def check_anonymous_ftp():
    target = "ftp.0x10.cloud"
    port = 2121

    print(f"[*] Connecting to {target} on port {port}...")
    time.sleep(0.5)  # Respect rate limit

    try:
        # Initialize FTP object and connect using the non-standard port
        ftp = ftplib.FTP()
        ftp.connect(target, port, timeout=5)
        
        print("[-] Connection successful. Attempting anonymous login...")
        
        # ftp.login() automatically attempts to log in as 'anonymous'
        response = ftp.login()
        
        if "230" in response:
            print("\n[!!!] BINGO: MEDIUM VULNERABILITY FOUND [!!!]")
            print("-> Risk: Anonymous FTP Access is enabled!")
            print("-> Impact: Attackers can log in without a password and steal files.")
        
        ftp.quit()

    except ftplib.all_errors as e:
        print(f"\n[-] Secure or Error: {e}")
        print("[-] The server rejected anonymous access or is not responding properly.")

if __name__ == "__main__":
    check_anonymous_ftp()