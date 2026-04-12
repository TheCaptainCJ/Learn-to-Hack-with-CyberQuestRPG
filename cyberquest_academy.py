"""
CyberQuest Academy — Cybersecurity Learning RPG
================================================
A quest-based learning app covering Linux, networking, web hacking,
cryptography, Python scripting, and more. Built for Parrot OS / Kali Linux.

Requirements: Python 3.8+ (standard library only)
Run with:     python cyberquest_academy.py
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# SAVE / LOAD SYSTEM
# Player progress is stored as JSON in the user's home directory.
# ---------------------------------------------------------------------------

SAVE_DIR  = Path.home() / ".cyberquest"
SAVE_FILE = SAVE_DIR / "academy_save.json"

def load_save():
    """Load the player's save file, or return a fresh empty save."""
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass  # Corrupt save? Fall through to a fresh start.

    return {
        "completed_quests": [],
        "bonus_completed":  [],
        "exam_scores":      {},
        "side_quests_done": [],
        "seen_requirements": False,
        "started": datetime.now().isoformat(),
    }


def write_save(data):
    """Write the player's progress to disk."""
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# GETTING STARTED TEXT
# Shown on first launch so the player knows what they need.
# ---------------------------------------------------------------------------

REQUIREMENTS_TEXT = """═══ CYBERQUEST ACADEMY — GETTING STARTED ═══

► REQUIRED OS:
  Parrot Security OS (recommended) or Kali Linux
  Download: https://www.parrotsec.org/download/
  Run inside Hyper-V, VirtualBox, or VMware

► HYPER-V SETUP (Windows 10/11):
  1. Enable Hyper-V: Settings → Apps → Optional Features → More Windows Features → Hyper-V
  2. Create VM: 4GB+ RAM, 40GB+ disk, Generation 1
  3. Mount Parrot ISO and install

► PYTHON 3 (should be pre-installed on Parrot):
  Verify: python3 --version
  If missing: sudo apt install python3 python3-pip
  Virtual env: python3 -m venv ~/myenv && source ~/myenv/bin/activate

► RECOMMENDED TOOLS (pre-installed on Parrot):
  nmap, wireshark, tcpdump, burpsuite, metasploit-framework,
  john, hashcat, hydra, gobuster, nikto, sqlmap, suricata

► PRACTICE TARGETS (set up in your lab):
  - Metasploitable 2 (intentionally vulnerable Linux)
  - DVWA (Damn Vulnerable Web Application)
  - OWASP Juice Shop (modern web app vulnerabilities)
  Install DVWA: sudo apt install dvwa

► THIS APP:
  Runs on Windows (where you manage your VMs).
  All hands-on commands run on your Parrot OS VM.
  Progress saves to: ~/.cyberquest/academy_save.json

► TIPS:
  - Start with Tier 1 quests in any tree
  - Complete quests to unlock higher tiers
  - Bonus objectives give extra XP (claim after completing quest)
  - Take exams to test your knowledge
  - Use the Python tab to learn scripting
  - Hit the hint button if you're stuck
"""


# ---------------------------------------------------------------------------
# SKILL TREES
# Each tree has a key used throughout the quest data, plus display info.
# ---------------------------------------------------------------------------

SKILL_TREES = {
    "linux":      {"name": "Linux Mastery",        "icon": "🐧", "color": "#00ff88"},
    "networking": {"name": "Networking",            "icon": "🌐", "color": "#00ccff"},
    "crypto":     {"name": "Cryptography",          "icon": "🔐", "color": "#ffcc00"},
    "recon":      {"name": "Recon & OSINT",         "icon": "🔍", "color": "#ff9900"},
    "webhack":    {"name": "Web Hacking",           "icon": "🕸️", "color": "#ff2266"},
    "passwords":  {"name": "Password Attacks",      "icon": "🔑", "color": "#cc44ff"},
    "exploit":    {"name": "System Exploitation",   "icon": "⚡", "color": "#ff4444"},
    "defense":    {"name": "Defensive Security",    "icon": "🛡️", "color": "#4488ff"},
    "governance": {"name": "Frameworks & CVEs",     "icon": "📋", "color": "#44ddaa"},
    "tools":      {"name": "Tools & Automation",    "icon": "🦞", "color": "#ff8844"},
    "python":     {"name": "Python Scripting",      "icon": "🐍", "color": "#3776ab"},
}


# ---------------------------------------------------------------------------
# RANKS
# XP thresholds unlock progressively cooler titles.
# ---------------------------------------------------------------------------

RANKS = [
    {"level":  1, "title": "Noob",              "xp":    0},
    {"level":  2, "title": "Script Kiddie",     "xp":  100},
    {"level":  3, "title": "Terminal Jockey",   "xp":  250},
    {"level":  4, "title": "Packet Sniffer",    "xp":  450},
    {"level":  5, "title": "Shell Popper",      "xp":  750},
    {"level":  6, "title": "Root Hunter",       "xp": 1100},
    {"level":  7, "title": "Exploit Dev",       "xp": 1600},
    {"level":  8, "title": "Zero-Day Scout",    "xp": 2200},
    {"level":  9, "title": "Shadow Operator",   "xp": 3000},
    {"level": 10, "title": "Ghost in the Wire", "xp": 4000},
    {"level": 11, "title": "Cipher Lord",       "xp": 5200},
    {"level": 12, "title": "White Hat Legend",  "xp": 6500},
]


# ---------------------------------------------------------------------------
# CAREER PROFILES
# Shown in the Careers tab so players can see real-world job paths.
# ---------------------------------------------------------------------------

CAREERS = [
    {
        "title":  "SOC Analyst (Tier 1-3)",
        "salary": "$55K - $120K",
        "desc":   "Monitor security alerts in a Security Operations Center. Analyze logs, triage incidents, and escalate threats. Entry-level cybersecurity role.",
        "skills": "SIEM (Splunk/ELK), log analysis, incident triage, networking basics, ticketing systems",
        "certs":  "CompTIA Security+, CySA+, Splunk Core Certified User, BTL1",
        "trees":  ["defense", "networking", "governance"],
    },
    {
        "title":  "Penetration Tester",
        "salary": "$80K - $160K",
        "desc":   "Ethically hack organizations to find vulnerabilities before real attackers do. Write reports with remediation advice.",
        "skills": "Nmap, Burp Suite, Metasploit, web app testing, network attacks, report writing",
        "certs":  "OSCP (gold standard), CEH, PNPT, eJPT",
        "trees":  ["recon", "webhack", "exploit", "passwords"],
    },
    {
        "title":  "Incident Responder",
        "salary": "$85K - $150K",
        "desc":   "Respond to active security breaches. Contain threats, investigate root cause, and restore systems.",
        "skills": "Digital forensics, malware analysis, log analysis, memory forensics, timeline analysis",
        "certs":  "GCIH, GCFA, CySA+, BTL2",
        "trees":  ["defense", "linux", "networking"],
    },
    {
        "title":  "Security Engineer",
        "salary": "$100K - $180K",
        "desc":   "Design, build, and maintain security infrastructure. Firewalls, IDS/IPS, SIEM, endpoint protection.",
        "skills": "Firewall config, IDS/IPS, cloud security, automation, scripting (Python/Bash)",
        "certs":  "CISSP, AWS Security Specialty, CCSP, CompTIA Security+",
        "trees":  ["defense", "networking", "python", "linux"],
    },
    {
        "title":  "Threat Hunter",
        "salary": "$95K - $165K",
        "desc":   "Proactively search for hidden threats that evade automated detection. Hypothesis-driven investigation.",
        "skills": "MITRE ATT&CK, behavioral analysis, SIEM queries, endpoint telemetry, threat intelligence",
        "certs":  "GCTI, GCIA, OSTH, CySA+",
        "trees":  ["defense", "networking", "recon"],
    },
    {
        "title":  "Red Team Operator",
        "salary": "$110K - $190K",
        "desc":   "Simulate advanced persistent threats (APTs). Full-scope adversary simulation including social engineering.",
        "skills": "Advanced exploitation, C2 frameworks, evasion, physical security, social engineering",
        "certs":  "OSCP, OSEP, CRTO, GXPN",
        "trees":  ["exploit", "recon", "webhack", "passwords"],
    },
    {
        "title":  "GRC Analyst",
        "salary": "$70K - $130K",
        "desc":   "Governance, Risk, and Compliance. Ensure organizations meet security standards and regulations.",
        "skills": "NIST CSF, ISO 27001, risk assessment, policy writing, audit management",
        "certs":  "CISSP, CISA, CRISC, CompTIA Security+",
        "trees":  ["governance"],
    },
    {
        "title":  "AppSec Engineer",
        "salary": "$100K - $175K",
        "desc":   "Secure software from design to deployment. Code review, SAST/DAST, threat modeling, DevSecOps.",
        "skills": "Secure coding, OWASP Top 10, CI/CD security, code review, threat modeling",
        "certs":  "CSSLP, GWEB, OSWE",
        "trees":  ["webhack", "python", "governance"],
    },
]


# ---------------------------------------------------------------------------
# ALL QUESTS
# Each quest dict has at minimum: id, tree, tier, xp, title, brief, mission.
# Optional keys: hint, benefit, bonus, bonus_xp, sandbox.
#
# Tiers control unlock order:
#   Tier 1 — always available
#   Tier 2 — unlocked after completing any Tier 1 quest in the same tree
#   Tier 3 — unlocked after completing any Tier 2 quest in the same tree
# ---------------------------------------------------------------------------

