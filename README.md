# Legion  
**Automatic Enumeration Tool**  

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#) [![License](https://img.shields.io/badge/license-Apache%202.0-blue)](#) [![Version](https://img.shields.io/badge/version-1.0.0-blueviolet)](#)

Legion automates service enumeration by orchestrating well-known open-source tools. Based on the [Pentesting Methodology](https://book.hacktricks.xyz/pentesting-methodology), it extracts maximal information from each discovered service so you don’t have to repeat the same manual steps.

---

## Table of Contents

- [New in This Fork](#new-in-this-fork)  
- [Features](#features)  
- [Installation](#installation)  
  - [From Source](#from-source)  
  - [Docker](#docker)  
- [Usage](#usage)  
  - [Quick Start](#quick-start)  
  - [Automatic Scan](#automatic-scan)  
  - [Semi-Automatic Scan](#semi-automatic-scan)  
  - [Manual Scan](#manual-scan)  
- [Configuration](#configuration)  
- [Protocols Supported](#protocols-supported)  
- [Brute Force](#brute-force)  
- [Internal Commands](#internal-commands)  
- [Contributing](#contributing)  
- [License](#license)  

---

## New in This Fork

- [ ] **Modular plugin system** for adding custom enumeration scripts  
- [ ] **YAML-based config** instead of interactive CLI defaults  
- [ ] **Parallel execution** across multiple hosts/subnets  
- [ ] **Enhanced reporting**: JSON, HTML and CSV outputs  
- [ ] [Your improvement here]  

*(Replace these placeholders with your actual enhancements.)*  

---

## Features

- Automatic, semi-automatic and manual enumeration modes  
- Common service checks: HTTP, SSH, SMB, FTP, Oracle, …  
- Built-in brute-forcing (Hydra/Metasploit/Nmap fallback)  
- Re-execution control to avoid redundant scans  
- Customisable work directory and verbosity levels  

---

## Installation

### From Source

```bash
git clone https://github.com/<your-org>/legion.git /opt/legion
cd /opt/legion
./install.sh
ln -s /opt/legion/legion.py /usr/local/bin/legion

For Oracle listener pentesting, follow the dependencies guide:
https://book.hacktricks.xyz/pentesting/1521-1522-1529-pentesting-oracle-listener/oracle-pentesting-requirements-installation

Docker

# Build image
docker build -t legion .

# Run container
docker run -it --rm legion bash
# Inside: ./legion.py <args>

Or pull prebuilt image:

docker pull carlospolop/legion:latest



⸻

Usage

Quick Start

legion -t 192.168.1.100

(Assumes default options: intensity=2, workdir=$HOME/.legion, verbose=False)

Automatic Scan

> startGeneral

Scans ports/services automatically, runs all relevant modules.

Semi-Automatic Scan

> set host 10.0.0.5
> set proto http
> set intensity 2
> run

Configurable, step-by-step enumeration.

Manual Scan

> exec <module_name>
# e.g. exec http_sqlmap

Run a single module on demand.

⸻

Configuration

Option	Description
host	Target IP or domain
proto	Protocol to enumerate (e.g. http, ssh)
port	Service port (0 = default)
intensity	1=basic, 2=full (default), 3=brute force
domain	DNS domain for virtual hosts or Oracle pentesting
extensions	Comma-separated list for web-file brute forcing
plist	Path to custom password list (default: built-in)
ulist	Path to custom username list (default: built-in)
verbose	True to stream module output, False to suppress until finish
notuse	Comma-separated modules to skip (e.g. msf)
workdir	Directory for scan results (default: $HOME/.legion)

Run help or info inside the CLI for full details.

⸻

Protocols Supported

List all supported protocols with:

legion protos



⸻

Brute Force

Enable brute force by setting intensity to 3. Legion will choose Hydra by default, then fall back to Metasploit or Nmap.

> set proto ssh
> set intensity 3
> run



⸻

Internal Commands

Use the help command to see all built-in operations:

> help


⸻

Contributing
	1.	Fork this repo
	2.	Create a feature branch: git checkout -b feature/my-enhancement
	3.	Commit your changes (git commit -m 'Add awesome feature')
	4.	Push: git push origin feature/my-enhancement
	5.	Open a Pull Request

Please follow PEP 8 and include tests for new modules.

⸻

License

This project is licensed under the Apache 2.0 License. See LICENSE for details.

---

