import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

def fetch_article_links(base_url, retries=3, delay=5):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"Connection error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            return fetch_article_links(base_url, retries - 1, delay)
        else:
            print(f"Failed to retrieve the website after several retries. Error: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')
    links = set(h3.find('a').get('href') for h3 in h3_tags if h3.find('a'))
    return list(links)

def scrape_article_details(url, retries=3, delay=5):
    if 'sponsored' in url or 'weekly-fund' in url:
        print(f"Skipping article: {url}")
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"Connection error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            return scrape_article_details(url, retries - 1, delay)
        else:
            print(f"Failed to retrieve the article after several retries. Error: {e}")
            return None

    soup = BeautifulSoup(response.content, 'html.parser')

    #extract the heading

    heading_tag = soup.find('h1', class_ = 'tdb-title-text')
    heading = heading_tag.get_text() if heading_tag else None

    # Extract author name
    author_tag = soup.find('a', class_='tdb-author-name')
    author_name = author_tag.get_text() if author_tag else 'Author not found'

    # Extract date and convert to Python date format
    date_tag = soup.find('time', class_='entry-date updated td-module-date')
    date_str = date_tag['datetime'] if date_tag else 'Date not found'
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date_formatted = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        date_formatted = 'Date not found'

    # Extract the div with the specified class
    body_div = soup.find('div', class_="td_block_wrap tdb_single_content tdi_83 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")
    if body_div:
        spans = body_div.find_all('span')
        all_text = " ".join(span.get_text(strip=True) for span in spans)
    else:
        all_text = 'Div not found'

    return {
        'url': url,
        'heading':heading,
        'author_name': author_name,
        'date': date_formatted,
        'body': all_text
    }

def main():
    base_url = 'https://www.eu-startups.com/'
    article_links = fetch_article_links(base_url)
    articles_details = []
    seen_urls = set()

    for link in article_links:
        if link not in seen_urls:
            article_details = scrape_article_details(link)
            if article_details:
                articles_details.append(article_details)
                seen_urls.add(link)
                print(f"Processed: {link}")

    # Remove duplicates based on URL
    unique_articles = {article['url']: article for article in articles_details}.values()

    # Save the results to a JSON file
    with open('articles.json', 'w') as f:
        json.dump(list(unique_articles), f, indent=4)

if __name__ == '__main__':
    main()
