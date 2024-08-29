#!/bin/bash

# File paths
unlabelled_Traffic_file="./../extracted_classes/Others.pcap"
original_file="./../youtube_whatsapp_team.pcap"

# Obtain Packet Counts
count_others=$(tshark -r "$unlabelled_Traffic_file" | wc -l)
count_original=$(tshark -r "$original_file" | wc -l)

# Calculate Percentage of Non-Coverage
percentage=$(echo "scale=2; ($count_others / $count_original) * 100" | bc)

echo "Percentage of Non-Coverage: $percentage%"