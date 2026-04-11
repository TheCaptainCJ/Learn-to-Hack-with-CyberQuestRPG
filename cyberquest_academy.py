"""
╔══════════════════════════════════════════════════════════════╗
║       CYBERQUEST ACADEMY — Ultimate Cybersecurity RPG       ║
║  Linux • Networking • Web Hacking • Crypto • Python • More  ║
║          Beginner to Advanced — Parrot OS Edition            ║
╚══════════════════════════════════════════════════════════════╝
Requirements: Python 3.8+ (standard library only)
Run: python cyberquest_academy.py
"""

import tkinter as tk
from tkinter import messagebox, font as tkfont
import json, os, subprocess, sys, tempfile
from pathlib import Path
from datetime import datetime

# ═══════════════════ SAVE SYSTEM ═══════════════════

SAVE_DIR = Path.home() / ".cyberquest"
SAVE_FILE = SAVE_DIR / "academy_save.json"

def load_save():
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"completed_quests":[],"bonus_completed":[],"exam_scores":{},"side_quests_done":[],"seen_requirements":False,"started":datetime.now().isoformat()}

def write_save(data):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ═══════════════════ REQUIREMENTS INFO ═══════════════════

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

# ═══════════════════ SKILL TREES ═══════════════════

SKILL_TREES = {
    "linux":      {"name": "Linux Mastery",         "icon": "🐧", "color": "#00ff88"},
    "networking": {"name": "Networking",             "icon": "🌐", "color": "#00ccff"},
    "crypto":     {"name": "Cryptography",           "icon": "🔐", "color": "#ffcc00"},
    "recon":      {"name": "Recon & OSINT",          "icon": "🔍", "color": "#ff9900"},
    "webhack":    {"name": "Web Hacking",            "icon": "🕸️", "color": "#ff2266"},
    "passwords":  {"name": "Password Attacks",       "icon": "🔑", "color": "#cc44ff"},
    "exploit":    {"name": "System Exploitation",    "icon": "⚡", "color": "#ff4444"},
    "defense":    {"name": "Defensive Security",     "icon": "🛡️", "color": "#4488ff"},
    "governance": {"name": "Frameworks & CVEs",      "icon": "📋", "color": "#44ddaa"},
    "tools":      {"name": "Tools & Automation",     "icon": "🦞", "color": "#ff8844"},
    "python":     {"name": "Python Scripting",       "icon": "🐍", "color": "#3776ab"},
}

RANKS = [
    {"level":1,"title":"Noob","xp":0},{"level":2,"title":"Script Kiddie","xp":100},
    {"level":3,"title":"Terminal Jockey","xp":250},{"level":4,"title":"Packet Sniffer","xp":450},
    {"level":5,"title":"Shell Popper","xp":750},{"level":6,"title":"Root Hunter","xp":1100},
    {"level":7,"title":"Exploit Dev","xp":1600},{"level":8,"title":"Zero-Day Scout","xp":2200},
    {"level":9,"title":"Shadow Operator","xp":3000},{"level":10,"title":"Ghost in the Wire","xp":4000},
    {"level":11,"title":"Cipher Lord","xp":5200},{"level":12,"title":"White Hat Legend","xp":6500},
]

# ═══════════════════ CAREER PROFILES ═══════════════════

CAREERS = [
    {"title": "SOC Analyst (Tier 1-3)", "salary": "$55K - $120K",
     "desc": "Monitor security alerts in a Security Operations Center. Analyze logs, triage incidents, and escalate threats. Entry-level cybersecurity role.",
     "skills": "SIEM (Splunk/ELK), log analysis, incident triage, networking basics, ticketing systems",
     "certs": "CompTIA Security+, CySA+, Splunk Core Certified User, BTL1",
     "trees": ["defense", "networking", "governance"]},
    {"title": "Penetration Tester", "salary": "$80K - $160K",
     "desc": "Ethically hack organizations to find vulnerabilities before real attackers do. Write reports with remediation advice.",
     "skills": "Nmap, Burp Suite, Metasploit, web app testing, network attacks, report writing",
     "certs": "OSCP (gold standard), CEH, PNPT, eJPT",
     "trees": ["recon", "webhack", "exploit", "passwords"]},
    {"title": "Incident Responder", "salary": "$85K - $150K",
     "desc": "Respond to active security breaches. Contain threats, investigate root cause, and restore systems.",
     "skills": "Digital forensics, malware analysis, log analysis, memory forensics, timeline analysis",
     "certs": "GCIH, GCFA, CySA+, BTL2",
     "trees": ["defense", "linux", "networking"]},
    {"title": "Security Engineer", "salary": "$100K - $180K",
     "desc": "Design, build, and maintain security infrastructure. Firewalls, IDS/IPS, SIEM, endpoint protection.",
     "skills": "Firewall config, IDS/IPS, cloud security, automation, scripting (Python/Bash)",
     "certs": "CISSP, AWS Security Specialty, CCSP, CompTIA Security+",
     "trees": ["defense", "networking", "python", "linux"]},
    {"title": "Threat Hunter", "salary": "$95K - $165K",
     "desc": "Proactively search for hidden threats that evade automated detection. Hypothesis-driven investigation.",
     "skills": "MITRE ATT&CK, behavioral analysis, SIEM queries, endpoint telemetry, threat intelligence",
     "certs": "GCTI, GCIA, OSTH, CySA+",
     "trees": ["defense", "networking", "recon"]},
    {"title": "Red Team Operator", "salary": "$110K - $190K",
     "desc": "Simulate advanced persistent threats (APTs). Full-scope adversary simulation including social engineering.",
     "skills": "Advanced exploitation, C2 frameworks, evasion, physical security, social engineering",
     "certs": "OSCP, OSEP, CRTO, GXPN",
     "trees": ["exploit", "recon", "webhack", "passwords"]},
    {"title": "GRC Analyst", "salary": "$70K - $130K",
     "desc": "Governance, Risk, and Compliance. Ensure organizations meet security standards and regulations.",
     "skills": "NIST CSF, ISO 27001, risk assessment, policy writing, audit management",
     "certs": "CISSP, CISA, CRISC, CompTIA Security+",
     "trees": ["governance"]},
    {"title": "AppSec Engineer", "salary": "$100K - $175K",
     "desc": "Secure software from design to deployment. Code review, SAST/DAST, threat modeling, DevSecOps.",
     "skills": "Secure coding, OWASP Top 10, CI/CD security, code review, threat modeling",
     "certs": "CSSLP, GWEB, OSWE",
     "trees": ["webhack", "python", "governance"]},
]

# ═══════════════════ ALL QUESTS ═══════════════════

