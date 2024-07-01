import requests
from bs4 import BeautifulSoup
import json

# Base URL and headers
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

def get_article_urls(base_url, headers, params, max_cursor=100):
    """Fetch article URLs from the API."""
    article_urls = []
    for cursor_value in range(1, max_cursor + 1):
        params['cursor'] = cursor_value
        response = requests.get(base_url, headers=headers, params=params)
        json_response = response.json()
        article_urls.extend([data["full_url"] for data in json_response['results']])
    return article_urls

def scrape_article(url, headers):
    """Scrape data from an article."""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            scraped_data = {}

            # Author Name
            author = soup.find(class_="article-meta__author-name")
            if author:
                scraped_data["Author"] = author.text.strip()

            # Extract heading
            heading = soup.find('h1')
            if heading:
                scraped_data['heading'] = heading.text.strip()

            # Extract important heading (if available)
            imp_heading = soup.find('p', class_='h-c-eyebrow')
            if imp_heading:
                scraped_data['imp_heading'] = imp_heading.text.strip()

            # Publish date
            publish_date = soup.find(class_="article-meta__published-at")
            if publish_date:
                scraped_data["Publish Date"] = publish_date.text.strip()

            # Extract body of the article
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

def save_to_json(data, output_file):
    """Save data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    article_urls = get_article_urls(base_url, headers, params)
    all_articles_data = []

    for article_url in article_urls:
        print("Scraping article:", article_url)
        article_data = scrape_article(article_url, headers)
        if article_data:
            all_articles_data.append(article_data)

    output_file = 'scraped_articles.json'
    save_to_json(all_articles_data, output_file)
    print(f"Scraped data saved to {output_file}")

if __name__ == "__main__":
    main()
