#!/bin/bash

# Input files
pcap_file="./../youtube_whatsapp_team.pcap"
json_file="./../JSONs/categorized_dns_queries.json"
output_dir="./../extracted_classes"

# Delete the output directory if it already exists, then recreate it
if [ -d "$output_dir" ]; then
  rm -rf "$output_dir"
fi
mkdir -p "$output_dir"

# Loop through each application class in the JSON file
jq -r 'keys[]' "$json_file" | while read -r app_class; do
  # Get the IPs associated with the current application class
  ip_addresses=$(jq -r --arg class "$app_class" '.[$class]' "$json_file")

  # Construct the filter string for tshark
  filter_string=$(echo "$ip_addresses" | tr ',' ' ' | sed 's/\([0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+\)/ip.addr == \1 or /g' | sed 's/ or $//')

  # Define the output file path for the current application class
  output_file="$output_dir/$app_class.pcap"

  # Run tshark to extract packets matching the IPs
  tshark -r "$pcap_file" -Y "$filter_string" -w "$output_file"

  echo "Extracted packets for $app_class saved to $output_file"
done

echo "Classes packet extraction completed!"