import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import ProxyError, RequestException

def convert_date_format(date_str):
    # Extract the relevant date part and convert to "MM/DD/YYYY"
    date_part = date_str.split(',')[0] + ' ' + date_str.split(',')[1].strip().split(' ')[0]
    date_obj = datetime.strptime(date_part, "%b %d %Y")
    return date_obj.strftime("%m/%d/%Y")

def prnewswire_article_list():
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
        'Referer': 'https://www.prnewswire.com/news-releases/financial-services-latest-news/financing-agreements-list/',
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

    url = "https://www.prnewswire.com/news-releases/financial-services-latest-news/financing-agreements-list/"
    try:
        response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return prnewswire_article_list()  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract hrefs for all <a> tags with the class 'newsreleaseconsolidatelink display-outline w-100'
        links = soup.find_all('a', class_='newsreleaseconsolidatelink display-outline w-100')
        for link in links:
            article_url = link.get('href')
            if article_url:
                # Convert relative URLs to absolute URLs
                if not article_url.startswith('https'):
                    article_url = 'https://www.prnewswire.com' + article_url
                article_links.add(article_url)

        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def prnewswire_article_details(url):
    missing_fields = []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else 'Title not found'

            # Extract the published date
            published_tag = soup.find('p', class_='mb-no')
            if published_tag:
                published_str = published_tag.get_text(strip=True).split(',')[0] + ' ' + published_tag.get_text(strip=True).split(',')[1].strip().split(' ')[0]
                published_datetime = datetime.strptime(published_str, '%b %d %Y')
                published = published_datetime.strftime('%m/%d/%Y')
            else:
                published = 'Published date not found'

            # Extract the body content
            body_div = soup.find('div', class_='col-lg-10 col-lg-offset-1')
            body = body_div.get_text(separator='\n', strip=True) if body_div else 'Body content not found'

            if not title or not published or not body:
                if missing_fields:
                    print(f"Missing fields for {url}: {', '.join(missing_fields)}")
                return None

            return {
                'url': url,
                'title': title,
                'publish_date': published,
                'body': body,
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return prnewswire_article_details(url)  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    total_article_links = prnewswire_article_list()
    if total_article_links:
        articles_data = []
        for url in total_article_links:
            article_details = prnewswire_article_details(url)
            if article_details:
                articles_data.append(article_details)
            time.sleep(random.uniform(2, 5))  # Introduce a delay between requests to avoid overwhelming the server
        
        # Save scraped data to a JSON file
        with open("prnewswire_articles.json", "w") as json_file:
            json.dump(articles_data, json_file, indent=4)

        print("Data fetched and stored in prnewswire_articles.json")
