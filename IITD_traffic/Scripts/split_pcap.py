import os
import argparse
import time
from scapy.all import PcapReader, PcapWriter
from tqdm import tqdm

def split_pcap(input_file, output_dir, max_packets=1000000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"[INFO] Starting execution. Reading from {input_file}")
    print()
    pcap_reader = PcapReader(input_file)

    packet_count = 0
    file_count = 1
    
    output_file = os.path.join(output_dir, f"split_{file_count}.pcap")
    pcap_writer = PcapWriter(output_file, append=True, sync=True)
    print(f"[INFO] Currently saving to {output_file}")

    for packet in pcap_reader:
        if packet_count >= max_packets:
            pcap_writer.close()
            file_count += 1
            output_file = os.path.join(output_dir, f"split_{file_count}.pcap")
            pcap_writer = PcapWriter(output_file, append=True, sync=True)
            print(f"[INFO] Currently saving to {output_file}")
            packet_count = 0

        pcap_writer.write(packet)
        packet_count += 1

    pcap_writer.close()
    pcap_reader.close()
    
    print("[INFO] Completed splitting the pcap file.")
    print()


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"


def main():
    parser = argparse.ArgumentParser(description="Split a large pcap file into smaller ones.")
    parser.add_argument("--input_path", type=str, required=True, help="Input pcap file path.")
    parser.add_argument("--output_path", type=str, required=True, help="Directory to save the split pcap files.")
    
    args = parser.parse_args()
    start_time = time.time()
    
    split_pcap(args.input_path, args.output_path)
    
    end_time = time.time()
    execution_time = end_time - start_time
    formatted_time = format_time(execution_time)
    print(f"[LOG] Execution completed in {formatted_time}.")


if __name__ == "__main__":
    main()