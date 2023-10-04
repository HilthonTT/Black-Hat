import socket
import os

def get_host_ip():
    host_name = socket.gethostname()

    host_ip = socket.gethostbyname(host_name)

    return host_ip

def print_directory_structure(root_dir, indent=''):
    print(indent + root_dir)
    items = os.listdir(root_dir)
    for item in items:
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + '    ')
        else:
            print(indent + '    ' + item)