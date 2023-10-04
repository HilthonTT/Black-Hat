import helpers.helper as helper
import ipaddress
import os
import socket
import struct
import sys

class IP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_sum = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human reachable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # map protocol constants to their name
        self.protocol_map = { 1: "ICMP", 6: "TCP", 17: "UDP" }
        try:
            self.protocol = self.protocol_map[self.protocol_sum]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_sum))
            self.protocol = str(self.protocol_sum)

def sniff(host):
    socket_protocol = None
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    if socket_protocol == None:
        return
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # read a packet
            raw_buffer = sniffer.recvfrom(65535)[0]
            # create an IP header from the first 20 bytes
            ip_header = IP(raw_buffer[0:20])
            # print the detected protocol and host
            print('Protocol: %s %s -> %s' % 
                    (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

def main():
    host = None
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = helper.get_host_ip()
    
    sniff(host)

if __name__ == '__main__':
    main()