ALL_QUESTS = [
    # ════════════ LINUX MASTERY ════════════
    {"id":"lx01","tree":"linux","tier":1,"xp":25,"title":"Terminal Awakening","brief":"Navigate the Linux filesystem",
     "hint":"Start with pwd to see where you are, then use ls -la and cd to explore. Pay special attention to /etc, /var/log, and /tmp.",
     "benefit":"Every cybersecurity job requires Linux command-line skills. SOC analysts read logs, pentesters navigate targets, sysadmins manage servers — all from the terminal.",
     "bonus":"Run: find /etc -name '*.conf' 2>/dev/null | head -20 — list 5 interesting config files in ~/linux_notes.txt","bonus_xp":10,
     "mission":"""═══ MISSION — Terminal Awakening ═══\n\nThe terminal is your cockpit. Every hacker lives here.\n\n► OBJECTIVES:\n\n  1. KNOW WHERE YOU ARE:\n     pwd                    # Print Working Directory\n     whoami                 # Who are you logged in as?\n     hostname               # What machine is this?\n\n  2. MOVE AROUND:\n     ls                     # List files\n     ls -la                 # ALL files with details\n     ls -lah                # Human-readable sizes\n     cd /home               # Change directory\n     cd ~                   # Your home directory\n     cd ..                  # Go up one level\n     cd -                   # Go back to previous\n\n  3. LINUX DIRECTORY STRUCTURE:\n     /           → Root of everything\n     /home       → User home directories\n     /root       → Root user's home (superuser)\n     /etc        → System config files (gold mine!)\n     /var        → Variable data (logs: /var/log)\n     /tmp        → Temp files (anyone can write here!)\n     /bin        → Essential commands\n     /sbin       → System admin commands\n     /usr        → User programs and data\n     /opt        → Third-party software\n     /dev        → Device files\n     /proc       → Process info (virtual filesystem)\n\n  4. EXPLORE:\n     ls /etc/              # Config files\n     ls /var/log/          # System logs\n     cat /etc/hostname     # Machine name\n     cat /etc/os-release   # OS version"""},
    {"id":"lx02","tree":"linux","tier":1,"xp":25,"title":"File Commander","brief":"Create, copy, move, search files",
     "hint":"grep is your best friend for searching inside files. find searches for filenames. Combine them with pipes (|) for power.",
     "benefit":"File manipulation and searching is used constantly in incident response (searching logs), forensics (finding evidence), and pentesting (finding credentials in configs).",
     "bonus":"Create a directory structure lab/scans lab/reports lab/wordlists with README.txt in each. List with ls -laR lab/","bonus_xp":10,
     "mission":"""═══ MISSION — File Commander ═══\n\n► OBJECTIVES:\n\n  1. CREATE:\n     touch notes.txt          # Create empty file\n     mkdir -p lab/targets/web  # Nested directories\n     echo \"target: 10.0.0.1\" > target.txt    # Write\n     echo \"port: 80\" >> target.txt            # Append\n\n  2. COPY, MOVE, RENAME:\n     cp target.txt backup.txt\n     cp -r lab/ lab_backup/\n     mv backup.txt old.txt       # Rename\n     mv old.txt /tmp/            # Move\n\n  3. DELETE:\n     rm target.txt               # Delete file\n     rm -r lab_backup/           # Delete directory\n     # ⚠️ NEVER: rm -rf /\n\n  4. VIEW:\n     cat target.txt              # Print file\n     head -5 /var/log/syslog     # First 5 lines\n     tail -20 /var/log/auth.log  # Last 20 lines\n     tail -f /var/log/syslog     # Follow real-time\n     less /etc/passwd            # Scrollable (q=quit)\n\n  5. SEARCH FOR FILES:\n     find / -name \"*.log\" 2>/dev/null\n     find / -perm -4000 2>/dev/null    # SUID files!\n\n  6. SEARCH INSIDE FILES:\n     grep \"Failed\" /var/log/auth.log\n     grep -r \"password\" /etc/ 2>/dev/null\n     grep -c \"Failed\" /var/log/auth.log  # Count"""},
    {"id":"lx03","tree":"linux","tier":1,"xp":30,"title":"Permission Enforcer","brief":"Understand permissions, SUID, ownership",
     "hint":"Remember: 4=read, 2=write, 1=execute. Add them up for each position (owner/group/others). SUID (4000) is a huge privesc vector — always check GTFOBins.",
     "benefit":"Permission misconfigurations are one of the top privilege escalation vectors. Every pentest report and security audit checks for these.",
     "bonus":"Find all SUID binaries, look up 3 on GTFOBins, document which are exploitable in ~/suid_audit.txt","bonus_xp":15,
     "mission":"""═══ MISSION — Permission Enforcer ═══\n\n► OBJECTIVES:\n\n  1. READ PERMISSIONS (ls -la output):\n     -rwxr-xr-- 1 captain users 4096 Jan 1 script.sh\n     │├─┤├─┤├─┤\n     │ │   │   └── Others: read only\n     │ │   └────── Group: read + execute\n     │ └────────── Owner: read + write + execute\n     └──────────── File type (- = file, d = dir)\n\n  2. CHANGE PERMISSIONS:\n     chmod 755 script.sh    # rwxr-xr-x\n     chmod 644 notes.txt    # rw-r--r--\n     chmod 600 secret.txt   # rw------- (owner only!)\n     chmod +x script.sh     # Add execute\n     # Numbers: 4=r, 2=w, 1=x → add up\n\n  3. OWNERSHIP:\n     sudo chown root:root secret.txt\n     sudo chown captain:users script.sh\n\n  4. SUID — Set User ID:\n     find / -perm -4000 -type f 2>/dev/null\n     # SUID runs as FILE OWNER (often root!)\n     # Vulnerable SUID = instant root\n\n  5. DANGEROUS PERMISSIONS:\n     find / -perm -o+w -type f 2>/dev/null | head -20\n     # World-writable = anyone can modify"""},
    {"id":"lx04","tree":"linux","tier":2,"xp":40,"title":"Process Assassin","brief":"Monitor processes, services, cron jobs",
     "hint":"Always check cron jobs (crontab -l, /etc/crontab, /etc/cron.d/) — if root runs a script you can write to, that's game over.",
     "benefit":"Understanding processes and services is critical for both incident response (what's running that shouldn't be?) and exploitation (what services are vulnerable?).",
     "bonus":"Audit all cron jobs on the system. Check permissions on every referenced script. Document in ~/cron_audit.txt","bonus_xp":15,
     "mission":"""═══ MISSION — Process Assassin ═══\n\n► OBJECTIVES:\n\n  1. VIEW PROCESSES:\n     ps aux                       # All processes\n     ps aux | grep ssh            # Find specific\n     top                          # Live monitor\n     htop                         # Better (sudo apt install htop)\n\n  2. KILL:\n     kill 1234                    # Graceful stop\n     kill -9 1234                 # Force kill\n     killall firefox              # By name\n\n  3. BACKGROUND:\n     python scan.py &             # Run in background\n     jobs                         # List bg jobs\n     fg %1                        # Bring to foreground\n     nohup python scan.py &       # Survives logout\n\n  4. SERVICES (systemd):\n     sudo systemctl status ssh\n     sudo systemctl start/stop/enable/disable ssh\n     sudo systemctl list-units --type=service\n\n  5. CRON JOBS:\n     crontab -l                   # Your cron jobs\n     sudo crontab -l              # Root's cron jobs\n     cat /etc/crontab             # System cron\n     ls /etc/cron.d/              # More cron configs\n     # Format: min hour day month weekday command"""},
    {"id":"lx05","tree":"linux","tier":2,"xp":40,"title":"User Overlord","brief":"Manage users, groups, sudo, /etc/shadow",
     "hint":"Always check sudo -l first for easy privesc. Look for NOPASSWD entries. Check /etc/passwd for unexpected UID 0 accounts.",
     "benefit":"User management knowledge is essential for system administration, incident response (finding rogue accounts), and privilege escalation during pentests.",
     "bonus":"Audit: UID 0 accounts, accounts with shells, empty passwords, sudo rules. Write ~/user_audit.txt","bonus_xp":15,
     "mission":"""═══ MISSION — User Overlord ═══\n\n► OBJECTIVES:\n\n  1. VIEW USERS:\n     cat /etc/passwd        # All accounts\n     sudo cat /etc/shadow   # Password hashes (root only)\n     id                     # Your info\n     who / w                # Who's logged in\n     last / lastb           # Login history / failures\n\n  2. /etc/passwd FORMAT:\n     captain:x:1000:1000:Captain:/home/captain:/bin/bash\n     # user:pass:UID:GID:comment:home:shell\n     # UID 0 = root (check for unexpected UID 0!)\n\n  3. /etc/shadow HASH TYPES:\n     $1$ = MD5 (weak)    $5$ = SHA-256\n     $6$ = SHA-512       $y$ = yescrypt (strongest)\n\n  4. MANAGE USERS:\n     sudo adduser testuser\n     sudo usermod -aG sudo testuser   # Add to sudo\n     sudo userdel -r testuser         # Delete + home\n\n  5. SUDO:\n     sudo -l                          # What can you sudo?\n     sudo visudo                      # Edit sudoers safely\n\n  6. CHECK FOR SUSPICIOUS:\n     awk -F: '$3 == 0 {print}' /etc/passwd  # UID 0 accounts\n     grep -v 'nologin' /etc/passwd          # Can login"""},
    {"id":"lx06","tree":"linux","tier":3,"xp":60,"title":"Shell Scripter","brief":"Automate with bash scripts",
     "hint":"Start every script with #!/bin/bash. Use variables with $, conditionals with [ ], and always chmod +x before running.",
     "benefit":"Automation is key in security — from automated scans to incident response playbooks. Every security role uses scripting daily.",
     "bonus":"Create a full system audit script: SUID, world-writable, UID 0, empty passwords, open ports, cron jobs. Save output with date stamp.","bonus_xp":20,
     "mission":"""═══ MISSION — Shell Scripter ═══\n\n► OBJECTIVES:\n\n  1. FIRST SCRIPT — save as ~/scan.sh:\n     #!/bin/bash\n     echo \"=== Quick Scanner ===\"\n     TARGET=$1\n     if [ -z \"$TARGET\" ]; then\n         echo \"Usage: ./scan.sh <ip>\"\n         exit 1\n     fi\n     for port in 21 22 80 443 8080; do\n         (echo >/dev/tcp/$TARGET/$port) 2>/dev/null && \\\n             echo \"  Port $port: OPEN\" || \\\n             echo \"  Port $port: closed\"\n     done\n\n  2. RUN IT:\n     chmod +x ~/scan.sh\n     ./scan.sh 127.0.0.1\n\n  3. LOOPS:\n     for ip in 192.168.1.{1..10}; do\n         ping -c 1 -W 1 $ip &>/dev/null && echo \"$ip UP\"\n     done\n\n  4. READING FILES:\n     while IFS= read -r line; do\n         echo \"Processing: $line\"\n     done < targets.txt\n\n  5. FUNCTIONS:\n     check_port() {\n         (echo >/dev/tcp/$1/$2) 2>/dev/null\n         return $?\n     }\n     if check_port 127.0.0.1 22; then\n         echo \"SSH running\"\n     fi"""},

    # ════════════ NETWORKING ════════════
    {"id":"net01","tree":"networking","tier":1,"xp":25,"title":"Network Foundations","brief":"IPs, subnets, OSI model, ports",
     "hint":"Memorize the OSI model with 'All People Seem To Need Data Processing' and the top 20 port numbers. These come up in every interview.",
     "benefit":"Networking is the backbone of ALL cybersecurity. You cannot defend or attack what you don't understand. Every cert exam tests networking heavily.",
     "bonus":"Write the OSI model with real examples at each layer. Memorize the top 20 ports. Document in ~/network_notes.txt","bonus_xp":10,
     "mission":"""═══ MISSION — Network Foundations ═══\n\n► THE OSI MODEL:\n  7 Application   → HTTP, FTP, SSH, DNS\n  6 Presentation  → SSL/TLS, encryption\n  5 Session       → Connection management\n  4 Transport     → TCP (reliable), UDP (fast)\n  3 Network       → IP addresses, routing\n  2 Data Link     → MAC addresses, switches\n  1 Physical      → Cables, wireless\n  Memory: \"All People Seem To Need Data Processing\"\n\n► IP ADDRESSES:\n  ip a                    # Your IPs\n  Private ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x\n  /24 = 256 addresses, /16 = 65,536\n\n► TCP vs UDP:\n  TCP: SYN→SYN-ACK→ACK (reliable, ordered)\n  UDP: fire-and-forget (fast, no guarantee)\n\n► KEY PORTS (memorize!):\n  21 FTP    22 SSH    23 Telnet   25 SMTP\n  53 DNS    80 HTTP   110 POP3    143 IMAP\n  443 HTTPS  445 SMB   3306 MySQL  3389 RDP\n\n► COMMANDS:\n  ip a / ip route / ping / traceroute\n  nslookup / dig / ss -tulnp"""},
    {"id":"net02","tree":"networking","tier":1,"xp":30,"title":"Packet Hunter","brief":"Capture and analyze network traffic",
     "hint":"Use tcpdump -A to see ASCII content — you can literally read unencrypted HTTP traffic. Wireshark's display filters are your best friend.",
     "benefit":"Packet analysis is used in forensics, incident response, IDS tuning, and network troubleshooting. PCAP files are evidence in investigations.",
     "bonus":"Capture 100 packets, open in Wireshark, find: DNS query, TCP handshake, any unencrypted data. Document in ~/packet_analysis.txt","bonus_xp":15,
     "mission":"""═══ MISSION — Packet Hunter ═══\n\n► TCPDUMP:\n  sudo tcpdump -i eth0 -c 20              # 20 packets\n  sudo tcpdump -i eth0 port 80            # HTTP only\n  sudo tcpdump -i eth0 -w capture.pcap    # Save\n  sudo tcpdump -i eth0 -A port 80         # ASCII content\n\n► READ OUTPUT:\n  12:34:56 IP 192.168.1.100.45678 > 93.184.216.34.80: Flags [S]\n  # Flags: [S]=SYN [S.]=SYN-ACK [.]=ACK [P.]=PUSH [F.]=FIN\n\n► WIRESHARK:\n  wireshark &\n  # Filters: tcp.port==80, ip.addr==192.168.1.1, http.request, dns\n\n► ARP:\n  arp -a                    # IP↔MAC mappings\n  ip neigh                  # ARP table\n\n► PROTOCOLS:\n  DHCP (67/68): Auto-assigns IPs to devices\n  ICMP: Ping and traceroute (no port number)\n  SNMP (161): Network device management\n  LDAP (389): Directory services (Active Directory)\n  SMB (445): Windows file sharing\n  RDP (3389): Remote desktop"""},
    {"id":"net03","tree":"networking","tier":2,"xp":45,"title":"Nmap Ninja","brief":"Master the network scanner",
     "hint":"Start with nmap -sn for discovery, then -sV -sC for detailed scanning. Use -oA to save in all formats. -T timing controls stealth.",
     "benefit":"Nmap is THE most used tool in pentesting. It's the first tool you run in any engagement and appears in every pentest methodology.",
     "bonus":"Full scan of localhost: nmap -sV -sC -O -oA ~/my_scan localhost — identify every service in all 3 output files.","bonus_xp":15,
     "mission":"""═══ MISSION — Nmap Ninja ═══\n\n⚠️ Only scan machines YOU own.\n\n► DISCOVERY:\n  nmap -sn 192.168.1.0/24       # Ping sweep\n\n► PORT SCANNING:\n  nmap TARGET                    # Top 1000 ports\n  nmap -p- TARGET                # ALL 65535 ports\n  nmap -p 22,80,443 TARGET       # Specific ports\n\n► SCAN TYPES:\n  -sS  SYN stealth (default)     -sT  TCP connect\n  -sU  UDP scan                  -sV  Version detection\n  -O   OS detection              -A   Aggressive (all)\n\n► NSE SCRIPTS:\n  nmap --script=default TARGET\n  nmap --script=vuln TARGET\n  nmap --script=http-enum TARGET\n  ls /usr/share/nmap/scripts/    # Browse scripts\n\n► OUTPUT:\n  -oN file.txt    Normal\n  -oX file.xml    XML\n  -oA prefix       All formats\n\n► STEALTH:\n  -T0 Paranoid  -T1 Sneaky  -T3 Normal  -T5 Insane\n  -f Fragment packets  -D RND:5 Decoys"""},
    {"id":"net04","tree":"networking","tier":3,"xp":55,"title":"DNS Deep Dive","brief":"DNS recon and enumeration",
     "hint":"Always check for zone transfers (dig axfr) — misconfigured DNS servers will give you the entire zone. Check TXT records for SPF/DKIM/DMARC.",
     "benefit":"DNS reconnaissance reveals network structure, mail servers, and subdomains — all without touching the target directly. Essential OSINT skill.",
     "bonus":"Full DNS recon on a domain you own: A, MX, NS, TXT records, zone transfer attempt, SPF/DMARC check. Document in ~/dns_recon.txt","bonus_xp":15,
     "mission":"""═══ MISSION — DNS Deep Dive ═══\n\n► DNS LOOKUPS:\n  dig example.com ANY\n  dig example.com MX / NS / TXT\n  dig -x 93.184.216.34           # Reverse lookup\n  nslookup / host example.com\n\n► RECORD TYPES:\n  A=IPv4  AAAA=IPv6  MX=Mail  NS=Nameserver\n  TXT=Text  CNAME=Alias  PTR=Reverse  SOA=Zone info\n\n► ENUMERATION:\n  dnsrecon -d example.com -t std\n  dnsenum example.com\n  fierce --domain example.com\n  dig axfr @ns1.example.com example.com  # Zone transfer\n\n► EMAIL SECURITY:\n  dig example.com TXT | grep spf\n  dig _dmarc.example.com TXT"""},

    # ════════════ CRYPTOGRAPHY ════════════
    {"id":"cr01","tree":"crypto","tier":1,"xp":25,"title":"CIA & Crypto Basics","brief":"CIA Triad, hashing, encryption fundamentals",
     "hint":"Remember: Encoding is NOT encryption (Base64 is trivially decoded). Hashing is one-way (can't reverse). Encryption is two-way (needs a key).",
     "benefit":"The CIA Triad is asked about in EVERY security interview. Understanding crypto lets you evaluate whether a system is truly secure or just looks secure.",
     "bonus":"Hash a file with SHA256, modify one byte, hash again — compare. Encrypt/decrypt with openssl. Document in ~/crypto_lab.txt","bonus_xp":10,
     "mission":"""═══ MISSION — CIA & Crypto Basics ═══\n\n► THE CIA TRIAD:\n  C — CONFIDENTIALITY: Only authorized access\n    → Encryption, access controls, MFA\n  I — INTEGRITY: Data hasn't been tampered with\n    → Hashing, digital signatures, checksums\n  A — AVAILABILITY: Systems accessible when needed\n    → Redundancy, backups, DDoS protection\n\n► HASHING (one-way):\n  echo -n \"password123\" | md5sum\n  echo -n \"password123\" | sha256sum\n  sha256sum /usr/bin/ls    # File integrity\n\n► ENCODING vs ENCRYPTION vs HASHING:\n  Encoding: echo -n \"hello\" | base64 → NOT secure\n  Hashing: one-way, can't reverse\n  Encryption: two-way with a key\n\n► SYMMETRIC: same key both ways (AES, ChaCha20)\n  ASYMMETRIC: public + private key pair (RSA, ECC)\n\n► TRY IT:\n  openssl genrsa -out private.pem 2048\n  openssl rsa -in private.pem -pubout -out public.pem\n  echo \"SECRET\" > msg.txt\n  openssl rsautl -encrypt -pubin -inkey public.pem -in msg.txt -out msg.enc\n  openssl rsautl -decrypt -inkey private.pem -in msg.enc"""},
    {"id":"cr02","tree":"crypto","tier":2,"xp":40,"title":"Hash Cracking Lab","brief":"Attack and defend password hashes",
     "hint":"Start with John + rockyou.txt for quick wins. Use --rules for mutations. hashcat is faster on GPUs. Always use strong, salted hashes for defense.",
     "benefit":"Understanding hash cracking lets you set effective password policies and assess the real strength of your organization's credentials.",
     "bonus":"Create 5 test accounts with different password strengths. Crack with John. Document which fell and how long each took.","bonus_xp":15,
     "mission":"""═══ MISSION — Hash Cracking Lab ═══\n\n⚠️ Only crack YOUR OWN hashes.\n\n► HASH TYPES:\n  $1$=MD5crypt $5$=SHA-256 $6$=SHA-512 $y$=yescrypt $2b$=bcrypt\n\n► WORDLISTS:\n  ls /usr/share/wordlists/\n  sudo gunzip /usr/share/wordlists/rockyou.txt.gz\n  wc -l /usr/share/wordlists/rockyou.txt  # ~14M passwords!\n\n► JOHN THE RIPPER:\n  sudo unshadow /etc/passwd /etc/shadow > hashes.txt\n  john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt\n  john --show hashes.txt\n\n► HASHCAT:\n  hashcat -m 1800 -a 0 hash.txt rockyou.txt\n  # -m 0=MD5 -m 1000=NTLM -m 1800=SHA-512crypt\n  # -a 0=dictionary -a 3=brute force\n\n► DEFEND:\n  Use bcrypt/argon2, 16+ char passwords, per-user salts,\n  account lockout, MFA"""},

    # ════════════ RECON & OSINT ════════════
    {"id":"rc01","tree":"recon","tier":1,"xp":25,"title":"Self Scanner","brief":"See yourself through an attacker's eyes",
     "hint":"Run ss -tulnp to see every listening service. For each one, ask: do I need this? Is it updated? Is it exposed to the network?",
     "benefit":"Self-assessment is the first step in hardening. You can't defend what you don't know exists. This is also the first thing pentesters do on a compromised host.",
     "bonus":"List every open port, identify each service, rate risk (low/medium/high). Save to ~/self_assessment.txt","bonus_xp":10,
     "mission":"""═══ MISSION — Self Scanner ═══\n\n► OBJECTIVES:\n  ip a                     # Your IPs\n  ss -tulnp                # Open ports + processes\n  nmap -sV localhost        # Service versions\n  nmap -sV -sC localhost    # With default scripts\n  curl ifconfig.me          # Your public IP\n\n► FOR EACH PORT ASK:\n  - Do I need this service?\n  - Is it up to date?\n  - Is it configured securely?\n  - Is it exposed to the internet?\n\n► DOCUMENT:\n  echo \"=== Self-Scan ==\" > ~/self_scan.txt\n  date >> ~/self_scan.txt\n  ss -tulnp >> ~/self_scan.txt"""},
    {"id":"rc02","tree":"recon","tier":2,"xp":45,"title":"OSINT Operator","brief":"Gather intel from public sources",
     "hint":"Start with whois and dig for passive recon. theHarvester automates email/subdomain discovery. Google dorking is surprisingly powerful.",
     "benefit":"OSINT is legal, passive, and devastatingly effective. Professional pentest teams spend days on OSINT before touching a keyboard.",
     "bonus":"Full OSINT assessment on a domain you own: DNS, WHOIS, emails, subdomains, technology. Create ~/osint_report.txt","bonus_xp":15,
     "mission":"""═══ MISSION — OSINT Operator ═══\n\n⚠️ Use a domain YOU own or have permission for.\n\n► DNS: whois, dig ANY, dnsrecon\n► EMAILS: theHarvester -d example.com -l 100 -b all\n► SUBDOMAINS: fierce --domain example.com\n► WEB TECH: whatweb, curl -I\n\n► GOOGLE DORKING:\n  site:example.com\n  filetype:pdf site:example.com\n  intitle:\"index of\" site:example.com\n  inurl:admin site:example.com\n\n► TOOLS ON PARROT:\n  recon-ng, maltego, spiderfoot"""},

    # ════════════ WEB HACKING ════════════
    {"id":"web01","tree":"webhack","tier":1,"xp":25,"title":"Web Recon","brief":"Enumerate web servers and hidden content",
     "hint":"Always check robots.txt first — it tells search engines what to hide, which means it shows YOU what's interesting. Try gobuster with common.txt.",
     "benefit":"Web application security is the largest attack surface for most organizations. Web recon is the first phase of any web app pentest.",
     "bonus":"Set up DVWA in your lab. Run full web recon against it. Document in ~/web_recon.txt","bonus_xp":15,
     "mission":"""═══ MISSION — Web Recon ═══\n\n⚠️ Only scan YOUR targets (set up DVWA/Juice Shop).\n\n► HTTP BASICS:\n  curl http://target / curl -I / curl -v\n\n► DIRECTORY ENUMERATION:\n  gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt\n  dirb http://target\n\n► CHECK:\n  curl http://target/robots.txt    # Hidden paths!\n  curl http://target/sitemap.xml\n  # Look for: /.git/ /admin/ /backup/ /wp-admin/\n\n► FINGERPRINTING:\n  whatweb http://target\n  curl -I http://target | grep -i server\n\n► SSL/TLS:\n  echo | openssl s_client -connect target:443 2>/dev/null | openssl x509 -text"""},
    {"id":"web02","tree":"webhack","tier":2,"xp":50,"title":"Injection Master","brief":"SQL injection, XSS, OWASP Top 10",
     "hint":"For SQLi, try adding a single quote (') to inputs and see if you get a database error. For XSS, try <script>alert(1)</script> in input fields.",
     "benefit":"Injection flaws are consistently the most dangerous web vulnerabilities. Understanding them is required for any web security role.",
     "bonus":"In DVWA (low security): perform SQLi to extract users, reflected XSS, stored XSS. Document attacks AND fixes in ~/injection_lab.txt","bonus_xp":20,
     "mission":"""═══ MISSION — Injection Master ═══\n\n⚠️ ONLY on YOUR lab targets (DVWA, Juice Shop).\n\n► SQL INJECTION:\n  Normal: SELECT * FROM users WHERE id = '1'\n  Injected: SELECT * FROM users WHERE id = '1' OR '1'='1'\n  Login bypass: admin' -- (comments out password check)\n\n► SQLMAP:\n  sqlmap -u \"http://target/page?id=1\" --batch\n  sqlmap -u \"URL\" --dbs / --tables / --dump\n\n► XSS:\n  <script>alert('XSS')</script>\n  <img src=x onerror=alert('XSS')>\n\n► OWASP TOP 10:\n  A01: Broken Access Control\n  A02: Cryptographic Failures\n  A03: Injection\n  A04: Insecure Design\n  A05: Security Misconfiguration\n  A06: Vulnerable Components\n  A07: Auth Failures\n  A08: Data Integrity Failures\n  A09: Logging Failures\n  A10: SSRF\n\n► DEFENSE: parameterized queries, input validation,\n  output encoding, CSP headers"""},
    {"id":"web03","tree":"webhack","tier":3,"xp":60,"title":"Burp Suite Operator","brief":"Intercept and modify web traffic",
     "hint":"Send interesting requests to Repeater first to test manually. Use Intruder for automated attacks. Always check cookies and hidden form fields.",
     "benefit":"Burp Suite is the industry standard for web app testing. Every professional pentester uses it daily. It's required knowledge for OSCP and most web security certs.",
     "bonus":"In Burp against DVWA: intercept login, modify in Repeater, brute force with Intruder. Document in ~/burp_lab.txt","bonus_xp":20,
     "mission":"""═══ MISSION — Burp Suite Operator ═══\n\n► SETUP:\n  burpsuite &\n  Browser proxy: 127.0.0.1:8080\n\n► PROXY: Intercept requests, inspect/modify, forward/drop\n► REPEATER: Right-click → Send to Repeater, modify & resend\n► INTRUDER: Automated attacks with wordlists\n  Attack types: Sniper, Battering Ram, Pitchfork, Cluster Bomb\n► DECODER: URL encode, Base64, HTML entities"""},

    # ════════════ PASSWORD ATTACKS ════════════
    {"id":"pw01","tree":"passwords","tier":1,"xp":25,"title":"Password Theory","brief":"How passwords are stored and attacked",
     "hint":"Explore /usr/share/wordlists/ on Parrot. rockyou.txt has 14M real passwords. CeWL creates custom wordlists from websites.",
     "benefit":"Weak passwords are the #1 way attackers get in. Understanding attack methods lets you build policies that actually work.",
     "bonus":"Generate 3 custom wordlists: CeWL from a website, crunch for 6-digit PINs, manual list of 20 common passwords. Save to ~/wordlists/","bonus_xp":10,
     "mission":"""═══ MISSION — Password Theory ═══\n\n► HOW LINUX STORES PASSWORDS:\n  /etc/passwd  → user info (readable)\n  /etc/shadow  → hashes (root only)\n  Format: user:$type$salt$hash:...\n\n► ATTACK TYPES:\n  Dictionary: try wordlist      Brute force: all combos\n  Rule-based: mutations         Rainbow tables: precomputed\n  Credential stuffing: reuse leaked creds\n\n► WORDLISTS ON PARROT:\n  ls /usr/share/wordlists/\n  rockyou.txt → 14M real passwords\n  /usr/share/wordlists/dirb/ → directory busting\n\n► CUSTOM WORDLISTS:\n  cewl http://target -w custom.txt    # From website\n  crunch 6 8 0123456789 -o pins.txt   # Generate patterns\n\n► DEFENSE:\n  16+ chars, passphrase, password manager, MFA, lockout"""},
    {"id":"pw02","tree":"passwords","tier":2,"xp":45,"title":"Crack & Defend","brief":"Crack with Hydra/John, defend with fail2ban",
     "hint":"Always set up fail2ban BEFORE running attack tools. Test the full cycle: attack → detect → block → verify the block worked.",
     "benefit":"Understanding both sides (attack AND defense) makes you vastly more effective. This dual perspective is what separates good security pros from great ones.",
     "bonus":"Set up fail2ban, run Hydra against your own SSH, verify the ban in logs. Document attack AND defense in ~/password_defense.txt","bonus_xp":15,
     "mission":"""═══ MISSION — Crack & Defend ═══\n\n⚠️ Only attack YOUR OWN systems.\n\n► OFFLINE — JOHN:\n  sudo unshadow /etc/passwd /etc/shadow > hashes.txt\n  john --wordlist=rockyou.txt hashes.txt\n  john --show hashes.txt\n\n► ONLINE — HYDRA:\n  hydra -l user -P rockyou.txt ssh://127.0.0.1 -t 4\n  hydra -l admin -P wordlist.txt http-post-form \"/login:user=^USER^&pass=^PASS^:Invalid\"\n\n► DEFEND — FAIL2BAN:\n  sudo apt install fail2ban\n  sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local\n  # Set: bantime=3600, maxretry=3\n  sudo systemctl enable --now fail2ban\n  sudo fail2ban-client status sshd"""},

    # ════════════ EXPLOITATION ════════════
    {"id":"ex01","tree":"exploit","tier":2,"xp":45,"title":"Metasploit Academy","brief":"Learn the exploitation framework",
     "hint":"Start with auxiliary modules (scanners) before exploit modules. Always 'show options' to see what needs configuring. 'search' is your friend.",
     "benefit":"Metasploit is the industry standard. Understanding it helps both offensive (pentesting) and defensive (writing detection rules for known exploits) roles.",
     "bonus":"Set up Metasploitable 2 in Hyper-V. Scan with nmap, exploit one vulnerability with Metasploit. Document full chain in ~/msf_lab.txt","bonus_xp":20,
     "mission":"""═══ MISSION — Metasploit Academy ═══\n\n⚠️ ONLY use against machines YOU own.\n\n► START:\n  sudo msfdb init && msfconsole\n\n► NAVIGATE:\n  search type:exploit platform:linux\n  use exploit/unix/ftp/vsftpd_234_backdoor\n  show options → set RHOSTS → run\n\n► KEY CONCEPTS:\n  Exploit = attack code    Payload = post-exploit code\n  Meterpreter = advanced shell    Auxiliary = scanning\n\n► METERPRETER:\n  sysinfo, getuid, pwd, ls, download, upload\n  shell (drop to system), hashdump, bg\n\n► AUXILIARIES:\n  auxiliary/scanner/portscan/tcp\n  auxiliary/scanner/smb/smb_version\n  auxiliary/scanner/ssh/ssh_login"""},
    {"id":"ex02","tree":"exploit","tier":3,"xp":60,"title":"Privilege Escalation","brief":"Go from user to root",
     "hint":"Run sudo -l FIRST — it's the quickest win. Then check SUID, writable cron scripts, and kernel version. LinPEAS automates the enumeration.",
     "benefit":"Privesc is a core pentest skill. Even in defensive roles, understanding how attackers escalate helps you harden systems and detect escalation attempts.",
     "bonus":"Run linpeas.sh on your Parrot box. Fix at least 2 issues. Document before/after in ~/privesc_audit.txt","bonus_xp":20,
     "mission":"""═══ MISSION — Privilege Escalation ═══\n\n⚠️ Practice on YOUR machines only.\n\n► CHECKLIST:\n  whoami && id\n  sudo -l                              # Easy wins!\n  uname -a                             # Kernel exploits\n  find / -perm -4000 2>/dev/null       # SUID\n  cat /etc/crontab && ls /etc/cron.d/  # Cron jobs\n  find /etc -writable 2>/dev/null      # Writable configs\n\n► AUTOMATED:\n  # LinPEAS:\n  curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh\n  chmod +x linpeas.sh && ./linpeas.sh\n\n► COMMON VECTORS:\n  a) sudo vim -c '!bash'  (if sudo allows vim)\n  b) SUID find: find . -exec /bin/bash -p \\;\n  c) Writable cron scripts\n  d) Writable /etc/passwd\n  → Check EVERY binary on GTFOBins.github.io"""},

    # ════════════ DEFENSIVE SECURITY ════════════
    {"id":"def01","tree":"defense","tier":1,"xp":30,"title":"Firewall Fortress","brief":"Configure UFW and iptables",
     "hint":"Start with deny all incoming, allow all outgoing. Then selectively open only what you need. Always verify with nmap from another machine.",
     "benefit":"Firewall configuration is a fundamental skill for any security role. It's the first line of defense and a core part of system hardening.",
     "bonus":"Configure UFW: allow SSH from subnet only, HTTP/HTTPS from anywhere, deny all else. Verify with nmap. Document in ~/firewall_config.txt","bonus_xp":10,
     "mission":"""═══ MISSION — Firewall Fortress ═══\n\n► UFW:\n  sudo ufw default deny incoming\n  sudo ufw default allow outgoing\n  sudo ufw enable\n  sudo ufw allow 22/tcp\n  sudo ufw allow 80,443/tcp\n  sudo ufw deny 23/tcp\n  sudo ufw status numbered\n\n► IPTABLES (advanced):\n  sudo iptables -L -v -n\n  sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n  sudo iptables -A INPUT -j DROP\n\n► VERIFY:\n  nmap YOUR_IP (from another machine)\n  sudo tail -f /var/log/ufw.log"""},
    {"id":"def02","tree":"defense","tier":2,"xp":50,"title":"IDS Guardian","brief":"Deploy Suricata intrusion detection",
     "hint":"Set HOME_NET to your lab subnet in suricata.yaml. Use suricata-update to get the latest rules. Watch fast.log for real-time alerts.",
     "benefit":"IDS/IPS deployment and tuning is a core security engineering skill. SOC analysts work with IDS alerts daily. Understanding rules helps write better detections.",
     "bonus":"Write 3 custom Suricata rules (port scan, SSH brute force, suspicious HTTP). Test each. Document in ~/ids_rules.txt","bonus_xp":20,
     "mission":"""═══ MISSION — IDS Guardian ═══\n\n► INSTALL & CONFIGURE:\n  sudo apt install suricata\n  sudo nano /etc/suricata/suricata.yaml\n  # Set HOME_NET, interface\n  sudo suricata-update\n\n► RUN:\n  sudo suricata -c /etc/suricata/suricata.yaml -i eth0\n  sudo tail -f /var/log/suricata/fast.log\n\n► TRIGGER ALERTS (from another machine):\n  nmap -sV YOUR_IP\n  curl \"http://YOUR_IP/../../etc/passwd\"\n\n► CUSTOM RULES:\n  # /var/lib/suricata/rules/local.rules\n  alert tcp any any -> $HOME_NET 22 (msg:\"SSH brute\";\n    threshold:type both,track by_src,count 5,seconds 60;\n    sid:1000001; rev:1;)"""},
    {"id":"def03","tree":"defense","tier":3,"xp":60,"title":"Hardening Master","brief":"Full system hardening — kernel, SSH, services",
     "hint":"Apply sysctl hardening, lock down SSH (disable root login, use keys, change port), minimize services, set up AIDE for file integrity.",
     "benefit":"System hardening is required for compliance (CIS Benchmarks, NIST). Security engineers spend significant time on hardening and auditing systems.",
     "bonus":"Apply ALL hardening steps. Run linpeas.sh again and compare to first run. Document improvements in ~/hardening_report.txt","bonus_xp":20,
     "mission":"""═══ MISSION — Hardening Master ═══\n\n► KERNEL (sysctl):\n  net.ipv4.ip_forward = 0\n  net.ipv4.tcp_syncookies = 1\n  net.ipv4.conf.all.rp_filter = 1\n  kernel.randomize_va_space = 2\n  kernel.dmesg_restrict = 1\n  → sudo sysctl -p\n\n► SSH:\n  PermitRootLogin no\n  PasswordAuthentication no\n  MaxAuthTries 3\n  Port 2222\n\n► SERVICES:\n  sudo systemctl list-units --type=service --state=running\n  Disable what you don't need\n\n► FILE INTEGRITY:\n  sudo apt install aide && sudo aideinit\n  sudo aide --check\n\n► AUDIT LOGGING:\n  sudo apt install auditd\n  sudo auditctl -w /etc/shadow -p wa -k shadow_changes"""},

    # ════════════ FRAMEWORKS & CVEs ════════════
    {"id":"gov01","tree":"governance","tier":1,"xp":25,"title":"NIST & CVE Basics","brief":"Security frameworks every pro must know",
     "hint":"Memorize the 5 NIST CSF functions: Identify, Protect, Detect, Respond, Recover. Know how to read a CVE entry and CVSS score.",
     "benefit":"Every security job references these frameworks. SOC analysts map to MITRE ATT&CK, auditors use NIST CSF, pentesters cite OWASP Top 10.",
     "bonus":"Map your lab to NIST CSF: for each function, list what you've done and what gaps remain. Save to ~/nist_assessment.txt","bonus_xp":10,
     "mission":"""═══ MISSION — NIST & CVE Basics ═══\n\n► NIST CSF (5 functions):\n  IDENTIFY  — What do we protect?\n  PROTECT   — How do we prevent attacks?\n  DETECT    — How do we catch attacks?\n  RESPOND   — What do we do when attacked?\n  RECOVER   — How do we get back to normal?\n\n► CVE (Common Vulnerabilities and Exposures):\n  Format: CVE-YYYY-NNNNN\n  Example: CVE-2021-44228 (Log4Shell)\n  Search: https://nvd.nist.gov\n\n► CVSS SCORES:\n  0.0 None  0.1-3.9 Low  4.0-6.9 Medium\n  7.0-8.9 High  9.0-10.0 Critical\n\n► OTHER FRAMEWORKS:\n  MITRE ATT&CK — Attacker technique catalog\n  OWASP Top 10 — Web vulnerabilities\n  CIS Benchmarks — Hardening guides\n  ISO 27001 — Security management standard"""},
    {"id":"gov02","tree":"governance","tier":2,"xp":40,"title":"CVE Hunter","brief":"Find, read, and assess vulnerabilities",
     "hint":"Use searchsploit to find exploits for specific software versions. Prioritize CVEs by: CVSS score, exploit availability, exposure, asset value.",
     "benefit":"Vulnerability management is a core security function. Understanding how to find, assess, and prioritize CVEs is essential for any security role.",
     "bonus":"Scan with nmap --script vuln. Look up each CVE, check CVSS, determine if affected. Write ~/vuln_report.txt","bonus_xp":15,
     "mission":"""═══ MISSION — CVE Hunter ═══\n\n► FIND CVEs:\n  dpkg -l | head -30              # What's installed?\n  apt show openssh-server          # Check versions\n  searchsploit openssh             # Find exploits\n  searchsploit apache 2.4\n  nmap --script vuln TARGET\n  nikto -h http://TARGET\n\n► READ A CVE:\n  CVE ID, Description, CVSS, Affected versions,\n  References (patches, exploits), CWE category\n\n► PRIORITIZE:\n  1. CVSS severity  2. Public exploit exists?\n  3. Internet-facing?  4. Asset criticality\n\n► PATCH:\n  sudo apt update && apt list --upgradable\n  sudo apt upgrade"""},

    # ════════════ TOOLS & AUTOMATION ════════════
    {"id":"tl01","tree":"tools","tier":1,"xp":35,"title":"Twingate VPN Setup","brief":"Zero-trust VPN for your lab",
     "hint":"Install with the one-liner curl script. Configure with 'sudo twingate setup'. Start WITHOUT sudo for desktop auth notifications.",
     "benefit":"Zero-trust networking is replacing traditional VPNs across the industry. Understanding it makes you valuable for both network security and DevOps roles.",
     "bonus":"Run twingate report and compare open ports before/after with ss -tulnp. Document differences in ~/vpn_audit.txt","bonus_xp":10,
     "mission":"""═══ MISSION — Twingate VPN Setup ═══\n\n► CONCEPTS:\n  Traditional VPN: encrypted tunnel, broad access once connected\n  Zero Trust (Twingate): every request verified, per-resource access\n\n► INSTALL:\n  1. Sign up: https://www.twingate.com\n  2. Install: curl -s https://binaries.twingate.com/client/linux/install.sh | sudo bash\n  3. Configure: sudo twingate setup\n  4. Start: twingate start (no sudo!)\n  5. Verify: twingate status\n\n► SET UP CONNECTOR:\n  1. Create Remote Network in admin console\n  2. Deploy Connector (Docker/Linux script)\n  3. Define Resources (your lab VMs)\n  4. Test access through Twingate\n\n► WHY ZERO TRUST:\n  Connectors only make OUTBOUND connections.\n  No inbound ports to scan or exploit.\n  Attacker doing recon won't even see the entry point."""},
    {"id":"tl02","tree":"tools","tier":2,"xp":50,"title":"OpenClaw Deploy","brief":"Install and secure an AI assistant",
     "hint":"Review tool permissions in openclaw.json BEFORE enabling exec. Always audit third-party skills — they run with your agent's permissions.",
     "benefit":"AI agents are the next frontier of both productivity and attack surface. Understanding their security model is cutting-edge knowledge few people have.",
     "bonus":"Restrict OpenClaw permissions, audit installed skills, connect through Twingate. Document security config in ~/openclaw_security.txt","bonus_xp":15,
     "mission":"""═══ MISSION — OpenClaw Deploy ═══\n\n⚠️ OpenClaw can execute shell commands. Understand the risks.\n\n► WHAT IS OPENCLAW?\n  Open-source AI agent running on YOUR machine.\n  Connects to AI models (Claude, GPT, local).\n  Uses 'skills' system (markdown instruction files).\n  Data stays local. Bring your own API keys.\n  ⚠️ CVE CONSIDERATION: Third-party skills can perform\n  data exfiltration and prompt injection. ALWAYS audit.\n\n► INSTALL ON PARROT:\n  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -\n  sudo apt install -y nodejs\n  npm install -g openclaw@latest\n  openclaw onboard --install-daemon\n\n► SECURITY HARDENING:\n  1. Edit openclaw.json:\n     \"tools\": {\"allow\": [\"web_search\"], \"deny\": [\"exec\"]}\n  2. Audit skills: ls ~/.openclaw/skills/\n  3. Review EVERY third-party skill before installing\n  4. Gateway should only listen on localhost\n  5. API keys: ensure not stored in plaintext\n\n► THREAT MODEL:\n  If compromised, what can the agent do?\n  Answer depends on permissions YOU granted.\n  Minimum necessary permissions, ALWAYS."""},
    {"id":"tl03","tree":"tools","tier":3,"xp":60,"title":"AI Red Team","brief":"Audit your OpenClaw + Twingate stack",
     "hint":"Think like an attacker: what's the blast radius if your AI agent is compromised? Check ports, permissions, API key storage, and skill integrity.",
     "benefit":"Auditing AI agent security is a brand-new skill that very few people have. As AI agents become common, this knowledge will be highly sought after.",
     "bonus":"Write a monitoring script for OpenClaw logs: alert on curl, wget, nc, rm -rf, /etc/shadow. Your first AI agent IDS!","bonus_xp":20,
     "mission":"""═══ MISSION — AI Red Team ═══\n\n⚠️ Audit your OWN setup.\n\n► AUDIT OPENCLAW:\n  ss -tulnp | grep node    # Gateway ports\n  cat ~/.openclaw/config.json   # Plaintext secrets?\n  Review tool permissions in openclaw.json\n  Check if dashboard is exposed beyond localhost\n\n► AUDIT TWINGATE:\n  twingate resources        # Access scoped correctly?\n  Check Connector privileges\n  Review access policies in admin console\n\n► TEST BLAST RADIUS:\n  If agent + shell + VPN = remote access trojan YOU installed\n  Create restricted profiles for specific resources\n  Document in ~/red_team_audit.txt\n\n► HARDEN:\n  Restrict exec to specific commands\n  Connector runs as dedicated service account\n  Monitor logs for suspicious commands"""},

    # ════════════ PYTHON SCRIPTING ════════════
    {"id":"py01","tree":"python","tier":1,"xp":20,"title":"Hello Hacker","brief":"Your first Python program",
     "hint":"print() outputs text. Strings go in quotes. # starts a comment. Python runs top to bottom.",
     "benefit":"Python is THE language of cybersecurity. Every major tool (Metasploit modules, Scapy, custom exploits, automation) uses Python.",
     "bonus":"Make a script that prints a formatted box with your agent codename and status using string formatting.","bonus_xp":5,
     "sandbox":'print("=== CyberQuest Python Academy ===")\nprint("Agent: Captain")\nprint("Status: Online")\nprint(f"Python version: {__import__(\'sys\').version}")',
     "mission":"""═══ MISSION — Hello Hacker ═══\n\n► OBJECTIVES:\n  1. Open terminal: python3\n  2. Try:\n     >>> print(\"Hello, Hacker!\")\n     >>> print(2 + 2)\n     >>> print(\"Name: \" + \"Captain\")\n\n  3. Create hello.py:\n     print(\"=== CyberQuest ===\")\n     print(\"Agent: Captain\")\n     print(\"Status: Online\")\n\n  4. Run: python3 hello.py\n\n► KEY CONCEPTS:\n  print() = function that outputs text\n  \"text\" = string\n  # = comment (Python ignores it)\n  Code runs top to bottom"""},
    {"id":"py02","tree":"python","tier":1,"xp":25,"title":"Variables & Types","brief":"Store data in variables",
     "hint":"f-strings are your friend: f\"Hello {name}\". Use type() to check any variable's type. Python figures out types automatically.",
     "benefit":"Variables store everything in security scripts — target IPs, port numbers, payloads, scan results. Understanding types prevents bugs.",
     "bonus":"Create a 'target profile' script with: target_ip, port, protocol, vuln_name, severity_score. Print formatted output.","bonus_xp":5,
     "sandbox":'name = "Captain"\nage = 25\nis_hacker = True\ntarget_ip = "192.168.1.100"\n\nprint(f"Agent: {name}, Age: {age}")\nprint(f"Hacker: {is_hacker}")\nprint(f"Target: {target_ip}")\nprint(f"Types: {type(name)}, {type(age)}, {type(is_hacker)}")',
     "mission":"""═══ MISSION — Variables & Types ═══\n\n► CREATE VARIABLES:\n  name = \"Captain\"       # String\n  age = 25               # Integer\n  height = 5.9           # Float\n  is_hacker = True       # Boolean\n\n► F-STRINGS:\n  print(f\"Name: {name}\")\n  print(f\"Age: {age}\")\n\n► MATH:\n  x=10; y=3\n  + - * / (divide) // (floor) % (mod) ** (power)\n\n► CHECK TYPES:\n  print(type(name))   # <class 'str'>"""},
    {"id":"py03","tree":"python","tier":1,"xp":30,"title":"Control Flow","brief":"if/else, loops, and logic",
     "hint":"Indentation matters! Use 4 spaces. Remember: == checks equality, = assigns. for+range() for counting, while for conditions.",
     "benefit":"Control flow lets you build decision-making tools — vulnerability classifiers, brute force scripts, automated scanners.",
     "bonus":"Build a brute force simulator: try passwords from a list against a stored password, count attempts, print results.","bonus_xp":10,
     "sandbox":'targets = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]\n\nfor ip in targets:\n    print(f"[*] Scanning {ip}...")\n    for port in [22, 80, 443]:\n        status = "OPEN" if port != 443 else "FILTERED"\n        print(f"    Port {port}: {status}")\n\npassword = "secret"\nguess = "secret"\nif guess == password:\n    print("\\nACCESS GRANTED")\nelse:\n    print("\\nACCESS DENIED")',
     "mission":"""═══ MISSION — Control Flow ═══\n\n► IF/ELIF/ELSE:\n  score = 85\n  if score >= 90:    print(\"CRITICAL\")\n  elif score >= 70:  print(\"HIGH\")\n  elif score >= 40:  print(\"MEDIUM\")\n  else:              print(\"LOW\")\n\n► COMPARISON: == != > < >= <=\n► LOGIC: and, or, not\n\n► FOR LOOP:\n  for i in range(5): print(i)\n  for ip in [\"10.0.0.1\",\"10.0.0.2\"]: print(ip)\n\n► WHILE LOOP:\n  attempts = 0\n  while attempts < 3:\n      pwd = input(\"Password: \")\n      if pwd == \"secret\": break\n      attempts += 1"""},
    {"id":"py04","tree":"python","tier":2,"xp":40,"title":"Functions & Errors","brief":"Reusable code and error handling",
     "hint":"Functions should do ONE thing. Use try/except for anything that might fail (user input, file operations, network calls).",
     "benefit":"Functions and error handling are what separate scripts from tools. Professional security tools need to handle edge cases gracefully.",
     "bonus":"Build a mini toolkit: port_classifier(), ip_validator(), password_scorer() functions. Call from a menu.","bonus_xp":10,
     "sandbox":'def classify_port(port):\n    if port < 1024: return "well-known"\n    elif port < 49152: return "registered"\n    return "dynamic"\n\ndef safe_input(prompt, type_fn=int):\n    try:\n        return type_fn(input(prompt))\n    except ValueError:\n        print("Invalid input!")\n        return None\n\nfor p in [22, 80, 3306, 8080, 50000]:\n    print(f"Port {p}: {classify_port(p)}")',
     "mission":"""═══ MISSION — Functions & Errors ═══\n\n► FUNCTIONS:\n  def classify_port(port):\n      if port < 1024: return \"well-known\"\n      return \"registered\"\n  result = classify_port(80)\n\n► DEFAULT PARAMS:\n  def scan(target, ports=[80,443], timeout=5):\n      print(f\"Scanning {target}\")\n\n► TRY/EXCEPT:\n  try:\n      port = int(input(\"Port: \"))\n  except ValueError:\n      print(\"Not a number!\")\n\n► RAISING ERRORS:\n  def set_port(port):\n      if not 1<=port<=65535:\n          raise ValueError(f\"Port {port} invalid\")\n      return port"""},
    {"id":"py05","tree":"python","tier":2,"xp":45,"title":"Data Structures","brief":"Lists, dicts, and comprehensions",
     "hint":"Lists for ordered collections, dicts for key-value pairs. List comprehension [x for x in list if condition] is powerful and Pythonic.",
     "benefit":"Every security tool uses data structures — port lists, host inventories, scan results. Comprehensions make your code clean and fast.",
     "bonus":"Build a host inventory tool: add hosts with IP/hostname/ports, search by IP or name, display all.","bonus_xp":10,
     "sandbox":'# Lists\nports = [21, 22, 80, 443, 8080]\nhigh = [p for p in ports if p > 1024]\nprint(f"High ports: {high}")\n\n# Dictionaries\ntarget = {\n    "ip": "192.168.1.100",\n    "hostname": "web-srv",\n    "ports": [22, 80, 443]\n}\nfor k, v in target.items():\n    print(f"  {k}: {v}")\n\n# Dict comprehension\nstatus = {p: ("open" if p < 1024 else "filtered") for p in ports}\nprint(f"\\nStatus: {status}")',
     "mission":"""═══ MISSION — Data Structures ═══\n\n► LISTS:\n  ports = [22, 80, 443]\n  ports.append(8080)\n  ports.sort()\n  high = [p for p in ports if p > 1024]  # Comprehension!\n\n► DICTIONARIES:\n  target = {\"ip\": \"192.168.1.1\", \"ports\": [22,80]}\n  target[\"status\"] = \"up\"\n  for key, val in target.items(): print(f\"{key}: {val}\")\n\n► NESTED:\n  network = {\n      \"192.168.1.1\": {\"name\":\"router\", \"ports\":[80]},\n      \"192.168.1.100\": {\"name\":\"web\", \"ports\":[22,80]}\n  }"""},
    {"id":"py06","tree":"python","tier":2,"xp":40,"title":"Files & Modules","brief":"File I/O, JSON, standard library",
     "hint":"Always use 'with open()' for file operations — it auto-closes. JSON is your go-to for structured data. hashlib for security work.",
     "benefit":"Real security tools read configs, parse logs, save results, and use crypto libraries. File I/O and modules make your scripts professional.",
     "bonus":"Write a script that hashes a password with SHA256, generates a secure token, logs the timestamp, saves to JSON.","bonus_xp":10,
     "sandbox":'import json, hashlib, secrets\nfrom datetime import datetime\n\nscan = {"target":"192.168.1.1","ports":[22,80,443],"time":str(datetime.now())}\n\nwith open("scan.json","w") as f:\n    json.dump(scan, f, indent=2)\n    print("Saved scan.json")\n\nwith open("scan.json","r") as f:\n    loaded = json.load(f)\n    print(f"Target: {loaded[\'target\']}")\n\npw = "password123"\nprint(f"\\nSHA256: {hashlib.sha256(pw.encode()).hexdigest()}")\nprint(f"Token: {secrets.token_hex(16)}")',
     "mission":"""═══ MISSION — Files & Modules ═══\n\n► FILE I/O:\n  with open(\"results.txt\", \"w\") as f:\n      f.write(\"Port 22: OPEN\\n\")\n  with open(\"results.txt\", \"r\") as f:\n      print(f.read())\n\n► JSON:\n  import json\n  data = {\"target\":\"192.168.1.1\", \"ports\":[22,80]}\n  with open(\"config.json\",\"w\") as f:\n      json.dump(data, f, indent=2)\n\n► USEFUL MODULES:\n  os: os.getcwd(), os.listdir()\n  hashlib: sha256, md5 hashing\n  secrets: cryptographic random\n  re: regex pattern matching\n  datetime: timestamps"""},
    {"id":"py07","tree":"python","tier":3,"xp":55,"title":"OOP & Advanced","brief":"Classes, decorators, generators",
     "hint":"Classes model real things (Target, Scanner, Vulnerability). Decorators add behavior to functions. Generators save memory with lazy evaluation.",
     "benefit":"Advanced Python separates script kiddies from tool developers. Professional security tools use OOP, decorators for logging/auth, generators for large datasets.",
     "bonus":"Build a Scanner class hierarchy: base Scanner, PortScanner, VulnScanner subclasses. Add a @timer decorator.","bonus_xp":15,
     "sandbox":'import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f"[{func.__name__}] {time.time()-start:.4f}s")\n        return result\n    return wrapper\n\nclass Scanner:\n    def __init__(self, target):\n        self.target = target\n        self.results = []\n    def report(self):\n        print(f"--- {self.target} ---")\n        for r in self.results: print(f"  {r}")\n\nclass PortScanner(Scanner):\n    @timer\n    def scan(self, ports):\n        for p in ports:\n            self.results.append(f"Port {p}: open")\n\nps = PortScanner("192.168.1.1")\nps.scan([22, 80, 443, 8080])\nps.report()',
     "mission":"""═══ MISSION — OOP & Advanced ═══\n\n► CLASSES:\n  class Target:\n      def __init__(self, ip, hostname):\n          self.ip = ip\n          self.hostname = hostname\n          self.ports = []\n      def add_port(self, port):\n          self.ports.append(port)\n      def report(self):\n          print(f\"{self.hostname}: {self.ports}\")\n\n► INHERITANCE:\n  class PortScanner(Scanner):\n      def scan(self, ports): ...\n\n► DECORATORS:\n  def timer(func):\n      def wrapper(*args):\n          start = time.time()\n          result = func(*args)\n          print(f\"Took {time.time()-start:.2f}s\")\n          return result\n      return wrapper\n  @timer\n  def slow_scan(): ...\n\n► COMPREHENSIONS & LAMBDA:\n  high = [p for p in ports if p > 1024]\n  classify = lambda p: \"low\" if p<1024 else \"high\"\n  sorted_ports = sorted(ports, key=lambda p: -p)"""},
    {"id":"py08","tree":"python","tier":3,"xp":70,"title":"Build a Security Tool","brief":"Capstone: build a real tool from scratch",
     "hint":"Plan before coding: what does the tool do? What classes do you need? What modules? Start with the simplest version, then add features.",
     "benefit":"Building your own tools is what separates a cybersecurity professional from someone who only runs other people's tools. This is portfolio material.",
     "bonus":"Add to your tool: export results to JSON, add a --verbose flag, handle all errors gracefully, add color output.","bonus_xp":20,
     "sandbox":'import secrets, string, json\nfrom datetime import datetime\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + "!@#$%^&*"\n    return "".join(secrets.choice(chars) for _ in range(length))\n\ndef score_password(pw):\n    checks = [len(pw)>=12, any(c.isupper() for c in pw),\n              any(c.isdigit() for c in pw), any(c in "!@#$%^&*" for c in pw)]\n    return sum(checks)\n\nprint("=== Password Generator & Scorer ===")\nfor i in range(5):\n    pw = generate_password(20)\n    sc = score_password(pw)\n    print(f"  {pw}  Score: {sc}/4")',
     "mission":"""═══ MISSION — Build a Security Tool ═══\n\nCombine everything into a REAL tool. Choose one:\n\n► OPTION A: LOG ANALYZER\n  - Parse auth.log for failed logins\n  - Count failures per IP\n  - Flag brute force (5+ fails in 5 min)\n  - Generate JSON report\n\n► OPTION B: PASSWORD VAULT\n  - Store service/username/password entries\n  - Basic XOR encryption (learning only!)\n  - Save/load from JSON\n  - Generate random passwords\n  - Score password strength\n\n► OPTION C: NETWORK SCANNER\n  - Ping sweep a subnet\n  - Port scan discovered hosts\n  - Service version detection\n  - Save results to JSON/CSV\n\n► REQUIREMENTS:\n  Use classes (OOP)\n  Use file I/O (JSON)\n  Use error handling (try/except)\n  Use 3+ standard library modules\n  Use list comprehension somewhere"""},
]

