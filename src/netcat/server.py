import socket
import threading

def handle_client(client_socket):
    print("[*] Receiving data from client...")
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
            
        print(data.decode(), end='')
    print("[!] Client disconneted.")
    client_socket.close()

def main():
    HOST = '0.0.0.0'
    PORT = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] Listening on port {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()

        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()