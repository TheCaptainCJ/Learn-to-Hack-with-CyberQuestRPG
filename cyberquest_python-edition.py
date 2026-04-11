"""
╔═══════════════════════════════════════════════════════╗
║     CYBERQUEST: PYTHON LEARNER EDITION                ║
║     From Beginner to Advanced — The Hacker Way        ║
║     Learn Python Like You're Building Exploits        ║
╚═══════════════════════════════════════════════════════╝

Requirements: Python 3.8+ (uses only standard library)
Run: python cyberquest_python.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import json
import os
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import tempfile

# ══════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════

SAVE_DIR = Path.home() / ".cyberquest"
SAVE_FILE = SAVE_DIR / "python_savegame.json"

def load_save():
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"completed_quests": [], "notes": {}, "started_date": datetime.now().isoformat()}

def write_save(data):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ══════════════════════════════════════════════════════
# GAME DATA
# ══════════════════════════════════════════════════════

SKILL_TREES = {
    "fundamentals": {"name": "Core Fundamentals",    "icon": "🐍", "color": "#00ff88"},
    "datastructs":  {"name": "Data Structures",      "icon": "📦", "color": "#00ccff"},
    "functions":    {"name": "Functions & Logic",     "icon": "⚙️",  "color": "#ff9900"},
    "oop":          {"name": "Object-Oriented",       "icon": "🏗️", "color": "#cc44ff"},
    "files":        {"name": "Files & Data",          "icon": "📂", "color": "#ff6600"},
    "modules":      {"name": "Modules & Libraries",   "icon": "📚", "color": "#4488ff"},
    "advanced":     {"name": "Advanced Python",        "icon": "🧠", "color": "#ff2266"},
    "projects":     {"name": "Build Projects",         "icon": "🚀", "color": "#ffcc00"},
}

RANKS = [
    {"level": 1,  "title": "Print Statement",    "xp": 0},
    {"level": 2,  "title": "Variable Wrangler",  "xp": 120},
    {"level": 3,  "title": "Loop Runner",        "xp": 300},
    {"level": 4,  "title": "Function Forger",     "xp": 550},
    {"level": 5,  "title": "Class Architect",     "xp": 900},
    {"level": 6,  "title": "Module Master",       "xp": 1350},
    {"level": 7,  "title": "Exception Handler",   "xp": 1900},
    {"level": 8,  "title": "Generator Guru",      "xp": 2600},
    {"level": 9,  "title": "Decorator Wizard",    "xp": 3500},
    {"level": 10, "title": "Pythonista",           "xp": 4500},
]

ALL_QUESTS = [
    # ═══════════════════════════════════════════════
    # CORE FUNDAMENTALS — Tier 1
    # ═══════════════════════════════════════════════
    {
        "id": "f01", "tree": "fundamentals", "tier": 1, "xp": 20,
        "title": "Hello, Hacker",
        "brief": "Your first Python program",
        "mission": """═══ MISSION — Hello, Hacker ═══

Every journey starts with a single print statement.

► OBJECTIVES:
  1. Open a terminal and type: python
     You're now in the Python REPL (Read-Eval-Print Loop).

  2. Type these one at a time and observe:
     >>> print("Hello, Hacker!")
     >>> print("I am learning Python")
     >>> print(2 + 2)
     >>> print("My name is " + "Captain")

  3. Now create your first script file:
     - Open a text editor (Notepad, VS Code, nano — anything)
     - Save this as hello.py:

       # My first Python program
       print("=== CyberQuest Python Academy ===")
       print("Agent codename: [your name]")
       print("Status: Online")
       print("Mission: Learn Python")

  4. Run it: python hello.py

► KEY CONCEPTS:
  - print() is a FUNCTION — it outputs text to the screen
  - Text in quotes is called a STRING
  - The # symbol starts a COMMENT (Python ignores it)
  - Python runs code TOP to BOTTOM, line by line

► WHY THIS MATTERS:
  Every hacking tool, every script, every automation starts
  exactly like this. Metasploit modules? Python. Nmap scripts?
  Written in scripting languages. Web scrapers? Python.

► CHALLENGE (+5 XP):
  Make your script print a box using characters:
  +---------------------------+
  |  Agent: [name]            |
  |  Status: ACTIVE           |
  +---------------------------+""",
        "sandbox": 'print("Hello, Hacker!")\nprint("I am learning Python")\nprint(2 + 2)',
    },
    {
        "id": "f02", "tree": "fundamentals", "tier": 1, "xp": 25,
        "title": "Variable Vault",
        "brief": "Store and manipulate data with variables",
        "mission": """═══ MISSION — Variable Vault ═══

Variables are containers that hold data. They're the memory of
your program.

► OBJECTIVES:
  1. Create variables of different types:

     name = "Captain"          # String (text)
     age = 25                  # Integer (whole number)
     height = 5.9              # Float (decimal)
     is_hacker = True          # Boolean (True/False)

  2. Print them with f-strings (formatted strings):
     print(f"Name: {name}")
     print(f"Age: {age}")
     print(f"Hacker: {is_hacker}")

  3. Do math with variables:
     x = 10
     y = 3
     print(f"Add: {x + y}")       # 13
     print(f"Subtract: {x - y}")  # 7
     print(f"Multiply: {x * y}")  # 30
     print(f"Divide: {x / y}")    # 3.333...
     print(f"Floor div: {x // y}")# 3
     print(f"Modulo: {x % y}")    # 1 (remainder)
     print(f"Power: {x ** y}")    # 1000

  4. Check types:
     print(type(name))    # <class 'str'>
     print(type(age))     # <class 'int'>
     print(type(height))  # <class 'float'>
     print(type(is_hacker))  # <class 'bool'>

► KEY CONCEPTS:
  - Variables are created with = (assignment)
  - Python figures out the type automatically (dynamic typing)
  - f"text {variable}" lets you embed variables in strings
  - Variable names: lowercase, underscores, no spaces, no
    starting with numbers

► HACKER CONNECTION:
  Every exploit script stores target IPs, ports, payloads in
  variables. When you see target_ip = "192.168.1.1" in a
  pentest script, that's exactly what you just learned.

► CHALLENGE (+5 XP):
  Create a "target profile" script that stores and prints:
  target_ip, target_port, protocol, vulnerability_name, severity_score""",
        "sandbox": 'name = "Captain"\nage = 25\nis_hacker = True\n\nprint(f"Agent: {name}")\nprint(f"Age: {age}")\nprint(f"Hacker: {is_hacker}")\nprint(f"Name type: {type(name)}")',
    },
    {
        "id": "f03", "tree": "fundamentals", "tier": 1, "xp": 25,
        "title": "Input Interceptor",
        "brief": "Get user input and make decisions",
        "mission": """═══ MISSION — Input Interceptor ═══

Programs that just print are boring. Let's make Python LISTEN.

► OBJECTIVES:
  1. Get input from the user:
     name = input("Enter your codename: ")
     print(f"Welcome, Agent {name}")

  2. Convert input types (input() always returns a string):
     age_str = input("Enter your age: ")
     age = int(age_str)           # Convert to integer
     print(f"In 10 years you'll be {age + 10}")

  3. One-liner conversion:
     port = int(input("Target port: "))
     print(f"Scanning port {port}...")

  4. Build an interactive script — save as interrogator.py:

     print("=== SYSTEM INTERROGATOR ===")
     target = input("Target IP: ")
     port = int(input("Port number: "))
     protocol = input("Protocol (tcp/udp): ")

     print(f"\\n--- Scan Configuration ---")
     print(f"Target:   {target}")
     print(f"Port:     {port}")
     print(f"Protocol: {protocol}")
     print(f"Command:  nmap -s{'T' if protocol == 'tcp' else 'U'} -p {port} {target}")

► KEY CONCEPTS:
  - input("prompt") pauses and waits for the user to type
  - It ALWAYS returns a string — convert with int() or float()
  - int("abc") will CRASH — you'll learn to handle that later
  - You can chain: int(input("Number: "))

► HACKER CONNECTION:
  Every interactive tool asks for input — target addresses,
  port ranges, wordlist paths. This is the foundation of
  building your own custom tools.

