#!/bin/bash

# File paths
labelled_Traffic_dir="./../extracted_dns_classes_p/"
original_file="./../capture_2024-03-04_15_05_50-anonymized.pcap"

# Obtain Packet Counts for all labelled traffic files
count_labelled=0
for file in "$labelled_Traffic_dir"/*.pcap; do
  if [[ -f "$file" ]]; then
    count=$(tshark -r "$file" | wc -l)
    count_labelled=$((count_labelled + count))
  fi
done

echo "Labelled packets : $count_labelled"

# Obtain Packet Count for the original file
count_original=$(capinfos -c "$original_file" | awk '/Number of packets/ {
  if ($5 == "M") print $4 * 1000000;
  else if ($5 == "K") print $4 * 1000;
  else print $4;
}')
echo "Total packets : $count_original"

# Calculate Percentage of Non-Coverage
percentage=$(echo "scale=2; (($count_original - $count_labelled) / $count_original) * 100" | bc)

echo "Percentage of Non-Coverage: $percentage%"