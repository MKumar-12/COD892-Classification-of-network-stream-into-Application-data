#!/bin/bash

# Input and output file paths
input_file="./../dns_ip_extract_custom.txt"
output_file="./../JSONs/dns_ip_dict.json"

# Declare an associative array (dictionary)
declare -A dns_ip_map

# Read the input file line by line
while IFS=$'\t' read -r dns_name ip_addresses; do
    # Remove any trailing newline or whitespace from IP addresses
    ip_addresses=$(echo "$ip_addresses" | tr -d '\r\n')
    
    # Split IP addresses by comma
    IFS=',' read -r -a ip_array <<< "$ip_addresses"

    # Check if DNS name already exists in the dictionary
    if [[ -v "dns_ip_map[$dns_name]" ]]; then
        # Append unique IPs to the existing list
        existing_ips=${dns_ip_map[$dns_name]}
        for ip in "${ip_array[@]}"; do
            ip=$(echo "$ip" | tr -d '\r\n')     # Remove any extra newline or whitespace
            if ! grep -q "\b$ip\b" <<< "$existing_ips"; then
                existing_ips+=",${ip}"
            fi
        done
        dns_ip_map[$dns_name]=$existing_ips
    else
        # Add new DNS name and IPs to the dictionary
        dns_ip_map[$dns_name]=$(IFS=','; echo "${ip_array[*]}")
    fi
done < "$input_file"

# Convert the dictionary to JSON format
{
    echo "{"
    first=true

    # Sort the keys and iterate over them
    for key in $(printf "%s\n" "${!dns_ip_map[@]}" | sort); do
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        echo -n "  \"$key\": [$(echo "${dns_ip_map[$key]}" | sed 's/,/\",\"/g;s/^/\"/;s/$/\"/')]"
    done

    echo
    echo "}"
} > "$output_file"

echo "Dictionary written to $output_file"