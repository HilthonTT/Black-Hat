import socket

def main():
    target_host = "127.0.0.1"
    target_port = 9998  # Use the same port as in server.py

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    with client as sock:
        sock.connect((target_host, target_port))
        sock.send(b"ABC")

        response = sock.recv(4096)
        print(response.decode())

if __name__ == "__main__":
    main()
