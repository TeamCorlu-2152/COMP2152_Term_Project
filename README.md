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

- Yigit Alkoc: [BURAYA YİĞİT'İN YOUTUBE LİNKİ GELECEK]
- Deniz Can: [BURAYA DENİZ'İN YOUTUBE LİNKİ GELECEK]

## Target

- Server: `0x10.cloud` and its subdomains
- Submission: http://submit.0x10.cloud
- Leaderboard: http://ranking.0x10.cloud

## Important: Rate Limit

The server allows **10 requests per second** per IP address. If you send requests too fast, you will get blocked (HTTP 429). Add a small delay between requests:

```python
import time
time.sleep(0.15)  # wait 150ms between requests
