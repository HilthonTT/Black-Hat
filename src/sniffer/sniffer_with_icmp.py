from sniffer_ip_header_decode import IP
import helpers.helper as helper
import os
import socket
import struct 
import sys

class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

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
            if ip_header.protocol == 'ICMP':
                print('Protocol: %s %s -> %s' % 
                    (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                print(f'Version: {ip_header.ver}')
                print(f'Header length: {ip_header.ihl} TTL: {ip_header.ttl}')

                # calculate where our ICMP packet starts
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                # create our ICMP structure
                icmp_header = ICMP(buf)
                print('ICMP -> Type %s Code: %s\n' % (icmp_header.type, icmp_header.code))

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

if __name__ == "__main__":
    main()