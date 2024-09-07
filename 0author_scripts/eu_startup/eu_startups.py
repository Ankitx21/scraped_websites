import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from proxy.proxies import data_center_proxies
from tech.models import Website, Articles
from websites.contrib import categories

def eu_startup_author_details(author_link):
    
    response= requests.get(author_link )
    soup = BeautifulSoup(response.text , 'html.parser')
    author_name = soup.find('h1', class_='entry-title td-page-title').text.strip()
    author_img = soup.find('div' ,class_='author-box-wrap td-author-page').find('img')['src']
    
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : "", "author_twitter" : ""}
    return author_details


def eu_startups_article_list(retries=3, delay=5):
    base_url = 'https://www.eu-startups.com/'
    proxies = data_center_proxies()
    try:
        response = requests.get(base_url, proxies=proxies)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"Connection error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            return eu_startups_article_list(retries - 1, delay)
        else:
            print(f"Failed to retrieve the website after several retries. Error: {e}")
            return []

    soup = BeautifulSoup(response.text, 'html.parser')
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')
    links = set(h3.find('a').get('href') for h3 in h3_tags if h3.find('a'))
    return list(links)

def eu_startups_article_details(url, retries=3, delay=5):
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
            return eu_startups_article_details(url, retries - 1, delay)
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

    author_link = author_tag['href']
    author_info = eu_startup_author_details(author_link)

    # Extract date and convert to Python date format
    date_tag = soup.find('time', class_='entry-date updated td-module-date')
    date_str = date_tag['datetime'] if date_tag else 'Date not found'
    published = date_str
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date_formatted = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        date_formatted = None
    published_date = date_formatted
    # Extract the div with the specified class
    body_div = soup.find('div', class_="td_block_wrap tdb_single_content tdi_83 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")
    if body_div:
        spans = body_div.find_all('span')
        all_text = " ".join(span.get_text(strip=True) for span in spans)
    else:
        all_text = 'Div not found'

    return {
        'url': url,
        'title':heading,
        'author': author_name,
        'author_details': author_info,
        'published': published, 
        "published_date" : published_date,
        'body': all_text
    }

def eu_startups_save():
    domain = "www.eu-startups.com"
    website = Website.objects.get(domain=domain)
    article_urls = eu_startups_article_list()
    for i, url in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=url).exists():
            art = Articles.objects.filter(url=url).first()
            article = {
                "author": art.author,
                'author_details': art.author_info,
                'title': art.title,
                "published": art.published,
                'url': art.url,
                "body" : art.body
            }
        else: 
            try: 
                article = eu_startups_article_details (url)
                art = Articles(
                    website = website,
                    url = article['url'],
                    title = article["title"],
                    author = article["author"],
                    author_details = article["author_info"],
                    body = article["body"],
                    published = article["published"],
                    published_date = article['published_date'],
                    category = categories['startups']
                )
                art.save()
            except Exception as e:
                print(e)
                pass 
    return article_urls




# def main():
#     base_url = 'https://www.eu-startups.com/'
#     article_links = fetch_article_links(base_url)
#     articles_details = []
#     seen_urls = set()

#     for link in article_links:
#         if link not in seen_urls:
#             article_details = scrape_article_details(link)
#             if article_details:
#                 articles_details.append(article_details)
#                 seen_urls.add(link)
#                 print(f"Processed: {link}")

#     # Remove duplicates based on URL
#     unique_articles = {article['url']: article for article in articles_details}.values()

#     # Save the results to a JSON file
#     with open('eustartup.json', 'w') as f:
#         json.dump(list(unique_articles), f, indent=4)

# if __name__ == '__main__':
#     main()