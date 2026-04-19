# COMP2152 — Term Project: CTF Bug Bounty

## Team Name
TeamCorlu-2152

## Team Members

| Member | Vulnerability Found | Branch Name |
|--------|-------------------|-------------|
| Yigit Alkoc | Cleartext Telnet Service on Port 2323 | yigit_telnet |
| Deniz Can | Exposed Redis Database on Port 6379 | deniz_ftp_hard |
| Yigit & Deniz (Bonus) | Anonymous FTP Login Allowed (Medium Risk) | bonus_ftp |

## Videos

Each team member records a short video (max 3 minutes) explaining their vulnerability. Add your YouTube links below:

- Yigit Alkoc: (https://www.youtube.com/watch?v=BF-N-GAjWTI)
- Deniz Can: https://youtu.be/T5J3xUznY_M 

## Target

- Server: `0x10.cloud` and its subdomains
- Submission: [http://submit.0x10.cloud](http://submit.0x10.cloud)
- Leaderboard: [http://ranking.0x10.cloud](http://ranking.0x10.cloud)

## Important: Rate Limit

The server allows **10 requests per second** per IP address. If you send requests too fast, you will get blocked (HTTP 429). Add a small delay between requests:

```python
import time
time.sleep(0.15)  # wait 150ms between requests
```

Getting Started
Look at the three example scripts:

example_http_check.py — checks if a site uses HTTPS (uses urllib)

example_port_check.py — checks if a port is open (uses socket)

example_header_check.py — reads HTTP response headers for info leaks (uses urllib)

Run all examples: python3 main.py

Create your own branch: git checkout -b your_vuln_name

Write a Python script that finds and demonstrates a vulnerability

Submit your finding at http://submit.0x10.cloud

Merge your branch into master when done

Rules
Python standard library only — socket, urllib, ssl, json, base64, time. No pip packages.

Only scan *.0x10.cloud — do not scan any other domain.

Respect the rate limit — 10 requests/second max.
