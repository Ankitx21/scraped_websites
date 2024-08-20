import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def latamlist_article_list():
    residential_proxies = {
        'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
    }
    ca_cert_path = 'ca.crt'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': 'advanced_ads_visitor=%7B%22browser_width%22%3A445%7D',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    url = "https://latamlist.com/"
    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    
    if response.status_code == 200:
        article_links = set()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <h2> tags with the specified class and extract URLs
        titles = soup.find_all('h2', class_='entry-title')
        for title in titles:
            link = title.find('a')
            if link:
                article_url = link.get('href')
                if article_url:
                    article_links.add(article_url)
        
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return None

def latamlist_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_tag = soup.find('h1', class_='entry-title')
            if title_tag:
                title = title_tag.text.strip()
            else:
                missing_fields.append("Title")

            # Extract the author
            author_tag = soup.find('span', class_='author')
            if author_tag:
                author_link = author_tag.find('a', class_='url fn n')
                if author_link:
                    author = author_link.text.strip()
                else:
                    author = ""
                    missing_fields.append("Author")
            else:
                author = ""
                missing_fields.append("Author")
            
            # Extract the published date
            published_tag = soup.find('li', class_='meta-date')
            if published_tag:
                published = published_tag.text.strip()
                published_date = convert_date_format(published)
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            body_tag = soup.find('div', class_='entry-content')
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
    total_article_links = latamlist_article_list()
    if total_article_links:
        articles_data = []
        for url in total_article_links:
            article_details = latamlist_article_details(url)
            if article_details:
                articles_data.append(article_details)
        
        # Save scraped data to a JSON file
        with open("latamlist_articles.json", "w") as json_file:
            json.dump(articles_data, json_file, indent=4)

        print("Data fetched and stored in latamlist_articles.json")
