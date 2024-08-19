import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def cbinsights_article_list():

    proxies = {
        'http': 'http://brd-customer-hl_f622b815-zone-web_unlocker1:v2zbd45ye9d0@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_f622b815-zone-web_unlocker1:v2zbd45ye9d0@brd.superproxy.io:22225',
    }


    url = "https://www.cbinsights.com/research/"
    ca_cert_path = 'ca.crt'
    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'ajs_anonymous_id=950cb2de-c6e6-4090-96b7-c0993a8c442a; _omappvp=E3CRwyhg6FGz3mB9mqWICrTH0vgRznp4cSDqBCRDic1aaoBzDnyXGVlvwM3DIXT6cjpNLqlrboht3JvMaGUcfBSdtpEI2nhp; _gcl_au=1.1.1730642248.1723813187; utm_campaign_stamp=cbinsights; utm_source_stamp=direct; utm_medium_stamp=direct; _omappvs=1723813186649; _ga=GA1.2.751404504.1723813187; _gid=GA1.2.969312004.1723813187; _gd_visitor=3b2d4776-b0f3-4daa-8df1-d2bd9ff36782; _gd_session=83413034-f088-478a-8611-f0487432a029; _fbp=fb.1.1723813187334.806285164400499549; _uetsid=6a8adf005bcf11efbd6bb7b7960ff497; _uetvid=6a8afa405bcf11efaf3547613939106a; _hjSessionUser_2417598=eyJpZCI6ImZmMDU5YmE2LTc5MjItNTIzNS1hYzNmLTliMTEzZDU4NzBmOCIsImNyZWF0ZWQiOjE3MjM4MTMxODc3MDQsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2417598=eyJpZCI6ImVlYzQyNzA0LWVlNmYtNDRiZi1hOGU2LWU1M2QyOGRkMjdmZSIsImMiOjE3MjM4MTMxODc3MDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%22b75a587b-675f-49e8-87c7-c370ababd136%22; slireg=https://scout.us1.salesloft.com; sliguid=9a6f9c94-4bf9-4512-84eb-e9ec4ac17a74; slirequested=true; drift_campaign_refresh=09b969f4-a1e2-4e81-9043-cb17d16e98f3; __hstc=168719870.dac3c70af4a1cfe78f94f901bed029b9.1723813189638.1723813189638.1723813189638.1; hubspotutk=dac3c70af4a1cfe78f94f901bed029b9; __hssrc=1; __hssc=168719870.1.1723813189638; drift_aid=3b7efed2-de3e-4d88-ad98-e6ca866f6ec9; driftt_aid=3b7efed2-de3e-4d88-ad98-e6ca866f6ec9; _ga_D567ES4C1N=GS1.1.1723813186.1.1.1723813201.0.0.0; _ga_F0YXXGK0LB=GS1.1.1723813187.1.0.1723813201.46.0.0; _dd_s=rum=1&id=d4fbb6d6-3775-4bad-9e48-5de21c7525e6&created=1723813186100&expire=1723814326107',
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

    response = requests.get(url, data=payload, headers=headers ,proxies=proxies , verify=ca_cert_path)
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.content ,'lxml')

        container = soup.find('div' ,class_ = 'content-wrap')
        if container:
            print('container found!')

        h1= container.find_all('h1' ,class_= 'article-title')
        if h1:
            for tag in h1:
                article = tag.find('a')
                link = article['href']
                if 'https://www.cbinsights.com/' not in link:
                    url = 'https://www.cbinsights.com'+link
                    # print(url)
                    article_links.add(url)
        print(len(article_links))
        return(article_links)         

    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})

def cbinsights_article_details(url):

    missing_fields = []  # List to store missing fields

    proxies = {
        'http': 'http://brd-customer-hl_f622b815-zone-web_unlocker1:v2zbd45ye9d0@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_f622b815-zone-web_unlocker1:v2zbd45ye9d0@brd.superproxy.io:22225',
    }
    
    
    ca_cert_path = 'ca.crt'

    try:
        response = requests.get(url ,proxies=proxies ,verify =ca_cert_path)
        
        if response.status_code == 200:
           
            soup = BeautifulSoup(response.content, 'lxml')

            # Extract the title
            title_tag = soup.find('div', class_= 'title')
            if title_tag:
                title = title_tag.text.strip()
                # print(title)
            else:
                title = ""
                missing_fields.append("Title")

            # Extracts author
            author=""

            # Extract the published date
            published_tag = soup.find('li' , class_='publish-date')
            if published_tag:
                published = published_tag.text.strip()
                
                published_date = convert_date_format(published)
                # print(published_date)
        
            else:
                published = ""
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            paragraph_texts = []
           
            paragraphs = soup.find_all('div', class_='article-content')
            # print(len(paragraphs))
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
    
if __name__ == "__main__":

    total_article_links = cbinsights_article_list()

    articles_data = []
    for url in total_article_links: 
        print('scraping for: ',url)       
        article_details = cbinsights_article_details(url)

        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file
    with open("zzsample outputs/cbinsights_articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)
        # 

    print("Data fetched and stored in cbinsights_articles.json")