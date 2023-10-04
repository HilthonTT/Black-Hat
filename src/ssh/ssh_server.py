from paramiko import ServerInterface
import os 
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY_FILENAME = os.path.join(CWD, 'test_rsa.key')

if not os.path.exists(HOSTKEY_FILENAME):
    print("[*] Generating RSA host key...")
    HOST_KEY = paramiko.RSAKey.generate(2048)
    HOST_KEY.write_private_key_file(HOSTKEY_FILENAME)
    print("[*] RSA host key generated and saved.")

else:
    HOST_KEY = paramiko.RSAKey(filename=HOSTKEY_FILENAME)

class Server(ServerInterface):
    def __init__(self):
        super().__init__()
        self.event = threading.Event()

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username: str, password: str) -> int:
        if (username == 'trident-msi\timothy tandt') and (password == 'secret_password'):
            return paramiko.AUTH_SUCCESSFUL
        
def main():
    server = '127.0.0.1'
    ssh_port = 2222
    client = None  # Initialize client variable outside the try block

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
        print('[+] Accepted connection from:', addr)
    except Exception as e:
        message = str(e)
        print('[-] Listen failed:', message)  
    else:
        print('[+] Got a connection from:', addr)

    if client is not None:
        print('[+] Creating SSH session...')
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(HOST_KEY)
        server = Server()
        bhSession.start_server(server=server)

        channel = bhSession.accept(20)
        if channel is None:
            print('*** No channel.')
            sys.exit(1)

        print('[+] Authenticated!')
        print(channel.recv(1024))
        channel.send('Welcome to bh_ssh')
        try:
            while True:
                command = input('Enter command: ')
                if command != 'exit':
                    channel.send(command)
                    r = channel.recv(8192)
                    print(r.decode())
                else:
                    channel.send('exit')
                    print("exiting.")
                    bhSession.close()
                    break
        except KeyboardInterrupt:
            bhSession.close()

if __name__ == '__main__':
    main()
