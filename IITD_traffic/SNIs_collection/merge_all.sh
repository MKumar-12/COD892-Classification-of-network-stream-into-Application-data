#!/bin/bash

# Input and output directories/files
pcap_dir="./Pcaps"
output_file="sni_merged.json"

# Check if output file exists, delete if it does
if [ -f "$output_file" ]; then
    echo "Removing existing output file: $output_file"
    rm "$output_file"
fi

echo "{" >> "$output_file"

# Loop through all pcap files in the directory
for pcap_file in "$pcap_dir"/*.pcap; do
    file_name=$(basename "$pcap_file")
    echo "Processing file: $file_name"

    # Extract SNI values using tshark
    sni_output=$(tshark -r "$pcap_file" -Y "tls.handshake.extensions_server_name" -T fields -e tls.handshake.extensions_server_name 2>/dev/null)

    if [[ ! -z "$sni_output" ]]; then
        echo "  \"$file_name\": [" >> "$output_file"

        # Use sort and uniq to remove duplicate SNI values
        sni_list=$(echo "$sni_output" | sort -u)

        # Write unique SNI values to the output JSON, avoid trailing comma
        echo "$sni_list" | while IFS= read -r sni; do
            echo "    \"$sni\"," >> "$output_file"
        done

        # Remove the trailing comma for the last element in the list
        sed -i '$ s/,$//' "$output_file"
        
        # Close the array for this file
        echo "  ]," >> "$output_file"
    else
        echo "  \"$file_name\": []," >> "$output_file"
    fi
done

# Close the JSON object
sed -i '$ s/,$//' "$output_file"  # Remove the trailing comma after the last file
echo "}" >> "$output_file"

echo "SNI extraction completed and saved to $output_file"