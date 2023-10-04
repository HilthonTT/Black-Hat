from sniffer_ip_header_decode import IP
from sniffer_with_icmp import ICMP
import helpers.helper as helper
import os
import socket
import ipaddress

import sys
import threading
import time

# subnet to target
SUBNET = "172.21.192.0/24"
# magic string we'll check ICMP responses for
MESSAGE = 'I LOVE NOODLES'

def is_in_network(ip_address):
    network = ipaddress.IPv4Network("172.21.192.0/24")
    ip = ipaddress.IPv4Address(ip_address)
    
    if ip in network:
        return True
    else:
        return False

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host

        socket_protocol= None
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

        self.socket.bind((host, 0))

        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f'{str(self.host)} *'])
        try:
            while True:
                # read a packet
                raw_buffer = self.socket.recvfrom(65535)[0]
                # create an IP header from the first 20 bytes
                ip_header = IP(raw_buffer[0:20])
                # if it's ICMP, we want it
                if ip_header.protocol == 'ICMP':
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            # make sure it has our magic message
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Host up: {tgt}')
        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\nUser interrupted.')
            if hosts_up:
                print(f'\n\nSummary: hosts up on {SUBNET}')
            for host in sorted(hosts_up):
                print(host)
            print('')
            sys.exit()

def main():
    host = None
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "172.21.192.1"

    if is_in_network(host):
        print("[*] Your host is in your network.")
    else:
        print("[*] Your host is NOT in the network.")
    
    s = Scanner(host)
    time.sleep(5)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()

if __name__ == '__main__':
    main()