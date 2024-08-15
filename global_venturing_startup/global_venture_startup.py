import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def global_venturing_article_list():
    residential_proxies = {
        'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
    }
    ca_cert_path = 'ca.crt'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://globalventuring.com/',
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

    url = "https://globalventuring.com/sectors/startups/"
    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    
    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with the specified class
        links = soup.find_all('a', class_='mt-2 bigNewsLink w-100 d-inline-block')

        for link in links:
            article_url = link.get('href')
            if article_url:
                if not article_url.startswith('https'):
                    article_url = 'https://globalventuring.com' + article_url
                article_links.add(article_url)
                
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def global_venturing_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1')
            if title_tag:
                title = title_tag.text.strip()
            else:
                missing_fields.append("Title")

            # Extract the author and published date
            author_tag = soup.find('h4', class_='lineTitle')
            if author_tag:
                author_span = author_tag.find('span')
                if author_span:
                    author_text = author_span.text.strip()
                    published_date_str = author_text.split('•')[0].strip()
                    author = author_text.split('•')[1].strip() if '•' in author_text else ""
                    published = published_date_str
                    published_date = convert_date_format(published)
                else:
                    author = ""
                    published = ""
                    missing_fields.extend(["Author", "Publish Date"])
            else:
                author = ""
                published = ""
                missing_fields.extend(["Author", "Publish Date"])

            # Extract the body content
            body_tag = soup.find('div', class_='hiddenWrap')
            if body_tag:
                body_content = body_tag.get_text(separator=' ', strip=True)
            else:
                body_content = ""
                missing_fields.append("Body Content")

            # Only return data if title, published date, and body content are present
            if not title or not published or not body_content:
                if missing_fields:
                    print(f"Missing fields for {url}: {', '.join(missing_fields)}")
                return None

            return {
                'url': url,
                'title': title,
                'published': published,
                'publish_date': published_date,
                'author': author,
                'body': body_content,
            }

        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except Exception as e:
        print({'url': url, 'error': str(e)})
        return None

if __name__ == "__main__":
    total_article_links = global_venturing_article_list()
    if total_article_links:
        articles_data = []
        for url in total_article_links:
            article_details = global_venturing_article_details(url)
            if article_details:
                articles_data.append(article_details)
        
        # Save scraped data to a JSON file
        with open("global_venturing_articles.json", "w") as json_file:
            json.dump(articles_data, json_file, indent=4)

        print("Data fetched and stored in global_venturing_articles.json")
