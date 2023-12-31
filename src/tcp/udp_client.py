import socket 

def main():
    target_host = '127.0.0.1'
    target_port = 9997

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with client as sock:
        sock.sendto(b"AAABBBCCC", (target_host, target_port))

        data, addr = client.recvfrom(4096)

        print(data.decode())
        sock.close()

if __name__ == "__main__":
    main()