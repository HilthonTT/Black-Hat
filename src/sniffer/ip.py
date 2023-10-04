from ctypes import *
import socket
import struct
import ipaddress

class IP_C(Structure):
    def __init__(self, socket_buffer = None):
        super().__init__(IP_C, self)
        # human reachable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))

    _fields_ = [
        ("version", c_ubyte, 4), # 4 bit unsigned char
        ("ihl", c_ubyte, 4), # 4 bit unsigned char
        ("tos", c_ubyte, 8), # 1 byte unsigned char
        ("len", c_ushort, 16), # 2 bytes unsigned char
        ("id", c_ushort, 16), # 2 bytes unsigned char
        ("offset", c_ushort, 16), # 2 bytes unsigned char
        ("ttl", c_ubyte, 8), # 1 byte unsigned char
        ("protocol_num", c_ubyte, 8), # 1 byte unsigned char
        ("sum", c_ushort, 16), # 2 bytes unsigned char
        ("src", c_uint32, 32) # 4 bytes unsigned char
        ("dst", c_uint32, 32) # 4 bytes unsigned char
    ]

    def __new__(cls, socket_buffer = None):
        return cls.from_buffer_copy(socket_buffer)
    
class IP_Decoder():
    def __init__(self, buff = None):
        # B: 1-byte unsigned char
        # H 2-byte unsigned char
        # s byte array with byte-width specification
        # EX: 4s = 4-byte string
        header = struct.unpack('<BBHHHBBH4s4s', buff) 
        self.ver = header[0] >> 4 # shifting 4 bits to the right (4: because IPV4)
                                # Ex: if header[0] = 0x45 -> 0x04
        self.ihl = header[0] & 0xF # (0xF = 00001111 in binary) preserving the last 4 bits of the byte. 
                                   # Ex: if header[0] = 0x45 -> 0x05

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
