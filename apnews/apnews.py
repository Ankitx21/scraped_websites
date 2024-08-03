import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def apnews_article_list():
    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'
    url = "https://apnews.com/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Cookie': '__cf_bm=2tuebJ49oY55gDci7oNB1ieqYXUEysmXyG3x83.sEQg-1722691079-1.0.1.1-5nZ54dV4.S6pIC6RzW0bSNs.5bNjwZs.IsF8BnjGKBjTqyg.coWOt_DzwM9OhgIhDHe9LHxmulEdRhUQb1ICrUoNA57t0.qjhoBOozvysWA'
    }

    response = requests.get(url, data=payload, headers=headers ,proxies=residential_proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('main' ,class_ = 'Page-oneColumn')
        if container:
            print('container found!')

        h3 = soup.find_all('h3', class_='PagePromo-title')
        h2 = soup.find_all('h2', class_='PagePromo-title')
        total_h = h2 +h3 
        print(len(total_h))

        articles = total_h
        if articles:
            for article in articles:
                anchor = article.find('a')
                link = anchor['href']
                if not link.startswith('https://apnews.com/'):
                    url = 'https://apnews.com/' + link
                else:
                    url = link  
                # print(url)
                article_links.add(url)
        else:
            print("Article section was not found")            
        print(len(article_links))
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})


# apnews_article_list()

def apnews_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_='Page-headline')
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = ""
                missing_fields.append("Title")

            # Extract the author
            author_tag = soup.find('div', class_='Page-authors')
            if author_tag:
                auth1 = author_tag.find('span')
                auth2 = author_tag.find('a')
                if auth1:
                    author= auth1.text.strip()
                else:
                    author= auth2.text.strip()

            else:   
                author =""
                missing_fields.append("Author")

            # Extract the published date
            published_tag = soup.find('meta' ,{'property':'article:published_time'})
            if published_tag:
                published = published_tag.get('content')
                print(published)
                part = published.split('T')
                published_date = part[0]
                
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
            para_container = soup.find_all('div', class_='RichTextStoryBody RichTextBody')

            if para_container:
                for para_cont in para_container:
                
                    paragraphs = para_cont.find_all('p')
                    if paragraphs:
                        for para in paragraphs:
                            paragraph_texts.append(para.text)
                        body_content = ' '.join(paragraph_texts)
                    else:
                        body_content = ""
                        missing_fields.append("Body Content")
            else:
                body_content = ""
                missing_fields.append("Paragraph Container")

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

    total_article_links = apnews_article_list()
    print(f"{len(total_article_links)} article links collected ")
    
    articles_data = []
    for url in total_article_links:        
        article_details = apnews_article_details(url)
        print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/apnews_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in morningstar_articles.json")