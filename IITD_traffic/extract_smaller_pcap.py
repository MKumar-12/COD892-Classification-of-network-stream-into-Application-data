import argparse
from scapy.all import rdpcap, wrpcap

def extract_packets(input_pcap, output_pcap, packet_count):
    # Read the input pcap file
    packets = rdpcap(input_pcap, count=packet_count)

    # Write the extracted packets to the output pcap file
    wrpcap(output_pcap, packets)

    print(f"Extracted {packet_count} packets to {output_pcap}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a subset of packets from a pcap file.")
    parser.add_argument("input_pcap", help="Path to the input pcap file")
    parser.add_argument("output_pcap", help="Path to the output pcap file")
    parser.add_argument("--count", type=int, default=100000, help="Number of packets to extract (default: 100000)")

    args = parser.parse_args()

    extract_packets(args.input_pcap, args.output_pcap, args.count)
