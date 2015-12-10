from __future__ import print_function
import dns.zone
import os.path
import sys
import dns.ipv4
import socket
import signal

# Handle user interrupt
def signal_handler(signal, frame):
    print("User interrupt...")
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

ip_map = {}
known_hosts = {}

def hostnametoip(domain):
    ip = known_hosts.get(domain)
    if ip is None:
        try:
            ip = socket.gethostbyname(domain)
        except:
            ip = '0.0.0.0'
            print("Failed to resolve DNS for %s" % domain, file=sys.stderr)
        known_hosts[domain] = ip

    return ip

def pushRecord(ip, target):
    # Remove . from end of the target
    if target.endswith('.'):
        target = target[:-1]

    l = ip_map.get(ip)

    if l is None:
        l = []
        ip_map[ip] = l

    l.append(target)

# Parse over all the input files
for filename in sys.argv[1:]:
    zone = dns.zone.from_file(filename, os.path.basename(filename), relativize=False)

    #Iterate over A records
    for (name, ttl, rdata) in zone.iterate_rdatas('A'):
        pushRecord(rdata.address, name.to_text())

    # Iterate over CNAME records
    for (name, ttl, rdata) in zone.iterate_rdatas('CNAME'):
        pushRecord(hostnametoip(rdata.target.to_text()), name.to_text())

keys = ip_map.keys()
keys.sort(lambda a1, a2: cmp(dns.ipv4.inet_aton(a1), dns.ipv4.inet_aton(a2)))
for ip in keys:

    # Get list of hostnames associated with this IP
    hostnames = ip_map[ip]
    hostnames.sort()

    # Convert names to strings for output
    hostnames = map(str, hostnames)
    print(ip)

    for hostname in hostnames:
        print("    %s" % hostname)

    print("")