ALL_QUESTS = [

    # =========================================================
    # LINUX MASTERY
    # =========================================================

    {
        "id": "lx01", "tree": "linux", "tier": 1, "xp": 25,
        "title": "Terminal Awakening",
        "brief": "Navigate the Linux filesystem",
        "hint":  "Start with pwd to see where you are, then use ls -la and cd to explore. Pay special attention to /etc, /var/log, and /tmp.",
        "benefit": "Every cybersecurity job requires Linux command-line skills. SOC analysts read logs, pentesters navigate targets, sysadmins manage servers — all from the terminal.",
        "bonus": "Run: find /etc -name '*.conf' 2>/dev/null | head -20 — list 5 interesting config files in ~/linux_notes.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Terminal Awakening ═══

The terminal is your cockpit. Every hacker lives here.

► OBJECTIVES:

  1. KNOW WHERE YOU ARE:
     pwd                    # Print Working Directory
     whoami                 # Who are you logged in as?
     hostname               # What machine is this?

  2. MOVE AROUND:
     ls                     # List files
     ls -la                 # ALL files with details
     ls -lah                # Human-readable sizes
     cd /home               # Change directory
     cd ~                   # Your home directory
     cd ..                  # Go up one level
     cd -                   # Go back to previous

  3. LINUX DIRECTORY STRUCTURE:
     /           → Root of everything
     /home       → User home directories
     /root       → Root user's home (superuser)
     /etc        → System config files (gold mine!)
     /var        → Variable data (logs: /var/log)
     /tmp        → Temp files (anyone can write here!)
     /bin        → Essential commands
     /sbin       → System admin commands
     /usr        → User programs and data
     /opt        → Third-party software
     /dev        → Device files
     /proc       → Process info (virtual filesystem)

  4. EXPLORE:
     ls /etc/              # Config files
     ls /var/log/          # System logs
     cat /etc/hostname     # Machine name
     cat /etc/os-release   # OS version""",
    },

    {
        "id": "lx02", "tree": "linux", "tier": 1, "xp": 25,
        "title": "File Commander",
        "brief": "Create, copy, move, search files",
        "hint":  "grep is your best friend for searching inside files. find searches for filenames. Combine them with pipes (|) for power.",
        "benefit": "File manipulation and searching is used constantly in incident response (searching logs), forensics (finding evidence), and pentesting (finding credentials in configs).",
        "bonus": "Create a directory structure lab/scans lab/reports lab/wordlists with README.txt in each. List with ls -laR lab/",
        "bonus_xp": 10,
        "mission": """═══ MISSION — File Commander ═══

► OBJECTIVES:

  1. CREATE:
     touch notes.txt          # Create empty file
     mkdir -p lab/targets/web  # Nested directories
     echo "target: 10.0.0.1" > target.txt    # Write
     echo "port: 80" >> target.txt            # Append

  2. COPY, MOVE, RENAME:
     cp target.txt backup.txt
     cp -r lab/ lab_backup/
     mv backup.txt old.txt       # Rename
     mv old.txt /tmp/            # Move

  3. DELETE:
     rm target.txt               # Delete file
     rm -r lab_backup/           # Delete directory
     # ⚠️ NEVER: rm -rf /

  4. VIEW:
     cat target.txt              # Print file
     head -5 /var/log/syslog     # First 5 lines
     tail -20 /var/log/auth.log  # Last 20 lines
     tail -f /var/log/syslog     # Follow real-time
     less /etc/passwd            # Scrollable (q=quit)

  5. SEARCH FOR FILES:
     find / -name "*.log" 2>/dev/null
     find / -perm -4000 2>/dev/null    # SUID files!

  6. SEARCH INSIDE FILES:
     grep "Failed" /var/log/auth.log
     grep -r "password" /etc/ 2>/dev/null
     grep -c "Failed" /var/log/auth.log  # Count""",
    },

    {
        "id": "lx03", "tree": "linux", "tier": 1, "xp": 30,
        "title": "Permission Enforcer",
        "brief": "Understand permissions, SUID, ownership",
        "hint":  "Remember: 4=read, 2=write, 1=execute. Add them up for each position (owner/group/others). SUID (4000) is a huge privesc vector — always check GTFOBins.",
        "benefit": "Permission misconfigurations are one of the top privilege escalation vectors. Every pentest report and security audit checks for these.",
        "bonus": "Find all SUID binaries, look up 3 on GTFOBins, document which are exploitable in ~/suid_audit.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Permission Enforcer ═══

► OBJECTIVES:

  1. READ PERMISSIONS (ls -la output):
     -rwxr-xr-- 1 captain users 4096 Jan 1 script.sh
     │├─┤├─┤├─┤
     │ │   │   └── Others: read only
     │ │   └────── Group: read + execute
     │ └────────── Owner: read + write + execute
     └──────────── File type (- = file, d = dir)

  2. CHANGE PERMISSIONS:
     chmod 755 script.sh    # rwxr-xr-x
     chmod 644 notes.txt    # rw-r--r--
     chmod 600 secret.txt   # rw------- (owner only!)
     chmod +x script.sh     # Add execute
     # Numbers: 4=r, 2=w, 1=x → add up

  3. OWNERSHIP:
     sudo chown root:root secret.txt
     sudo chown captain:users script.sh

  4. SUID — Set User ID:
     find / -perm -4000 -type f 2>/dev/null
     # SUID runs as FILE OWNER (often root!)
     # Vulnerable SUID = instant root

  5. DANGEROUS PERMISSIONS:
     find / -perm -o+w -type f 2>/dev/null | head -20
     # World-writable = anyone can modify""",
    },

    {
        "id": "lx04", "tree": "linux", "tier": 2, "xp": 40,
        "title": "Process Assassin",
        "brief": "Monitor processes, services, cron jobs",
        "hint":  "Always check cron jobs (crontab -l, /etc/crontab, /etc/cron.d/) — if root runs a script you can write to, that's game over.",
        "benefit": "Understanding processes and services is critical for both incident response (what's running that shouldn't be?) and exploitation (what services are vulnerable?).",
        "bonus": "Audit all cron jobs on the system. Check permissions on every referenced script. Document in ~/cron_audit.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Process Assassin ═══

► OBJECTIVES:

  1. VIEW PROCESSES:
     ps aux                       # All processes
     ps aux | grep ssh            # Find specific
     top                          # Live monitor
     htop                         # Better (sudo apt install htop)

  2. KILL:
     kill 1234                    # Graceful stop
     kill -9 1234                 # Force kill
     killall firefox              # By name

  3. BACKGROUND:
     python scan.py &             # Run in background
     jobs                         # List bg jobs
     fg %1                        # Bring to foreground
     nohup python scan.py &       # Survives logout

  4. SERVICES (systemd):
     sudo systemctl status ssh
     sudo systemctl start/stop/enable/disable ssh
     sudo systemctl list-units --type=service

  5. CRON JOBS:
     crontab -l                   # Your cron jobs
     sudo crontab -l              # Root's cron jobs
     cat /etc/crontab             # System cron
     ls /etc/cron.d/              # More cron configs
     # Format: min hour day month weekday command""",
    },

    {
        "id": "lx05", "tree": "linux", "tier": 2, "xp": 40,
        "title": "User Overlord",
        "brief": "Manage users, groups, sudo, /etc/shadow",
        "hint":  "Always check sudo -l first for easy privesc. Look for NOPASSWD entries. Check /etc/passwd for unexpected UID 0 accounts.",
        "benefit": "User management knowledge is essential for system administration, incident response (finding rogue accounts), and privilege escalation during pentests.",
        "bonus": "Audit: UID 0 accounts, accounts with shells, empty passwords, sudo rules. Write ~/user_audit.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — User Overlord ═══

► OBJECTIVES:

  1. VIEW USERS:
     cat /etc/passwd        # All accounts
     sudo cat /etc/shadow   # Password hashes (root only)
     id                     # Your info
     who / w                # Who's logged in
     last / lastb           # Login history / failures

  2. /etc/passwd FORMAT:
     captain:x:1000:1000:Captain:/home/captain:/bin/bash
     # user:pass:UID:GID:comment:home:shell
     # UID 0 = root (check for unexpected UID 0!)

  3. /etc/shadow HASH TYPES:
     $1$ = MD5 (weak)    $5$ = SHA-256
     $6$ = SHA-512       $y$ = yescrypt (strongest)

  4. MANAGE USERS:
     sudo adduser testuser
     sudo usermod -aG sudo testuser   # Add to sudo
     sudo userdel -r testuser         # Delete + home

  5. SUDO:
     sudo -l                          # What can you sudo?
     sudo visudo                      # Edit sudoers safely

  6. CHECK FOR SUSPICIOUS:
     awk -F: '$3 == 0 {print}' /etc/passwd  # UID 0 accounts
     grep -v 'nologin' /etc/passwd          # Can login""",
    },

    {
        "id": "lx06", "tree": "linux", "tier": 3, "xp": 60,
        "title": "Shell Scripter",
        "brief": "Automate with bash scripts",
        "hint":  "Start every script with #!/bin/bash. Use variables with $, conditionals with [ ], and always chmod +x before running.",
        "benefit": "Automation is key in security — from automated scans to incident response playbooks. Every security role uses scripting daily.",
        "bonus": "Create a full system audit script: SUID, world-writable, UID 0, empty passwords, open ports, cron jobs. Save output with date stamp.",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Shell Scripter ═══

► OBJECTIVES:

  1. FIRST SCRIPT — save as ~/scan.sh:
     #!/bin/bash
     echo "=== Quick Scanner ==="
     TARGET=$1
     if [ -z "$TARGET" ]; then
         echo "Usage: ./scan.sh <ip>"
         exit 1
     fi
     for port in 21 22 80 443 8080; do
         (echo >/dev/tcp/$TARGET/$port) 2>/dev/null && \\
             echo "  Port $port: OPEN" || \\
             echo "  Port $port: closed"
     done

  2. RUN IT:
     chmod +x ~/scan.sh
     ./scan.sh 127.0.0.1

  3. LOOPS:
     for ip in 192.168.1.{1..10}; do
         ping -c 1 -W 1 $ip &>/dev/null && echo "$ip UP"
     done

  4. READING FILES:
     while IFS= read -r line; do
         echo "Processing: $line"
     done < targets.txt

  5. FUNCTIONS:
     check_port() {
         (echo >/dev/tcp/$1/$2) 2>/dev/null
         return $?
     }
     if check_port 127.0.0.1 22; then
         echo "SSH running"
     fi""",
    },


    # =========================================================
    # NETWORKING
    # =========================================================

    {
        "id": "net01", "tree": "networking", "tier": 1, "xp": 25,
        "title": "Network Foundations",
        "brief": "IPs, subnets, OSI model, ports",
        "hint":  "Memorize the OSI model with 'All People Seem To Need Data Processing' and the top 20 port numbers. These come up in every interview.",
        "benefit": "Networking is the backbone of ALL cybersecurity. You cannot defend or attack what you don't understand. Every cert exam tests networking heavily.",
        "bonus": "Write the OSI model with real examples at each layer. Memorize the top 20 ports. Document in ~/network_notes.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Network Foundations ═══

► THE OSI MODEL:
  7 Application   → HTTP, FTP, SSH, DNS
  6 Presentation  → SSL/TLS, encryption
  5 Session       → Connection management
  4 Transport     → TCP (reliable), UDP (fast)
  3 Network       → IP addresses, routing
  2 Data Link     → MAC addresses, switches
  1 Physical      → Cables, wireless
  Memory: "All People Seem To Need Data Processing"

► IP ADDRESSES:
  ip a                    # Your IPs
  Private ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
  /24 = 256 addresses, /16 = 65,536

► TCP vs UDP:
  TCP: SYN→SYN-ACK→ACK (reliable, ordered)
  UDP: fire-and-forget (fast, no guarantee)

► KEY PORTS (memorize!):
  21 FTP    22 SSH    23 Telnet   25 SMTP
  53 DNS    80 HTTP   110 POP3    143 IMAP
  443 HTTPS  445 SMB   3306 MySQL  3389 RDP

► COMMANDS:
  ip a / ip route / ping / traceroute
  nslookup / dig / ss -tulnp""",
    },

    {
        "id": "net02", "tree": "networking", "tier": 1, "xp": 30,
        "title": "Packet Hunter",
        "brief": "Capture and analyze network traffic",
        "hint":  "Use tcpdump -A to see ASCII content — you can literally read unencrypted HTTP traffic. Wireshark's display filters are your best friend.",
        "benefit": "Packet analysis is used in forensics, incident response, IDS tuning, and network troubleshooting. PCAP files are evidence in investigations.",
        "bonus": "Capture 100 packets, open in Wireshark, find: DNS query, TCP handshake, any unencrypted data. Document in ~/packet_analysis.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Packet Hunter ═══

► TCPDUMP:
  sudo tcpdump -i eth0 -c 20              # 20 packets
  sudo tcpdump -i eth0 port 80            # HTTP only
  sudo tcpdump -i eth0 -w capture.pcap    # Save
  sudo tcpdump -i eth0 -A port 80         # ASCII content

► READ OUTPUT:
  12:34:56 IP 192.168.1.100.45678 > 93.184.216.34.80: Flags [S]
  # Flags: [S]=SYN [S.]=SYN-ACK [.]=ACK [P.]=PUSH [F.]=FIN

► WIRESHARK:
  wireshark &
  # Filters: tcp.port==80, ip.addr==192.168.1.1, http.request, dns

► ARP:
  arp -a                    # IP↔MAC mappings
  ip neigh                  # ARP table

► PROTOCOLS:
  DHCP (67/68): Auto-assigns IPs to devices
  ICMP: Ping and traceroute (no port number)
  SNMP (161): Network device management
  LDAP (389): Directory services (Active Directory)
  SMB (445): Windows file sharing
  RDP (3389): Remote desktop""",
    },

    {
        "id": "net03", "tree": "networking", "tier": 2, "xp": 45,
        "title": "Nmap Ninja",
        "brief": "Master the network scanner",
        "hint":  "Start with nmap -sn for discovery, then -sV -sC for detailed scanning. Use -oA to save in all formats. -T timing controls stealth.",
        "benefit": "Nmap is THE most used tool in pentesting. It's the first tool you run in any engagement and appears in every pentest methodology.",
        "bonus": "Full scan of localhost: nmap -sV -sC -O -oA ~/my_scan localhost — identify every service in all 3 output files.",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Nmap Ninja ═══

⚠️ Only scan machines YOU own.

► DISCOVERY:
  nmap -sn 192.168.1.0/24       # Ping sweep

► PORT SCANNING:
  nmap TARGET                    # Top 1000 ports
  nmap -p- TARGET                # ALL 65535 ports
  nmap -p 22,80,443 TARGET       # Specific ports

► SCAN TYPES:
  -sS  SYN stealth (default)     -sT  TCP connect
  -sU  UDP scan                  -sV  Version detection
  -O   OS detection              -A   Aggressive (all)

► NSE SCRIPTS:
  nmap --script=default TARGET
  nmap --script=vuln TARGET
  nmap --script=http-enum TARGET
  ls /usr/share/nmap/scripts/    # Browse scripts

► OUTPUT:
  -oN file.txt    Normal
  -oX file.xml    XML
  -oA prefix       All formats

► STEALTH:
  -T0 Paranoid  -T1 Sneaky  -T3 Normal  -T5 Insane
  -f Fragment packets  -D RND:5 Decoys""",
    },

    {
        "id": "net04", "tree": "networking", "tier": 3, "xp": 55,
        "title": "DNS Deep Dive",
        "brief": "DNS recon and enumeration",
        "hint":  "Always check for zone transfers (dig axfr) — misconfigured DNS servers will give you the entire zone. Check TXT records for SPF/DKIM/DMARC.",
        "benefit": "DNS reconnaissance reveals network structure, mail servers, and subdomains — all without touching the target directly. Essential OSINT skill.",
        "bonus": "Full DNS recon on a domain you own: A, MX, NS, TXT records, zone transfer attempt, SPF/DMARC check. Document in ~/dns_recon.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — DNS Deep Dive ═══

► DNS LOOKUPS:
  dig example.com ANY
  dig example.com MX / NS / TXT
  dig -x 93.184.216.34           # Reverse lookup
  nslookup / host example.com

► RECORD TYPES:
  A=IPv4  AAAA=IPv6  MX=Mail  NS=Nameserver
  TXT=Text  CNAME=Alias  PTR=Reverse  SOA=Zone info

► ENUMERATION:
  dnsrecon -d example.com -t std
  dnsenum example.com
  fierce --domain example.com
  dig axfr @ns1.example.com example.com  # Zone transfer

► EMAIL SECURITY:
  dig example.com TXT | grep spf
  dig _dmarc.example.com TXT""",
    },


    # =========================================================
    # CRYPTOGRAPHY
    # =========================================================

    {
        "id": "cr01", "tree": "crypto", "tier": 1, "xp": 25,
        "title": "CIA & Crypto Basics",
        "brief": "CIA Triad, hashing, encryption fundamentals",
        "hint":  "Remember: Encoding is NOT encryption (Base64 is trivially decoded). Hashing is one-way (can't reverse). Encryption is two-way (needs a key).",
        "benefit": "The CIA Triad is asked about in EVERY security interview. Understanding crypto lets you evaluate whether a system is truly secure or just looks secure.",
        "bonus": "Hash a file with SHA256, modify one byte, hash again — compare. Encrypt/decrypt with openssl. Document in ~/crypto_lab.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — CIA & Crypto Basics ═══

► THE CIA TRIAD:
  C — CONFIDENTIALITY: Only authorized access
    → Encryption, access controls, MFA
  I — INTEGRITY: Data hasn't been tampered with
    → Hashing, digital signatures, checksums
  A — AVAILABILITY: Systems accessible when needed
    → Redundancy, backups, DDoS protection

► HASHING (one-way):
  echo -n "password123" | md5sum
  echo -n "password123" | sha256sum
  sha256sum /usr/bin/ls    # File integrity

► ENCODING vs ENCRYPTION vs HASHING:
  Encoding: echo -n "hello" | base64 → NOT secure
  Hashing: one-way, can't reverse
  Encryption: two-way with a key

► SYMMETRIC: same key both ways (AES, ChaCha20)
  ASYMMETRIC: public + private key pair (RSA, ECC)

► TRY IT:
  openssl genrsa -out private.pem 2048
  openssl rsa -in private.pem -pubout -out public.pem
  echo "SECRET" > msg.txt
  openssl rsautl -encrypt -pubin -inkey public.pem -in msg.txt -out msg.enc
  openssl rsautl -decrypt -inkey private.pem -in msg.enc""",
    },

    {
        "id": "cr02", "tree": "crypto", "tier": 2, "xp": 40,
        "title": "Hash Cracking Lab",
        "brief": "Attack and defend password hashes",
        "hint":  "Start with John + rockyou.txt for quick wins. Use --rules for mutations. hashcat is faster on GPUs. Always use strong, salted hashes for defense.",
        "benefit": "Understanding hash cracking lets you set effective password policies and assess the real strength of your organization's credentials.",
        "bonus": "Create 5 test accounts with different password strengths. Crack with John. Document which fell and how long each took.",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Hash Cracking Lab ═══

⚠️ Only crack YOUR OWN hashes.

► HASH TYPES:
  $1$=MD5crypt $5$=SHA-256 $6$=SHA-512 $y$=yescrypt $2b$=bcrypt

► WORDLISTS:
  ls /usr/share/wordlists/
  sudo gunzip /usr/share/wordlists/rockyou.txt.gz
  wc -l /usr/share/wordlists/rockyou.txt  # ~14M passwords!

► JOHN THE RIPPER:
  sudo unshadow /etc/passwd /etc/shadow > hashes.txt
  john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
  john --show hashes.txt

► HASHCAT:
  hashcat -m 1800 -a 0 hash.txt rockyou.txt
  # -m 0=MD5 -m 1000=NTLM -m 1800=SHA-512crypt
  # -a 0=dictionary -a 3=brute force

► DEFEND:
  Use bcrypt/argon2, 16+ char passwords, per-user salts,
  account lockout, MFA""",
    },


    # =========================================================
    # RECON & OSINT
    # =========================================================

    {
        "id": "rc01", "tree": "recon", "tier": 1, "xp": 25,
        "title": "Self Scanner",
        "brief": "See yourself through an attacker's eyes",
        "hint":  "Run ss -tulnp to see every listening service. For each one, ask: do I need this? Is it updated? Is it exposed to the network?",
        "benefit": "Self-assessment is the first step in hardening. You can't defend what you don't know exists. This is also the first thing pentesters do on a compromised host.",
        "bonus": "List every open port, identify each service, rate risk (low/medium/high). Save to ~/self_assessment.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Self Scanner ═══

► OBJECTIVES:
  ip a                     # Your IPs
  ss -tulnp                # Open ports + processes
  nmap -sV localhost        # Service versions
  nmap -sV -sC localhost    # With default scripts
  curl ifconfig.me          # Your public IP

► FOR EACH PORT ASK:
  - Do I need this service?
  - Is it up to date?
  - Is it configured securely?
  - Is it exposed to the internet?

► DOCUMENT:
  echo "=== Self-Scan ==" > ~/self_scan.txt
  date >> ~/self_scan.txt
  ss -tulnp >> ~/self_scan.txt""",
    },

    {
        "id": "rc02", "tree": "recon", "tier": 2, "xp": 45,
        "title": "OSINT Operator",
        "brief": "Gather intel from public sources",
        "hint":  "Start with whois and dig for passive recon. theHarvester automates email/subdomain discovery. Google dorking is surprisingly powerful.",
        "benefit": "OSINT is legal, passive, and devastatingly effective. Professional pentest teams spend days on OSINT before touching a keyboard.",
        "bonus": "Full OSINT assessment on a domain you own: DNS, WHOIS, emails, subdomains, technology. Create ~/osint_report.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — OSINT Operator ═══

⚠️ Use a domain YOU own or have permission for.

► DNS: whois, dig ANY, dnsrecon
► EMAILS: theHarvester -d example.com -l 100 -b all
► SUBDOMAINS: fierce --domain example.com
► WEB TECH: whatweb, curl -I

► GOOGLE DORKING:
  site:example.com
  filetype:pdf site:example.com
  intitle:"index of" site:example.com
  inurl:admin site:example.com

► TOOLS ON PARROT:
  recon-ng, maltego, spiderfoot""",
    },


    # =========================================================
    # WEB HACKING
    # =========================================================

    {
        "id": "web01", "tree": "webhack", "tier": 1, "xp": 25,
        "title": "Web Recon",
        "brief": "Enumerate web servers and hidden content",
        "hint":  "Always check robots.txt first — it tells search engines what to hide, which means it shows YOU what's interesting. Try gobuster with common.txt.",
        "benefit": "Web application security is the largest attack surface for most organizations. Web recon is the first phase of any web app pentest.",
        "bonus": "Set up DVWA in your lab. Run full web recon against it. Document in ~/web_recon.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Web Recon ═══

⚠️ Only scan YOUR targets (set up DVWA/Juice Shop).

► HTTP BASICS:
  curl http://target / curl -I / curl -v

► DIRECTORY ENUMERATION:
  gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt
  dirb http://target

► CHECK:
  curl http://target/robots.txt    # Hidden paths!
  curl http://target/sitemap.xml
  # Look for: /.git/ /admin/ /backup/ /wp-admin/

► FINGERPRINTING:
  whatweb http://target
  curl -I http://target | grep -i server

► SSL/TLS:
  echo | openssl s_client -connect target:443 2>/dev/null | openssl x509 -text""",
    },

    {
        "id": "web02", "tree": "webhack", "tier": 2, "xp": 50,
        "title": "Injection Master",
        "brief": "SQL injection, XSS, OWASP Top 10",
        "hint":  "For SQLi, try adding a single quote (') to inputs and see if you get a database error. For XSS, try <script>alert(1)</script> in input fields.",
        "benefit": "Injection flaws are consistently the most dangerous web vulnerabilities. Understanding them is required for any web security role.",
        "bonus": "In DVWA (low security): perform SQLi to extract users, reflected XSS, stored XSS. Document attacks AND fixes in ~/injection_lab.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Injection Master ═══

⚠️ ONLY on YOUR lab targets (DVWA, Juice Shop).

► SQL INJECTION:
  Normal: SELECT * FROM users WHERE id = '1'
  Injected: SELECT * FROM users WHERE id = '1' OR '1'='1'
  Login bypass: admin' -- (comments out password check)

► SQLMAP:
  sqlmap -u "http://target/page?id=1" --batch
  sqlmap -u "URL" --dbs / --tables / --dump

► XSS:
  <script>alert('XSS')</script>
  <img src=x onerror=alert('XSS')>

► OWASP TOP 10:
  A01: Broken Access Control
  A02: Cryptographic Failures
  A03: Injection
  A04: Insecure Design
  A05: Security Misconfiguration
  A06: Vulnerable Components
  A07: Auth Failures
  A08: Data Integrity Failures
  A09: Logging Failures
  A10: SSRF

► DEFENSE: parameterized queries, input validation,
  output encoding, CSP headers""",
    },

    {
        "id": "web03", "tree": "webhack", "tier": 3, "xp": 60,
        "title": "Burp Suite Operator",
        "brief": "Intercept and modify web traffic",
        "hint":  "Send interesting requests to Repeater first to test manually. Use Intruder for automated attacks. Always check cookies and hidden form fields.",
        "benefit": "Burp Suite is the industry standard for web app testing. Every professional pentester uses it daily. It's required knowledge for OSCP and most web security certs.",
        "bonus": "In Burp against DVWA: intercept login, modify in Repeater, brute force with Intruder. Document in ~/burp_lab.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Burp Suite Operator ═══

► SETUP:
  burpsuite &
  Browser proxy: 127.0.0.1:8080

► PROXY: Intercept requests, inspect/modify, forward/drop
► REPEATER: Right-click → Send to Repeater, modify & resend
► INTRUDER: Automated attacks with wordlists
  Attack types: Sniper, Battering Ram, Pitchfork, Cluster Bomb
► DECODER: URL encode, Base64, HTML entities""",
    },


    # =========================================================
    # PASSWORD ATTACKS
    # =========================================================

    {
        "id": "pw01", "tree": "passwords", "tier": 1, "xp": 25,
        "title": "Password Theory",
        "brief": "How passwords are stored and attacked",
        "hint":  "Explore /usr/share/wordlists/ on Parrot. rockyou.txt has 14M real passwords. CeWL creates custom wordlists from websites.",
        "benefit": "Weak passwords are the #1 way attackers get in. Understanding attack methods lets you build policies that actually work.",
        "bonus": "Generate 3 custom wordlists: CeWL from a website, crunch for 6-digit PINs, manual list of 20 common passwords. Save to ~/wordlists/",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Password Theory ═══

► HOW LINUX STORES PASSWORDS:
  /etc/passwd  → user info (readable)
  /etc/shadow  → hashes (root only)
  Format: user:$type$salt$hash:...

► ATTACK TYPES:
  Dictionary: try wordlist      Brute force: all combos
  Rule-based: mutations         Rainbow tables: precomputed
  Credential stuffing: reuse leaked creds

► WORDLISTS ON PARROT:
  ls /usr/share/wordlists/
  rockyou.txt → 14M real passwords
  /usr/share/wordlists/dirb/ → directory busting

► CUSTOM WORDLISTS:
  cewl http://target -w custom.txt    # From website
  crunch 6 8 0123456789 -o pins.txt   # Generate patterns

► DEFENSE:
  16+ chars, passphrase, password manager, MFA, lockout""",
    },

    {
        "id": "pw02", "tree": "passwords", "tier": 2, "xp": 45,
        "title": "Crack & Defend",
        "brief": "Crack with Hydra/John, defend with fail2ban",
        "hint":  "Always set up fail2ban BEFORE running attack tools. Test the full cycle: attack → detect → block → verify the block worked.",
        "benefit": "Understanding both sides (attack AND defense) makes you vastly more effective. This dual perspective is what separates good security pros from great ones.",
        "bonus": "Set up fail2ban, run Hydra against your own SSH, verify the ban in logs. Document attack AND defense in ~/password_defense.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — Crack & Defend ═══

⚠️ Only attack YOUR OWN systems.

► OFFLINE — JOHN:
  sudo unshadow /etc/passwd /etc/shadow > hashes.txt
  john --wordlist=rockyou.txt hashes.txt
  john --show hashes.txt

► ONLINE — HYDRA:
  hydra -l user -P rockyou.txt ssh://127.0.0.1 -t 4
  hydra -l admin -P wordlist.txt http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

► DEFEND — FAIL2BAN:
  sudo apt install fail2ban
  sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
  # Set: bantime=3600, maxretry=3
  sudo systemctl enable --now fail2ban
  sudo fail2ban-client status sshd""",
    },


    # =========================================================
    # SYSTEM EXPLOITATION
    # =========================================================

    {
        "id": "ex01", "tree": "exploit", "tier": 2, "xp": 45,
        "title": "Metasploit Academy",
        "brief": "Learn the exploitation framework",
        "hint":  "Start with auxiliary modules (scanners) before exploit modules. Always 'show options' to see what needs configuring. 'search' is your friend.",
        "benefit": "Metasploit is the industry standard. Understanding it helps both offensive (pentesting) and defensive (writing detection rules for known exploits) roles.",
        "bonus": "Set up Metasploitable 2 in Hyper-V. Scan with nmap, exploit one vulnerability with Metasploit. Document full chain in ~/msf_lab.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Metasploit Academy ═══

⚠️ ONLY use against machines YOU own.

► START:
  sudo msfdb init && msfconsole

► NAVIGATE:
  search type:exploit platform:linux
  use exploit/unix/ftp/vsftpd_234_backdoor
  show options → set RHOSTS → run

► KEY CONCEPTS:
  Exploit = attack code    Payload = post-exploit code
  Meterpreter = advanced shell    Auxiliary = scanning

► METERPRETER:
  sysinfo, getuid, pwd, ls, download, upload
  shell (drop to system), hashdump, bg

► AUXILIARIES:
  auxiliary/scanner/portscan/tcp
  auxiliary/scanner/smb/smb_version
  auxiliary/scanner/ssh/ssh_login""",
    },

    {
        "id": "ex02", "tree": "exploit", "tier": 3, "xp": 60,
        "title": "Privilege Escalation",
        "brief": "Go from user to root",
        "hint":  "Run sudo -l FIRST — it's the quickest win. Then check SUID, writable cron scripts, and kernel version. LinPEAS automates the enumeration.",
        "benefit": "Privesc is a core pentest skill. Even in defensive roles, understanding how attackers escalate helps you harden systems and detect escalation attempts.",
        "bonus": "Run linpeas.sh on your Parrot box. Fix at least 2 issues. Document before/after in ~/privesc_audit.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Privilege Escalation ═══

⚠️ Practice on YOUR machines only.

► CHECKLIST:
  whoami && id
  sudo -l                              # Easy wins!
  uname -a                             # Kernel exploits
  find / -perm -4000 2>/dev/null       # SUID
  cat /etc/crontab && ls /etc/cron.d/  # Cron jobs
  find /etc -writable 2>/dev/null      # Writable configs

► AUTOMATED:
  # LinPEAS:
  curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
  chmod +x linpeas.sh && ./linpeas.sh

► COMMON VECTORS:
  a) sudo vim -c '!bash'  (if sudo allows vim)
  b) SUID find: find . -exec /bin/bash -p \\;
  c) Writable cron scripts
  d) Writable /etc/passwd
  → Check EVERY binary on GTFOBins.github.io""",
    },


    # =========================================================
    # DEFENSIVE SECURITY
    # =========================================================

    {
        "id": "def01", "tree": "defense", "tier": 1, "xp": 30,
        "title": "Firewall Fortress",
        "brief": "Configure UFW and iptables",
        "hint":  "Start with deny all incoming, allow all outgoing. Then selectively open only what you need. Always verify with nmap from another machine.",
        "benefit": "Firewall configuration is a fundamental skill for any security role. It's the first line of defense and a core part of system hardening.",
        "bonus": "Configure UFW: allow SSH from subnet only, HTTP/HTTPS from anywhere, deny all else. Verify with nmap. Document in ~/firewall_config.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Firewall Fortress ═══

► UFW:
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw enable
  sudo ufw allow 22/tcp
  sudo ufw allow 80,443/tcp
  sudo ufw deny 23/tcp
  sudo ufw status numbered

► IPTABLES (advanced):
  sudo iptables -L -v -n
  sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
  sudo iptables -A INPUT -j DROP

► VERIFY:
  nmap YOUR_IP (from another machine)
  sudo tail -f /var/log/ufw.log""",
    },

    {
        "id": "def02", "tree": "defense", "tier": 2, "xp": 50,
        "title": "IDS Guardian",
        "brief": "Deploy Suricata intrusion detection",
        "hint":  "Set HOME_NET to your lab subnet in suricata.yaml. Use suricata-update to get the latest rules. Watch fast.log for real-time alerts.",
        "benefit": "IDS/IPS deployment and tuning is a core security engineering skill. SOC analysts work with IDS alerts daily. Understanding rules helps write better detections.",
        "bonus": "Write 3 custom Suricata rules (port scan, SSH brute force, suspicious HTTP). Test each. Document in ~/ids_rules.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — IDS Guardian ═══

► INSTALL & CONFIGURE:
  sudo apt install suricata
  sudo nano /etc/suricata/suricata.yaml
  # Set HOME_NET, interface
  sudo suricata-update

► RUN:
  sudo suricata -c /etc/suricata/suricata.yaml -i eth0
  sudo tail -f /var/log/suricata/fast.log

► TRIGGER ALERTS (from another machine):
  nmap -sV YOUR_IP
  curl "http://YOUR_IP/../../etc/passwd"

► CUSTOM RULES:
  # /var/lib/suricata/rules/local.rules
  alert tcp any any -> $HOME_NET 22 (msg:"SSH brute";
    threshold:type both,track by_src,count 5,seconds 60;
    sid:1000001; rev:1;)""",
    },

    {
        "id": "def03", "tree": "defense", "tier": 3, "xp": 60,
        "title": "Hardening Master",
        "brief": "Full system hardening — kernel, SSH, services",
        "hint":  "Apply sysctl hardening, lock down SSH (disable root login, use keys, change port), minimize services, set up AIDE for file integrity.",
        "benefit": "System hardening is required for compliance (CIS Benchmarks, NIST). Security engineers spend significant time on hardening and auditing systems.",
        "bonus": "Apply ALL hardening steps. Run linpeas.sh again and compare to first run. Document improvements in ~/hardening_report.txt",
        "bonus_xp": 20,
        "mission": """═══ MISSION — Hardening Master ═══

► KERNEL (sysctl):
  net.ipv4.ip_forward = 0
  net.ipv4.tcp_syncookies = 1
  net.ipv4.conf.all.rp_filter = 1
  kernel.randomize_va_space = 2
  kernel.dmesg_restrict = 1
  → sudo sysctl -p

► SSH:
  PermitRootLogin no
  PasswordAuthentication no
  MaxAuthTries 3
  Port 2222

► SERVICES:
  sudo systemctl list-units --type=service --state=running
  Disable what you don't need

► FILE INTEGRITY:
  sudo apt install aide && sudo aideinit
  sudo aide --check

► AUDIT LOGGING:
  sudo apt install auditd
  sudo auditctl -w /etc/shadow -p wa -k shadow_changes""",
    },


    # =========================================================
    # FRAMEWORKS & CVEs
    # =========================================================

    {
        "id": "gov01", "tree": "governance", "tier": 1, "xp": 25,
        "title": "NIST & CVE Basics",
        "brief": "Security frameworks every pro must know",
        "hint":  "Memorize the 5 NIST CSF functions: Identify, Protect, Detect, Respond, Recover. Know how to read a CVE entry and CVSS score.",
        "benefit": "Every security job references these frameworks. SOC analysts map to MITRE ATT&CK, auditors use NIST CSF, pentesters cite OWASP Top 10.",
        "bonus": "Map your lab to NIST CSF: for each function, list what you've done and what gaps remain. Save to ~/nist_assessment.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — NIST & CVE Basics ═══

► NIST CSF (5 functions):
  IDENTIFY  — What do we protect?
  PROTECT   — How do we prevent attacks?
  DETECT    — How do we catch attacks?
  RESPOND   — What do we do when attacked?
  RECOVER   — How do we get back to normal?

► CVE (Common Vulnerabilities and Exposures):
  Format: CVE-YYYY-NNNNN
  Example: CVE-2021-44228 (Log4Shell)
  Search: https://nvd.nist.gov

► CVSS SCORES:
  0.0 None  0.1-3.9 Low  4.0-6.9 Medium
  7.0-8.9 High  9.0-10.0 Critical

► OTHER FRAMEWORKS:
  MITRE ATT&CK — Attacker technique catalog
  OWASP Top 10 — Web vulnerabilities
  CIS Benchmarks — Hardening guides
  ISO 27001 — Security management standard""",
    },

    {
        "id": "gov02", "tree": "governance", "tier": 2, "xp": 40,
        "title": "CVE Hunter",
        "brief": "Find, read, and assess vulnerabilities",
        "hint":  "Use searchsploit to find exploits for specific software versions. Prioritize CVEs by: CVSS score, exploit availability, exposure, asset value.",
        "benefit": "Vulnerability management is a core security function. Understanding how to find, assess, and prioritize CVEs is essential for any security role.",
        "bonus": "Scan with nmap --script vuln. Look up each CVE, check CVSS, determine if affected. Write ~/vuln_report.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — CVE Hunter ═══

► FIND CVEs:
  dpkg -l | head -30              # What's installed?
  apt show openssh-server          # Check versions
  searchsploit openssh             # Find exploits
  searchsploit apache 2.4
  nmap --script vuln TARGET
  nikto -h http://TARGET

► READ A CVE:
  CVE ID, Description, CVSS, Affected versions,
  References (patches, exploits), CWE category

► PRIORITIZE:
  1. CVSS severity  2. Public exploit exists?
  3. Internet-facing?  4. Asset criticality

► PATCH:
  sudo apt update && apt list --upgradable
  sudo apt upgrade""",
    },


    # =========================================================
    # TOOLS & AUTOMATION
    # =========================================================

    {
        "id": "tl01", "tree": "tools", "tier": 1, "xp": 35,
        "title": "Twingate VPN Setup",
        "brief": "Zero-trust VPN for your lab",
        "hint":  "Install with the one-liner curl script. Configure with 'sudo twingate setup'. Start WITHOUT sudo for desktop auth notifications.",
        "benefit": "Zero-trust networking is replacing traditional VPNs across the industry. Understanding it makes you valuable for both network security and DevOps roles.",
        "bonus": "Run twingate report and compare open ports before/after with ss -tulnp. Document differences in ~/vpn_audit.txt",
        "bonus_xp": 10,
        "mission": """═══ MISSION — Twingate VPN Setup ═══

► CONCEPTS:
  Traditional VPN: encrypted tunnel, broad access once connected
  Zero Trust (Twingate): every request verified, per-resource access

► INSTALL:
  1. Sign up: https://www.twingate.com
  2. Install: curl -s https://binaries.twingate.com/client/linux/install.sh | sudo bash
  3. Configure: sudo twingate setup
  4. Start: twingate start (no sudo!)
  5. Verify: twingate status

► SET UP CONNECTOR:
  1. Create Remote Network in admin console
  2. Deploy Connector (Docker/Linux script)
  3. Define Resources (your lab VMs)
  4. Test access through Twingate

► WHY ZERO TRUST:
  Connectors only make OUTBOUND connections.
  No inbound ports to scan or exploit.
  Attacker doing recon won't even see the entry point.""",
    },

    {
        "id": "tl02", "tree": "tools", "tier": 2, "xp": 50,
        "title": "OpenClaw Deploy",
        "brief": "Install and secure an AI assistant",
        "hint":  "Review tool permissions in openclaw.json BEFORE enabling exec. Always audit third-party skills — they run with your agent's permissions.",
        "benefit": "AI agents are the next frontier of both productivity and attack surface. Understanding their security model is cutting-edge knowledge few people have.",
        "bonus": "Restrict OpenClaw permissions, audit installed skills, connect through Twingate. Document security config in ~/openclaw_security.txt",
        "bonus_xp": 15,
        "mission": """═══ MISSION — OpenClaw Deploy ═══

⚠️ OpenClaw can execute shell commands. Understand the risks.

► WHAT IS OPENCLAW?
  Open-source AI agent running on YOUR machine.
  Connects to AI models (Claude, GPT, local).
  Uses 'skills' system (markdown instruction files).
  Data stays local. Bring your own API keys.
  ⚠️ CVE CONSIDERATION: Third-party skills can perform
  data exfiltration and prompt injection. ALWAYS audit.

► INSTALL ON PARROT:
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt install -y nodejs
  npm install -g openclaw@latest
  openclaw onboard --install-daemon

► SECURITY HARDENING:
  1. Edit openclaw.json:
     "tools": {"allow": ["web_search"], "deny": ["exec"]}
  2. Audit skills: ls ~/.openclaw/skills/
  3. Review EVERY third-party skill before installing
  4. Gateway should only listen on localhost
  5. API keys: ensure not stored in plaintext

► THREAT MODEL:
  If compromised, what can the agent do?
  Answer depends on permissions YOU granted.
  Minimum necessary permissions, ALWAYS.""",
    },

    {
        "id": "tl03", "tree": "tools", "tier": 3, "xp": 60,
        "title": "AI Red Team",
        "brief": "Audit your OpenClaw + Twingate stack",
        "hint":  "Think like an attacker: what's the blast radius if your AI agent is compromised? Check ports, permissions, API key storage, and skill integrity.",
        "benefit": "Auditing AI agent security is a brand-new skill that very few people have. As AI agents become common, this knowledge will be highly sought after.",
        "bonus": "Write a monitoring script for OpenClaw logs: alert on curl, wget, nc, rm -rf, /etc/shadow. Your first AI agent IDS!",
        "bonus_xp": 20,
        "mission": """═══ MISSION — AI Red Team ═══

⚠️ Audit your OWN setup.

► AUDIT OPENCLAW:
  ss -tulnp | grep node    # Gateway ports
  cat ~/.openclaw/config.json   # Plaintext secrets?
  Review tool permissions in openclaw.json
  Check if dashboard is exposed beyond localhost

► AUDIT TWINGATE:
  twingate resources        # Access scoped correctly?
  Check Connector privileges
  Review access policies in admin console

► TEST BLAST RADIUS:
  If agent + shell + VPN = remote access trojan YOU installed
  Create restricted profiles for specific resources
  Document in ~/red_team_audit.txt

► HARDEN:
  Restrict exec to specific commands
  Connector runs as dedicated service account
  Monitor logs for suspicious commands""",
    },


    # =========================================================
    # PYTHON SCRIPTING
    # =========================================================

    {
        "id": "py01", "tree": "python", "tier": 1, "xp": 20,
        "title": "Hello Hacker",
        "brief": "Your first Python program",
        "hint":  "print() outputs text. Strings go in quotes. # starts a comment. Python runs top to bottom.",
        "benefit": "Python is THE language of cybersecurity. Every major tool (Metasploit modules, Scapy, custom exploits, automation) uses Python.",
        "bonus": "Make a script that prints a formatted box with your agent codename and status using string formatting.",
        "bonus_xp": 5,
        "sandbox": 'print("=== CyberQuest Python Academy ===")\nprint("Agent: Captain")\nprint("Status: Online")\nprint(f"Python version: {__import__(\'sys\').version}")',
        "mission": """═══ MISSION — Hello Hacker ═══

► OBJECTIVES:
  1. Open terminal: python3
  2. Try:
     >>> print("Hello, Hacker!")
     >>> print(2 + 2)
     >>> print("Name: " + "Captain")

  3. Create hello.py:
     print("=== CyberQuest ===")
     print("Agent: Captain")
     print("Status: Online")

  4. Run: python3 hello.py

► KEY CONCEPTS:
  print() = function that outputs text
  "text" = string
  # = comment (Python ignores it)
  Code runs top to bottom""",
    },

    {
        "id": "py02", "tree": "python", "tier": 1, "xp": 25,
        "title": "Variables & Types",
        "brief": "Store data in variables",
        "hint":  "f-strings are your friend: f\"Hello {name}\". Use type() to check any variable's type. Python figures out types automatically.",
        "benefit": "Variables store everything in security scripts — target IPs, port numbers, payloads, scan results. Understanding types prevents bugs.",
        "bonus": "Create a 'target profile' script with: target_ip, port, protocol, vuln_name, severity_score. Print formatted output.",
        "bonus_xp": 5,
        "sandbox": 'name = "Captain"\nage = 25\nis_hacker = True\ntarget_ip = "192.168.1.100"\n\nprint(f"Agent: {name}, Age: {age}")\nprint(f"Hacker: {is_hacker}")\nprint(f"Target: {target_ip}")\nprint(f"Types: {type(name)}, {type(age)}, {type(is_hacker)}")',
        "mission": """═══ MISSION — Variables & Types ═══

► CREATE VARIABLES:
  name = "Captain"       # String
  age = 25               # Integer
  height = 5.9           # Float
  is_hacker = True       # Boolean

► F-STRINGS:
  print(f"Name: {name}")
  print(f"Age: {age}")

► MATH:
  x=10; y=3
  + - * / (divide) // (floor) % (mod) ** (power)

► CHECK TYPES:
  print(type(name))   # <class 'str'>""",
    },

    {
        "id": "py03", "tree": "python", "tier": 1, "xp": 30,
        "title": "Control Flow",
        "brief": "if/else, loops, and logic",
        "hint":  "Indentation matters! Use 4 spaces. Remember: == checks equality, = assigns. for+range() for counting, while for conditions.",
        "benefit": "Control flow lets you build decision-making tools — vulnerability classifiers, brute force scripts, automated scanners.",
        "bonus": "Build a brute force simulator: try passwords from a list against a stored password, count attempts, print results.",
        "bonus_xp": 10,
        "sandbox": 'targets = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]\n\nfor ip in targets:\n    print(f"[*] Scanning {ip}...")\n    for port in [22, 80, 443]:\n        status = "OPEN" if port != 443 else "FILTERED"\n        print(f"    Port {port}: {status}")\n\npassword = "secret"\nguess = "secret"\nif guess == password:\n    print("\\nACCESS GRANTED")\nelse:\n    print("\\nACCESS DENIED")',
        "mission": """═══ MISSION — Control Flow ═══

► IF/ELIF/ELSE:
  score = 85
  if score >= 90:    print("CRITICAL")
  elif score >= 70:  print("HIGH")
  elif score >= 40:  print("MEDIUM")
  else:              print("LOW")

► COMPARISON: == != > < >= <=
► LOGIC: and, or, not

► FOR LOOP:
  for i in range(5): print(i)
  for ip in ["10.0.0.1","10.0.0.2"]: print(ip)

► WHILE LOOP:
  attempts = 0
  while attempts < 3:
      pwd = input("Password: ")
      if pwd == "secret": break
      attempts += 1""",
    },

    {
        "id": "py04", "tree": "python", "tier": 2, "xp": 40,
        "title": "Functions & Errors",
        "brief": "Reusable code and error handling",
        "hint":  "Functions should do ONE thing. Use try/except for anything that might fail (user input, file operations, network calls).",
        "benefit": "Functions and error handling are what separate scripts from tools. Professional security tools need to handle edge cases gracefully.",
        "bonus": "Build a mini toolkit: port_classifier(), ip_validator(), password_scorer() functions. Call from a menu.",
        "bonus_xp": 10,
        "sandbox": 'def classify_port(port):\n    if port < 1024: return "well-known"\n    elif port < 49152: return "registered"\n    return "dynamic"\n\ndef safe_input(prompt, type_fn=int):\n    try:\n        return type_fn(input(prompt))\n    except ValueError:\n        print("Invalid input!")\n        return None\n\nfor p in [22, 80, 3306, 8080, 50000]:\n    print(f"Port {p}: {classify_port(p)}")',
        "mission": """═══ MISSION — Functions & Errors ═══

► FUNCTIONS:
  def classify_port(port):
      if port < 1024: return "well-known"
      return "registered"
  result = classify_port(80)

► DEFAULT PARAMS:
  def scan(target, ports=[80,443], timeout=5):
      print(f"Scanning {target}")

► TRY/EXCEPT:
  try:
      port = int(input("Port: "))
  except ValueError:
      print("Not a number!")

► RAISING ERRORS:
  def set_port(port):
      if not 1<=port<=65535:
          raise ValueError(f"Port {port} invalid")
      return port""",
    },

    {
        "id": "py05", "tree": "python", "tier": 2, "xp": 45,
        "title": "Data Structures",
        "brief": "Lists, dicts, and comprehensions",
        "hint":  "Lists for ordered collections, dicts for key-value pairs. List comprehension [x for x in list if condition] is powerful and Pythonic.",
        "benefit": "Every security tool uses data structures — port lists, host inventories, scan results. Comprehensions make your code clean and fast.",
        "bonus": "Build a host inventory tool: add hosts with IP/hostname/ports, search by IP or name, display all.",
        "bonus_xp": 10,
        "sandbox": '# Lists\nports = [21, 22, 80, 443, 8080]\nhigh = [p for p in ports if p > 1024]\nprint(f"High ports: {high}")\n\n# Dictionaries\ntarget = {\n    "ip": "192.168.1.100",\n    "hostname": "web-srv",\n    "ports": [22, 80, 443]\n}\nfor k, v in target.items():\n    print(f"  {k}: {v}")\n\n# Dict comprehension\nstatus = {p: ("open" if p < 1024 else "filtered") for p in ports}\nprint(f"\\nStatus: {status}")',
        "mission": """═══ MISSION — Data Structures ═══

► LISTS:
  ports = [22, 80, 443]
  ports.append(8080)
  ports.sort()
  high = [p for p in ports if p > 1024]  # Comprehension!

► DICTIONARIES:
  target = {"ip": "192.168.1.1", "ports": [22,80]}
  target["status"] = "up"
  for key, val in target.items(): print(f"{key}: {val}")

► NESTED:
  network = {
      "192.168.1.1": {"name":"router", "ports":[80]},
      "192.168.1.100": {"name":"web", "ports":[22,80]}
  }""",
    },

    {
        "id": "py06", "tree": "python", "tier": 2, "xp": 40,
        "title": "Files & Modules",
        "brief": "File I/O, JSON, standard library",
        "hint":  "Always use 'with open()' for file operations — it auto-closes. JSON is your go-to for structured data. hashlib for security work.",
        "benefit": "Real security tools read configs, parse logs, save results, and use crypto libraries. File I/O and modules make your scripts professional.",
        "bonus": "Write a script that hashes a password with SHA256, generates a secure token, logs the timestamp, saves to JSON.",
        "bonus_xp": 10,
        "sandbox": 'import json, hashlib, secrets\nfrom datetime import datetime\n\nscan = {"target":"192.168.1.1","ports":[22,80,443],"time":str(datetime.now())}\n\nwith open("scan.json","w") as f:\n    json.dump(scan, f, indent=2)\n    print("Saved scan.json")\n\nwith open("scan.json","r") as f:\n    loaded = json.load(f)\n    print(f"Target: {loaded[\'target\']}")\n\npw = "password123"\nprint(f"\\nSHA256: {hashlib.sha256(pw.encode()).hexdigest()}")\nprint(f"Token: {secrets.token_hex(16)}")',
        "mission": """═══ MISSION — Files & Modules ═══

► FILE I/O:
  with open("results.txt", "w") as f:
      f.write("Port 22: OPEN\\n")
  with open("results.txt", "r") as f:
      print(f.read())

► JSON:
  import json
  data = {"target":"192.168.1.1", "ports":[22,80]}
  with open("config.json","w") as f:
      json.dump(data, f, indent=2)

► USEFUL MODULES:
  os: os.getcwd(), os.listdir()
  hashlib: sha256, md5 hashing
  secrets: cryptographic random
  re: regex pattern matching
  datetime: timestamps""",
    },

    {
        "id": "py07", "tree": "python", "tier": 3, "xp": 55,
        "title": "OOP & Advanced",
        "brief": "Classes, decorators, generators",
        "hint":  "Classes model real things (Target, Scanner, Vulnerability). Decorators add behavior to functions. Generators save memory with lazy evaluation.",
        "benefit": "Advanced Python separates script kiddies from tool developers. Professional security tools use OOP, decorators for logging/auth, generators for large datasets.",
        "bonus": "Build a Scanner class hierarchy: base Scanner, PortScanner, VulnScanner subclasses. Add a @timer decorator.",
        "bonus_xp": 15,
        "sandbox": 'import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f"[{func.__name__}] {time.time()-start:.4f}s")\n        return result\n    return wrapper\n\nclass Scanner:\n    def __init__(self, target):\n        self.target = target\n        self.results = []\n    def report(self):\n        print(f"--- {self.target} ---")\n        for r in self.results: print(f"  {r}")\n\nclass PortScanner(Scanner):\n    @timer\n    def scan(self, ports):\n        for p in ports:\n            self.results.append(f"Port {p}: open")\n\nps = PortScanner("192.168.1.1")\nps.scan([22, 80, 443, 8080])\nps.report()',
        "mission": """═══ MISSION — OOP & Advanced ═══

► CLASSES:
  class Target:
      def __init__(self, ip, hostname):
          self.ip = ip
          self.hostname = hostname
          self.ports = []
      def add_port(self, port):
          self.ports.append(port)
      def report(self):
          print(f"{self.hostname}: {self.ports}")

► INHERITANCE:
  class PortScanner(Scanner):
      def scan(self, ports): ...

► DECORATORS:
  def timer(func):
      def wrapper(*args):
          start = time.time()
          result = func(*args)
          print(f"Took {time.time()-start:.2f}s")
          return result
      return wrapper
  @timer
  def slow_scan(): ...

► COMPREHENSIONS & LAMBDA:
  high = [p for p in ports if p > 1024]
  classify = lambda p: "low" if p<1024 else "high"
  sorted_ports = sorted(ports, key=lambda p: -p)""",
    },

    {
        "id": "py08", "tree": "python", "tier": 3, "xp": 70,
        "title": "Build a Security Tool",
        "brief": "Capstone: build a real tool from scratch",
        "hint":  "Plan before coding: what does the tool do? What classes do you need? What modules? Start with the simplest version, then add features.",
        "benefit": "Building your own tools is what separates a cybersecurity professional from someone who only runs other people's tools. This is portfolio material.",
        "bonus": "Add to your tool: export results to JSON, add a --verbose flag, handle all errors gracefully, add color output.",
        "bonus_xp": 20,
        "sandbox": 'import secrets, string, json\nfrom datetime import datetime\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + "!@#$%^&*"\n    return "".join(secrets.choice(chars) for _ in range(length))\n\ndef score_password(pw):\n    checks = [len(pw)>=12, any(c.isupper() for c in pw),\n              any(c.isdigit() for c in pw), any(c in "!@#$%^&*" for c in pw)]\n    return sum(checks)\n\nprint("=== Password Generator & Scorer ===")\nfor i in range(5):\n    pw = generate_password(20)\n    sc = score_password(pw)\n    print(f"  {pw}  Score: {sc}/4")',
        "mission": """═══ MISSION — Build a Security Tool ═══

Combine everything into a REAL tool. Choose one:

► OPTION A: LOG ANALYZER
  - Parse auth.log for failed logins
  - Count failures per IP
  - Flag brute force (5+ fails in 5 min)
  - Generate JSON report

► OPTION B: PASSWORD VAULT
  - Store service/username/password entries
  - Basic XOR encryption (learning only!)
  - Save/load from JSON
  - Generate random passwords
  - Score password strength

► OPTION C: NETWORK SCANNER
  - Ping sweep a subnet
  - Port scan discovered hosts
  - Service version detection
  - Save results to JSON/CSV

► REQUIREMENTS:
  Use classes (OOP)
  Use file I/O (JSON)
  Use error handling (try/except)
  Use 3+ standard library modules
  Use list comprehension somewhere""",
    },
]


