#!/bin/bash

# Input files and directories
fragments_dir="./../fragments_5th_march"
result_file="./../Logs/dns_queries_extract_new_5th_march.txt"

# Loop through all PCAP fragment files in the specified directory
for pcap_file in "$fragments_dir"/*.pcap; do
    if [ -e "$pcap_file" ]; then
        echo "Processing $pcap_file"
        
        # Extract DNS queries where both the query name and response address are available
        tshark -r "$pcap_file" -Y "dns && dns.qry.name && dns.a" -T fields -e dns.qry.name -e dns.a >> "$result_file"
        
    else
        echo "No .pcap files found in the directory."
    fi
done

echo "DNS queries extraction completed. Results saved in $result_file."