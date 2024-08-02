
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json



def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def apple_article_list():
    residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
    ca_cert_path = 'ca.crt'

    import requests

    url = "https://www.apple.com/newsroom/"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'geo=IN; s_fid=367A2D7592AC2056-0CB0258F381687C7; s_cc=true; s_vi=[CS]v1|3356786321246CCD-400001E9C5970DEC[CE]; s_sq=%5B%5BB%5D%5D; pt-dm=v1~x~otm2bbu8~m~1; mk_epub=%7B%22btuid%22%3A%22xgwunz%22%2C%22events%22%3A%22event220%3D0.017%2Cevent221%3D0.000%2Cevent222%3D0.000%2Cevent223%3D0.000%2Cevent224%3D0.912%2Cevent225%3D0.015%2Cevent226%3D1.458%2Cevent227%3D0.013%2Cevent228%3D0.274%2Cevent229%3D1.764%2C%22%2C%22prop57%22%3A%22www.us.newsroom%22%7D',
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
        article_links =[]
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('main' ,class_ = 'main')
        if container:
            print('container found!')

        articles = container.find_all('a')
        if articles:
            for article in articles:
                link = article['href']
                if not link.startswith('https://www.apple.com/') and '/newsroom/' in link:
                    url = 'https://www.apple.com' + link

                    print(url)
                    
                article_links.append(url)
        print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})


def apple_article_details(url):
    missing_fields = []  # List to store missing fields

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('h1', class_= 'hero-headline')
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author=""

            # Extract the published date
            published_tag = soup.find('span' , class_='category-eyebrow__date')
            if published_tag:
                published = published_tag.text.strip()
                published_date = convert_date_format(published)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            paragraphs = soup.find_all('div', class_='pagebody-copy')
            print(len(paragraphs))
            if paragraphs:
                for para in paragraphs:
                    paragraph_texts.append(para.text)
                body_content = ' '.join(paragraph_texts)
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

# driver code
if __name__ == "__main__":

    total_article_links = apple_article_list()
    print(f"{len(total_article_links)} article links collected ")

    articles_data = []
    for url in total_article_links:        
        article_details = apple_article_details(url)
        # print(f"scraping {url}")
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    articles_data.append(article_details)
    with open("zzsample outputs/apple_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored in apple_articles.json")