# ---------------------------------------------------------------------------
# KNOWLEDGE EXAMS
# Shown in the Exams tab. Pass with 70%+ to earn XP.
# ---------------------------------------------------------------------------

SIDE_QUESTS = [
    {
        "id": "exam_linux",
        "title": "🧪 Linux Fundamentals Exam",
        "xp": 30,
        "required_tree": "linux",
        "questions": [
            {"q": "What command shows your current directory?",       "options": ["ls","pwd","cd","whoami"],                         "answer": 1},
            {"q": "Which directory stores config files?",             "options": ["/home","/tmp","/etc","/bin"],                     "answer": 2},
            {"q": "What does chmod 755 mean?",                        "options": ["Owner:rwx Group:r-x Others:r-x","All:rwx","Owner:rw- Others:r--","Owner:rwx Group:rwx Others:rwx"], "answer": 0},
            {"q": "SUID bit does what?",                              "options": ["Makes read-only","Runs as file owner","Deletes after use","Encrypts file"], "answer": 1},
            {"q": "Find SUID files command?",                         "options": ["grep -r suid /","find / -perm -4000","ls -suid","chmod --find-suid"], "answer": 1},
            {"q": "Password hashes stored in?",                       "options": ["/etc/passwd","/etc/shadow","/etc/hashes","/var/log/auth"], "answer": 1},
            {"q": "sudo -l shows?",                                   "options": ["Last login","Load","What you can sudo","Ports"],   "answer": 2},
            {"q": "Default world-writable dir?",                      "options": ["/etc","/home","/tmp","/root"],                    "answer": 2},
        ],
    },
    {
        "id": "exam_network",
        "title": "🧪 Networking Exam",
        "xp": 30,
        "required_tree": "networking",
        "questions": [
            {"q": "TCP operates at OSI layer?",  "options": ["2","3","4","7"],                                           "answer": 2},
            {"q": "SSH default port?",           "options": ["21","22","80","443"],                                      "answer": 1},
            {"q": "SYN packet indicates?",       "options": ["Closing","Data transfer","Connection request","Error"],    "answer": 2},
            {"q": "nmap -sS does?",              "options": ["UDP scan","SYN stealth","Full connect","Ping sweep"],      "answer": 1},
            {"q": "DNS resolves?",               "options": ["IPs to MACs","Names to IPs","MACs to names","Ports to services"], "answer": 1},
            {"q": "/24 subnet mask?",            "options": ["255.0.0.0","255.255.0.0","255.255.255.0","255.255.255.128"], "answer": 2},
            {"q": "Captures packets?",           "options": ["netstat","ifconfig","tcpdump","ping"],                     "answer": 2},
            {"q": "ARP resolves?",               "options": ["IP to hostname","IP to MAC","MAC to IP","Host to IP"],     "answer": 1},
        ],
    },
    {
        "id": "exam_security",
        "title": "🧪 Security Foundations Exam",
        "xp": 35,
        "required_tree": "governance",
        "questions": [
            {"q": "'C' in CIA Triad?",          "options": ["Control","Compliance","Confidentiality","Cryptography"],   "answer": 2},
            {"q": "CVSS Critical range?",        "options": ["7.0-8.9","8.0-9.9","9.0-10.0","10.0 only"],              "answer": 2},
            {"q": "NIST 'Detect' function?",     "options": ["Prevent attacks","Monitor for attacks","Respond to attacks","Recover"], "answer": 1},
            {"q": "CVE format?",                 "options": ["CVE-YYYY-NNNNN","VULN-NNNNN","SEC-YYYY","NVD-NNNNN"],     "answer": 0},
            {"q": "OWASP Top 10 focuses on?",    "options": ["Network vulns","Web app vulns","Hardware","Social engineering"], "answer": 1},
            {"q": "$6$ hash type?",              "options": ["MD5","SHA-256","SHA-512","bcrypt"],                        "answer": 2},
            {"q": "Zero-day is?",                "options": ["Patched vuln","No known fix","Low severity","Day-zero bug"], "answer": 1},
            {"q": "Defense in depth?",           "options": ["One strong firewall","Multiple security layers","Deep packet inspection","Encrypt everything"], "answer": 1},
        ],
    },
    {
        "id": "exam_web",
        "title": "🧪 Web Hacking Exam",
        "xp": 30,
        "required_tree": "webhack",
        "questions": [
            {"q": "SQL injection is?",           "options": ["CSS injection","Malicious SQL in queries","DDoS","XSS"],   "answer": 1},
            {"q": "XSS stands for?",             "options": ["Cross-System Scripting","Cross-Site Scripting","eXtra Secure Socket","XML Site Service"], "answer": 1},
            {"q": "Intercepts HTTP requests?",   "options": ["Nmap","Wireshark","Burp Suite","Metasploit"],              "answer": 2},
            {"q": "Reveals hidden web paths?",   "options": ["index.html","robots.txt",".htaccess","config.php"],        "answer": 1},
            {"q": "OWASP #1 (2021)?",            "options": ["Injection","Broken Access Control","XSS","SSRF"],          "answer": 1},
            {"q": "sqlmap automates?",           "options": ["Port scanning","SQL injection","Password cracking","Firewall config"], "answer": 1},
        ],
    },
    {
        "id": "exam_python",
        "title": "🧪 Python Fundamentals Exam",
        "xp": 30,
        "required_tree": "python",
        "questions": [
            {"q": "Print output in Python?",    "options": ["echo()","printf()","print()","output()"],                  "answer": 2},
            {"q": "f-string syntax?",           "options": ["f'Hello {name}'","'Hello' + name","format('Hello', name)","Hello.format(name)"], "answer": 0},
            {"q": "List comprehension?",        "options": ["list(x for x)","[x for x in list]","{x: x}","(x for x)"], "answer": 1},
            {"q": "Handle errors with?",        "options": ["if/else","try/except","for/while","def/return"],           "answer": 1},
            {"q": "__init__ is?",               "options": ["Destructor","Constructor","Iterator","Decorator"],          "answer": 1},
            {"q": "Read a file safely?",        "options": ["open('f').read()","with open('f') as f:","file.get('f')","read('f')"], "answer": 1},
        ],
    },
]


