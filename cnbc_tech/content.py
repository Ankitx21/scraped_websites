import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define the URL
url = 'https://www.cnbc.com/2024/07/26/dexcom-shares-plunge-more-than-40percent-after-q2-earnings.html'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape the headline
    headline = soup.find('h1', class_='ArticleHeader-headline')
    headline_text = headline.get_text(strip=True) if headline else 'No headline found'

    # Scrape the published date
    published_time = soup.find('time', {'data-testid': 'published-timestamp'})
    published_date = published_time['datetime'] if published_time else 'No date found'
    if published_time:
        published_date = datetime.fromisoformat(published_date).strftime('%Y-%m-%d %H:%M:%S')

    # Scrape the author name
    author = soup.find('a', class_='Author-authorName')
    author_name = author.get_text(strip=True) if author else 'No author found'

    # Scrape the key points
    key_points_div = soup.find('div', class_='RenderKeyPoints-list')
    key_points = key_points_div.get_text(strip=True) if key_points_div else 'No key points found'

    # Scrape the body content
    body_divs = soup.find_all('div', class_='group')
    body_texts = []
    for body_div in body_divs:
        paragraphs = body_div.find_all('p')
        body_texts.append("\n".join(p.get_text(strip=True) for p in paragraphs))
    body_text = "\n\n".join(body_texts) if body_texts else 'No body content found'

    # Print the scraped content
    print("Headline:", headline_text)
    print("Published Date:", published_date)
    print("Author Name:", author_name)
    print("Key Points:", key_points)
    print("Body Content:", body_text)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
