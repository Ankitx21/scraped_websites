import requests
from bs4 import BeautifulSoup

# Define the URL
url = 'https://www.cnbc.com/technology/'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with the class 'Card-title'
    card_title_links = soup.find_all('a', class_='Card-title')
    # Find all <a> tags with the class 'TrendingNowItem-title'
    trending_now_links = soup.find_all('a', class_='TrendingNowItem-title')

    # Combine the links
    all_links = card_title_links + trending_now_links

    # Extract and print the URLs
    for link in all_links:
        href = link.get('href')
        print(href)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
