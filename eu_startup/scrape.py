import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://www.eu-startups.com/'

# Send an HTTP request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 tags with the specified class
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')

    # Extract URLs from the nested a tags
    for h3 in h3_tags:
        a_tag = h3.find('a')
        if a_tag:
            link = a_tag.get('href')
            if link:
                print(link)
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")
