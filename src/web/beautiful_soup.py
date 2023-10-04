from bs4 import BeautifulSoup as bs
import requests

def main():
    url = 'https://bing.com'
    r = requests.get(url)

    tree = bs(r.text, 'html.parser') # parse into tree

    for link in tree.find_all('a'): # find all anchors tags.
        print(f"{link.get('href')} => {link.text}")


if __name__ == "__main__":
    main()