► CHALLENGE (+5 XP):
  Build a "password strength checker" that asks for a password
  and prints its length, whether it has numbers, and whether
  it's longer than 8 characters.""",
        "sandbox": 'name = input("Enter your codename: ")\nprint(f"Welcome, Agent {name}")\n\nport = int(input("Target port: "))\nprint(f"Scanning port {port}...")',
    },

    # ═══════════════════════════════════════════════
    # CORE FUNDAMENTALS — Tier 1 (continued)
    # ═══════════════════════════════════════════════
    {
        "id": "f04", "tree": "fundamentals", "tier": 1, "xp": 30,
        "title": "Decision Matrix",
        "brief": "Control flow with if/elif/else",
        "mission": """═══ MISSION — Decision Matrix ═══

Programs need to make decisions. Time to teach Python to think.

► OBJECTIVES:
  1. Basic if statement:
     password = input("Enter password: ")
     if password == "letmein":
         print("ACCESS GRANTED")
     else:
         print("ACCESS DENIED")

  2. Multiple conditions with elif:
     score = int(input("Security score (0-100): "))
     if score >= 90:
         print("Rating: CRITICAL — Patch immediately!")
     elif score >= 70:
         print("Rating: HIGH — Patch within 24 hours")
     elif score >= 40:
         print("Rating: MEDIUM — Schedule patch")
     else:
         print("Rating: LOW — Monitor only")

  3. Combining conditions with and, or, not:
     age = int(input("Age: "))
     has_cert = input("Has certification? (y/n): ") == "y"

     if age >= 18 and has_cert:
         print("Cleared for penetration testing")
     elif age >= 18 and not has_cert:
         print("Needs certification first")
     else:
         print("Must be 18+ for this role")

  4. Comparison operators:
     ==  (equals)         !=  (not equals)
     >   (greater than)   <   (less than)
     >=  (greater/equal)  <=  (less/equal)

► KEY CONCEPTS:
  - Indentation MATTERS in Python (4 spaces or 1 tab)
  - if/elif/else must end with a colon :
  - == checks equality, = assigns a value (common mistake!)
  - and, or, not combine conditions
  - Code blocks are defined by indentation, not brackets

► CHALLENGE (+10 XP):
  Build a "vulnerability scanner simulator" that asks for:
  port number, service name, version — then uses if/elif
  to classify the risk level based on known bad versions
  (e.g., Apache 2.4.49 = CRITICAL).""",
        "sandbox": 'password = "letmein"\nguess = input("Enter password: ")\n\nif guess == password:\n    print("ACCESS GRANTED")\nelse:\n    print("ACCESS DENIED")\n    print(f"Attempts remaining: 2")',
    },
    {
        "id": "f05", "tree": "fundamentals", "tier": 1, "xp": 30,
        "title": "Loop Breaker",
        "brief": "Repeat actions with for and while loops",
        "mission": """═══ MISSION — Loop Breaker ═══

Why type something 100 times when a loop does it instantly?

► OBJECTIVES:
  1. For loop — iterate over a sequence:
     for i in range(5):
         print(f"Scanning port {i + 1}...")

  2. Loop through a list:
     targets = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
     for ip in targets:
         print(f"Pinging {ip}...")

  3. While loop — repeat until a condition is false:
     attempts = 0
     max_attempts = 3
     while attempts < max_attempts:
         password = input("Password: ")
         if password == "secret":
             print("ACCESS GRANTED")
             break
         attempts += 1
         print(f"Wrong! {max_attempts - attempts} attempts left")
     else:
         print("ACCOUNT LOCKED")

  4. Useful loop patterns:
     # range(start, stop, step)
     for port in range(80, 90):
         print(f"Port {port}: scanning...")

     # enumerate gives you index + value
     services = ["ssh", "http", "ftp", "smtp"]
     for i, svc in enumerate(services):
         print(f"{i+1}. {svc}")

     # break = exit loop early
     # continue = skip to next iteration

► KEY CONCEPTS:
  - for loops: iterate a known number of times
  - while loops: repeat until a condition changes
  - range(n) generates 0, 1, 2, ... n-1
  - break exits the loop, continue skips current iteration
  - Infinite loop: while True: (use break to escape!)

► CHALLENGE (+10 XP):
  Build a "brute force simulator" that tries passwords from
  a list against a stored password. Print each attempt and
  whether it succeeded. Count total attempts.""",
        "sandbox": 'targets = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]\n\nfor ip in targets:\n    print(f"[*] Scanning {ip}...")\n    for port in range(80, 85):\n        print(f"    Port {port}: open")\n\nprint("\\nScan complete!")',
    },

    # ═══════════════════════════════════════════════
    # DATA STRUCTURES — Tier 1
    # ═══════════════════════════════════════════════
    {
        "id": "d01", "tree": "datastructs", "tier": 1, "xp": 30,
        "title": "List Arsenal",
        "brief": "Master Python lists — your data armory",
        "mission": """═══ MISSION — List Arsenal ═══

Lists are ordered, mutable collections. Your go-to data container.

► OBJECTIVES:
  1. Create and access lists:
     ports = [22, 80, 443, 8080, 3306]
     print(ports[0])      # 22 (first item)
     print(ports[-1])     # 3306 (last item)
     print(ports[1:3])    # [80, 443] (slice)

  2. Modify lists:
     ports.append(8443)         # Add to end
     ports.insert(0, 21)        # Insert at position
     ports.remove(80)           # Remove by value
     popped = ports.pop()       # Remove & return last
     ports.sort()               # Sort in place
     ports.reverse()            # Reverse in place

  3. List operations:
     a = [1, 2, 3]
     b = [4, 5, 6]
     combined = a + b           # [1,2,3,4,5,6]
     print(len(ports))          # Length
     print(80 in ports)         # True/False membership
     print(min(ports), max(ports))

  4. List comprehension (powerful shorthand):
     # Old way:
     squares = []
     for x in range(10):
         squares.append(x ** 2)

     # List comprehension:
     squares = [x ** 2 for x in range(10)]

     # With filter:
     high_ports = [p for p in ports if p > 1024]

► HACKER CONNECTION:
  Port lists, IP ranges, wordlists, scan results — all stored
  as lists. List comprehension is used everywhere in real tools.

► CHALLENGE (+10 XP):
  Create a port scanner simulator: start with a list of common
  ports, let the user add/remove ports, then "scan" each one
  and randomly report open/closed.""",
        "sandbox": 'ports = [21, 22, 80, 443, 8080]\nprint(f"Scanning {len(ports)} ports...")\n\nfor port in sorted(ports):\n    status = "OPEN" if port in [22, 80, 443] else "CLOSED"\n    print(f"  Port {port}: {status}")\n\nhigh_ports = [p for p in ports if p > 1024]\nprint(f"\\nHigh ports: {high_ports}")',
    },
    {
        "id": "d02", "tree": "datastructs", "tier": 1, "xp": 30,
        "title": "Dictionary Decoder",
        "brief": "Key-value pairs — the hacker's database",
        "mission": """═══ MISSION — Dictionary Decoder ═══

Dictionaries store data as key:value pairs. Think of them as
mini databases.

► OBJECTIVES:
  1. Create and access:
     target = {
         "ip": "192.168.1.100",
         "hostname": "web-server-01",
         "os": "Ubuntu 22.04",
         "ports": [22, 80, 443],
         "vulnerable": True
     }
     print(target["ip"])
     print(target.get("os", "Unknown"))

  2. Modify:
     target["status"] = "compromised"    # Add new key
     target["os"] = "Ubuntu 24.04"       # Update value
     del target["vulnerable"]             # Delete key

  3. Iterate:
     for key, value in target.items():
         print(f"  {key}: {value}")

  4. Nested dictionaries:
     network = {
         "192.168.1.1": {"hostname": "router", "ports": [80, 443]},
         "192.168.1.100": {"hostname": "web-srv", "ports": [22, 80]},
         "192.168.1.200": {"hostname": "db-srv", "ports": [3306]},
     }
     for ip, info in network.items():
         print(f"{ip} ({info['hostname']}): {info['ports']}")

► KEY CONCEPTS:
  - Keys must be unique and immutable (strings, numbers, tuples)
  - Values can be anything — even other dicts or lists
  - .get(key, default) is safer than [key] (won't crash)
  - Dictionaries are UNORDERED (but preserve insertion order 3.7+)

► CHALLENGE (+10 XP):
  Build a "host inventory" tool: let the user add hosts with
  IP, hostname, OS, and open ports. Store them in a dict of
  dicts. Add a search function by IP or hostname.""",
        "sandbox": 'target = {\n    "ip": "192.168.1.100",\n    "hostname": "web-server-01",\n    "os": "Ubuntu 22.04",\n    "ports": [22, 80, 443]\n}\n\nprint("=== Target Profile ===")\nfor key, value in target.items():\n    print(f"  {key}: {value}")',
    },

    # ═══════════════════════════════════════════════
    # FUNCTIONS & LOGIC — Tier 2
    # ═══════════════════════════════════════════════
    {
        "id": "fn01", "tree": "functions", "tier": 2, "xp": 40,
        "title": "Function Factory",
        "brief": "Write reusable code blocks",
        "mission": """═══ MISSION — Function Factory ═══

Functions are reusable blocks of code. Write once, use everywhere.

► OBJECTIVES:
  1. Basic function:
     def greet(name):
         print(f"Welcome, Agent {name}!")

     greet("Captain")
     greet("Shadow")

  2. Return values:
     def classify_port(port):
         if port < 1024:
             return "well-known"
         elif port < 49152:
             return "registered"
         else:
             return "dynamic"

     result = classify_port(80)
     print(f"Port 80 is {result}")

  3. Default parameters:
     def scan(target, ports=[80, 443], timeout=5):
         print(f"Scanning {target}")
         print(f"Ports: {ports}")
         print(f"Timeout: {timeout}s")

     scan("192.168.1.1")
     scan("10.0.0.1", ports=[22, 80, 8080], timeout=10)

  4. Multiple return values:
     def analyze_password(password):
         length = len(password)
         has_upper = any(c.isupper() for c in password)
         has_digit = any(c.isdigit() for c in password)
         has_special = any(c in "!@#$%^&*" for c in password)
         score = sum([length >= 8, has_upper, has_digit, has_special])
         return score, length

     score, length = analyze_password("P@ssw0rd!")
     print(f"Score: {score}/4, Length: {length}")

► KEY CONCEPTS:
  - def keyword defines a function
  - Parameters go in parentheses
  - return sends a value back to the caller
  - Functions should do ONE thing well (single responsibility)

► CHALLENGE (+10 XP):
  Build a mini toolkit with functions: port_classifier(),
  ip_validator(), password_scorer(). Call them from a menu.""",
        "sandbox": 'def classify_port(port):\n    if port < 1024:\n        return "well-known"\n    elif port < 49152:\n        return "registered"\n    return "dynamic"\n\nports = [22, 80, 443, 3306, 8080, 50000]\nfor p in ports:\n    category = classify_port(p)\n    print(f"Port {p}: {category}")',
    },
    {
        "id": "fn02", "tree": "functions", "tier": 2, "xp": 40,
        "title": "Error Wrangler",
        "brief": "Handle errors gracefully with try/except",
        "mission": """═══ MISSION — Error Wrangler ═══

Programs crash. Good programs crash GRACEFULLY.

► OBJECTIVES:
  1. Basic try/except:
     try:
         port = int(input("Port: "))
         print(f"Scanning port {port}")
     except ValueError:
         print("Error: That's not a valid number!")

  2. Multiple exception types:
     try:
         targets = ["192.168.1.1", "10.0.0.1"]
         index = int(input("Target index: "))
         print(f"Selected: {targets[index]}")
     except ValueError:
         print("Enter a number!")
     except IndexError:
         print(f"Index must be 0-{len(targets)-1}")

  3. Finally block (always runs):
     try:
         f = open("scan_results.txt", "r")
         data = f.read()
     except FileNotFoundError:
         print("File not found — running first scan")
     finally:
         print("Cleanup complete")

  4. Raising your own errors:
     def set_port(port):
         if not 1 <= port <= 65535:
             raise ValueError(f"Port {port} out of range (1-65535)")
         return port

     try:
         set_port(99999)
     except ValueError as e:
         print(f"Invalid: {e}")

► KEY CONCEPTS:
  - try: code that might fail
  - except: what to do when it fails
  - finally: runs no matter what (cleanup)
  - raise: throw your own error
  - NEVER use bare except: — always catch specific errors

► CHALLENGE (+10 XP):
  Make your previous scripts crash-proof. Wrap all input()
  calls in try/except so bad input doesn't kill the program.""",
        "sandbox": 'def safe_port_input():\n    while True:\n        try:\n            port = int(input("Enter port (1-65535): "))\n            if 1 <= port <= 65535:\n                return port\n            print("Port out of range!")\n        except ValueError:\n            print("Not a valid number!")\n\nport = safe_port_input()\nprint(f"Scanning port {port}...")',
    },

    # ═══════════════════════════════════════════════
    # OOP — Tier 2
    # ═══════════════════════════════════════════════
    {
        "id": "o01", "tree": "oop", "tier": 2, "xp": 50,
        "title": "Class Constructor",
        "brief": "Build your first Python class",
        "mission": """═══ MISSION — Class Constructor ═══

Classes let you create your own data types with built-in behavior.

► OBJECTIVES:
  1. Basic class:
     class Target:
         def __init__(self, ip, hostname, os_name):
             self.ip = ip
             self.hostname = hostname
             self.os_name = os_name
             self.ports = []
             self.compromised = False

         def add_port(self, port):
             self.ports.append(port)

         def scan_report(self):
             status = "COMPROMISED" if self.compromised else "SECURE"
             print(f"--- {self.hostname} ({self.ip}) ---")
             print(f"  OS: {self.os_name}")
             print(f"  Ports: {self.ports}")
             print(f"  Status: {status}")

  2. Create objects (instances):
     web = Target("192.168.1.100", "web-srv", "Ubuntu 22.04")
     web.add_port(22)
     web.add_port(80)
     web.add_port(443)
     web.scan_report()

     db = Target("192.168.1.200", "db-srv", "CentOS 8")
     db.add_port(3306)
     db.compromised = True
     db.scan_report()

  3. Special methods:
     class Target:
         # ... previous code ...

         def __str__(self):
             return f"Target({self.ip} - {self.hostname})"

         def __len__(self):
             return len(self.ports)

     print(web)          # Target(192.168.1.100 - web-srv)
     print(len(web))     # 3 (number of ports)

► KEY CONCEPTS:
  - class defines a blueprint, objects are instances
  - __init__ is the constructor (runs when you create an object)
  - self refers to the current instance
  - Methods are functions that belong to a class
  - __str__, __len__, __repr__ are "magic methods"

► CHALLENGE (+15 XP):
  Build a Network class that contains multiple Target objects.
  Add methods: add_target(), remove_target(), scan_all(),
  find_compromised().""",
        "sandbox": 'class Target:\n    def __init__(self, ip, hostname):\n        self.ip = ip\n        self.hostname = hostname\n        self.ports = []\n\n    def add_port(self, port):\n        self.ports.append(port)\n\n    def report(self):\n        print(f"{self.hostname} ({self.ip}): {self.ports}")\n\nsrv = Target("192.168.1.100", "web-srv")\nsrv.add_port(22)\nsrv.add_port(80)\nsrv.report()',
    },
    {
        "id": "o02", "tree": "oop", "tier": 2, "xp": 50,
        "title": "Inheritance Chain",
        "brief": "Extend classes with inheritance",
        "mission": """═══ MISSION — Inheritance Chain ═══

Inheritance lets you build specialized classes from general ones.

► OBJECTIVES:
  1. Base class and child class:
     class Scanner:
         def __init__(self, target):
             self.target = target
             self.results = []

         def scan(self):
             raise NotImplementedError("Subclasses must implement scan()")

         def report(self):
             print(f"Results for {self.target}:")
             for r in self.results:
                 print(f"  {r}")

     class PortScanner(Scanner):
         def __init__(self, target, ports):
             super().__init__(target)
             self.ports = ports

         def scan(self):
             for port in self.ports:
                 self.results.append(f"Port {port}: open")

     class VulnScanner(Scanner):
         def __init__(self, target, checks):
             super().__init__(target)
             self.checks = checks

         def scan(self):
             for check in self.checks:
                 self.results.append(f"Vuln check: {check} — PASS")

  2. Use polymorphism:
     scanners = [
         PortScanner("192.168.1.1", [22, 80, 443]),
         VulnScanner("192.168.1.1", ["CVE-2024-1234", "CVE-2024-5678"]),
     ]
     for scanner in scanners:
         scanner.scan()
         scanner.report()

► KEY CONCEPTS:
  - super().__init__() calls the parent constructor
  - Override methods to specialize behavior
  - Polymorphism: same method name, different behavior
  - Use inheritance for "is-a" relationships

► CHALLENGE (+15 XP):
  Add a ServiceScanner subclass that checks for running services.
  Create a ScanSuite class that runs all scanner types.""",
        "sandbox": 'class Scanner:\n    def __init__(self, target):\n        self.target = target\n        self.results = []\n    def report(self):\n        print(f"--- {self.target} ---")\n        for r in self.results:\n            print(f"  {r}")\n\nclass PortScanner(Scanner):\n    def scan(self, ports):\n        for p in ports:\n            self.results.append(f"Port {p}: open")\n\nps = PortScanner("192.168.1.1")\nps.scan([22, 80, 443])\nps.report()',
    },

    # ═══════════════════════════════════════════════
    # FILES & DATA — Tier 2
    # ═══════════════════════════════════════════════
    {
        "id": "fi01", "tree": "files", "tier": 2, "xp": 40,
        "title": "File Operator",
        "brief": "Read, write, and parse files",
        "mission": """═══ MISSION — File Operator ═══

Real tools read config files, parse logs, and save results.

► OBJECTIVES:
  1. Write to a file:
     with open("scan_results.txt", "w") as f:
         f.write("=== Scan Results ===\\n")
         f.write("Port 22: OPEN\\n")
         f.write("Port 80: OPEN\\n")
         f.write("Port 443: CLOSED\\n")

  2. Read a file:
     with open("scan_results.txt", "r") as f:
         content = f.read()
         print(content)

     # Read line by line:
     with open("scan_results.txt", "r") as f:
         for line in f:
             print(line.strip())

  3. Append to a file:
     with open("scan_results.txt", "a") as f:
         f.write("Port 8080: OPEN\\n")

  4. Work with CSV data:
     import csv

     # Write CSV
     with open("hosts.csv", "w", newline="") as f:
         writer = csv.writer(f)
         writer.writerow(["IP", "Hostname", "Status"])
         writer.writerow(["192.168.1.1", "router", "up"])
         writer.writerow(["192.168.1.100", "web-srv", "up"])

     # Read CSV
     with open("hosts.csv", "r") as f:
         reader = csv.reader(f)
         for row in reader:
             print(row)

  5. JSON files:
     import json

     data = {"target": "192.168.1.1", "ports": [22, 80]}
     with open("config.json", "w") as f:
         json.dump(data, f, indent=2)

     with open("config.json", "r") as f:
         loaded = json.load(f)
         print(loaded["target"])

► KEY CONCEPTS:
  - with open() as f: auto-closes the file (best practice)
  - "w" = write (overwrites), "a" = append, "r" = read
  - CSV for tabular data, JSON for structured data
  - Always use with statement — never leave files open

► CHALLENGE (+10 XP):
  Build a log parser that reads a sample auth.log file,
  counts failed login attempts per IP, and saves the
  results to a JSON file.""",
        "sandbox": 'import json\n\nscan = {\n    "target": "192.168.1.1",\n    "ports": [22, 80, 443],\n    "status": "complete"\n}\n\n# Save\nwith open("scan.json", "w") as f:\n    json.dump(scan, f, indent=2)\n    print("Saved scan.json")\n\n# Load\nwith open("scan.json", "r") as f:\n    loaded = json.load(f)\n    print(f"Target: {loaded[\'target\']}")\n    print(f"Ports: {loaded[\'ports\']}")',
    },

    # ═══════════════════════════════════════════════
    # MODULES & LIBRARIES — Tier 2
    # ═══════════════════════════════════════════════
    {
        "id": "m01", "tree": "modules", "tier": 2, "xp": 45,
        "title": "Module Hunter",
        "brief": "Import and use Python's standard library",
        "mission": """═══ MISSION — Module Hunter ═══

Python's standard library is massive. Learn to wield it.

► OBJECTIVES:
  1. os module — interact with the operating system:
     import os
     print(os.getcwd())            # Current directory
     print(os.listdir("."))        # List files
     print(os.path.exists("scan.txt"))  # Check if file exists

  2. sys module — system-specific parameters:
     import sys
     print(sys.version)            # Python version
     print(sys.platform)           # Operating system
     print(sys.argv)               # Command-line arguments

  3. datetime — work with time:
     from datetime import datetime
     now = datetime.now()
     print(f"Scan started: {now.strftime('%Y-%m-%d %H:%M:%S')}")

  4. hashlib — generate hashes:
     import hashlib
     text = "password123"
     md5 = hashlib.md5(text.encode()).hexdigest()
     sha256 = hashlib.sha256(text.encode()).hexdigest()
     print(f"MD5:    {md5}")
     print(f"SHA256: {sha256}")

  5. random & secrets:
     import random
     import secrets
     # random — NOT cryptographically secure
     print(random.randint(1, 100))
     # secrets — cryptographically secure
     token = secrets.token_hex(16)
     print(f"Secure token: {token}")

  6. re — regular expressions:
     import re
     log = "Failed login from 192.168.1.50 at 03:14:22"
     ip = re.search(r'\\d+\\.\\d+\\.\\d+\\.\\d+', log)
     if ip:
         print(f"Found IP: {ip.group()}")

► CHALLENGE (+10 XP):
  Write a script that: hashes a given password with SHA256,
  generates a secure random token, logs the timestamp, and
  saves everything to a JSON file.""",
        "sandbox": 'import hashlib\nimport secrets\nfrom datetime import datetime\n\npassword = "password123"\nhash_val = hashlib.sha256(password.encode()).hexdigest()\ntoken = secrets.token_hex(16)\n\nprint(f"Time: {datetime.now()}")\nprint(f"Password: {password}")\nprint(f"SHA256: {hash_val}")\nprint(f"Token: {token}")',
    },

    # ═══════════════════════════════════════════════
    # ADVANCED — Tier 3
    # ═══════════════════════════════════════════════
    {
        "id": "a01", "tree": "advanced", "tier": 3, "xp": 60,
        "title": "Lambda & Comprehension",
        "brief": "Write concise, powerful one-liners",
        "mission": """═══ MISSION — Lambda & Comprehension ═══

Advanced Python is about doing more with less code.

► OBJECTIVES:
  1. Lambda functions (anonymous functions):
     classify = lambda port: "low" if port < 1024 else "high"
     print(classify(80))    # "low"
     print(classify(8080))  # "high"

  2. map, filter, sorted with lambda:
     ports = [8080, 22, 443, 21, 3306, 80]

     # Sort by value
     sorted_ports = sorted(ports)

     # Filter high ports
     high = list(filter(lambda p: p > 1024, ports))

     # Transform
     labels = list(map(lambda p: f"port-{p}", ports))

  3. Dictionary comprehension:
     ports = [22, 80, 443, 8080]
     port_status = {p: ("open" if p in [22, 80] else "closed") for p in ports}

  4. Nested comprehension:
     matrix = [[i*j for j in range(5)] for i in range(5)]

  5. Generator expressions (memory efficient):
     # List comp — creates entire list in memory
     big_list = [x**2 for x in range(1000000)]

     # Generator — creates values on demand
     big_gen = (x**2 for x in range(1000000))
     print(next(big_gen))  # 0
     print(next(big_gen))  # 1

► KEY CONCEPTS:
  - Lambda: small throwaway functions
  - Comprehensions: concise list/dict/set creation
  - Generators: lazy evaluation, memory efficient
  - These are Pythonic — use them to write cleaner code

► CHALLENGE (+15 XP):
  Rewrite one of your earlier scripts to use comprehensions
  and lambdas where appropriate. Compare line counts.""",
        "sandbox": 'ports = [8080, 22, 443, 21, 3306, 80, 8443]\n\n# Sort, filter, transform in one chain\nresult = sorted(\n    filter(lambda p: p > 100, ports)\n)\nprint(f"Filtered & sorted: {result}")\n\n# Dict comprehension\nstatus = {p: ("open" if p < 1024 else "filtered") for p in ports}\nfor port, st in status.items():\n    print(f"  {port}: {st}")',
    },
    {
        "id": "a02", "tree": "advanced", "tier": 3, "xp": 60,
        "title": "Decorator Forge",
        "brief": "Modify functions with decorators",
        "mission": """═══ MISSION — Decorator Forge ═══

Decorators wrap functions to add behavior without changing them.

► OBJECTIVES:
  1. Basic decorator:
     def timer(func):
         import time
         def wrapper(*args, **kwargs):
             start = time.time()
             result = func(*args, **kwargs)
             elapsed = time.time() - start
             print(f"[{func.__name__}] took {elapsed:.4f}s")
             return result
         return wrapper

     @timer
     def slow_scan(target):
         import time
         time.sleep(1)
         print(f"Scanned {target}")

     slow_scan("192.168.1.1")

  2. Decorator with arguments:
     def retry(max_attempts=3):
         def decorator(func):
             def wrapper(*args, **kwargs):
                 for attempt in range(1, max_attempts + 1):
                     try:
                         return func(*args, **kwargs)
                     except Exception as e:
                         print(f"Attempt {attempt} failed: {e}")
                 print("All attempts failed!")
             return wrapper
         return decorator

     @retry(max_attempts=3)
     def risky_connection(host):
         import random
         if random.random() < 0.7:
             raise ConnectionError("Connection refused")
         print(f"Connected to {host}!")

  3. Logging decorator:
     def log_call(func):
         def wrapper(*args, **kwargs):
             print(f"[LOG] Calling {func.__name__}({args}, {kwargs})")
             result = func(*args, **kwargs)
             print(f"[LOG] {func.__name__} returned {result}")
             return result
         return wrapper

► KEY CONCEPTS:
  - @ syntax is syntactic sugar for func = decorator(func)
  - *args catches positional args, **kwargs catches keyword args
  - Decorators are used heavily in Flask, Django, pytest
  - Stack multiple decorators: @timer @log_call def func():

► CHALLENGE (+15 XP):
  Create an @authenticate decorator that checks for a valid
  API key before allowing a function to run.""",
        "sandbox": 'import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        elapsed = time.time() - start\n        print(f"[{func.__name__}] {elapsed:.4f}s")\n        return result\n    return wrapper\n\n@timer\ndef scan_ports(target, count=100):\n    # Simulate scan\n    total = sum(range(count * 1000))\n    print(f"Scanned {target}: {count} ports")\n\nscan_ports("192.168.1.1")\nscan_ports("10.0.0.1", count=500)',
    },

    # ═══════════════════════════════════════════════
    # BUILD PROJECTS — Tier 3
    # ═══════════════════════════════════════════════
    {
        "id": "p01", "tree": "projects", "tier": 3, "xp": 80,
        "title": "Password Vault",
        "brief": "Build an encrypted password manager",
        "mission": """═══ MISSION — Password Vault ═══

Combine everything you've learned into a real tool.

► BUILD A PASSWORD MANAGER with these features:

  1. CLASSES:
     - PasswordEntry: stores service, username, encrypted password
     - PasswordVault: manages a collection of entries

  2. ENCRYPTION (simple XOR for learning — NOT production-safe):
     def xor_encrypt(text, key):
         return ''.join(chr(ord(c) ^ ord(key[i % len(key)]))
                        for i, c in enumerate(text))

  3. FILE STORAGE:
     - Save vault to JSON file
     - Load vault on startup
     - Auto-save on changes

  4. USER INTERFACE (terminal menu):
     === Password Vault ===
     1. Add password
     2. View passwords
     3. Search
     4. Generate random password
     5. Export (encrypted)
     6. Quit

  5. PASSWORD GENERATOR:
     import secrets, string
     def generate_password(length=16):
         chars = string.ascii_letters + string.digits + "!@#$%"
         return ''.join(secrets.choice(chars) for _ in range(length))

  6. ERROR HANDLING:
     - Handle missing files gracefully
     - Validate all user input
     - Don't crash on bad data

► REQUIREMENTS:
  - Use classes (OOP)
  - Use file I/O (JSON)
  - Use error handling (try/except)
  - Use at least 3 standard library modules
  - Use list comprehension somewhere

► CHALLENGE (+20 XP):
  Add a "password strength analyzer" that scores each stored
  password and warns about weak ones.""",
        "sandbox": 'import secrets\nimport string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + "!@#$%^&*"\n    return "".join(secrets.choice(chars) for _ in range(length))\n\nprint("=== Password Generator ===")\nfor i in range(5):\n    pw = generate_password(20)\n    strength = len(set(pw)) / len(pw)\n    print(f"  {pw}  (uniqueness: {strength:.0%})")',
    },
    {
        "id": "p02", "tree": "projects", "tier": 3, "xp": 80,
        "title": "Log Analyzer",
        "brief": "Build a security log analysis tool",
        "mission": """═══ MISSION — Log Analyzer ═══

Build a tool that parses security logs and detects threats.

► BUILD A LOG ANALYZER with these features:

  1. LOG PARSER:
     - Read log files line by line
     - Extract: timestamp, source IP, event type, message
     - Use regex (re module) for pattern matching

  2. DETECTION RULES:
     - Brute force: 5+ failed logins from same IP in 5 minutes
     - Port scan: connections to 10+ different ports from same IP
     - Privilege escalation: sudo commands from unexpected users
     - Anomaly: logins at unusual hours (2-5 AM)

  3. SAMPLE LOG GENERATOR:
     import random
     from datetime import datetime, timedelta

     def generate_sample_logs(count=100):
         events = []
         ips = ["192.168.1." + str(i) for i in range(50, 60)]
         for _ in range(count):
             ip = random.choice(ips)
             event = random.choice(["LOGIN_OK", "LOGIN_FAIL",
                                     "SUDO", "PORT_CONNECT"])
             time = datetime.now() - timedelta(
                 minutes=random.randint(0, 1440))
             events.append(f"{time},{ip},{event}")
         return events

  4. REPORTING:
     - Summary: total events, unique IPs, threat count
     - Per-IP breakdown of suspicious activity
     - Save report to file (JSON and/or text)

  5. ARCHITECTURE:
     class LogEntry: parse a single log line
     class RuleEngine: apply detection rules
     class Analyzer: orchestrate parsing + rules + reporting

► REQUIREMENTS:
  - Use OOP with at least 3 classes
  - Use file I/O for reading logs and saving reports
  - Use re module for pattern matching
  - Use datetime for time-based analysis
  - Use collections.Counter for aggregation

► CHALLENGE (+20 XP):
  Add a "live mode" that watches a log file for new entries
  (tail -f style) and alerts in real-time.""",
        "sandbox": 'import random\nfrom datetime import datetime, timedelta\nfrom collections import Counter\n\n# Generate sample logs\nips = [f"192.168.1.{i}" for i in range(50, 55)]\nevents = []\nfor _ in range(50):\n    ip = random.choice(ips)\n    event = random.choice(["LOGIN_OK", "LOGIN_FAIL", "LOGIN_FAIL", "SUDO"])\n    events.append({"ip": ip, "event": event})\n\n# Analyze\nfail_counts = Counter(e["ip"] for e in events if e["event"] == "LOGIN_FAIL")\n\nprint("=== Brute Force Detection ===")\nfor ip, count in fail_counts.most_common():\n    flag = " ⚠️ ALERT!" if count >= 5 else ""\n    print(f"  {ip}: {count} failures{flag}")',
    },
]