# ---------------------------------------------------------------------------
# ACHIEVEMENTS
# Checked dynamically against the player's save data.
# ---------------------------------------------------------------------------

def get_achievements(save):
    """Return a list of achievement dicts, each with a 'check' lambda."""
    completed   = save.get("completed_quests", [])
    bonuses     = save.get("bonus_completed",  [])
    exam_scores = save.get("exam_scores",      {})
    exams_done  = save.get("side_quests_done", [])

    return [
        {"id": "first",   "name": "First Blood",    "desc": "Complete first quest",         "icon": "🩸",  "check": lambda: len(completed) >= 1},
        {"id": "five",    "name": "Grinding",        "desc": "Complete 5 quests",            "icon": "⚔️",  "check": lambda: len(completed) >= 5},
        {"id": "ten",     "name": "Double Digits",   "desc": "Complete 10 quests",           "icon": "🔟",  "check": lambda: len(completed) >= 10},
        {"id": "twenty",  "name": "Unstoppable",     "desc": "Complete 20 quests",           "icon": "🔥",  "check": lambda: len(completed) >= 20},
        {"id": "all",     "name": "Completionist",   "desc": "ALL quests done",              "icon": "👑",  "check": lambda: len(completed) >= len(ALL_QUESTS)},
        {"id": "bonus1",  "name": "Extra Credit",    "desc": "Claim a bonus",                "icon": "⭐",  "check": lambda: len(bonuses) >= 1},
        {"id": "bonus5",  "name": "Overachiever",    "desc": "5 bonuses claimed",            "icon": "🌟",  "check": lambda: len(bonuses) >= 5},
        {"id": "exam1",   "name": "Test Taker",      "desc": "Pass an exam",                 "icon": "📝",  "check": lambda: len(exams_done) >= 1},
        {"id": "exams_all","name": "Scholar",        "desc": "Pass all exams",               "icon": "🎓",  "check": lambda: len(exams_done) >= len(SIDE_QUESTS)},
        {"id": "perfect", "name": "Perfect Score",   "desc": "100% on any exam",             "icon": "💯",  "check": lambda: any(v == 100 for v in exam_scores.values())},
        {"id": "linux",   "name": "Penguin Master",  "desc": "All Linux quests",             "icon": "🐧",  "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "linux")},
        {"id": "web",     "name": "Web Warrior",     "desc": "All Web quests",               "icon": "🕸️",  "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "webhack")},
        {"id": "def",     "name": "Shield Wall",     "desc": "All Defense quests",           "icon": "🛡️",  "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "defense")},
        {"id": "py",      "name": "Pythonista",      "desc": "All Python quests",            "icon": "🐍",  "check": lambda: all(q["id"] in completed for q in ALL_QUESTS if q["tree"] == "python")},
        {"id": "trees",   "name": "Renaissance",     "desc": "Quest in every tree",          "icon": "🌈",  "check": lambda: all(any(q["id"] in completed for q in ALL_QUESTS if q["tree"] == t) for t in SKILL_TREES)},
    ]


# ---------------------------------------------------------------------------
# XP AND RANK HELPERS
# ---------------------------------------------------------------------------

def get_rank(xp):
    """Return the rank dict the player currently holds."""
    current_rank = RANKS[0]
    for rank in RANKS:
        if xp >= rank["xp"]:
            current_rank = rank
    return current_rank


def get_next_rank(xp):
    """Return the next rank the player is working toward, or None if maxed."""
    for rank in RANKS:
        if rank["xp"] > xp:
            return rank
    return None


def total_xp(save):
    """Sum up all XP earned from quests, bonuses, and passed exams."""
    xp = 0

    # XP from completed quests
    xp += sum(q["xp"] for q in ALL_QUESTS if q["id"] in save.get("completed_quests", []))

    # XP from claimed bonus objectives
    for bonus_id in save.get("bonus_completed", []):
        quest = next((q for q in ALL_QUESTS if q["id"] == bonus_id), None)
        if quest:
            xp += quest.get("bonus_xp", 0)

    # XP from passed exams
    xp += sum(sq["xp"] for sq in SIDE_QUESTS if sq["id"] in save.get("side_quests_done", []))

    return xp


# ---------------------------------------------------------------------------
# MAIN APPLICATION CLASS
# ---------------------------------------------------------------------------

class App:
    # --- Color palette (dark terminal theme) ---
    BG  = "#0a0a0f"   # Main background
    BG2 = "#111118"   # Card / panel background
    BGH = "#1a1a24"   # Hover / selected background
    BGC = "#08080e"   # Code / text area background
    FG  = "#cccccc"   # Body text
    FGD = "#555566"   # Dimmed / secondary text
    FGB = "#ffffff"   # Bright / heading text
    ACC = "#00ff88"   # Accent (green)
    BRD = "#222233"   # Border color
    DON = "#0a1a10"   # Completed quest background

    def __init__(self, root):
        self.root = root
        self.root.title("CyberQuest Academy")
        self.root.configure(bg=self.BG)
        self.root.geometry("980x760")
        self.root.minsize(740, 540)

        self.save     = load_save()
        self.sel_tree = None  # Currently filtered skill tree (None = show all)

        # Font sizes used throughout the UI
        self.ft = tkfont.Font(family="Consolas", size=18, weight="bold")  # Title
        self.fs = tkfont.Font(family="Consolas", size=9)                  # Small
        self.fh = tkfont.Font(family="Consolas", size=12, weight="bold")  # Header
        self.fn = tkfont.Font(family="Consolas", size=10)                 # Normal
        self.fb = tkfont.Font(family="Consolas", size=10, weight="bold")  # Bold body
        self.fr = tkfont.Font(family="Consolas", size=15, weight="bold")  # Rank title
        self.fx = tkfont.Font(family="Consolas", size=22, weight="bold")  # XP number

        self._build_layout()

        # Show the getting-started popup on first launch
        if not self.save.get("seen_requirements"):
            self.root.after(500, self._show_requirements)

        self.show_dashboard()

    # -----------------------------------------------------------------------
    # LAYOUT CONSTRUCTION
    # -----------------------------------------------------------------------

    def _build_layout(self):
        """Create the persistent shell: header, rank bar, nav tabs, scroll area."""
        self.mf = tk.Frame(self.root, bg=self.BG)
        self.mf.pack(fill="both", expand=True)

        # App title
        header = tk.Frame(self.mf, bg=self.BG)
        header.pack(fill="x", padx=20, pady=(8, 2))
        tk.Label(header, text="CYBERQUEST ACADEMY", font=self.ft, fg=self.ACC, bg=self.BG).pack()
        tk.Label(header, text="BEGINNER → ADVANCED  •  PARROT OS", font=self.fs, fg=self.FGD, bg=self.BG).pack()

        # Rank / XP bar (rebuilt on every XP change via _rank())
        self.rf = tk.Frame(self.mf, bg=self.BG2, highlightbackground="#00cc66", highlightthickness=1)
        self.rf.pack(fill="x", padx=20, pady=5)
        self._rank()

        # Navigation tabs
        nav = tk.Frame(self.mf, bg=self.BG)
        nav.pack(fill="x", padx=20, pady=(0, 2))
        tab_definitions = [
            ("⚔ QUESTS",       self.show_dashboard),
            ("🐍 PYTHON",      self.show_python),
            ("🧪 EXAMS",       self.show_exams),
            ("🏆 ACHIEVEMENTS", self.show_achievements),
            ("💼 CAREERS",     self.show_careers),
            ("📋 SETUP",       self._show_requirements),
        ]
        self.tab_btns = []
        for label, command in tab_definitions:
            btn = tk.Button(
                nav, text=label, font=self.fs,
                bg=self.BG2, fg=self.FGD,
                activebackground=self.BGH, activeforeground=self.ACC,
                bd=0, padx=8, pady=5, cursor="hand2",
                command=command,
            )
            btn.pack(side="left", expand=True, fill="x", padx=1)
            self.tab_btns.append(btn)

        # Scrollable content area
        content = tk.Frame(self.mf, bg=self.BG)
        content.pack(fill="both", expand=True, padx=20, pady=(2, 6))

        self.cv = tk.Canvas(content, bg=self.BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(content, orient="vertical", command=self.cv.yview, bg=self.BG2, troughcolor=self.BG)

        self.sf = tk.Frame(self.cv, bg=self.BG)
        self.sf.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cw = self.cv.create_window((0, 0), window=self.sf, anchor="nw")

        self.cv.configure(yscrollcommand=scrollbar.set)
        self.cv.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling and width sync
        self.cv.bind_all("<MouseWheel>", lambda e: self.cv.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfig(self.cw, width=e.width))

    def _rank(self):
        """Rebuild the rank/XP bar with current progress."""
        for widget in self.rf.winfo_children():
            widget.destroy()

        xp       = total_xp(self.save)
        rank     = get_rank(xp)
        next_rk  = get_next_rank(xp)

        inner = tk.Frame(self.rf, bg=self.BG2)
        inner.pack(fill="x", padx=12, pady=7)

        # Left: rank level + title. Right: XP number.
        top = tk.Frame(inner, bg=self.BG2)
        top.pack(fill="x")

        left = tk.Frame(top, bg=self.BG2)
        left.pack(side="left")
        tk.Label(left, text=f"RANK {rank['level']}", font=self.fs, fg=self.ACC, bg=self.BG2).pack(anchor="w")
        tk.Label(left, text=rank["title"], font=self.fr, fg=self.FGB, bg=self.BG2).pack(anchor="w")

        right = tk.Frame(top, bg=self.BG2)
        right.pack(side="right")
        xp_frame = tk.Frame(right, bg=self.BG2)
        xp_frame.pack(anchor="e")
        tk.Label(xp_frame, text=str(xp),   font=self.fx, fg=self.FGB, bg=self.BG2).pack(side="left")
        tk.Label(xp_frame, text=" XP",     font=self.fh, fg=self.ACC, bg=self.BG2).pack(side="left", pady=(3, 0))

        # Progress bar toward next rank
        if next_rk:
            progress_frame = tk.Frame(inner, bg=self.BG2)
            progress_frame.pack(fill="x", pady=(4, 0))

            labels = tk.Frame(progress_frame, bg=self.BG2)
            labels.pack(fill="x")
            tk.Label(labels, text=rank["title"],                                font=self.fs, fg=self.FGD, bg=self.BG2).pack(side="left")
            tk.Label(labels, text=f"{next_rk['title']} — {next_rk['xp']-xp} XP to go", font=self.fs, fg=self.FGD, bg=self.BG2).pack(side="right")

            bar_bg = tk.Frame(progress_frame, bg=self.BRD, height=6)
            bar_bg.pack(fill="x", pady=(2, 0))
            bar_bg.pack_propagate(False)
            progress = (xp - rank["xp"]) / max(1, next_rk["xp"] - rank["xp"])
            tk.Frame(bar_bg, bg=self.ACC, height=6).place(relwidth=min(progress, 1.0), relheight=1.0)

        # Quest / bonus / exam counts
        counts = tk.Frame(inner, bg=self.BG2)
        counts.pack(fill="x", pady=(4, 0))
        n_quests = len(self.save.get("completed_quests", []))
        n_bonus  = len(self.save.get("bonus_completed",  []))
        n_exams  = len(self.save.get("side_quests_done", []))
        tk.Label(
            counts,
            text=f"{n_quests}/{len(ALL_QUESTS)} Quests • {n_bonus} Bonuses • {n_exams} Exams",
            font=self.fs, fg=self.FGD, bg=self.BG2,
        ).pack()

    def _clear(self):
        """Remove all widgets from the scroll area and scroll back to top."""
        for widget in self.sf.winfo_children():
            widget.destroy()
        self.cv.yview_moveto(0)

    def _tabs(self, active_index):
        """Highlight the active navigation tab."""
        for i, btn in enumerate(self.tab_btns):
            btn.configure(fg=self.ACC if i == active_index else self.FGD)

    def _avail(self, tree_filter=None):
        """
        Return quests the player can currently see, respecting tier locks.
        Tier 2 unlocks after any Tier 1 in the same tree is complete.
        Tier 3 unlocks after any Tier 2 in the same tree is complete.
        """
        available = []
        completed = self.save.get("completed_quests", [])
        active_filter = tree_filter or self.sel_tree

        for quest in ALL_QUESTS:
            # Apply tree filter if one is set
            if active_filter and quest["tree"] != active_filter:
                continue

            if quest["tier"] == 1:
                available.append(quest)
            elif quest["tier"] == 2:
                # Require at least one completed Tier 1 in the same tree
                has_tier1 = any(
                    c for c in completed
                    if any(q["id"] == c and q["tree"] == quest["tree"] and q["tier"] == 1
                           for q in ALL_QUESTS)
                )
                if has_tier1:
                    available.append(quest)
            elif quest["tier"] == 3:
                # Require at least one completed Tier 2 in the same tree
                has_tier2 = any(
                    c for c in completed
                    if any(q["id"] == c and q["tree"] == quest["tree"] and q["tier"] == 2
                           for q in ALL_QUESTS)
                )
                if has_tier2:
                    available.append(quest)

        return available

    # -----------------------------------------------------------------------
    # GETTING STARTED POPUP
    # -----------------------------------------------------------------------

    def _show_requirements(self):
        """Show the first-launch setup instructions in a modal popup."""
        popup = tk.Toplevel(self.root)
        popup.title("Getting Started")
        popup.geometry("700x550")
        popup.configure(bg=self.BG)
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text="📋 BEFORE YOU BEGIN", font=self.fh, fg="#ffcc00", bg=self.BG).pack(pady=(12, 5))

        text_frame = tk.Frame(popup, bg=self.BGC)
        text_frame.pack(fill="both", expand=True, padx=15, pady=5)
        text_widget = tk.Text(text_frame, font=self.fn, bg=self.BGC, fg=self.FG, wrap="word", relief="flat", padx=12, pady=10)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", REQUIREMENTS_TEXT)
        text_widget.configure(state="disabled")

        def dismiss():
            self.save["seen_requirements"] = True
            write_save(self.save)
            popup.destroy()

        tk.Button(
            popup, text="✓  GOT IT — LET'S GO!", font=self.fh,
            bg=self.BG2, fg=self.ACC, bd=0, pady=10, cursor="hand2",
            command=dismiss,
        ).pack(fill="x", padx=15, pady=10)

    # -----------------------------------------------------------------------
    # DASHBOARD (main quest list)
    # -----------------------------------------------------------------------

    def show_dashboard(self):
        self._clear()
        self._tabs(0)

        # Tree filter buttons (icons only, except ALL)
        filter_row = tk.Frame(self.sf, bg=self.BG)
        filter_row.pack(fill="x", pady=(0, 4))

        def set_filter(tree_key):
            self.sel_tree = tree_key
            self.show_dashboard()

        tk.Button(
            filter_row, text="ALL", font=self.fs,
            bg=self.BGH if not self.sel_tree else self.BG2,
            fg=self.FGB if not self.sel_tree else self.FGD,
            bd=0, padx=5, pady=2, cursor="hand2",
            command=lambda: set_filter(None),
        ).pack(side="left", padx=(0, 1))

        for key, tree in SKILL_TREES.items():
            if key == "python":
                continue  # Python lives on its own tab
            selected = self.sel_tree == key
            tk.Button(
                filter_row, text=tree["icon"], font=self.fs,
                bg=self.BGH if selected else self.BG2,
                fg=tree["color"] if selected else self.FGD,
                bd=0, padx=4, pady=2, cursor="hand2",
                command=lambda k=key: set_filter(k),
            ).pack(side="left", padx=1)

        # Per-tree XP progress mini-bars
        progress_grid = tk.Frame(self.sf, bg=self.BG)
        progress_grid.pack(fill="x", pady=(0, 6))
        non_python_trees = {k: v for k, v in SKILL_TREES.items() if k != "python"}
        cols = min(5, len(non_python_trees))

        for i, (key, tree) in enumerate(non_python_trees.items()):
            tree_xp  = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests", []) and q["tree"] == key)
            max_xp   = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == key)

            cell = tk.Frame(progress_grid, bg=self.BG2, padx=4, pady=3)
            cell.grid(row=i // cols, column=i % cols, sticky="ew", padx=1, pady=1)
            tk.Label(cell, text=f"{tree['icon']} {tree['name'].split()[0]}", font=self.fs, fg=tree["color"], bg=self.BG2, anchor="w").pack(fill="x")

            bar_bg = tk.Frame(cell, bg=self.BRD, height=4)
            bar_bg.pack(fill="x", pady=(2, 0))
            bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=tree["color"], height=4).place(relwidth=min(tree_xp / max(1, max_xp), 1.0), relheight=1.0)

        for col in range(cols):
            progress_grid.columnconfigure(col, weight=1)

        # Quest cards
        available = [q for q in self._avail() if q["tree"] != "python"]
        for quest in available:
            self._card(quest)

        if not available:
            tk.Label(self.sf, text="No quests. Complete lower tiers to unlock.", font=self.fn, fg=self.FGD, bg=self.BG, pady=20).pack()

        tk.Label(self.sf, text="", bg=self.BG).pack(pady=3)
        tk.Button(
            self.sf, text="🔄 RESET ALL PROGRESS", font=self.fs,
            bg="#1a0a0a", fg="#ff4444", bd=0, pady=5, cursor="hand2",
            command=self._reset,
        ).pack(fill="x")

    # -----------------------------------------------------------------------
    # PYTHON TAB
    # -----------------------------------------------------------------------

    def show_python(self):
        self._clear()
        self._tabs(1)

        tk.Label(self.sf, text="🐍 PYTHON SCRIPTING", font=self.fh, fg="#3776ab", bg=self.BG).pack(anchor="w", pady=(0, 4))
        tk.Label(self.sf, text="Learn Python the hacker way. Each quest has a built-in code sandbox.", font=self.fs, fg=self.FGD, bg=self.BG).pack(anchor="w", pady=(0, 8))

        # Python-specific XP progress bar
        tree_xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests", []) and q["tree"] == "python")
        max_xp  = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == "python")

        prog_frame = tk.Frame(self.sf, bg=self.BG2, padx=8, pady=6)
        prog_frame.pack(fill="x", pady=(0, 8))
        tk.Label(prog_frame, text=f"🐍 Python Progress: {tree_xp}/{max_xp} XP", font=self.fb, fg="#3776ab", bg=self.BG2).pack(anchor="w")
        bar_bg = tk.Frame(prog_frame, bg=self.BRD, height=6)
        bar_bg.pack(fill="x", pady=(4, 0))
        bar_bg.pack_propagate(False)
        tk.Frame(bar_bg, bg="#3776ab", height=6).place(relwidth=min(tree_xp / max(1, max_xp), 1.0), relheight=1.0)

        for quest in self._avail(tree_filter="python"):
            self._card(quest)

    # -----------------------------------------------------------------------
    # QUEST CARD (list view)
    # -----------------------------------------------------------------------

    def _card(self, quest):
        """Render a single clickable quest card in the current scroll area."""
        tree      = SKILL_TREES[quest["tree"]]
        completed = quest["id"] in self.save.get("completed_quests", [])
        bonus_done = quest["id"] in self.save.get("bonus_completed",  [])
        bg        = self.DON if completed else self.BG2

        card = tk.Frame(
            self.sf, bg=bg, cursor="hand2",
            highlightbackground=self.ACC if completed else self.BRD,
            highlightthickness=1,
        )
        card.pack(fill="x", pady=2)

        inner = tk.Frame(card, bg=bg)
        inner.pack(fill="x", padx=10, pady=6)

        top_row = tk.Frame(inner, bg=bg)
        top_row.pack(fill="x")

        # Tree icon + tier badge
        tk.Label(top_row, text=f"{tree['icon']} T{quest['tier']}", font=self.fs, fg=tree["color"], bg=bg).pack(side="left")

        # Quest title with checkmark if done
        prefix = "  ✓ " if completed else "  "
        tk.Label(top_row, text=f"{prefix}{quest['title']}", font=self.fb, fg=self.ACC if completed else self.FGB, bg=bg).pack(side="left")

        # XP label (includes bonus star if applicable)
        xp_text = f"+{quest['xp']}"
        if quest.get("bonus_xp"):
            xp_text += f" (+{quest['bonus_xp']}★)" if not bonus_done else f" +{quest['bonus_xp']}★"
        tk.Label(top_row, text=xp_text, font=self.fb, fg=tree["color"], bg=bg).pack(side="right")

        # Brief description
        tk.Label(inner, text=quest["brief"], font=self.fs, fg=self.FGD, bg=bg, anchor="w").pack(fill="x", pady=(1, 0))

        # Make every sub-widget clickable too
        clickable_widgets = [card, inner, top_row] + list(inner.winfo_children()) + list(top_row.winfo_children())
        for widget in clickable_widgets:
            widget.bind("<Button-1>", lambda e, q=quest: self._detail(q))

    # -----------------------------------------------------------------------
    # QUEST DETAIL VIEW
    # -----------------------------------------------------------------------

    def _detail(self, quest):
        """Show the full mission brief, hints, sandbox button, and completion controls."""
        self._clear()
        self._tabs(1 if quest["tree"] == "python" else 0)

        tree       = SKILL_TREES[quest["tree"]]
        completed  = quest["id"] in self.save.get("completed_quests", [])
        bonus_done = quest["id"] in self.save.get("bonus_completed",  [])
        back_cmd   = self.show_python if quest["tree"] == "python" else self.show_dashboard

        # Back button
        tk.Button(self.sf, text="← Back", font=self.fb, bg=self.BG, fg=self.ACC, bd=0, cursor="hand2", command=back_cmd).pack(anchor="w", pady=(0, 5))

        # Quest header card
        header = tk.Frame(self.sf, bg=self.BG2, highlightbackground=tree["color"], highlightthickness=1)
        header.pack(fill="x")
        header_inner = tk.Frame(header, bg=self.BG2)
        header_inner.pack(fill="x", padx=12, pady=7)

        top = tk.Frame(header_inner, bg=self.BG2)
        top.pack(fill="x")
        tk.Label(top, text=f"{tree['icon']} {tree['name'].upper()} • TIER {quest['tier']}", font=self.fs, fg=tree["color"], bg=self.BG2).pack(side="left")
        tk.Label(top, text=f"+{quest['xp']} XP", font=self.fh, fg=tree["color"], bg=self.BG2).pack(side="right")
        tk.Label(header_inner, text=quest["title"], font=self.fh, fg=self.FGB, bg=self.BG2, anchor="w").pack(fill="x", pady=(2, 0))

        # "Why learn this?" benefit box (blue accent)
        if quest.get("benefit"):
            benefit_box = tk.Frame(self.sf, bg="#0f1018", highlightbackground="#4488ff", highlightthickness=1)
            benefit_box.pack(fill="x", pady=(3, 0))
            tk.Label(
                benefit_box,
                text=f"💎 WHY LEARN THIS: {quest['benefit']}",
                font=self.fs, fg="#88bbff", bg="#0f1018",
                wraplength=700, justify="left", padx=10, pady=6,
            ).pack(fill="x")

        # Mission text area (read-only, syntax-highlighted headers)
        mission_frame = tk.Frame(self.sf, bg=self.BGC, highlightbackground=self.BRD, highlightthickness=1)
        mission_frame.pack(fill="x", pady=(3, 0))

        mission_text = tk.Text(
            mission_frame, font=self.fn, bg=self.BGC, fg=self.FG,
            wrap="word", relief="flat", padx=12, pady=10, height=14,
        )
        mission_text.pack(fill="both", expand=True)
        mission_text.insert("1.0", quest["mission"])

        # Colour lines that start with section markers or warnings
        mission_text.tag_configure("hdr",  foreground=tree["color"], font=self.fb)
        mission_text.tag_configure("warn", foreground="#ff6688")
        for i, line in enumerate(mission_text.get("1.0", "end").split("\n"), 1):
            if line.startswith("═══") or line.startswith("►"):
                mission_text.tag_add("hdr",  f"{i}.0", f"{i}.end")
            elif line.startswith("⚠"):
                mission_text.tag_add("warn", f"{i}.0", f"{i}.end")
        mission_text.configure(state="disabled")

        # Hint button
        if quest.get("hint"):
            tk.Button(
                self.sf, text="💡 SHOW HINT", font=self.fb,
                bg=self.BG2, fg="#ffcc00", bd=0, pady=6, cursor="hand2",
                command=lambda: messagebox.showinfo("💡 Hint", quest["hint"]),
            ).pack(fill="x", pady=(4, 0))

        # Python sandbox button (Python quests only)
        if quest.get("sandbox"):
            tk.Button(
                self.sf, text="⚡ OPEN IN SANDBOX", font=self.fb,
                bg=self.BG2, fg="#3776ab", bd=0, pady=6, cursor="hand2",
                command=lambda: self._sandbox(quest["sandbox"]),
            ).pack(fill="x", pady=(3, 0))

        # Complete / already completed indicator
        if not completed:
            tk.Button(
                self.sf, text="✓ MARK COMPLETE", font=self.fh,
                bg=self.BG2, fg=tree["color"], bd=0, pady=8, cursor="hand2",
                command=lambda: self._complete(quest),
            ).pack(fill="x", pady=(4, 0))
        else:
            tk.Label(self.sf, text="✓ QUEST COMPLETED", font=self.fh, fg=self.ACC, bg=self.DON, pady=8).pack(fill="x", pady=(4, 0))

        # Bonus objective section
        if quest.get("bonus"):
            bonus_box = tk.Frame(self.sf, bg="#0f0f18", highlightbackground="#ffcc00", highlightthickness=1)
            bonus_box.pack(fill="x", pady=(4, 0))
            bonus_inner = tk.Frame(bonus_box, bg="#0f0f18")
            bonus_inner.pack(fill="x", padx=10, pady=6)

            tk.Label(bonus_inner, text=f"★ BONUS (+{quest.get('bonus_xp', 0)} XP)", font=self.fb, fg="#ffcc00", bg="#0f0f18").pack(anchor="w")
            tk.Label(bonus_inner, text=quest["bonus"], font=self.fs, fg=self.FG, bg="#0f0f18", wraplength=680, justify="left").pack(fill="x", pady=(3, 0))

            if completed and not bonus_done:
                tk.Button(
                    bonus_inner, text="★ CLAIM BONUS XP", font=self.fb,
                    bg="#1a1a10", fg="#ffcc00", bd=0, pady=5, cursor="hand2",
                    command=lambda: self._claim_bonus(quest),
                ).pack(fill="x", pady=(4, 0))
            elif bonus_done:
                tk.Label(bonus_inner, text="★ BONUS CLAIMED", font=self.fb, fg="#ffcc00", bg="#0a1a10", pady=5).pack(fill="x", pady=(4, 0))

    # -----------------------------------------------------------------------
    # PYTHON SANDBOX
    # -----------------------------------------------------------------------

    def _sandbox(self, starter_code):
        """Open a small code editor window that can execute Python locally."""
        win = tk.Toplevel(self.root)
        win.title("⚡ Python Sandbox")
        win.geometry("700x550")
        win.configure(bg=self.BG)
        win.transient(self.root)

        tk.Label(win, text="⚡ PYTHON SANDBOX", font=self.fh, fg="#ffcc00", bg=self.BG).pack(pady=(8, 3))

        # Code editor
        editor_frame = tk.Frame(win, bg=self.BGC, highlightbackground="#ffcc00", highlightthickness=1)
        editor_frame.pack(fill="both", expand=True, padx=10, pady=3)
        editor = tk.Text(
            editor_frame, font=tkfont.Font(family="Consolas", size=10),
            bg=self.BGC, fg="#00ff88", wrap="word", relief="flat",
            padx=10, pady=8, insertbackground="#ffcc00", height=12,
        )
        editor.pack(fill="both", expand=True)
        editor.insert("1.0", starter_code)

        # Output display
        tk.Label(win, text="OUTPUT:", font=self.fs, fg=self.FGD, bg=self.BG).pack(anchor="w", padx=10, pady=(3, 1))
        output_frame = tk.Frame(win, bg="#050508", highlightbackground=self.BRD, highlightthickness=1)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        output = tk.Text(
            output_frame, font=tkfont.Font(family="Consolas", size=10),
            bg="#050508", fg="#aaa", wrap="word", relief="flat",
            padx=10, pady=8, height=8, state="disabled",
        )
        output.pack(fill="both", expand=True)

        def run_code():
            code = editor.get("1.0", "end").strip()
            if not code:
                return

            output.configure(state="normal")
            output.delete("1.0", "end")

            try:
                # Write code to a temp file and execute it
                with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
                    tmp.write(code)
                    tmp_path = tmp.name

                result = subprocess.run(
                    [sys.executable, tmp_path],
                    capture_output=True, text=True, timeout=10,
                    input="Captain\n80\ntcp\n",  # Stdin for input() prompts
                )
                result_text = result.stdout
                if result.stderr:
                    result_text += f"\n--- ERRORS ---\n{result.stderr}"
                output.insert("1.0", result_text or "(No output)")

            except subprocess.TimeoutExpired:
                output.insert("1.0", "⚠️ Timed out (10s)")
            except Exception as err:
                output.insert("1.0", f"Error: {err}")
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

            output.configure(state="disabled")

        # Run / Close buttons
        btn_row = tk.Frame(win, bg=self.BG)
        btn_row.pack(fill="x", padx=10, pady=(0, 8))
        tk.Button(btn_row, text="▶ RUN",  font=self.fh, bg="#1a2a10", fg=self.ACC,  bd=0, padx=20, pady=6, cursor="hand2", command=run_code).pack(side="left", expand=True, fill="x", padx=(0, 3))
        tk.Button(btn_row, text="CLOSE",  font=self.fh, bg=self.BG2,  fg=self.FGD,  bd=0, padx=20, pady=6, cursor="hand2", command=win.destroy).pack(side="left", expand=True, fill="x", padx=(3, 0))

    # -----------------------------------------------------------------------
    # QUEST COMPLETION
    # -----------------------------------------------------------------------

    def _complete(self, quest):
        """Mark a quest as complete, save, and refresh the UI."""
        completed = self.save.get("completed_quests", [])
        if quest["id"] not in completed:
            completed.append(quest["id"])
            self.save["completed_quests"] = completed
            write_save(self.save)
            self._rank()
            self._detail(quest)
            messagebox.showinfo(
                "Quest Complete!",
                f"+{quest['xp']} XP!\nRank: {get_rank(total_xp(self.save))['title']}",
            )

    def _claim_bonus(self, quest):
        """Mark a bonus objective as claimed and award bonus XP."""
        bonus_list = self.save.get("bonus_completed", [])
        if quest["id"] not in bonus_list:
            bonus_list.append(quest["id"])
            self.save["bonus_completed"] = bonus_list
            write_save(self.save)
            self._rank()
            self._detail(quest)
            messagebox.showinfo("Bonus Claimed!", f"+{quest.get('bonus_xp', 0)} Bonus XP!")

    def _reset(self):
        """Wipe all progress after double confirmation."""
        if messagebox.askyesno("Reset", "ERASE all progress?"):
            if messagebox.askyesno("Confirm", "Really? No undo."):
                self.save = {
                    "completed_quests": [],
                    "bonus_completed":  [],
                    "exam_scores":      {},
                    "side_quests_done": [],
                    "seen_requirements": True,
                    "started": datetime.now().isoformat(),
                }
                write_save(self.save)
                self._rank()
                self.show_dashboard()
                messagebox.showinfo("Reset", "All progress erased. Fresh start!")

    # -----------------------------------------------------------------------
    # EXAMS TAB
    # -----------------------------------------------------------------------

    def show_exams(self):
        self._clear()
        self._tabs(2)

        tk.Label(self.sf, text="🧪 KNOWLEDGE EXAMS", font=self.fh, fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0, 3))
        tk.Label(self.sf, text="Score 70%+ to pass and earn XP. Retake anytime.", font=self.fs, fg=self.FGD, bg=self.BG).pack(anchor="w", pady=(0, 8))

        exams_done = self.save.get("side_quests_done", [])
        scores     = self.save.get("exam_scores", {})

        for exam in SIDE_QUESTS:
            passed  = exam["id"] in exams_done
            score   = scores.get(exam["id"])
            bg      = self.DON if passed else self.BG2

            card = tk.Frame(self.sf, bg=bg, highlightbackground=self.ACC if passed else self.BRD, highlightthickness=1, cursor="hand2")
            card.pack(fill="x", pady=2)

            inner = tk.Frame(card, bg=bg)
            inner.pack(fill="x", padx=10, pady=7)

            top = tk.Frame(inner, bg=bg)
            top.pack(fill="x")

            title_text = f"{'✓ ' if passed else ''}{exam['title']}"
            tk.Label(top, text=title_text, font=self.fb, fg=self.ACC if passed else self.FGB, bg=bg).pack(side="left")

            xp_text = f"+{exam['xp']} XP"
            if score is not None:
                xp_text += f"  (Best: {score}%)"
            tk.Label(top, text=xp_text, font=self.fb, fg="#ffcc00", bg=bg).pack(side="right")

            tk.Label(inner, text=f"{len(exam['questions'])} questions", font=self.fs, fg=self.FGD, bg=bg).pack(anchor="w")

            # Make the whole card clickable
            for widget in [card, inner, top] + list(inner.winfo_children()) + list(top.winfo_children()):
                widget.bind("<Button-1>", lambda e, ex=exam: self._start_exam(ex))

    def _start_exam(self, exam):
        """Render the exam question sheet."""
        self._clear()
        self._tabs(2)

        tk.Button(self.sf, text="← Back", font=self.fb, bg=self.BG, fg=self.ACC, bd=0, cursor="hand2", command=self.show_exams).pack(anchor="w", pady=(0, 6))
        tk.Label(self.sf, text=exam["title"], font=self.fh, fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0, 8))

        self.exam_vars = []  # Holds the IntVar for each question's radio selection

        for i, question in enumerate(exam["questions"]):
            q_frame = tk.Frame(self.sf, bg=self.BG2, highlightbackground=self.BRD, highlightthickness=1)
            q_frame.pack(fill="x", pady=2)

            q_inner = tk.Frame(q_frame, bg=self.BG2)
            q_inner.pack(fill="x", padx=10, pady=6)

            tk.Label(
                q_inner, text=f"Q{i+1}: {question['q']}",
                font=self.fb, fg=self.FGB, bg=self.BG2,
                anchor="w", wraplength=680, justify="left",
            ).pack(fill="x", pady=(0, 4))

            var = tk.IntVar(value=-1)  # -1 = nothing selected yet
            self.exam_vars.append(var)

            for j, option in enumerate(question["options"]):
                tk.Radiobutton(
                    q_inner, text=option, variable=var, value=j,
                    font=self.fn, bg=self.BG2, fg=self.FG,
                    selectcolor=self.BGH,
                    activebackground=self.BG2, activeforeground=self.ACC,
                    anchor="w",
                ).pack(fill="x", padx=8)

        tk.Button(
            self.sf, text="📝 SUBMIT", font=self.fh,
            bg="#1a1a10", fg="#ffcc00", bd=0, pady=8, cursor="hand2",
            command=lambda: self._submit_exam(exam),
        ).pack(fill="x", pady=(6, 0))

    def _submit_exam(self, exam):
        """Grade the exam, save the result, and show a pass/fail message."""
        questions = exam["questions"]
        correct   = sum(1 for i, q in enumerate(questions) if self.exam_vars[i].get() == q["answer"])
        score     = int((correct / len(questions)) * 100)
        passed    = score >= 70

        # Keep the player's best score
        prev_best = self.save.get("exam_scores", {}).get(exam["id"], 0)
        self.save.setdefault("exam_scores", {})[exam["id"]] = max(score, prev_best)

        if passed and exam["id"] not in self.save.get("side_quests_done", []):
            self.save.setdefault("side_quests_done", []).append(exam["id"])

        write_save(self.save)
        self._rank()

        if passed:
            messagebox.showinfo("Passed! 🎉", f"Score: {correct}/{len(questions)} ({score}%)\n+{exam['xp']} XP!")
        else:
            messagebox.showinfo("Not Yet",    f"Score: {correct}/{len(questions)} ({score}%)\nNeed 70% to pass.")

        self.show_exams()

    # -----------------------------------------------------------------------
    # ACHIEVEMENTS TAB
    # -----------------------------------------------------------------------

    def show_achievements(self):
        self._clear()
        self._tabs(3)

        achievements = get_achievements(self.save)
        earned_count = sum(1 for a in achievements if a["check"]())

        tk.Label(self.sf, text=f"{earned_count}/{len(achievements)} ACHIEVEMENTS", font=self.fh, fg=self.ACC, bg=self.BG).pack(pady=(0, 6))

        for achievement in achievements:
            earned = achievement["check"]()
            bg     = self.DON if earned else self.BG2

            card = tk.Frame(self.sf, bg=bg, highlightbackground=self.ACC if earned else self.BRD, highlightthickness=1)
            card.pack(fill="x", pady=2)

            inner = tk.Frame(card, bg=bg)
            inner.pack(fill="x", padx=10, pady=6)

            row = tk.Frame(inner, bg=bg)
            row.pack(fill="x")

            # Icon (locked if not earned)
            tk.Label(row, text=achievement["icon"] if earned else "🔒", font=self.fh, bg=bg).pack(side="left", padx=(0, 8))

            # Name and description
            info = tk.Frame(row, bg=bg)
            info.pack(side="left")
            tk.Label(info, text=achievement["name"], font=self.fb, fg=self.ACC if earned else self.FGD, bg=bg, anchor="w").pack(fill="x")
            tk.Label(info, text=achievement["desc"], font=self.fs, fg=self.FGD, bg=bg, anchor="w").pack(fill="x")

    # -----------------------------------------------------------------------
    # CAREERS TAB
    # -----------------------------------------------------------------------

    def show_careers(self):
        self._clear()
        self._tabs(4)

        tk.Label(self.sf, text="💼 CYBERSECURITY CAREER PATHS", font=self.fh, fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0, 3))
        tk.Label(self.sf, text="Where CyberQuest skills lead in the real world.", font=self.fs, fg=self.FGD, bg=self.BG).pack(anchor="w", pady=(0, 8))

        for career in CAREERS:
            card = tk.Frame(self.sf, bg=self.BG2, highlightbackground=self.BRD, highlightthickness=1)
            card.pack(fill="x", pady=3)

            inner = tk.Frame(card, bg=self.BG2)
            inner.pack(fill="x", padx=12, pady=8)

            top = tk.Frame(inner, bg=self.BG2)
            top.pack(fill="x")
            tk.Label(top, text=career["title"],  font=self.fb, fg=self.FGB, bg=self.BG2).pack(side="left")
            tk.Label(top, text=career["salary"], font=self.fb, fg=self.ACC, bg=self.BG2).pack(side="right")

            tk.Label(inner, text=career["desc"],            font=self.fs, fg=self.FG,  bg=self.BG2, wraplength=680, justify="left", anchor="w").pack(fill="x", pady=(4, 0))
            tk.Label(inner, text=f"Skills: {career['skills']}", font=self.fs, fg=self.FGD, bg=self.BG2, wraplength=680, justify="left", anchor="w").pack(fill="x", pady=(3, 0))
            tk.Label(inner, text=f"Certs:  {career['certs']}",  font=self.fs, fg="#ffcc00", bg=self.BG2, anchor="w").pack(fill="x", pady=(2, 0))

            tree_icons = " ".join(SKILL_TREES[t]["icon"] for t in career.get("trees", []) if t in SKILL_TREES)
            tk.Label(inner, text=f"Related skill trees: {tree_icons}", font=self.fs, fg=self.FGD, bg=self.BG2, anchor="w").pack(fill="x", pady=(2, 0))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    root = tk.Tk()

    # Try to enable dark window chrome on Windows (makes the title bar dark too)
    try:
        import ctypes
        root.update()
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            ctypes.windll.user32.GetParent(root.winfo_id()),
            20,
            ctypes.byref(ctypes.c_int(1)),
            ctypes.sizeof(ctypes.c_int),
        )
    except Exception:
        pass  # Not on Windows, or DWM not available — that's fine.

    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