# ═══════════════════ SIDE QUESTS (EXAMS) ═══════════════════

SIDE_QUESTS = [
    {"id":"exam_linux","title":"🧪 Linux Fundamentals Exam","xp":30,"required_tree":"linux",
     "questions":[
        {"q":"What command shows your current directory?","options":["ls","pwd","cd","whoami"],"answer":1},
        {"q":"Which directory stores config files?","options":["/home","/tmp","/etc","/bin"],"answer":2},
        {"q":"What does chmod 755 mean?","options":["Owner:rwx Group:r-x Others:r-x","All:rwx","Owner:rw- Others:r--","Owner:rwx Group:rwx Others:rwx"],"answer":0},
        {"q":"SUID bit does what?","options":["Makes read-only","Runs as file owner","Deletes after use","Encrypts file"],"answer":1},
        {"q":"Find SUID files command?","options":["grep -r suid /","find / -perm -4000","ls -suid","chmod --find-suid"],"answer":1},
        {"q":"Password hashes stored in?","options":["/etc/passwd","/etc/shadow","/etc/hashes","/var/log/auth"],"answer":1},
        {"q":"sudo -l shows?","options":["Last login","Load","What you can sudo","Ports"],"answer":2},
        {"q":"Default world-writable dir?","options":["/etc","/home","/tmp","/root"],"answer":2},
    ]},
    {"id":"exam_network","title":"🧪 Networking Exam","xp":30,"required_tree":"networking",
     "questions":[
        {"q":"TCP operates at OSI layer?","options":["2","3","4","7"],"answer":2},
        {"q":"SSH default port?","options":["21","22","80","443"],"answer":1},
        {"q":"SYN packet indicates?","options":["Closing","Data transfer","Connection request","Error"],"answer":2},
        {"q":"nmap -sS does?","options":["UDP scan","SYN stealth","Full connect","Ping sweep"],"answer":1},
        {"q":"DNS resolves?","options":["IPs to MACs","Names to IPs","MACs to names","Ports to services"],"answer":1},
        {"q":"/24 subnet mask?","options":["255.0.0.0","255.255.0.0","255.255.255.0","255.255.255.128"],"answer":2},
        {"q":"Captures packets?","options":["netstat","ifconfig","tcpdump","ping"],"answer":2},
        {"q":"ARP resolves?","options":["IP to hostname","IP to MAC","MAC to IP","Host to IP"],"answer":1},
    ]},
    {"id":"exam_security","title":"🧪 Security Foundations Exam","xp":35,"required_tree":"governance",
     "questions":[
        {"q":"'C' in CIA Triad?","options":["Control","Compliance","Confidentiality","Cryptography"],"answer":2},
        {"q":"CVSS Critical range?","options":["7.0-8.9","8.0-9.9","9.0-10.0","10.0 only"],"answer":2},
        {"q":"NIST 'Detect' function?","options":["Prevent attacks","Monitor for attacks","Respond to attacks","Recover"],"answer":1},
        {"q":"CVE format?","options":["CVE-YYYY-NNNNN","VULN-NNNNN","SEC-YYYY","NVD-NNNNN"],"answer":0},
        {"q":"OWASP Top 10 focuses on?","options":["Network vulns","Web app vulns","Hardware","Social engineering"],"answer":1},
        {"q":"$6$ hash type?","options":["MD5","SHA-256","SHA-512","bcrypt"],"answer":2},
        {"q":"Zero-day is?","options":["Patched vuln","No known fix","Low severity","Day-zero bug"],"answer":1},
        {"q":"Defense in depth?","options":["One strong firewall","Multiple security layers","Deep packet inspection","Encrypt everything"],"answer":1},
    ]},
    {"id":"exam_web","title":"🧪 Web Hacking Exam","xp":30,"required_tree":"webhack",
     "questions":[
        {"q":"SQL injection is?","options":["CSS injection","Malicious SQL in queries","DDoS","XSS"],"answer":1},
        {"q":"XSS stands for?","options":["Cross-System Scripting","Cross-Site Scripting","eXtra Secure Socket","XML Site Service"],"answer":1},
        {"q":"Intercepts HTTP requests?","options":["Nmap","Wireshark","Burp Suite","Metasploit"],"answer":2},
        {"q":"Reveals hidden web paths?","options":["index.html","robots.txt",".htaccess","config.php"],"answer":1},
        {"q":"OWASP #1 (2021)?","options":["Injection","Broken Access Control","XSS","SSRF"],"answer":1},
        {"q":"sqlmap automates?","options":["Port scanning","SQL injection","Password cracking","Firewall config"],"answer":1},
    ]},
    {"id":"exam_python","title":"🧪 Python Fundamentals Exam","xp":30,"required_tree":"python",
     "questions":[
        {"q":"Print output in Python?","options":["echo()","printf()","print()","output()"],"answer":2},
        {"q":"f-string syntax?","options":["f'Hello {name}'","'Hello' + name","format('Hello', name)","Hello.format(name)"],"answer":0},
        {"q":"List comprehension?","options":["list(x for x)","[x for x in list]","{x: x}","(x for x)"],"answer":1},
        {"q":"Handle errors with?","options":["if/else","try/except","for/while","def/return"],"answer":1},
        {"q":"__init__ is?","options":["Destructor","Constructor","Iterator","Decorator"],"answer":1},
        {"q":"Read a file safely?","options":["open('f').read()","with open('f') as f:","file.get('f')","read('f')"],"answer":1},
    ]},
]

