#!/bin/bash

# paths to the input JSON files
dns_ip_dict="./../JSONs/dns_ip_dict.json"
app_classes_dict="./../JSONs/app_classes_dict.json"

# Define the output file
output_file="./../JSONs/categorized_dns_queries.json"

# Create or empty the output file
if [ -f "$output_file" ]; then
  rm -f "$output_file"
fi

# Create or empty the output file
echo "{}" > "$output_file"

# Initialize an array to hold all categorized IPs
categorized_ips=()

# Read the application classes from app_classes_dict.json
for app_class in $(jq -r 'keys[]' "$app_classes_dict"); do
  # Initialize an array to hold IPs for the current application class
  ip_list=()

  # Iterate over the DNS names for the current application class
  for dns_name in $(jq -r --arg class "$app_class" '.[$class][]' "$app_classes_dict"); do
    # Extract the IPs from dns_ip_dict.json for the current DNS name
    ip_array=$(jq -r --arg dns "$dns_name" '.[$dns] | join(",")' "$dns_ip_dict")
    
    # Append the IPs to the list
    ip_list+=("$ip_array")
    categorized_ips+=($(echo "$ip_array" | tr ',' '\n'))
  done

  # Flatten the list of IPs
  flattened_ips=$(printf "%s\n" "${ip_list[@]}" | tr ',' '\n' | sort -u | tr '\n' ',' | sed 's/,$//')

  # Add the result to the output file
  jq --arg class "$app_class" --arg ips "$flattened_ips" \
     '. + {($class): $ips}' "$output_file" > "$output_file.tmp" && mv "$output_file.tmp" "$output_file"
done


# Convert the categorized IPs array to a unique list
categorized_ips=$(printf "%s\n" "${categorized_ips[@]}" | sort -u)

# Find DNS names that were not categorized
all_dns_names=$(jq -r 'keys[]' "$dns_ip_dict")
categorized_dns_names=$(jq -r 'keys[]' "$output_file")

# Identify uncategorized DNS names
for dns_name in $all_dns_names; do
  if ! echo "$categorized_dns_names" | grep -q "^$dns_name$"; then
    # Extract the IPs for uncategorized DNS names
    ip_array=$(jq -r --arg dns "$dns_name" '.[$dns] | join(",")' "$dns_ip_dict")
    
    # Remove any IPs that have already been categorized
    ip_array=$(echo "$ip_array" | tr ',' '\n' | grep -Fxv -f <(echo "$categorized_ips") | tr '\n' ',' | sed 's/,$//')
    
    # Skip if no uncategorized IPs are left
    [ -z "$ip_array" ] && continue

    # Handle the "Others" category, ensuring it merges arrays correctly
    jq --arg class "Others" --arg ips "$ip_array" \
       'if .[$class] == null then .[$class] = $ips
        else .[$class] |= (. + "," + $ips | split(",") | unique | join(",")) end' "$output_file" > "$output_file.tmp" && mv "$output_file.tmp" "$output_file"
  fi
done

echo "Application Categorization completed. Written to '$output_file' file."