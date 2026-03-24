# How the Starter Code Works

This document breaks down each script so you understand what every line does and why.

---

## example_http_check.py

**Goal:** Determine if `blog.0x10.cloud` uses HTTPS.

```python
import urllib.request
```
`urllib.request` is Python's built-in HTTP client. It handles HTTP and HTTPS requests, follows redirects, and gives you the response object.

```python
response = urllib.request.urlopen(target)
```
This opens a connection to the URL and returns a response object. If the server redirects (e.g., `http://` to `https://`), `urlopen` follows the redirect automatically. The key insight: after `urlopen` finishes, `response.url` contains the **final** URL after all redirects.

```python
final_url = response.url
```
If the server redirected `http://blog.0x10.cloud` to `https://blog.0x10.cloud`, then `final_url` would start with `https://`. If it stayed on `http://`, the server never redirected — meaning no HTTPS enforcement.

```python
if final_url.startswith("http://"):
```
This is the actual vulnerability check. A site that stays on `http://` sends all traffic unencrypted. Anyone on the same network (coffee shop WiFi, shared LAN) can read everything — login credentials, session cookies, form data.

**Why `try/except`:** The server might be down, DNS might not resolve, or the connection might time out. Without error handling, the script crashes with a traceback instead of a clean error message.

---

## example_port_check.py

**Goal:** Check if Telnet (port 2323) is open on `telnet.0x10.cloud`.

```python
import socket
```
`socket` is Python's low-level networking module. It lets you create raw TCP/UDP connections — the same layer that HTTP, FTP, SSH, and every other protocol is built on.

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
Creates a TCP socket. `AF_INET` = IPv4 addressing. `SOCK_STREAM` = TCP (reliable, ordered, connection-based). If you wanted UDP, you'd use `SOCK_DGRAM`.

```python
sock.settimeout(2)
```
Without a timeout, `connect_ex` blocks indefinitely if the server doesn't respond. Two seconds is enough for a server that's up. If it takes longer, the port is either closed or firewalled.

```python
result = sock.connect_ex((target, port))
```
`connect_ex` is different from `connect`. Regular `connect` raises an exception on failure. `connect_ex` returns an error code instead — `0` means success (port is open), anything else means failure (port closed, refused, or unreachable). This is the same approach your Assignment 2 port scanner used.

The argument is a tuple `(host, port)`. Python resolves the hostname to an IP internally using DNS.

```python
if result == 0:
```
Port is open. For Telnet, an open port is itself the vulnerability — Telnet transmits everything in plaintext including passwords. There is no encrypted version of Telnet. The secure replacement is SSH.

```python
sock.close()
```
Closes the TCP connection and releases the file descriptor. Not closing sockets leads to resource leaks — the OS has a limit on open file descriptors.

**Why port 2323 instead of 23:** The server runs services on non-standard ports. Default Telnet is port 23, but this server uses 2323. In real-world security, services often run on non-standard ports. A good scanner checks more than just the defaults.

---

## example_header_check.py

**Goal:** Read HTTP response headers to find information leaks.

### Check 1: Server version disclosure

```python
response = urllib.request.urlopen(target, timeout=5)
headers = dict(response.headers)
```
`response.headers` is an `http.client.HTTPMessage` object. Converting it to a `dict` makes it easier to look up specific headers by name.

```python
server = headers.get("Server", "Not disclosed")
powered_by = headers.get("X-Powered-By", "Not disclosed")
```
`.get(key, default)` returns the header value if it exists, or the default string if it doesn't. Two headers matter here:

- **`Server`** — usually set by the web server software (Apache, nginx, IIS). If it includes a version number (e.g., `nginx/1.14.0`), an attacker can search for known vulnerabilities in that exact version.
- **`X-Powered-By`** — set by the application framework (Express, PHP, Django). Same risk — version disclosure narrows the attack surface.

Production servers should either remove these headers entirely or set them to a generic value.

### Check 2: Internal IP leak

```python
interesting = ["X-Forwarded-For", "X-Real-IP", "X-Backend-Server", "Via"]
```
These headers are typically set by reverse proxies and load balancers. They're meant for internal use — the proxy tells the backend server where the request originally came from. When these headers leak to the client:

- **`X-Forwarded-For`** — the client's real IP, but if misconfigured it contains the internal proxy's IP instead
- **`X-Real-IP`** — same purpose, used by nginx
- **`X-Backend-Server`** — reveals the internal hostname of the backend server
- **`Via`** — shows the proxy chain, often including internal IPs

Internal IPs (10.x.x.x, 192.168.x.x, 172.16-31.x.x) reveal network topology. An attacker now knows how many servers exist, what subnets they're on, and can target them specifically if they gain internal access.

---

## main.py

**Goal:** Run all three example scripts in sequence.

```python
script_dir = os.path.dirname(os.path.abspath(__file__))
```
`__file__` is the path of the currently running script. `os.path.abspath` makes it absolute (not relative). `os.path.dirname` strips the filename, leaving just the directory. This ensures the runner finds the example scripts no matter what directory you run it from.

```python
print("=" * 50, flush=True)
```
`flush=True` forces Python to write the output immediately. Without it, Python buffers stdout — meaning your header text might appear *after* the subprocess output, which looks broken.

```python
subprocess.run([sys.executable, script_path])
```
`sys.executable` is the path to the Python interpreter running this script (e.g., `/usr/bin/python3`). Using it instead of hardcoding `"python3"` ensures the same Python version runs the sub-scripts. `subprocess.run` starts a new process, waits for it to finish, then continues.

---

## Patterns to Reuse

When you write your own vulnerability scripts, you'll use the same building blocks:

| Task | Module | Key function |
|------|--------|-------------|
| HTTP request (GET) | `urllib.request` | `urlopen(url)` |
| HTTP request (POST) | `urllib.request` | `urlopen(Request(url, data=...))` |
| Read response headers | `urllib.request` | `dict(response.headers)` |
| TCP port check | `socket` | `sock.connect_ex((host, port))` |
| Send/receive raw TCP | `socket` | `sock.sendall(data)` / `sock.recv(1024)` |
| Read response body | `urllib.request` | `response.read().decode()` |
| Parse JSON response | `json` | `json.loads(body)` |
| Decode base64 | `base64` | `base64.b64decode(data)` |
| Rate limit yourself | `time` | `time.sleep(0.15)` |

Every vulnerability on `0x10.cloud` can be found using some combination of these.
