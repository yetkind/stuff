# This script retrieves the current firewall rules from the Windows Firewall using the netsh command and exports them to CSV 
# file named firewall_rules.csv. It parses the output of the netsh command to extract rule information. The extracted 
# information is then written to the CSV file, easy to sort and filter.

import csv
import subprocess

def allow_traffic(protocol, port):
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=AllowTraffic", "protocol="+protocol, "dir=in", "localport="+str(port), "action=allow"])
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=AllowTraffic", "protocol="+protocol, "dir=out", "localport="+str(port), "action=allow"])

def block_traffic(protocol, port):
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockTraffic", "protocol="+protocol, "dir=in", "localport="+str(port), "action=block"])
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockTraffic", "protocol="+protocol, "dir=out", "localport="+str(port), "action=block"])

def block_ip(ip_address):
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP", "dir=in", "action=block", "remoteip="+ip_address])
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=BlockIP", "dir=out", "action=block", "remoteip="+ip_address])

def unblock_ip(ip_address):
    subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=BlockIP", "dir=in", "remoteip="+ip_address])
    subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=BlockIP", "dir=out", "remoteip="+ip_address])

    
def parse_rules(output):
    rules = []
    current_rule = {}
    current_rule_name = None
    for line in output.splitlines():
        if line.startswith("Rule Name:"):
            if current_rule:
                current_rule["Rule Name"] = current_rule_name
                rules.append(current_rule)
            current_rule = {}
            current_rule_name = line.split(":", 1)[1].strip()
        elif line.strip() == "":
            continue
        else:
            parts = line.split(":", 1)
            if len(parts) == 2:
                key, value = parts
                current_rule[key.strip()] = value.strip()
    if current_rule:
        current_rule["Rule Name"] = current_rule_name
        rules.append(current_rule)
    return rules

def list_rules():
    with open('firewall_rules.csv', 'w', newline='') as csvfile:
        fieldnames = ["Rule Name", "Description", "Enabled", "Direction", "Profiles", "Grouping", "LocalIP", "RemoteIP", "Protocol", "LocalPort", "RemotePort", "Edge traversal", "Action"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with subprocess.Popen(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
            output, _ = process.communicate()
            rules = parse_rules(output)
            for rule in rules:
                writer.writerow(rule)

    print("Firewall rules exported to 'firewall_rules.csv'")

    
def main():
    while True:
        print("            _       _  __          ")
        print("  _ __ ___ (_)_ __ (_)/ _|_      __")
        print(" | '_ ` _ \| | '_ \| | |_\ \ /\ / /")
        print(" | | | | | | | | | | |  _|\ V  V / ")
        print(" |_| |_| |_|_|_| |_|_|_|   \_/\_/  ")
        print("                       -yetkin 2024")
        print("1. Allow traffic")
        print("2. Block traffic")
        print("3. Block IP address")
        print("4. Unblock IP address")
        print("5. List current rules")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            protocol = input("Enter protocol (e.g., tcp, udp): ")
            port = int(input("Enter port number: "))
            allow_traffic(protocol, port)
            print("Traffic allowed for protocol {} on port {}".format(protocol, port))
        elif choice == "2":
            protocol = input("Enter protocol (e.g., tcp, udp): ")
            port = int(input("Enter port number: "))
            block_traffic(protocol, port)
            print("Traffic blocked for protocol {} on port {}".format(protocol, port))
        elif choice == "3":
            ip_address = input("Enter IP address to block: ")
            block_ip(ip_address)
            print("Traffic blocked for IP address {}".format(ip_address))
        elif choice == "4":
            ip_address = input("Enter IP address to unblock: ")
            unblock_ip(ip_address)
            print("Traffic unblocked for IP address {}".format(ip_address))
        elif choice == "5":
            print("Current firewall rules:")
            list_rules()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
