#!/bin/bash

# Input and output directories/files
pcap_dir="./Pcaps"           
output_dir="dns_responses"  


# Create output directory if it doesn't exist
mkdir -p "$output_dir"

process_pcap() {
    local pcap_file=$1
    local base_name=$(basename "$pcap_file" .pcap)  
    local output_json="$output_dir/${base_name}_SNIs.json" 

    # Initialize an empty JSON object for each PCAP file
    echo "[]" > "$output_json"

    # Rextract DNS query names and answers
    tshark_output=$(tshark -r "$pcap_file" -Y "dns && dns.qry.name && dns.a" -T fields -e dns.qry.name -e dns.a 2>/dev/null)

    # Loop over each line in the output and format it into a JSON object
    while IFS=$'\t' read -r dns_query dns_answer; do
        if [[ -n "$dns_query" && -n "$dns_answer" ]]; then
            # Append the DNS query and answer to the JSON file
            jq --arg query "$dns_query" --arg answer "$dns_answer" \
               '. += [{"dns_query": $query, "dns_answer": $answer}]' \
               "$output_json" > tmp.$$.json && mv tmp.$$.json "$output_json"
        fi
    done <<< "$tshark_output"

    echo "Processed $pcap_file -> $output_json"
}


# For all PCAP files in the directory, process them
for pcap_file in "$pcap_dir"/*.pcap; do
    process_pcap "$pcap_file"
done

echo "All DNS responses saved to $output_dir"