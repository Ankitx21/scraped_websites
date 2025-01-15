import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 
    date_obj = datetime.strptime(date_str, "%Y%m%d")
    date_str = date_obj.strftime("%Y-%m-%d")
    return date_str



def coindesk_author_details(url):
    response =requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    author_linkedin=author_twitter=author_img=''

    author_name = soup.find('meta', {'property':'og:title'})['content'].split("|")[0].strip()
    author_img = "https://www.coindesk.com" + soup.find('img' ,class_ = "w-full h-full object-cover rounded-full max-w-full max-h-full")['src']
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def coindesk_article_list():
 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
        'Cookie': 'city=Ashburn; country=US; currencyCode=USD; currencyName=United%20States%20dollar; currencySymbol=%24; oficialCountryName=United%20States%20of%20America; region=iad1; subregion=North%20America'
    }


    url = "https://www.coindesk.com/tech"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find_all('div' ,class_="flex flex-col")
        if articles:
            for article in articles:
                anchor = article.find('a')
                if anchor.get('href') == None:
                    continue
                link = anchor.get('href')

                url = "https://www.coindesk.com" +link
                article_links.add(url)
                # print(url)
        else:
            print("Article section was not found")            
        # print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})


# coindesk_article_list()
# url = "https://www.coindesk.com/tech/2025/01/10/babylon-labs-brings-new-momentum-to-bitcoin-zk-tech-through-bridge-to-cosmos-chains"

def coindesk_article_details(url):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
        'Cookie': 'city=Ashburn; country=US; currencyCode=USD; currencyName=United%20States%20dollar; currencySymbol=%24; oficialCountryName=United%20States%20of%20America; region=iad1; subregion=North%20America'
    }

    
    response = requests.request("GET", url, headers=headers ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("meta", {"property":"og:title"})['content']
    # print(title)
    article_image = soup.find("meta", {"property":"og:image"})['content']

    author_container = soup.find('div', class_= "uppercase Noto_Sans_xs_Sans-600-xs").find('a')
    author = author_container.text

    author_link = "https://www.coindesk.com"+author_container.get('href')
    author_info =  coindesk_author_details(author_link)

    published = soup.find("meta", {"name":"publish_date"})['content']
    published_date = convert_date_format(published)


    
    body = ""
    paragraphs = soup.find('div',{"data-module-name":"article-body"}).find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "coindesk.com",
        'title': title,
        'published': published,
        "published_date": published_date,  
        'author': author,
        "article_image": article_image,
        'author_details': author_info,
        'url': url,
        'body': body
    }
    return payload



if __name__ == "__main__":

    total_article_links = coindesk_article_list()

    articles_data = []
   
    for url in total_article_links:        
        article_details = coindesk_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file  scraped_websites\zzsample outputs
    
    with open('0author_scripts/coindesk/coindesk_article_details.json', 'w') as f:
        json.dump(articles_data, f, indent=4)
   
    # print("Data fetched and stored in coindesk_articles.json")


