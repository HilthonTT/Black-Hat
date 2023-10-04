from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque
import requests
import os

FILTERED = ['.jpg', '.gif', '.png', '.css']
TARGET = ''

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

visited_urls = set()
def scrape_html(url):
    try:
        # Make sure the URL is a valid web page URL
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            return

        # Make an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Process the page content here, e.g., save it or extract data

            # Add the current URL to the visited set
            visited_urls.add(url)

            # Find all links on the page
            links = soup.find_all('a', href=True)
            for link in links:
                # Join the relative URL with the base URL
                next_url = urljoin(url, link['href'])
                print(link['href'])

                # Check if it's a new URL and not in the visited set
                if next_url not in visited_urls:
                    # Recursively scrape the next URL
                    scrape_html(next_url)
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

def scrape_website(target_url, download_directory):
    # Send an HTTP GET request to the website
    response = requests.get(target_url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Create the download directory if it doesn't exist
    create_directory(download_directory)

    # Download and save each image
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            img_url = urljoin(target_url, img_url)

            img_filename = os.path.basename(urlparse(img_url).path)

            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                img_path = os.path.join(download_directory, img_filename)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Downloaded: {img_path}")
            else:
                print(f"Failed to download image: {img_url}")


def get_all_possible_urls(target_url):
    # Send an HTTP GET request to the website
    response = requests.get(target_url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a')

    possible_urls = []

    # Extract and append all href attributes to possible_urls
    for link in links:
        link_url = link.get('href')
        if link_url:
            link_url = urljoin(target_url, link_url)
            possible_urls.append(link_url)

    return possible_urls

def normalize_url(base_url, link):
    return urljoin(base_url, link)

# Function to extract all URL paths from a website
def get_all_paths(base_url):
    visited_urls = set()  # To keep track of visited URLs
    queue = deque()       # Queue for BFS

    # Start with the base URL
    queue.append(base_url)

    while queue:
        current_url = queue.popleft()
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links on the page
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href:
                    new_url = normalize_url(current_url, href)

                    # Check if it's part of the same domain and hasn't been visited
                    if urlparse(new_url).netloc == urlparse(base_url).netloc and new_url not in visited_urls:
                        queue.append(new_url)
                        visited_urls.add(new_url)

        except Exception as e:
            print(f"Error processing URL: {current_url} - {e}")

    return visited_urls

def main():
    download_dir = input("Input your download directory: ")
    download_dir = download_dir.replace('\\', '/')  # Replace backslashes with forward slashes

    scrape_website(TARGET, download_dir)

    # Get all possible URLs from the TARGET website
    all_possible_urls = get_all_possible_urls(TARGET)
    
    # Print all the possible URLs
    print("All possible URLs on the website:")
    for url in all_possible_urls:
        print(url)



if __name__ == "__main__":
    # main()

    # all_paths = get_all_paths(TARGET)
    
    # Print all the possible URL paths
    scrape_html(TARGET)