# ═══════════════════ ACHIEVEMENTS ═══════════════════

def get_achievements(save):
    c = save.get("completed_quests",[])
    b = save.get("bonus_completed",[])
    e = save.get("exam_scores",{})
    s = save.get("side_quests_done",[])
    return [
        {"id":"first","name":"First Blood","desc":"Complete first quest","icon":"🩸","check":lambda:len(c)>=1},
        {"id":"five","name":"Grinding","desc":"Complete 5 quests","icon":"⚔️","check":lambda:len(c)>=5},
        {"id":"ten","name":"Double Digits","desc":"Complete 10 quests","icon":"🔟","check":lambda:len(c)>=10},
        {"id":"twenty","name":"Unstoppable","desc":"Complete 20 quests","icon":"🔥","check":lambda:len(c)>=20},
        {"id":"all","name":"Completionist","desc":"ALL quests done","icon":"👑","check":lambda:len(c)>=len(ALL_QUESTS)},
        {"id":"bonus1","name":"Extra Credit","desc":"Claim a bonus","icon":"⭐","check":lambda:len(b)>=1},
        {"id":"bonus5","name":"Overachiever","desc":"5 bonuses claimed","icon":"🌟","check":lambda:len(b)>=5},
        {"id":"exam1","name":"Test Taker","desc":"Pass an exam","icon":"📝","check":lambda:len(s)>=1},
        {"id":"exams_all","name":"Scholar","desc":"Pass all exams","icon":"🎓","check":lambda:len(s)>=len(SIDE_QUESTS)},
        {"id":"perfect","name":"Perfect Score","desc":"100% on any exam","icon":"💯","check":lambda:any(v==100 for v in e.values())},
        {"id":"linux","name":"Penguin Master","desc":"All Linux quests","icon":"🐧","check":lambda:all(q["id"] in c for q in ALL_QUESTS if q["tree"]=="linux")},
        {"id":"web","name":"Web Warrior","desc":"All Web quests","icon":"🕸️","check":lambda:all(q["id"] in c for q in ALL_QUESTS if q["tree"]=="webhack")},
        {"id":"def","name":"Shield Wall","desc":"All Defense quests","icon":"🛡️","check":lambda:all(q["id"] in c for q in ALL_QUESTS if q["tree"]=="defense")},
        {"id":"py","name":"Pythonista","desc":"All Python quests","icon":"🐍","check":lambda:all(q["id"] in c for q in ALL_QUESTS if q["tree"]=="python")},
        {"id":"trees","name":"Renaissance","desc":"Quest in every tree","icon":"🌈","check":lambda:all(any(q["id"] in c for q in ALL_QUESTS if q["tree"]==t) for t in SKILL_TREES)},
    ]

