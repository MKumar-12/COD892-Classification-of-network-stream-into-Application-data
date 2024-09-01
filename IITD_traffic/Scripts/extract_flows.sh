#!/bin/bash

# Input files
pcap_file="./../capture_2024-03-04_15_05_50-anonymized.pcap"
json_file="./../JSONs/dns_ip_dict.json"
output_dir="./../extracted_dns_classes"

# Check if output directory exists, delete if it does
if [ -d "$output_dir" ]; then
    echo "Removing existing output directory: $output_dir"
    rm -rf "$output_dir"
fi

# Create the output directory
echo "Creating output directory: $output_dir"
mkdir -p "$output_dir"

# Read the JSON file and extract packets for each DNS name
jq -r 'to_entries[] | "\(.key) \(.value[])"' "$json_file" | while read -r dns_name ip_addresses; do
    # Sanitize DNS name for use as a filename
    sanitized_dns_name=$(echo "$dns_name" | tr -cd '[:alnum:]._-')

    # Initialize the filter with the first IP address
    filter="ip.addr == $ip_addresses"

    # Continue reading the remaining IPs and append them to the filter
    while read -r ip; do
        filter="$filter || ip.addr == $ip"
    done <<< "$(jq -r --arg dns_name "$dns_name" '.[$dns_name][]' "$json_file")"

    # Extract packets matching the combined filter
    output_pcap="$output_dir/$sanitized_dns_name.pcap"
    
    echo "tshark -r \"$pcap_file\" -Y \"$filter\" -w \"$output_pcap\" 2>./../Logs/warnings.log"
    
    tshark -r "$pcap_file" -Y "$filter" -w "$output_pcap" 2>./../Logs/warnings.log
    echo "Extraction for $dns_name completed!"
    echo ""
done