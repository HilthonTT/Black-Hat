from io import BytesIO
from lxml import etree
import requests

def post():
    url = ''
    response = requests.get(url) # GET

    data = {'user': 'john', 'password': 'abc-123'}
    response = requests.post(url, data) # POST
    print(response.text) # response.text = text; response.Content = bytestring

def get_website_links():
    url = 'https://nostarch.com'
    r = requests.get(url)
    content = r.content # content is of type 'bytes' 

    parser = etree.HTMLParser()
    content = etree.parse(BytesIO(content), parser) # Parse into tree
    for link in content.findall('//a'): # find all anchor types in HTML page
        print(f'{link.get("href")} -> {link.text}')


if __name__ == '__main__':
    # post()
    get_website_links()