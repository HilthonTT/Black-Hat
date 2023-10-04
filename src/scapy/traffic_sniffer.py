import sys
from scapy.all import sniff, UDP, TCP, IP

def packet_callback(packet):
    layer = None
    if packet.haslayer(UDP):
        layer = UDP
    else:
        layer = TCP

    if packet[layer].payload:
        mypacket = str(packet[layer].payload)
        # Handle UDP packet content here
        print(f"[*] Destination IP: {packet[IP].dst}")
        print(f"[*] Source Port: {packet[layer].sport}, Destination Port: {packet[layer].dport}")
        print(f"[*] {mypacket}\n")
    else:
        print("[*] No data")

def main():
    print("Usage: ./traffic_sniffer.py [filtering]")
    print("Example: ./traffic_sniffer.py udp port 51820")

    if len(sys.argv) == 1:
        filtering = 'udp port 51820 or udp port 1234 or udp port 5678'
    else:
        filtering = sys.argv[1]

    sniff(filter=filtering, prn=packet_callback, store=0)

if __name__ == '__main__':
    main()