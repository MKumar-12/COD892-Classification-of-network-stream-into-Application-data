#!/bin/bash

# Input files and directories
fragments_dir="./../fragments"
json_file="./../JSONs/dns_ip_dict_rem.json"
output_dir="./../extracted_dns_classes_np_rem"
log_file="./../Logs/warnings_np_rem.log"
results_file="./../JSONs/extraction_results_np_rem.json"

# Remove log file if it exists
if [ -f "$log_file" ]; then
    echo "Removing existing log file: $log_file"
    rm "$log_file"
fi

# Remove result file if it exists
if [ -f "$results_file" ]; then
    echo "Removing existing result file: $results_file"
    rm "$results_file"
fi

# Check if output directory exists, delete if it does
if [ -d "$output_dir" ]; then
    echo "Removing existing output directory: $output_dir"
    rm -rf "$output_dir"
fi

# Create the output directory
echo "Creating output directory: $output_dir"
mkdir -p "$output_dir"

# Initialize results dictionary
declare -A results

echo ""
# Read the JSON file and extract packets for each DNS name
jq -r 'to_entries[] | "\(.key) \(.value | unique | join(" || ip.addr == "))"' "$json_file" | while IFS= read -r line; do
    dns_name=$(echo "$line" | awk '{print $1}')
    ip_addresses=$(echo "$line" | awk '{$1=""; print substr($0,2)}')
    
    # Sanitize DNS name for use as a filename
    sanitized_dns_name=$(echo "$dns_name" | tr -cd '[:alnum:]._-')

    # Initialize the filter with the first IP address
    filter="ip.addr == $ip_addresses"

    # Combined output file for this DNS name
    output_pcap="$output_dir/$sanitized_dns_name.pcap"

    # Initialize packet count
    total_filtered_packets=0

    echo "DNS Name: $dns_name"
    echo "Current filter: $filter"
    # Process each fragment in the fragments directory and append the results to the combined output
    for fragment in "$fragments_dir"/*.pcap; do
        # echo "Processing fragment $fragment"
        
        # Filter packets and count them in one go using a temporary file
        temp_pcap=$(mktemp)
        tshark -r "$fragment" -Y "$filter" -w "$temp_pcap" 2>>$log_file

        # Count the number of filtered packets in this fragment
        filtered_packets=$(tshark -r "$temp_pcap" -T fields -e frame.number | wc -l)
        total_filtered_packets=$((total_filtered_packets + filtered_packets))

        # Append the filtered packets to the final output file
        cat "$temp_pcap" >> "$output_pcap"

        # Remove the temporary file
        rm "$temp_pcap"
    done

    # Store the result in the dictionary
    results["$dns_name"]=$total_filtered_packets

    echo "Extraction completed! Packets filtered: $total_filtered_packets"
    echo ""
done

# Convert the results dictionary to JSON and save it
echo "Saving results to $results_file"
printf "%s\n" "${!results[@]}" | jq -R -s 'split("\n") | map(select(length > 0) | split(" ") | {(. | .[0]): .[1]} ) | add' > "$results_file"

echo "Results saved to $results_file"