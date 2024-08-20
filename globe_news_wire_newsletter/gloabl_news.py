import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import ProxyError, RequestException

def convert_date_format(date_str):
    # Extract just the date part (e.g., "August 17, 2024")
    date_part = date_str.split()[0:3]  # ["August", "17,", "2024"]
    date_str_cleaned = " ".join(date_part)  # "August 17, 2024"
    
    # Convert to the desired format "MM/DD/YYYY"
    date_obj = datetime.strptime(date_str_cleaned, "%B %d, %Y")
    formatted_date = date_obj.strftime("%m/%d/%Y")
    
    return formatted_date


def globenewswire_article_list():
    residential_proxies = {
        'http': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_0d20a254-zone-residential_proxy1:iy1rz2azj4by@brd.superproxy.io:22225'
    }
    ca_cert_path = 'ca.crt'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.globenewswire.com/newsroom',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    url = "https://www.globenewswire.com/newsroom"
    try:
        response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return globenewswire_article_list()  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract hrefs for all <a> tags with the attribute 'data-section' = 'article-url'
        links = soup.find_all('a', {'data-section': 'article-url'})
        for link in links:
            article_url = link.get('href')
            if article_url:
                # Convert relative URLs to absolute URLs
                if not article_url.startswith('https'):
                    article_url = 'https://www.globenewswire.com' + article_url
                article_links.add(article_url)

        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def globenewswire_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1', class_='article-headline')
            title = title_tag.text.strip() if title_tag else ""
            if not title:
                missing_fields.append("Title")

            # Extract the published date
            published_tag = soup.find('time')
            if published_tag:
                published_text = published_tag.text.strip()
                try:
                    published_date = convert_date_format(published_text)
                except ValueError:
                    published_date = ""
            else:
                published_text = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the author (organization)
            author_tag = soup.find('span', class_='article-source')
            author_span = author_tag.find('a', itemprop='name') if author_tag else None
            author = author_span.text.strip() if author_span else ""
            if not author:
                missing_fields.append("Author")

            # Extract the body content
            body_tag = soup.find('div', class_='main-body-container article-body')
            body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""
            if not body_content:
                missing_fields.append("Body Content")

            # Only return data if title, published date, and body content are present
            if not title or not published_date or not body_content:
                if missing_fields:
                    print(f"Missing fields for {url}: {', '.join(missing_fields)}")
                return None

            return {
                'url': url,
                'title': title,
                'published': published_text,
                'publish_date': published_date,
                'author': author,
                'body': body_content,
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return globenewswire_article_details(url)  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    total_article_links = globenewswire_article_list()
    if total_article_links:
        articles_data = []
        for url in total_article_links:
            article_details = globenewswire_article_details(url)
            if article_details:
                articles_data.append(article_details)
            time.sleep(random.uniform(2, 5))  # Introduce a delay between requests to avoid overwhelming the server
        
        # Save scraped data to a JSON file
        with open("globenewswire_articles.json", "w") as json_file:
            json.dump(articles_data, json_file, indent=4)

        print("Data fetched and stored in globenewswire_articles.json")
