import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def vcwire_article_list():
    url = "https://vcwire.tech/"

    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.1.1419953599.1723815384; _ga_E5NH8C0QL0=GS1.1.1723815384.1.0.1723815387.57.0.0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('div' ,id = 'tdi_44')
        if container:
            print('container found!')

        h3= container.find_all('h3' ,class_= 'entry-title td-module-title')
        if h3:
            for tag in h3:
                article = tag.find('a')
                url = article['href']           
                article_links.add(url)
        print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

def vcwire_article_details(url):

    missing_fields = []  # List to store missing fields

    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'
    try:
        response = requests.get(url ,proxies=residential_proxies ,verify=ca_cert_path)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_= 'tdb-title-text')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author=""

            # Extract the published date
            published_tag = soup.find('time' , class_='entry-date updated td-module-date')
            if published_tag:
                published = published_tag.text.strip()
                # print(published)
                published_date = convert_date_format(published)
                # print(published_date)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            paragraphs = soup.find_all('div', class_='tdb-block-inner')[7]
            # print(len(paragraphs))
            if paragraphs:
                for para in paragraphs:
                    paragraph_texts.append(para.text)
                body_content = ' '.join(paragraph_texts[0:-2])
            else:
                body_content = ""
                missing_fields.append("Body Content")

            # print(body_content)
            
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

    total_article_links = vcwire_article_list()

    articles_data = []
    for url in total_article_links:   
        print('scraping for: ',url)     
        article_details = vcwire_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/vcwire_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in vcwire_articles.json")