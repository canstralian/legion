# -*- coding: utf-8 -*-

from warriors.warrior import Warrior
import shlex # Useful for splitting command strings safely

# You can test this module against sizzle.htb (10.10.10.103)

class Dns_warrior(Warrior):
    def __init__(self, host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec_tool):
        # Pass exec_tool to the parent constructor if Warrior expects it
        super().__init__(host, port, workdir, protocol, intensity, username, ulist, password, plist, notuse, extensions, path, reexec, ipv6, domain, interactive, verbose, executed, exec_tool)

        self.protocol_port = self.port if self.port != '0' else '53' # Use 53 as default DNS port

        # Define commands categorized by their purpose
        self.command_categories = {
            "basic_enum": [],
            "reverse_dns": [],
            "zone_transfer": [],
            "bruteforce": [],
            "vulnerability_checks": [],
            "ipv6_specific": [],
            "dnssec_specific": []
        }

        self._define_commands()

    def _add_command(self, category, name, cmd_template, shell=False, chain=False):
        """Helper to add a command to a specific category."""
        # Basic formatting/templating for the command string
        cmd_string = cmd_template.format(
            host=self.host,
            port=self.protocol_port,
            ip=self.ip,
            ipv6=self.ipv6,
            domain=self.domain,
            username=self.username,
            ulist=self.ulist,
            password=self.password,
            plist=self.plist,
            workdir=self.workdir # Access workdir if needed in commands
        )
        self.command_categories[category].append({
            "name": name,
            "cmd": cmd_string,
            "shell": shell,
            "chain": chain
        })

    def _define_commands(self):
        """Defines all possible commands based on configuration and intensity."""

        # Basic Enumeration
        self._add_command("basic_enum", f"nmap_dns_tcp_{self.protocol_port}",
                          'nmap -n -sV --script "(*dns* and (default or (discovery and safe))) or dns-random-txid or dns-random-srcport" -p {port} {host}', shell=True)
        self._add_command("basic_enum", f"nmap_dns_udp_{self.protocol_port}",
                          'nmap -n -sV -sU --script "(*dns* and (default or (discovery and safe))) or dns-random-txid or dns-random-srcport" -p {port} {host}', shell=True)

        if self.domain:
            # Using _add_command for dig commands with chaining
            dig_command_template = "dig {record_type} @{host} {domain}"
            self._add_command("basic_enum", "dig_AXFR", dig_command_template.format(record_type="axfr", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_ANY", dig_command_template.format(record_type="ANY", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_A", dig_command_template.format(record_type="A", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_AAAA", dig_command_template.format(record_type="AAAA", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_TXT", dig_command_template.format(record_type="TXT", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_MX", dig_command_template.format(record_type="MX", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_NS", dig_command_template.format(record_type="NS", **self.__dict__), shell=True, chain=True)
            self._add_command("basic_enum", "dig_SOA", dig_command_template.format(record_type="SOA", **self.__dict__), shell=True) # Last command in chain

            self._add_command("basic_enum", "dnsrecon_domain", 'dnsrecon -d {domain} -a -n {host}')
            msfmodules_enum = [{"path": "auxiliary/gather/enum_dns", "toset": {"DOMAIN": self.domain, "NS": self.host}}]
            self._add_command("basic_enum", "msf_enum_dns", self.create_msf_cmd(msfmodules_enum), shell=True)


        # Reverse DNS
        if self.ip:
            self._add_command("reverse_dns", f"dig_PTR_ipv4_{self.protocol_port}", 'dig -x {ip} @{host}', shell=True)
            # dnsrecon for IP range - reconsider the fixed ranges, maybe make them configurable or based on target IP
            self._add_command("reverse_dns", f"dnsrecon_ip_range_{self.ip.replace('.', '_')}_24", 'dnsrecon -r {ip}/24 -n {host}') # Example: 192.168.1.5 -> 192.168.1.0/24

        if self.ipv6:
             self._add_command("ipv6_specific", f"dig_PTR_ipv6", 'dig -x {ipv6} @{host}', shell=True)
             # Add more IPv6 specific reconnaissance tools/commands here

        # Vulnerability Checks (Intensity >= 2)
        if int(self.intensity) >= 2:
            msfmodules_vuln = [{"path": "auxiliary/scanner/dns/dns_amp", "toset": {"RPORT": self.protocol_port, "RHOSTS": self.host}}]
            self._add_command("vulnerability_checks", f"msf_dns_amp_{self.protocol_port}", self.create_msf_cmd(msfmodules_vuln), shell=True)
            # Add other DNS vulnerability scanning commands (e.g., from nmap scripts, other tools)

        # Bruteforce (Intensity == 3)
        if int(self.intensity) == 3 and self.domain:
            self.wordlist = self.plist if self.plist else self.wordlists_path + '/subdomains.txt'
            self._add_command("bruteforce", "dnsrecon_brute", f'dnsrecon -D {self.wordlist} -d {{domain}} -n {{host}}') # Using f-string and template variables

        # DNSSEC Attacks (TODO)
        # Add commands for DNSSEC checking and attacks
        self._add_command("dnssec_specific", "dig_DNSKEY", "dig DNSKEY {domain} @{host}", shell=True)
        self._add_command("dnssec_specific", "dig_DS", "dig DS {domain} @{host}", shell=True)
        self._add_command("dnssec_specific", "dnssec-analyzer", "dnssec-analyzer {domain} @{host}") # Example tool, might need installation
        # Add more advanced DNSSEC tools/scripts

        # Now, flatten the commands into the self.cmds list for execution
        self.cmds = []
        for category in self.command_categories:
            # Optional: Add a visual separator or header for each category in verbose output
            # if self.verbose and self.command_categories[category]:
            #     self.cmds.append({"name": f"--- {category.replace('_', ' ').title()} ---", "cmd": "", "shell": False, "chain": False})
                
            self.cmds.extend(self.command_categories[category])

    # The dig_cmds method is no longer needed with the new _add_command approach
    # def dig_cmds(self, record_types):
    #     """Generates a chained dig command string for multiple record types."""
    #     final_cmd = ""
    #     for i, record_type in enumerate(record_types):
    #         final_cmd += f"dig {record_type} @{self.host} {self.domain}"
    #         if i < len(record_types) - 1:
    #             final_cmd += ";" # Chain commands
    #     return final_cmd

# Example of how to use the updated Dns_warrior (within the main_run or interactive logic)
# Assuming 'config' is the object/namespace containing all parsed arguments
# dns_scanner = Dns_warrior(
#     host=config.host,
#     port=str(config.port), # Ensure port is a string if Warrior expects it
#     workdir=config.workdir,
#     protocol=config.proto,
#     intensity=str(config.intensity), # Ensure intensity is a string
#     username=config.username,
#     ulist=config.ulist,
#     password=config.password,
#     plist=config.plist,
#     notuse=config.notuse,
#     extensions=config.extensions,
#     path=config.path,
#     reexec=False, # Determine how reexec is handled in the new structure
#     ipv6=config.ipv6,
#     domain=config.domain,
#     interactive=config.interactive,
#     verbose=config.verbose,
#     executed=[], # Track executed commands
#     exec_tool=config.execonly # Pass the specific tool to execute
# )
#
# # The execution logic would then iterate through dns_scanner.cmds
# # and run each command, respecting 'shell', 'chain', and 'notuse'
# # and checking 'exec_tool' if specified.
