import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define the URL
url = "https://www.eu-startups.com/2024/07/eu-startups-podcast-episode-77-dominik-angerer-co-founder-and-ceo-of-storyblok/"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract author name
author_tag = soup.find('a', class_='tdb-author-name')
author_name = author_tag.get_text() if author_tag else 'Author not found'

# Extract date and convert to Python date format
date_tag = soup.find('time', class_='entry-date updated td-module-date')
date_str = date_tag['datetime'] if date_tag else 'Date not found'
date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

# Extract the div with the specified class
body_div = soup.find('div', class_="td_block_wrap tdb_single_content tdi_83 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")
if body_div:
    # Extract all text from spans within the div
    spans = body_div.find_all('span')
    all_text = " ".join(span.get_text(strip=True) for span in spans)
else:
    all_text = 'Div not found'

# Print the extracted text
print(f"Author Name: {author_name}")
print(f"Date: {date_obj.strftime('%Y-%m-%d')}")
print("Extracted Text:")
print(all_text)