def get_achievements(completed):
    return [
        {"id": "first_quest", "name": "First Line", "desc": "Complete your first quest", "icon": "🐣",
         "check": lambda q: len(q) >= 1},
        {"id": "five_quests", "name": "Getting Hooked", "desc": "Complete 5 quests", "icon": "🎣",
         "check": lambda q: len(q) >= 5},
        {"id": "ten_quests", "name": "Double Digits", "desc": "Complete 10 quests", "icon": "🔟",
         "check": lambda q: len(q) >= 10},
        {"id": "all_trees", "name": "Full Stack Pythonista", "desc": "Quest in every skill tree", "icon": "🌟",
         "check": lambda q: all(any(next((aq for aq in ALL_QUESTS if aq["id"] == qid), {}).get("tree") == t for qid in q) for t in SKILL_TREES)},
        {"id": "tier2", "name": "Intermediate", "desc": "Complete a Tier 2 quest", "icon": "📈",
         "check": lambda q: any(next((aq for aq in ALL_QUESTS if aq["id"] == qid), {}).get("tier", 0) >= 2 for qid in q)},
        {"id": "tier3", "name": "Advanced Operator", "desc": "Complete a Tier 3 quest", "icon": "💎",
         "check": lambda q: any(next((aq for aq in ALL_QUESTS if aq["id"] == qid), {}).get("tier", 0) >= 3 for qid in q)},
        {"id": "fund_done", "name": "Solid Foundation", "desc": "Complete all Fundamentals", "icon": "🏛️",
         "check": lambda q: all(aq["id"] in q for aq in ALL_QUESTS if aq["tree"] == "fundamentals")},
        {"id": "oop_done", "name": "Object Oriented", "desc": "Complete all OOP quests", "icon": "🏗️",
         "check": lambda q: all(aq["id"] in q for aq in ALL_QUESTS if aq["tree"] == "oop")},
        {"id": "project_done", "name": "Builder", "desc": "Complete a project quest", "icon": "🚀",
         "check": lambda q: any(next((aq for aq in ALL_QUESTS if aq["id"] == qid), {}).get("tree") == "projects" for qid in q)},
        {"id": "all_done", "name": "Python Master", "desc": "Complete ALL quests", "icon": "👑",
         "check": lambda q: len(q) >= len(ALL_QUESTS)},
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


def total_xp(completed):
    return sum(q["xp"] for q in ALL_QUESTS if q["id"] in completed)


def tree_xp(completed, tree):
    return sum(q["xp"] for q in ALL_QUESTS if q["id"] in completed and q["tree"] == tree)


# ══════════════════════════════════════════════════════
# GUI APPLICATION
# ══════════════════════════════════════════════════════

class CyberQuestPython:
    BG = "#0a0a0f"
    BG_CARD = "#111118"
    BG_HOVER = "#1a1a24"
    BG_INPUT = "#15151f"
    BG_CODE = "#08080e"
    FG = "#cccccc"
    FG_DIM = "#555566"
    FG_BRIGHT = "#ffffff"
    ACCENT = "#00ff88"
    ACCENT_DIM = "#00cc66"
    ACCENT_BLUE = "#4488ff"
    BORDER = "#222233"
    COMPLETED_BG = "#0a1a10"
    CODE_GREEN = "#00ff88"
    CODE_YELLOW = "#ffcc00"
    CODE_BLUE = "#66bbff"

    def __init__(self, root):
        self.root = root
        self.root.title("CyberQuest: Python Learner Edition")
        self.root.configure(bg=self.BG)
        self.root.geometry("960x720")
        self.root.minsize(720, 520)

        self.save_data = load_save()
        self.completed = self.save_data.get("completed_quests", [])
        self.selected_tree = None

        self.font_title = tkfont.Font(family="Consolas", size=22, weight="bold")
        self.font_subtitle = tkfont.Font(family="Consolas", size=9)
        self.font_heading = tkfont.Font(family="Consolas", size=13, weight="bold")
        self.font_normal = tkfont.Font(family="Consolas", size=10)
        self.font_small = tkfont.Font(family="Consolas", size=9)
        self.font_mission = tkfont.Font(family="Consolas", size=10)
        self.font_button = tkfont.Font(family="Consolas", size=10, weight="bold")
        self.font_rank = tkfont.Font(family="Consolas", size=16, weight="bold")
        self.font_xp = tkfont.Font(family="Consolas", size=26, weight="bold")
        self.font_code = tkfont.Font(family="Consolas", size=10)

        self.build_ui()
        self.show_dashboard()

    def build_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.BG)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.header_frame = tk.Frame(self.main_frame, bg=self.BG)
        self.header_frame.pack(fill="x", padx=20, pady=(12, 4))

        title_frame = tk.Frame(self.header_frame, bg=self.BG)
        title_frame.pack()
        tk.Label(title_frame, text="CYBERQUEST", font=self.font_title,
                 fg="#ffcc00", bg=self.BG).pack(side="left")
        tk.Label(title_frame, text=" PYTHON", font=self.font_title,
                 fg=self.ACCENT, bg=self.BG).pack(side="left")
        tk.Label(self.header_frame, text="LEARN PYTHON  •  THE HACKER WAY",
                 font=self.font_subtitle, fg=self.FG_DIM, bg=self.BG).pack()

        # Rank card
        self.rank_frame = tk.Frame(self.main_frame, bg=self.BG_CARD,
                                    highlightbackground="#ffcc00",
                                    highlightthickness=1)
        self.rank_frame.pack(fill="x", padx=20, pady=8)
        self.build_rank_card()

        # Nav
        self.nav_frame = tk.Frame(self.main_frame, bg=self.BG)
        self.nav_frame.pack(fill="x", padx=20, pady=(0, 4))

        self.btn_quests = tk.Button(self.nav_frame, text="🐍  QUESTS", font=self.font_button,
                                    bg=self.BG_CARD, fg=self.ACCENT, activebackground=self.BG_HOVER,
                                    activeforeground=self.ACCENT, bd=0, padx=20, pady=7,
                                    cursor="hand2", command=self.show_dashboard)
        self.btn_quests.pack(side="left", expand=True, fill="x", padx=(0, 2))

        self.btn_achievements = tk.Button(self.nav_frame, text="🏆  ACHIEVEMENTS", font=self.font_button,
                                           bg=self.BG_CARD, fg=self.FG_DIM, activebackground=self.BG_HOVER,
                                           activeforeground=self.ACCENT, bd=0, padx=20, pady=7,
                                           cursor="hand2", command=self.show_achievements)
        self.btn_achievements.pack(side="left", expand=True, fill="x", padx=(2, 2))

        self.btn_sandbox = tk.Button(self.nav_frame, text="⚡  SANDBOX", font=self.font_button,
                                      bg=self.BG_CARD, fg=self.FG_DIM, activebackground=self.BG_HOVER,
                                      activeforeground="#ffcc00", bd=0, padx=20, pady=7,
                                      cursor="hand2", command=self.show_sandbox)
        self.btn_sandbox.pack(side="left", expand=True, fill="x", padx=(2, 0))

        # Content
        self.content_container = tk.Frame(self.main_frame, bg=self.BG)
        self.content_container.pack(fill="both", expand=True, padx=20, pady=(4, 10))

        self.canvas = tk.Canvas(self.content_container, bg=self.BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.content_container, orient="vertical",
                                       command=self.canvas.yview, bg=self.BG_CARD,
                                       troughcolor=self.BG)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.BG)

        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def build_rank_card(self):
        for w in self.rank_frame.winfo_children():
            w.destroy()

        xp = total_xp(self.completed)
        rank = get_rank(xp)
        next_r = get_next_rank(xp)

        inner = tk.Frame(self.rank_frame, bg=self.BG_CARD)
        inner.pack(fill="x", padx=15, pady=10)

        top = tk.Frame(inner, bg=self.BG_CARD)
        top.pack(fill="x")

        left = tk.Frame(top, bg=self.BG_CARD)
        left.pack(side="left")
        tk.Label(left, text=f"LEVEL {rank['level']}", font=self.font_small,
                 fg="#ffcc00", bg=self.BG_CARD).pack(anchor="w")
        tk.Label(left, text=rank["title"], font=self.font_rank,
                 fg=self.FG_BRIGHT, bg=self.BG_CARD).pack(anchor="w")

        right = tk.Frame(top, bg=self.BG_CARD)
        right.pack(side="right")
        xp_frame = tk.Frame(right, bg=self.BG_CARD)
        xp_frame.pack(anchor="e")
        tk.Label(xp_frame, text=str(xp), font=self.font_xp,
                 fg=self.FG_BRIGHT, bg=self.BG_CARD).pack(side="left")
        tk.Label(xp_frame, text=" XP", font=self.font_heading,
                 fg="#ffcc00", bg=self.BG_CARD).pack(side="left", pady=(6, 0))

        if next_r:
            prog_frame = tk.Frame(inner, bg=self.BG_CARD)
            prog_frame.pack(fill="x", pady=(6, 0))

            lf = tk.Frame(prog_frame, bg=self.BG_CARD)
            lf.pack(fill="x")
            tk.Label(lf, text=rank["title"], font=self.font_small,
                     fg=self.FG_DIM, bg=self.BG_CARD).pack(side="left")
            tk.Label(lf, text=f"{next_r['title']} — {next_r['xp'] - xp} XP to go",
                     font=self.font_small, fg=self.FG_DIM, bg=self.BG_CARD).pack(side="right")

            bar_bg = tk.Frame(prog_frame, bg=self.BORDER, height=8)
            bar_bg.pack(fill="x", pady=(3, 0))
            bar_bg.pack_propagate(False)
            progress = (xp - rank["xp"]) / max(1, next_r["xp"] - rank["xp"])
            bar_fill = tk.Frame(bar_bg, bg="#ffcc00", height=8)
            bar_fill.place(relwidth=min(progress, 1.0), relheight=1.0)

        cf = tk.Frame(inner, bg=self.BG_CARD)
        cf.pack(fill="x", pady=(6, 0))
        tk.Label(cf, text=f"{len(self.completed)}/{len(ALL_QUESTS)} QUESTS COMPLETE",
                 font=self.font_small, fg=self.FG_DIM, bg=self.BG_CARD).pack()

    def clear_content(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)

    def set_active_tab(self, active):
        self.btn_quests.configure(fg=self.ACCENT if active == "quests" else self.FG_DIM)
        self.btn_achievements.configure(fg=self.ACCENT if active == "achievements" else self.FG_DIM)
        self.btn_sandbox.configure(fg="#ffcc00" if active == "sandbox" else self.FG_DIM)

    # ══════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════

    def show_dashboard(self):
        self.clear_content()
        self.set_active_tab("quests")

        # Filter buttons
        ff = tk.Frame(self.scrollable_frame, bg=self.BG)
        ff.pack(fill="x", pady=(0, 6))

        def set_filter(t):
            self.selected_tree = t
            self.show_dashboard()

        btn_all = tk.Button(ff, text="ALL", font=self.font_small,
                            bg=self.BG_HOVER if not self.selected_tree else self.BG_CARD,
                            fg=self.FG_BRIGHT if not self.selected_tree else self.FG_DIM,
                            bd=0, padx=8, pady=3, cursor="hand2",
                            command=lambda: set_filter(None))
        btn_all.pack(side="left", padx=(0, 2))

        for key, tree in SKILL_TREES.items():
            is_sel = self.selected_tree == key
            b = tk.Button(ff, text=f"{tree['icon']} {tree['name'].split()[0]}",
                          font=self.font_small,
                          bg=self.BG_HOVER if is_sel else self.BG_CARD,
                          fg=tree["color"] if is_sel else self.FG_DIM,
                          bd=0, padx=6, pady=3, cursor="hand2",
                          command=lambda k=key: set_filter(k))
            b.pack(side="left", padx=1)

        # XP bars
        xp_grid = tk.Frame(self.scrollable_frame, bg=self.BG)
        xp_grid.pack(fill="x", pady=(0, 10))

        for i, (key, tree) in enumerate(SKILL_TREES.items()):
            txp = tree_xp(self.completed, key)
            max_xp = sum(q["xp"] for q in ALL_QUESTS if q["tree"] == key)

            cell = tk.Frame(xp_grid, bg=self.BG_CARD, padx=6, pady=5)
            cell.grid(row=i // 4, column=i % 4, sticky="ew", padx=2, pady=2)

            tk.Label(cell, text=f"{tree['icon']} {tree['name']}", font=self.font_small,
                     fg=tree["color"], bg=self.BG_CARD, anchor="w").pack(fill="x")

            bar_bg = tk.Frame(cell, bg=self.BORDER, height=5)
            bar_bg.pack(fill="x", pady=(3, 1))
            bar_bg.pack_propagate(False)
            prog = txp / max(1, max_xp)
            tk.Frame(bar_bg, bg=tree["color"], height=5).place(relwidth=min(prog, 1.0), relheight=1.0)

            tk.Label(cell, text=f"{txp} XP", font=self.font_small,
                     fg=self.FG_DIM, bg=self.BG_CARD, anchor="w").pack(fill="x")

        for c in range(4):
            xp_grid.columnconfigure(c, weight=1)

        # Quests
        available = self._get_available()
        for q in available:
            self._quest_card(q)

        if not available:
            tk.Label(self.scrollable_frame,
                     text="No quests available. Complete lower tiers to unlock.",
                     font=self.font_normal, fg=self.FG_DIM, bg=self.BG, pady=30).pack()

    def _get_available(self):
        quests = []
        for q in ALL_QUESTS:
            if self.selected_tree and q["tree"] != self.selected_tree:
                continue
            if q["tier"] == 1:
                quests.append(q)
            elif q["tier"] == 2:
                if any(cid for cid in self.completed if any(
                    aq["id"] == cid and aq["tree"] == q["tree"] and aq["tier"] == 1 for aq in ALL_QUESTS)):
                    quests.append(q)
            elif q["tier"] == 3:
                if any(cid for cid in self.completed if any(
                    aq["id"] == cid and aq["tree"] == q["tree"] and aq["tier"] == 2 for aq in ALL_QUESTS)):
                    quests.append(q)
        return quests

    def _quest_card(self, quest):
        tree = SKILL_TREES[quest["tree"]]
        done = quest["id"] in self.completed
        bg = self.COMPLETED_BG if done else self.BG_CARD

        card = tk.Frame(self.scrollable_frame, bg=bg, cursor="hand2",
                        highlightbackground=self.ACCENT if done else self.BORDER,
                        highlightthickness=1)
        card.pack(fill="x", pady=2)

        inner = tk.Frame(card, bg=bg)
        inner.pack(fill="x", padx=12, pady=8)

        top = tk.Frame(inner, bg=bg)
        top.pack(fill="x")

        tk.Label(top, text=f"{tree['icon']} T{quest['tier']}", font=self.font_small,
                 fg=tree["color"], bg=bg).pack(side="left")

        title_text = f"  ✓ {quest['title']}" if done else f"  {quest['title']}"
        tk.Label(top, text=title_text, font=self.font_button,
                 fg=self.ACCENT if done else self.FG_BRIGHT, bg=bg).pack(side="left")
        tk.Label(top, text=f"+{quest['xp']} XP", font=self.font_button,
                 fg=tree["color"], bg=bg).pack(side="right")

        tk.Label(inner, text=quest["brief"], font=self.font_small,
                 fg=self.FG_DIM, bg=bg, anchor="w").pack(fill="x", pady=(2, 0))

        for w in [card, inner, top]:
            w.bind("<Button-1>", lambda e, q=quest: self.show_quest(q))
        for w in inner.winfo_children():
            w.bind("<Button-1>", lambda e, q=quest: self.show_quest(q))
        for w in top.winfo_children():
            w.bind("<Button-1>", lambda e, q=quest: self.show_quest(q))

    # ══════════════════════════════════════════════
    # QUEST DETAIL
    # ══════════════════════════════════════════════

    def show_quest(self, quest):
        self.clear_content()
        self.set_active_tab("quests")

        tree = SKILL_TREES[quest["tree"]]
        done = quest["id"] in self.completed

        tk.Button(self.scrollable_frame, text="← Back to Quests",
                  font=self.font_button, bg=self.BG, fg=self.ACCENT,
                  bd=0, cursor="hand2", activebackground=self.BG,
                  activeforeground=self.FG_BRIGHT,
                  command=self.show_dashboard).pack(anchor="w", pady=(0, 8))

        # Header
        hdr = tk.Frame(self.scrollable_frame, bg=self.BG_CARD,
                        highlightbackground=tree["color"], highlightthickness=1)
        hdr.pack(fill="x")

        hi = tk.Frame(hdr, bg=self.BG_CARD)
        hi.pack(fill="x", padx=15, pady=10)

        top = tk.Frame(hi, bg=self.BG_CARD)
        top.pack(fill="x")
        tk.Label(top, text=f"{tree['icon']} {tree['name'].upper()} • TIER {quest['tier']}",
                 font=self.font_small, fg=tree["color"], bg=self.BG_CARD).pack(side="left")
        tk.Label(top, text=f"+{quest['xp']} XP", font=self.font_heading,
                 fg=tree["color"], bg=self.BG_CARD).pack(side="right")
        tk.Label(hi, text=quest["title"], font=self.font_heading,
                 fg=self.FG_BRIGHT, bg=self.BG_CARD, anchor="w").pack(fill="x", pady=(4, 0))

        # Mission
        mf = tk.Frame(self.scrollable_frame, bg=self.BG_CODE,
                       highlightbackground=self.BORDER, highlightthickness=1)
        mf.pack(fill="x", pady=(4, 0))

        mt = tk.Text(mf, font=self.font_mission, bg=self.BG_CODE,
                      fg=self.FG, wrap="word", relief="flat", padx=15, pady=12,
                      height=18)
        mt.pack(fill="both", expand=True)
        mt.insert("1.0", quest["mission"])

        mt.tag_configure("hdr", foreground=tree["color"], font=self.font_button)
        mt.tag_configure("warn", foreground="#ff6688")

        content = mt.get("1.0", "end")
        for i, line in enumerate(content.split("\n"), 1):
            if line.startswith("═══") or line.startswith("►"):
                mt.tag_add("hdr", f"{i}.0", f"{i}.end")
            elif line.startswith("⚠"):
                mt.tag_add("warn", f"{i}.0", f"{i}.end")

        mt.configure(state="disabled")

        # Sandbox button
        if quest.get("sandbox"):
            tk.Button(self.scrollable_frame, text="⚡  OPEN IN SANDBOX",
                      font=self.font_button, bg=self.BG_CARD, fg="#ffcc00",
                      bd=0, pady=8, cursor="hand2",
                      activebackground=self.BG_HOVER,
                      command=lambda: self.show_sandbox(quest["sandbox"])
                      ).pack(fill="x", pady=(6, 0))

        # Complete button
        if not done:
            tk.Button(self.scrollable_frame, text="✓  MARK COMPLETE",
                      font=self.font_heading, bg=self.BG_CARD, fg=tree["color"],
                      bd=0, pady=10, cursor="hand2",
                      activebackground=self.BG_HOVER,
                      command=lambda: self._complete(quest)
                      ).pack(fill="x", pady=(6, 0))
        else:
            tk.Label(self.scrollable_frame, text="✓  COMPLETED", font=self.font_heading,
                     fg=self.ACCENT, bg=self.COMPLETED_BG, pady=10).pack(fill="x", pady=(6, 0))

    def _complete(self, quest):
        if quest["id"] not in self.completed:
            self.completed.append(quest["id"])
            self.save_data["completed_quests"] = self.completed
            write_save(self.save_data)

            new_achs = []
            for a in get_achievements(self.completed):
                if a["check"](self.completed):
                    prev = self.completed[:-1]
                    if not a["check"](prev):
                        new_achs.append(a)

            self.build_rank_card()
            self.show_quest(quest)

            if new_achs:
                txt = "\n".join(f"{a['icon']} {a['name']} — {a['desc']}" for a in new_achs)
                messagebox.showinfo("🏆 Achievement Unlocked!", f"+{quest['xp']} XP!\n\n{txt}")
            else:
                messagebox.showinfo("Quest Complete!",
                    f"+{quest['xp']} XP!\n\nRank: {get_rank(total_xp(self.completed))['title']}")

    # ══════════════════════════════════════════════
    # ACHIEVEMENTS
    # ══════════════════════════════════════════════

    def show_achievements(self):
        self.clear_content()
        self.set_active_tab("achievements")

        all_achs = get_achievements(self.completed)
        earned = sum(1 for a in all_achs if a["check"](self.completed))

        tk.Label(self.scrollable_frame,
                 text=f"{earned}/{len(all_achs)} ACHIEVEMENTS UNLOCKED",
                 font=self.font_heading, fg="#ffcc00", bg=self.BG).pack(pady=(0, 10))

        for a in all_achs:
            is_earned = a["check"](self.completed)
            bg = self.COMPLETED_BG if is_earned else self.BG_CARD

            card = tk.Frame(self.scrollable_frame, bg=bg,
                            highlightbackground=self.ACCENT if is_earned else self.BORDER,
                            highlightthickness=1)
            card.pack(fill="x", pady=2)

            inner = tk.Frame(card, bg=bg)
            inner.pack(fill="x", padx=12, pady=8)

            row = tk.Frame(inner, bg=bg)
            row.pack(fill="x")

            tk.Label(row, text=a["icon"] if is_earned else "🔒",
                     font=self.font_heading, bg=bg).pack(side="left", padx=(0, 10))

            info = tk.Frame(row, bg=bg)
            info.pack(side="left", fill="x")

            tk.Label(info, text=a["name"], font=self.font_button,
                     fg=self.ACCENT if is_earned else self.FG_DIM, bg=bg,
                     anchor="w").pack(fill="x")
            tk.Label(info, text=a["desc"], font=self.font_small,
                     fg=self.FG_DIM, bg=bg, anchor="w").pack(fill="x")

    # ══════════════════════════════════════════════
    # SANDBOX — Run Python code
    # ══════════════════════════════════════════════

    def show_sandbox(self, prefill=""):
        self.clear_content()
        self.set_active_tab("sandbox")

        tk.Label(self.scrollable_frame,
                 text="⚡ PYTHON SANDBOX", font=self.font_heading,
                 fg="#ffcc00", bg=self.BG).pack(anchor="w", pady=(0, 4))
        tk.Label(self.scrollable_frame,
                 text="Write code below and hit RUN. Output appears underneath.",
                 font=self.font_small, fg=self.FG_DIM, bg=self.BG).pack(anchor="w", pady=(0, 8))

        # Code editor
        editor_frame = tk.Frame(self.scrollable_frame, bg=self.BG_CODE,
                                 highlightbackground="#ffcc00", highlightthickness=1)
        editor_frame.pack(fill="x")

        self.code_editor = tk.Text(editor_frame, font=self.font_code, bg=self.BG_CODE,
                                    fg=self.CODE_GREEN, wrap="word", relief="flat",
                                    padx=12, pady=10, insertbackground="#ffcc00",
                                    selectbackground="#333355", height=14)
        self.code_editor.pack(fill="both", expand=True)

        if prefill:
            self.code_editor.insert("1.0", prefill)

        # Buttons
        btn_row = tk.Frame(self.scrollable_frame, bg=self.BG)
        btn_row.pack(fill="x", pady=(6, 0))

        tk.Button(btn_row, text="▶  RUN CODE", font=self.font_heading,
                  bg="#1a2a10", fg=self.ACCENT, bd=0, padx=20, pady=8,
                  cursor="hand2", activebackground=self.BG_HOVER,
                  command=self._run_code).pack(side="left", expand=True, fill="x", padx=(0, 3))

        tk.Button(btn_row, text="🗑  CLEAR", font=self.font_heading,
                  bg=self.BG_CARD, fg=self.FG_DIM, bd=0, padx=20, pady=8,
                  cursor="hand2", activebackground=self.BG_HOVER,
                  command=lambda: (self.code_editor.delete("1.0", "end"),
                                   self.output_text.configure(state="normal"),
                                   self.output_text.delete("1.0", "end"),
                                   self.output_text.configure(state="disabled"))
                  ).pack(side="left", expand=True, fill="x", padx=(3, 0))

        # Output
        tk.Label(self.scrollable_frame, text="OUTPUT:", font=self.font_small,
                 fg=self.FG_DIM, bg=self.BG, anchor="w").pack(fill="x", pady=(8, 2))

        out_frame = tk.Frame(self.scrollable_frame, bg="#050508",
                              highlightbackground=self.BORDER, highlightthickness=1)
        out_frame.pack(fill="x")

        self.output_text = tk.Text(out_frame, font=self.font_code, bg="#050508",
                                    fg="#aaaaaa", wrap="word", relief="flat",
                                    padx=12, pady=10, height=10, state="disabled")
        self.output_text.pack(fill="both", expand=True)

    def _run_code(self):
        code = self.code_editor.get("1.0", "end").strip()
        if not code:
            return

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")

        # Run in subprocess for safety
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True, text=True, timeout=10,
                input="Captain\n80\ntcp\n"  # default inputs for interactive scripts
            )

            output = result.stdout
            if result.stderr:
                output += f"\n--- ERRORS ---\n{result.stderr}"

            if not output.strip():
                output = "(No output)"

            self.output_text.insert("1.0", output)

        except subprocess.TimeoutExpired:
            self.output_text.insert("1.0", "⚠️ Code timed out after 10 seconds.\n"
                                            "(Infinite loop? Waiting for input?)")
        except Exception as e:
            self.output_text.insert("1.0", f"Error running code: {e}")
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

        self.output_text.configure(state="disabled")


# ══════════════════════════════════════════════════════
# LAUNCH
# ══════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    try:
        root.iconname("CyberQuest Python")
    except:
        pass

    try:
        import ctypes
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, 20, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int))
    except:
        pass

    app = CyberQuestPython(root)
    root.mainloop()


if __name__ == "__main__":
    main()
