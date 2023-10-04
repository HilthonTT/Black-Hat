import urllib.parse
import urllib.request
import sys

def get_request(url):
    with urllib.request.urlopen(url) as response: # GET REQUEST
        content = response.read()
    print(content)


def post_request(url):
    info = { 'user': 'John', 'password': '31337' }
    data = urllib.parse.urlencode(info).encode() # data is now of type bytes

    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response: # POST
         content = response.read()

    print(content)

def main():
    print("Leave blank for a default value.")
    inputed_url = input("URL: ")

    if inputed_url == "":
        url = ''
    else:
        url = inputed_url

    # get_request(url)
    post_request(url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] You interrupted the request.")
    finally:
        sys.exit()
