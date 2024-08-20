import requests
from bs4 import BeautifulSoup
import json
import time
import random
from requests.exceptions import ProxyError, RequestException

def scrape_finsmes_article_list():
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
        'Referer': 'https://www.finsmes.com/',
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

    url = "https://www.finsmes.com/"
    try:
        response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return scrape_finsmes_article_list()  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')
        for h3_tag in soup.find_all('h3', class_='entry-title td-module-title'):
            a_tag = h3_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                article_links.add(a_tag['href'])

        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def scrape_finsmes_article_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1', class_='tdb-title-text')
            title = title_tag.text.strip() if title_tag else ""
            if not title:
                print(f"Missing Title for {url}")
                return None

            # Extract the published date
            published_tag = soup.find('time', class_='entry-date updated td-module-date')
            published_date = published_tag['datetime'].split("T")[0] if published_tag else ""
            if not published_date:
                print(f"Missing Publish Date for {url}")
                return None

            # Extract the body content
            body_tag = soup.find('div', class_='td_block_wrap tdb_single_content tdi_58 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else ""
            if not body_content:
                print(f"Missing Body Content for {url}")
                return None

            return {
                'url': url,
                'title': title,
                'publish_date': published_date,
                'body': body_content
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except ProxyError as e:
        print(f"Proxy error: {e}. Retrying...")
        time.sleep(5)
        return scrape_finsmes_article_details(url)  # Retry once on proxy failure
    except RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    article_links = scrape_finsmes_article_list()
    if article_links:
        articles_data = []
        for url in article_links:
            article_details = scrape_finsmes_article_details(url)
            if article_details:
                articles_data.append(article_details)
            time.sleep(random.uniform(2, 5))  # Introduce a delay between requests to avoid overwhelming the server
        
        # Save scraped data to a JSON file
        with open("finsmes_articles.json", "w") as json_file:
            json.dump(articles_data, json_file, indent=4)

        print("Data fetched and stored in finsmes_articles.json")
