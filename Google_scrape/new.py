import requests
from bs4 import BeautifulSoup
import json

base_url = "https://blog.google/api/v2/latest/"
params = {
    'author_ids': '',
    'hero_template': 'heroArticleItem',
    'image_format': 'webp',
    'cursor': 1,  # Starting cursor value
    'paginate': 6,
    'show_hero': True,
    'site_id': 2,
    'tags': 'search'
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://blog.google/products/search/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

def scrape_article(url):
    # Set up headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send a GET request to the article URL with headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize variables to store scraped data
            scraped_data = {}

            # Author Name

            author = soup.find(class_ = "article-meta__author-name")
            scraped_data["Author"] = author.text.strip()

            # Extract heading
            heading = soup.find('h1')
            if heading:
                scraped_data['heading'] = heading.text.strip()

            # Extract important heading (if available)
            imp_heading = soup.find('p', class_='h-c-eyebrow')
            if imp_heading:
                scraped_data['imp_heading'] = imp_heading.text.strip()

            publish_date = soup.find(class_ = "article-meta__published-at")
            scraped_data["Publish Date"] = publish_date.text.strip()

            # Extract body of the article (assuming the class name provided)
            article_paragraphs = soup.find_all('div', class_='uni-paragraph article-paragraph')
            scraped_data['article_paragraphs'] = [paragraph.text.strip() for paragraph in article_paragraphs]

            # Include the URL of the article in the scraped data
            scraped_data['article_url'] = url

            return scraped_data
        
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# List to store scraped data for all articles
all_articles_data = []

# Iterate over cursor values from 1 to 5
for cursor_value in range(1, 2):
    params['cursor'] = cursor_value

    response = requests.get(base_url, headers=headers, params=params)
    json_response = response.json()

    # Process each article in the current response
    for data in json_response['results']:
        article_url = data["full_url"]
        print("Scraping article:", article_url)
        
        # Call scrape_article function to get data for each article URL
        article_data = scrape_article(article_url)
        
        # If data is scraped successfully, add to the list
        if article_data:
            all_articles_data.append(article_data)

# Save all_articles_data to a JSON file
output_file = 'scraped_articles.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_articles_data, f, ensure_ascii=False, indent=4)

print(f"Scraped data saved to {output_file}")
