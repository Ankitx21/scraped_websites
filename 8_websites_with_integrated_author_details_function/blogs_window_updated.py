import requests
from bs4 import BeautifulSoup
from datetime import datetime

def blogs_windows_article_urls():
    url = "https://blogs.windows.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs
    cards = soup.find_all('a', class_='c-card__link')
    article_urls = ["https://blogs.windows.com" + card['href'] if not card['href'].startswith('http') else card['href'] for card in cards if card.get('href')]

    return article_urls

def blogs_windows_article_details(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title = soup.find('h1', class_='h2').text.strip() if soup.find('h1', class_='h2') else ""

    # Scrape the author name and URL
    author_tag = soup.find('ul', class_='article-header__author-list').find('a') if soup.find('ul', class_='article-header__author-list') else None
    author_name = author_tag.text.strip().split('–')[0].strip() if author_tag else ""
    author_url = author_tag['href'] if author_tag else ""

    # Scrape the published date
    published = soup.find('div', class_='article-header__date article-header__date--left').text.strip() if soup.find('div', class_='article-header__date article-header__date--left') else None
    published_date = blogs_windows_date(published) if published else ""

    # If the published date is missing, skip the article
    if not published_date:
        return None

    # Scrape the article body
    body = soup.find('section', class_='panel s-wrapper site-panel site-panel--wysiwyg-with-aside').text.strip() if soup.find('section', class_='panel s-wrapper site-panel site-panel--wysiwyg-with-aside') else ""

    # Return the article details
    article_details = {
        "title": title,
        "author_name": author_name,
        "published": published,
        "published_date": published_date,
        "body": body
    }

    return article_details

def blogs_windows_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

# Example usage
article_urls = blogs_windows_article_urls()
for article_url in article_urls:
    article_details = blogs_windows_article_details(article_url)
    if article_details:  # Only print if article details are not None
        print(article_details)