def get_rank(xp):
    r = RANKS[0]
    for x in RANKS:
        if xp >= x["xp"]: r = x
    return r

def get_next_rank(xp):
    for r in RANKS:
        if r["xp"] > xp: return r
    return None

def total_xp(save):
    xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in save.get("completed_quests",[]))
    xp += sum(next((q.get("bonus_xp",0) for q in ALL_QUESTS if q["id"]==bid),0) for bid in save.get("bonus_completed",[]))
    xp += sum(sq["xp"] for sq in SIDE_QUESTS if sq["id"] in save.get("side_quests_done",[]))
    return xp

# ═══════════════════ GUI ═══════════════════

class App:
    BG="#0a0a0f";BG2="#111118";BGH="#1a1a24";BGC="#08080e"
    FG="#cccccc";FGD="#555566";FGB="#ffffff"
    ACC="#00ff88";BRD="#222233";DON="#0a1a10"

    def __init__(self, root):
        self.root = root
        self.root.title("CyberQuest Academy")
        self.root.configure(bg=self.BG)
        self.root.geometry("980x760")
        self.root.minsize(740,540)
        self.save = load_save()
        self.sel_tree = None
        self.ft=tkfont.Font(family="Consolas",size=18,weight="bold")
        self.fs=tkfont.Font(family="Consolas",size=9)
        self.fh=tkfont.Font(family="Consolas",size=12,weight="bold")
        self.fn=tkfont.Font(family="Consolas",size=10)
        self.fb=tkfont.Font(family="Consolas",size=10,weight="bold")
        self.fr=tkfont.Font(family="Consolas",size=15,weight="bold")
        self.fx=tkfont.Font(family="Consolas",size=22,weight="bold")
        self._build()
        if not self.save.get("seen_requirements"):
            self.root.after(500, self._show_requirements)
        self.show_dashboard()

    def _show_requirements(self):
        w = tk.Toplevel(self.root)
        w.title("Getting Started")
        w.geometry("700x550")
        w.configure(bg=self.BG)
        w.transient(self.root)
        w.grab_set()
        tk.Label(w, text="📋 BEFORE YOU BEGIN", font=self.fh, fg="#ffcc00", bg=self.BG).pack(pady=(12,5))
        tf = tk.Frame(w, bg=self.BGC)
        tf.pack(fill="both", expand=True, padx=15, pady=5)
        t = tk.Text(tf, font=self.fn, bg=self.BGC, fg=self.FG, wrap="word", relief="flat", padx=12, pady=10)
        t.pack(fill="both", expand=True)
        t.insert("1.0", REQUIREMENTS_TEXT)
        t.configure(state="disabled")
        def dismiss():
            self.save["seen_requirements"] = True
            write_save(self.save)
            w.destroy()
        tk.Button(w, text="✓  GOT IT — LET'S GO!", font=self.fh, bg=self.BG2, fg=self.ACC, bd=0, pady=10, cursor="hand2", command=dismiss).pack(fill="x", padx=15, pady=10)

    def _build(self):
        self.mf = tk.Frame(self.root, bg=self.BG)
        self.mf.pack(fill="both", expand=True)
        hf = tk.Frame(self.mf, bg=self.BG)
        hf.pack(fill="x", padx=20, pady=(8,2))
        tk.Label(hf, text="CYBERQUEST ACADEMY", font=self.ft, fg=self.ACC, bg=self.BG).pack()
        tk.Label(hf, text="BEGINNER → ADVANCED  •  PARROT OS", font=self.fs, fg=self.FGD, bg=self.BG).pack()
        self.rf = tk.Frame(self.mf, bg=self.BG2, highlightbackground="#00cc66", highlightthickness=1)
        self.rf.pack(fill="x", padx=20, pady=5)
        self._rank()
        nf = tk.Frame(self.mf, bg=self.BG)
        nf.pack(fill="x", padx=20, pady=(0,2))
        tabs = [("⚔ QUESTS",self.show_dashboard),("🐍 PYTHON",self.show_python),("🧪 EXAMS",self.show_exams),("🏆 ACHIEVEMENTS",self.show_achievements),("💼 CAREERS",self.show_careers),("📋 SETUP",lambda:self._show_requirements())]
        self.tab_btns = []
        for txt,cmd in tabs:
            b = tk.Button(nf, text=txt, font=self.fs, bg=self.BG2, fg=self.FGD, activebackground=self.BGH, activeforeground=self.ACC, bd=0, padx=8, pady=5, cursor="hand2", command=cmd)
            b.pack(side="left", expand=True, fill="x", padx=1)
            self.tab_btns.append(b)
        cc = tk.Frame(self.mf, bg=self.BG)
        cc.pack(fill="both", expand=True, padx=20, pady=(2,6))
        self.cv = tk.Canvas(cc, bg=self.BG, highlightthickness=0)
        sb = tk.Scrollbar(cc, orient="vertical", command=self.cv.yview, bg=self.BG2, troughcolor=self.BG)
        self.sf = tk.Frame(self.cv, bg=self.BG)
        self.sf.bind("<Configure>", lambda e: self.cv.configure(scrollregion=self.cv.bbox("all")))
        self.cw = self.cv.create_window((0,0), window=self.sf, anchor="nw")
        self.cv.configure(yscrollcommand=sb.set)
        self.cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.cv.bind_all("<MouseWheel>", lambda e: self.cv.yview_scroll(int(-1*(e.delta/120)),"units"))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfig(self.cw, width=e.width))

    def _rank(self):
        for w in self.rf.winfo_children(): w.destroy()
        xp=total_xp(self.save); rk=get_rank(xp); nr=get_next_rank(xp)
        inn=tk.Frame(self.rf,bg=self.BG2); inn.pack(fill="x",padx=12,pady=7)
        top=tk.Frame(inn,bg=self.BG2); top.pack(fill="x")
        lf=tk.Frame(top,bg=self.BG2); lf.pack(side="left")
        tk.Label(lf,text=f"RANK {rk['level']}",font=self.fs,fg=self.ACC,bg=self.BG2).pack(anchor="w")
        tk.Label(lf,text=rk["title"],font=self.fr,fg=self.FGB,bg=self.BG2).pack(anchor="w")
        rt=tk.Frame(top,bg=self.BG2); rt.pack(side="right")
        xf=tk.Frame(rt,bg=self.BG2); xf.pack(anchor="e")
        tk.Label(xf,text=str(xp),font=self.fx,fg=self.FGB,bg=self.BG2).pack(side="left")
        tk.Label(xf,text=" XP",font=self.fh,fg=self.ACC,bg=self.BG2).pack(side="left",pady=(3,0))
        if nr:
            pf=tk.Frame(inn,bg=self.BG2); pf.pack(fill="x",pady=(4,0))
            ll=tk.Frame(pf,bg=self.BG2); ll.pack(fill="x")
            tk.Label(ll,text=rk["title"],font=self.fs,fg=self.FGD,bg=self.BG2).pack(side="left")
            tk.Label(ll,text=f"{nr['title']} — {nr['xp']-xp} XP to go",font=self.fs,fg=self.FGD,bg=self.BG2).pack(side="right")
            bb=tk.Frame(pf,bg=self.BRD,height=6); bb.pack(fill="x",pady=(2,0)); bb.pack_propagate(False)
            p=(xp-rk["xp"])/max(1,nr["xp"]-rk["xp"])
            tk.Frame(bb,bg=self.ACC,height=6).place(relwidth=min(p,1.0),relheight=1.0)
        cf=tk.Frame(inn,bg=self.BG2); cf.pack(fill="x",pady=(4,0))
        c=len(self.save.get("completed_quests",[])); b=len(self.save.get("bonus_completed",[])); e=len(self.save.get("side_quests_done",[]))
        tk.Label(cf,text=f"{c}/{len(ALL_QUESTS)} Quests • {b} Bonuses • {e} Exams",font=self.fs,fg=self.FGD,bg=self.BG2).pack()

    def _clear(self):
        for w in self.sf.winfo_children(): w.destroy()
        self.cv.yview_moveto(0)

    def _tabs(self, idx):
        for i,b in enumerate(self.tab_btns):
            b.configure(fg=self.ACC if i==idx else self.FGD)

    def _avail(self, tree_filter=None):
        qs=[]; comp=self.save.get("completed_quests",[])
        for q in ALL_QUESTS:
            tf = tree_filter or self.sel_tree
            if tf and q["tree"]!=tf: continue
            if q["tier"]==1: qs.append(q)
            elif q["tier"]==2 and any(c for c in comp if any(a["id"]==c and a["tree"]==q["tree"] and a["tier"]==1 for a in ALL_QUESTS)): qs.append(q)
            elif q["tier"]==3 and any(c for c in comp if any(a["id"]==c and a["tree"]==q["tree"] and a["tier"]==2 for a in ALL_QUESTS)): qs.append(q)
        return qs

    # ═══════════ DASHBOARD ═══════════
    def show_dashboard(self):
        self._clear(); self._tabs(0)
        ff=tk.Frame(self.sf,bg=self.BG); ff.pack(fill="x",pady=(0,4))
        def sf(t): self.sel_tree=t; self.show_dashboard()
        tk.Button(ff,text="ALL",font=self.fs,bg=self.BGH if not self.sel_tree else self.BG2,fg=self.FGB if not self.sel_tree else self.FGD,bd=0,padx=5,pady=2,cursor="hand2",command=lambda:sf(None)).pack(side="left",padx=(0,1))
        for k,t in SKILL_TREES.items():
            if k=="python": continue
            s=self.sel_tree==k
            tk.Button(ff,text=t["icon"],font=self.fs,bg=self.BGH if s else self.BG2,fg=t["color"] if s else self.FGD,bd=0,padx=4,pady=2,cursor="hand2",command=lambda k=k:sf(k)).pack(side="left",padx=1)
        xg=tk.Frame(self.sf,bg=self.BG); xg.pack(fill="x",pady=(0,6))
        non_py = {k:v for k,v in SKILL_TREES.items() if k!="python"}
        cols=min(5,len(non_py))
        for i,(k,t) in enumerate(non_py.items()):
            txp=sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests",[]) and q["tree"]==k)
            mxp=sum(q["xp"] for q in ALL_QUESTS if q["tree"]==k)
            c=tk.Frame(xg,bg=self.BG2,padx=4,pady=3); c.grid(row=i//cols,column=i%cols,sticky="ew",padx=1,pady=1)
            tk.Label(c,text=f"{t['icon']} {t['name'].split()[0]}",font=self.fs,fg=t["color"],bg=self.BG2,anchor="w").pack(fill="x")
            bg=tk.Frame(c,bg=self.BRD,height=4); bg.pack(fill="x",pady=(2,0)); bg.pack_propagate(False)
            tk.Frame(bg,bg=t["color"],height=4).place(relwidth=min(txp/max(1,mxp),1.0),relheight=1.0)
        for c in range(cols): xg.columnconfigure(c,weight=1)
        avail=[q for q in self._avail() if q["tree"]!="python"]
        for q in avail: self._card(q)
        if not avail: tk.Label(self.sf,text="No quests. Complete lower tiers to unlock.",font=self.fn,fg=self.FGD,bg=self.BG,pady=20).pack()
        tk.Label(self.sf,text="",bg=self.BG).pack(pady=3)
        tk.Button(self.sf,text="🔄 RESET ALL PROGRESS",font=self.fs,bg="#1a0a0a",fg="#ff4444",bd=0,pady=5,cursor="hand2",command=self._reset).pack(fill="x")

    # ═══════════ PYTHON TAB ═══════════
    def show_python(self):
        self._clear(); self._tabs(1)
        tk.Label(self.sf,text="🐍 PYTHON SCRIPTING",font=self.fh,fg="#3776ab",bg=self.BG).pack(anchor="w",pady=(0,4))
        tk.Label(self.sf,text="Learn Python the hacker way. Each quest has a built-in code sandbox.",font=self.fs,fg=self.FGD,bg=self.BG).pack(anchor="w",pady=(0,8))
        txp=sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests",[]) and q["tree"]=="python")
        mxp=sum(q["xp"] for q in ALL_QUESTS if q["tree"]=="python")
        pf=tk.Frame(self.sf,bg=self.BG2,padx=8,pady=6); pf.pack(fill="x",pady=(0,8))
        tk.Label(pf,text=f"🐍 Python Progress: {txp}/{mxp} XP",font=self.fb,fg="#3776ab",bg=self.BG2).pack(anchor="w")
        bg=tk.Frame(pf,bg=self.BRD,height=6); bg.pack(fill="x",pady=(4,0)); bg.pack_propagate(False)
        tk.Frame(bg,bg="#3776ab",height=6).place(relwidth=min(txp/max(1,mxp),1.0),relheight=1.0)
        for q in self._avail(tree_filter="python"): self._card(q)

    def _card(self, q):
        t=SKILL_TREES[q["tree"]]; comp=self.save.get("completed_quests",[]); bcomp=self.save.get("bonus_completed",[])
        d=q["id"] in comp; bd=q["id"] in bcomp; bg=self.DON if d else self.BG2
        cd=tk.Frame(self.sf,bg=bg,cursor="hand2",highlightbackground=self.ACC if d else self.BRD,highlightthickness=1)
        cd.pack(fill="x",pady=2)
        inn=tk.Frame(cd,bg=bg); inn.pack(fill="x",padx=10,pady=6)
        top=tk.Frame(inn,bg=bg); top.pack(fill="x")
        tk.Label(top,text=f"{t['icon']} T{q['tier']}",font=self.fs,fg=t["color"],bg=bg).pack(side="left")
        pf="  ✓ " if d else "  "
        tk.Label(top,text=f"{pf}{q['title']}",font=self.fb,fg=self.ACC if d else self.FGB,bg=bg).pack(side="left")
        xt=f"+{q['xp']}"
        if q.get("bonus_xp"): xt+=f" (+{q['bonus_xp']}★)" if not bd else f" +{q['bonus_xp']}★"
        tk.Label(top,text=xt,font=self.fb,fg=t["color"],bg=bg).pack(side="right")
        tk.Label(inn,text=q["brief"],font=self.fs,fg=self.FGD,bg=bg,anchor="w").pack(fill="x",pady=(1,0))
        for w in [cd,inn,top]+list(inn.winfo_children())+list(top.winfo_children()):
            w.bind("<Button-1>",lambda e,q=q:self._detail(q))

    def _detail(self, q):
        self._clear()
        self._tabs(1 if q["tree"]=="python" else 0)
        t=SKILL_TREES[q["tree"]]; comp=self.save.get("completed_quests",[]); bcomp=self.save.get("bonus_completed",[])
        d=q["id"] in comp; bd=q["id"] in bcomp
        back_cmd = self.show_python if q["tree"]=="python" else self.show_dashboard
        tk.Button(self.sf,text="← Back",font=self.fb,bg=self.BG,fg=self.ACC,bd=0,cursor="hand2",command=back_cmd).pack(anchor="w",pady=(0,5))
        hd=tk.Frame(self.sf,bg=self.BG2,highlightbackground=t["color"],highlightthickness=1); hd.pack(fill="x")
        hi=tk.Frame(hd,bg=self.BG2); hi.pack(fill="x",padx=12,pady=7)
        tp=tk.Frame(hi,bg=self.BG2); tp.pack(fill="x")
        tk.Label(tp,text=f"{t['icon']} {t['name'].upper()} • TIER {q['tier']}",font=self.fs,fg=t["color"],bg=self.BG2).pack(side="left")
        tk.Label(tp,text=f"+{q['xp']} XP",font=self.fh,fg=t["color"],bg=self.BG2).pack(side="right")
        tk.Label(hi,text=q["title"],font=self.fh,fg=self.FGB,bg=self.BG2,anchor="w").pack(fill="x",pady=(2,0))
        # Benefit
        if q.get("benefit"):
            bf=tk.Frame(self.sf,bg="#0f1018",highlightbackground="#4488ff",highlightthickness=1); bf.pack(fill="x",pady=(3,0))
            tk.Label(bf,text=f"💎 WHY LEARN THIS: {q['benefit']}",font=self.fs,fg="#88bbff",bg="#0f1018",wraplength=700,justify="left",padx=10,pady=6).pack(fill="x")
        # Mission
        mf=tk.Frame(self.sf,bg=self.BGC,highlightbackground=self.BRD,highlightthickness=1); mf.pack(fill="x",pady=(3,0))
        mt=tk.Text(mf,font=self.fn,bg=self.BGC,fg=self.FG,wrap="word",relief="flat",padx=12,pady=10,height=14)
        mt.pack(fill="both",expand=True)
        mt.insert("1.0",q["mission"])
        mt.tag_configure("hdr",foreground=t["color"],font=self.fb)
        mt.tag_configure("warn",foreground="#ff6688")
        for i,line in enumerate(mt.get("1.0","end").split("\n"),1):
            if line.startswith("═══") or line.startswith("►"): mt.tag_add("hdr",f"{i}.0",f"{i}.end")
            elif line.startswith("⚠"): mt.tag_add("warn",f"{i}.0",f"{i}.end")
        mt.configure(state="disabled")
        # Hint button
        if q.get("hint"):
            tk.Button(self.sf,text="💡 SHOW HINT",font=self.fb,bg=self.BG2,fg="#ffcc00",bd=0,pady=6,cursor="hand2",
                      command=lambda:messagebox.showinfo("💡 Hint",q["hint"])).pack(fill="x",pady=(4,0))
        # Sandbox button (Python quests)
        if q.get("sandbox"):
            tk.Button(self.sf,text="⚡ OPEN IN SANDBOX",font=self.fb,bg=self.BG2,fg="#3776ab",bd=0,pady=6,cursor="hand2",
                      command=lambda:self._sandbox(q["sandbox"])).pack(fill="x",pady=(3,0))
        # Complete
        if not d:
            tk.Button(self.sf,text="✓ MARK COMPLETE",font=self.fh,bg=self.BG2,fg=t["color"],bd=0,pady=8,cursor="hand2",
                      command=lambda:self._complete(q)).pack(fill="x",pady=(4,0))
        else:
            tk.Label(self.sf,text="✓ QUEST COMPLETED",font=self.fh,fg=self.ACC,bg=self.DON,pady=8).pack(fill="x",pady=(4,0))
        # Bonus
        if q.get("bonus"):
            bf2=tk.Frame(self.sf,bg="#0f0f18",highlightbackground="#ffcc00",highlightthickness=1); bf2.pack(fill="x",pady=(4,0))
            bi=tk.Frame(bf2,bg="#0f0f18"); bi.pack(fill="x",padx=10,pady=6)
            tk.Label(bi,text=f"★ BONUS (+{q.get('bonus_xp',0)} XP)",font=self.fb,fg="#ffcc00",bg="#0f0f18").pack(anchor="w")
            tk.Label(bi,text=q["bonus"],font=self.fs,fg=self.FG,bg="#0f0f18",wraplength=680,justify="left").pack(fill="x",pady=(3,0))
            if d and not bd:
                tk.Button(bi,text="★ CLAIM BONUS XP",font=self.fb,bg="#1a1a10",fg="#ffcc00",bd=0,pady=5,cursor="hand2",
                          command=lambda:self._claim_bonus(q)).pack(fill="x",pady=(4,0))
            elif bd:
                tk.Label(bi,text="★ BONUS CLAIMED",font=self.fb,fg="#ffcc00",bg="#0a1a10",pady=5).pack(fill="x",pady=(4,0))

    def _sandbox(self, code):
        w=tk.Toplevel(self.root); w.title("⚡ Python Sandbox"); w.geometry("700x550"); w.configure(bg=self.BG); w.transient(self.root)
        tk.Label(w,text="⚡ PYTHON SANDBOX",font=self.fh,fg="#ffcc00",bg=self.BG).pack(pady=(8,3))
        ef=tk.Frame(w,bg=self.BGC,highlightbackground="#ffcc00",highlightthickness=1); ef.pack(fill="both",expand=True,padx=10,pady=3)
        editor=tk.Text(ef,font=tkfont.Font(family="Consolas",size=10),bg=self.BGC,fg="#00ff88",wrap="word",relief="flat",padx=10,pady=8,insertbackground="#ffcc00",height=12)
        editor.pack(fill="both",expand=True); editor.insert("1.0",code)
        tk.Label(w,text="OUTPUT:",font=self.fs,fg=self.FGD,bg=self.BG).pack(anchor="w",padx=10,pady=(3,1))
        of=tk.Frame(w,bg="#050508",highlightbackground=self.BRD,highlightthickness=1); of.pack(fill="both",expand=True,padx=10,pady=(0,5))
        output=tk.Text(of,font=tkfont.Font(family="Consolas",size=10),bg="#050508",fg="#aaa",wrap="word",relief="flat",padx=10,pady=8,height=8,state="disabled")
        output.pack(fill="both",expand=True)
        def run():
            c=editor.get("1.0","end").strip()
            if not c: return
            output.configure(state="normal"); output.delete("1.0","end")
            try:
                with tempfile.NamedTemporaryFile(mode="w",suffix=".py",delete=False) as f:
                    f.write(c); tp=f.name
                r=subprocess.run([sys.executable,tp],capture_output=True,text=True,timeout=10,input="Captain\n80\ntcp\n")
                o=r.stdout+(f"\n--- ERRORS ---\n{r.stderr}" if r.stderr else "")
                output.insert("1.0",o or "(No output)")
            except subprocess.TimeoutExpired: output.insert("1.0","⚠️ Timed out (10s)")
            except Exception as e: output.insert("1.0",f"Error: {e}")
            finally:
                try: os.unlink(tp)
                except: pass
            output.configure(state="disabled")
        bf=tk.Frame(w,bg=self.BG); bf.pack(fill="x",padx=10,pady=(0,8))
        tk.Button(bf,text="▶ RUN",font=self.fh,bg="#1a2a10",fg=self.ACC,bd=0,padx=20,pady=6,cursor="hand2",command=run).pack(side="left",expand=True,fill="x",padx=(0,3))
        tk.Button(bf,text="CLOSE",font=self.fh,bg=self.BG2,fg=self.FGD,bd=0,padx=20,pady=6,cursor="hand2",command=w.destroy).pack(side="left",expand=True,fill="x",padx=(3,0))

    def _complete(self, q):
        comp=self.save.get("completed_quests",[])
        if q["id"] not in comp:
            comp.append(q["id"]); self.save["completed_quests"]=comp; write_save(self.save)
            self._rank(); self._detail(q)
            messagebox.showinfo("Quest Complete!",f"+{q['xp']} XP!\nRank: {get_rank(total_xp(self.save))['title']}")

    def _claim_bonus(self, q):
        bc=self.save.get("bonus_completed",[])
        if q["id"] not in bc:
            bc.append(q["id"]); self.save["bonus_completed"]=bc; write_save(self.save)
            self._rank(); self._detail(q)
            messagebox.showinfo("Bonus Claimed!",f"+{q.get('bonus_xp',0)} Bonus XP!")

    def _reset(self):
        if messagebox.askyesno("Reset","ERASE all progress?") and messagebox.askyesno("Confirm","Really? No undo."):
            self.save={"completed_quests":[],"bonus_completed":[],"exam_scores":{},"side_quests_done":[],"seen_requirements":True,"started":datetime.now().isoformat()}
            write_save(self.save); self._rank(); self.show_dashboard()
            messagebox.showinfo("Reset","All progress erased. Fresh start!")

    # ═══════════ EXAMS ═══════════
    def show_exams(self):
        self._clear(); self._tabs(2)
        tk.Label(self.sf,text="🧪 KNOWLEDGE EXAMS",font=self.fh,fg="#ffcc00",bg=self.BG).pack(anchor="w",pady=(0,3))
        tk.Label(self.sf,text="Score 70%+ to pass and earn XP. Retake anytime.",font=self.fs,fg=self.FGD,bg=self.BG).pack(anchor="w",pady=(0,8))
        done=self.save.get("side_quests_done",[]); scores=self.save.get("exam_scores",{})
        for sq in SIDE_QUESTS:
            p=sq["id"] in done; sc=scores.get(sq["id"]); bg=self.DON if p else self.BG2
            cd=tk.Frame(self.sf,bg=bg,highlightbackground=self.ACC if p else self.BRD,highlightthickness=1,cursor="hand2"); cd.pack(fill="x",pady=2)
            inn=tk.Frame(cd,bg=bg); inn.pack(fill="x",padx=10,pady=7)
            top=tk.Frame(inn,bg=bg); top.pack(fill="x")
            tk.Label(top,text=f"{'✓ ' if p else ''}{sq['title']}",font=self.fb,fg=self.ACC if p else self.FGB,bg=bg).pack(side="left")
            rt=f"+{sq['xp']} XP"+f"  (Best: {sc}%)" if sc else f"+{sq['xp']} XP"
            tk.Label(top,text=rt,font=self.fb,fg="#ffcc00",bg=bg).pack(side="right")
            tk.Label(inn,text=f"{len(sq['questions'])} questions",font=self.fs,fg=self.FGD,bg=bg).pack(anchor="w")
            for w in [cd,inn,top]+list(inn.winfo_children())+list(top.winfo_children()):
                w.bind("<Button-1>",lambda e,s=sq:self._start_exam(s))

    def _start_exam(self, sq):
        self._clear(); self._tabs(2)
        tk.Button(self.sf,text="← Back",font=self.fb,bg=self.BG,fg=self.ACC,bd=0,cursor="hand2",command=self.show_exams).pack(anchor="w",pady=(0,6))
        tk.Label(self.sf,text=sq["title"],font=self.fh,fg="#ffcc00",bg=self.BG).pack(anchor="w",pady=(0,8))
        self.exam_vars=[]
        for i,question in enumerate(sq["questions"]):
            qf=tk.Frame(self.sf,bg=self.BG2,highlightbackground=self.BRD,highlightthickness=1); qf.pack(fill="x",pady=2)
            qi=tk.Frame(qf,bg=self.BG2); qi.pack(fill="x",padx=10,pady=6)
            tk.Label(qi,text=f"Q{i+1}: {question['q']}",font=self.fb,fg=self.FGB,bg=self.BG2,anchor="w",wraplength=680,justify="left").pack(fill="x",pady=(0,4))
            var=tk.IntVar(value=-1); self.exam_vars.append(var)
            for j,opt in enumerate(question["options"]):
                tk.Radiobutton(qi,text=opt,variable=var,value=j,font=self.fn,bg=self.BG2,fg=self.FG,selectcolor=self.BGH,activebackground=self.BG2,activeforeground=self.ACC,anchor="w").pack(fill="x",padx=8)
        tk.Button(self.sf,text="📝 SUBMIT",font=self.fh,bg="#1a1a10",fg="#ffcc00",bd=0,pady=8,cursor="hand2",command=lambda:self._submit_exam(sq)).pack(fill="x",pady=(6,0))

    def _submit_exam(self, sq):
        correct=sum(1 for i,q in enumerate(sq["questions"]) if self.exam_vars[i].get()==q["answer"])
        score=int((correct/len(sq["questions"]))*100); passed=score>=70
        self.save.setdefault("exam_scores",{})[sq["id"]]=max(score,self.save.get("exam_scores",{}).get(sq["id"],0))
        if passed and sq["id"] not in self.save.get("side_quests_done",[]):
            self.save.setdefault("side_quests_done",[]).append(sq["id"])
        write_save(self.save); self._rank()
        if passed: messagebox.showinfo("Passed! 🎉",f"Score: {correct}/{len(sq['questions'])} ({score}%)\n+{sq['xp']} XP!")
        else: messagebox.showinfo("Not Yet",f"Score: {correct}/{len(sq['questions'])} ({score}%)\nNeed 70% to pass.")
        self.show_exams()

    # ═══════════ ACHIEVEMENTS ═══════════
    def show_achievements(self):
        self._clear(); self._tabs(3)
        achs=get_achievements(self.save); earned=sum(1 for a in achs if a["check"]())
        tk.Label(self.sf,text=f"{earned}/{len(achs)} ACHIEVEMENTS",font=self.fh,fg=self.ACC,bg=self.BG).pack(pady=(0,6))
        for a in achs:
            e=a["check"](); bg=self.DON if e else self.BG2
            cd=tk.Frame(self.sf,bg=bg,highlightbackground=self.ACC if e else self.BRD,highlightthickness=1); cd.pack(fill="x",pady=2)
            inn=tk.Frame(cd,bg=bg); inn.pack(fill="x",padx=10,pady=6)
            r=tk.Frame(inn,bg=bg); r.pack(fill="x")
            tk.Label(r,text=a["icon"] if e else "🔒",font=self.fh,bg=bg).pack(side="left",padx=(0,8))
            inf=tk.Frame(r,bg=bg); inf.pack(side="left")
            tk.Label(inf,text=a["name"],font=self.fb,fg=self.ACC if e else self.FGD,bg=bg,anchor="w").pack(fill="x")
            tk.Label(inf,text=a["desc"],font=self.fs,fg=self.FGD,bg=bg,anchor="w").pack(fill="x")

    # ═══════════ CAREERS ═══════════
    def show_careers(self):
        self._clear(); self._tabs(4)
        tk.Label(self.sf,text="💼 CYBERSECURITY CAREER PATHS",font=self.fh,fg="#ffcc00",bg=self.BG).pack(anchor="w",pady=(0,3))
        tk.Label(self.sf,text="Where CyberQuest skills lead in the real world.",font=self.fs,fg=self.FGD,bg=self.BG).pack(anchor="w",pady=(0,8))
        for career in CAREERS:
            cd=tk.Frame(self.sf,bg=self.BG2,highlightbackground=self.BRD,highlightthickness=1); cd.pack(fill="x",pady=3)
            inn=tk.Frame(cd,bg=self.BG2); inn.pack(fill="x",padx=12,pady=8)
            top=tk.Frame(inn,bg=self.BG2); top.pack(fill="x")
            tk.Label(top,text=career["title"],font=self.fb,fg=self.FGB,bg=self.BG2).pack(side="left")
            tk.Label(top,text=career["salary"],font=self.fb,fg=self.ACC,bg=self.BG2).pack(side="right")
            tk.Label(inn,text=career["desc"],font=self.fs,fg=self.FG,bg=self.BG2,wraplength=680,justify="left",anchor="w").pack(fill="x",pady=(4,0))
            tk.Label(inn,text=f"Skills: {career['skills']}",font=self.fs,fg=self.FGD,bg=self.BG2,wraplength=680,justify="left",anchor="w").pack(fill="x",pady=(3,0))
            tk.Label(inn,text=f"Certs: {career['certs']}",font=self.fs,fg="#ffcc00",bg=self.BG2,anchor="w").pack(fill="x",pady=(2,0))
            tree_icons = " ".join(SKILL_TREES[t]["icon"] for t in career.get("trees",[]) if t in SKILL_TREES)
            tk.Label(inn,text=f"Related skill trees: {tree_icons}",font=self.fs,fg=self.FGD,bg=self.BG2,anchor="w").pack(fill="x",pady=(2,0))

# ═══════════════════ LAUNCH ═══════════════════

def main():
    root = tk.Tk()
    try:
        import ctypes; root.update()
        ctypes.windll.dwmapi.DwmSetWindowAttribute(ctypes.windll.user32.GetParent(root.winfo_id()),20,ctypes.byref(ctypes.c_int(1)),ctypes.sizeof(ctypes.c_int))
    except: pass
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
