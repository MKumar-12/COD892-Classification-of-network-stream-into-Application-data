#!/bin/bash

# Input files
pcap_file="./../youtube_whatsapp_team.pcap"
json_file="./../JSONs/dns_ip_dict.json"
output_dir="./../extracted_dns_classes"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Read the JSON file and extract packets for each DNS name
jq -r 'to_entries[] | "\(.key) \(.value[])"' "$json_file" | while read -r dns_name ip_address; do
    # Sanitize DNS name for use as a filename
    sanitized_dns_name=$(echo "$dns_name" | tr -cd '[:alnum:]._-')
    
    # Build the tshark filter string for the current IP address
    filter="ip.addr == $ip_address"
    
    # Extract packets matching the filter
    output_pcap="$output_dir/$sanitized_dns_name.pcap"
    tshark -r "$pcap_file" -Y "$filter" -w "$output_pcap"
    
    echo "Extracted packets for $dns_name ($ip_address) into $output_pcap"
done
