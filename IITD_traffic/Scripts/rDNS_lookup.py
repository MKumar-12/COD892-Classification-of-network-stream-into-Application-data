import json
import socket
import os
from tqdm import tqdm
import itertools

# Load the DNS queries from JSON file
def load_dns_queries(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# Resolve DNS queries
def resolve_dns_queries(dns_queries):
    results = {}
    for domain, ips in tqdm(dns_queries.items(), desc="Resolving DNS Queries"):
        results[domain] = {}
        # Iterate over the IPs for each domain\
        for ip in ips:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                results[domain][ip] = hostname
            except socket.herror:
                results[domain][ip] = "Unknown"
    return results

# Path to JSON file
json_file_path = './../JSONs/dns_ip_dict.json'

if os.path.exists(json_file_path):
    print(f"Loading DNS queries...")
    dns_queries = load_dns_queries(json_file_path)

    # Resolve the DNS queries
    first_20_queries = dict(itertools.islice(dns_queries.items(), 20))
    resolved_dns = resolve_dns_queries(first_20_queries)

    # Print results
    for domain, ip_info in resolved_dns.items():
        print(f"DNS Query: {domain}")
        for ip, hostname in ip_info.items():
            print(f"  IP: {ip} -> Hostname: {hostname}")
        print()
else:
    print("File not found. Please check the path.")