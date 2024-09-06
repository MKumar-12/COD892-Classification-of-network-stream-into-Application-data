#!/bin/bash

# Input files and directories
fragments_dir="./../fragments"
json_file="./../JSONs/dns_ip_dict_rem.json"
output_dir="./../extracted_dns_classes_p"
log_file="./../Logs/warnings_p.log"
core_log_file="./../Logs/core_debug.log"

# Remove log files if they exist
if [ -f "$log_file" ]; then
    echo "Removing existing log file: $log_file" | tee /dev/tty
    rm "$log_file"
fi

if [ -f "$core_log_file" ]; then
    echo "Removing existing core debug log file: $core_log_file" | tee /dev/tty
    rm "$core_log_file"
fi

# Check if output directory exists, delete if it does
if [ -d "$output_dir" ]; then
    echo "Removing existing output directory: $output_dir" | tee /dev/tty
    rm -rf "$output_dir"
fi

# Create the output directory
echo "Creating output directory: $output_dir" | tee /dev/tty
mkdir -p "$output_dir"

echo "" | tee /dev/tty

# Initialize results dictionary
declare -A results

# Function to process each DNS name and filter packets
process_dns() {
    dns_name=$1
    ip_addresses=$2
    sanitized_dns_name=$(echo "$dns_name" | tr -cd '[:alnum:]._-')
    filter="ip.addr == $ip_addresses"
    output_pcap="$output_dir/$sanitized_dns_name.pcap"
    total_filtered_packets=0

    # Log core information
    echo "$(date +"%Y-%m-%d %H:%M:%S") - PID: $$ is working on DNS name: $dns_name" >> "$core_log_file"

    for fragment in "$fragments_dir"/*.pcap; do
        fragment_name=$(basename "$fragment")
        echo "$(date +"%Y-%m-%d %H:%M:%S") - PID: $$ processing fragment: $fragment_name for DNS name: $dns_name" >> "$core_log_file"

        temp_pcap=$(mktemp)
        tshark -r "$fragment" -Y "$filter" -w "$temp_pcap" 2>>$log_file

        filtered_packets=$(tshark -r "$temp_pcap" -T fields -e frame.number | wc -l)
        total_filtered_packets=$((total_filtered_packets + filtered_packets))

        # Log filtered packets
        echo "$(date +"%Y-%m-%d %H:%M:%S") - PID: $$ filtered $filtered_packets packets from fragment: $fragment_name for DNS name: $dns_name" >> "$core_log_file"

        # Append the filtered packets to the final output file
        cat "$temp_pcap" >> "$output_pcap"

        # Remove the temporary file
        rm "$temp_pcap"
    done

    echo "$(date +"%Y-%m-%d %H:%M:%S") - PID: $$ completed DNS name: $dns_name, total packets filtered: $total_filtered_packets" | tee /dev/tty
    echo "$(date +"%Y-%m-%d %H:%M:%S") - PID: $$ completed DNS name: $dns_name, total packets filtered: $total_filtered_packets" >> "$core_log_file"
}

# Export functions and variables needed by parallel
export -f process_dns
export fragments_dir log_file output_dir core_log_file

# Read the JSON file and parallelize the processing
jq -r 'to_entries[] | "\(.key) \(.value | unique | join(" || ip.addr == "))"' "$json_file" | \
    stdbuf -oL -eL parallel --colsep ' ' process_dns {1} {2}

echo "Execution Completed!" | tee /dev/tty
