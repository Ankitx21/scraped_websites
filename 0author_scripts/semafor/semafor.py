import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_str

def semafor_author_details(url="https://www.semafor.com/author/mizy-clifton"):
    response =requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    author_linkedin=author_twitter=author_img=''

    author_name = soup.find('h2' , class_='styles_name__sSMUW').text.strip()
    author_img = soup.find('img', class_='styles_image__H7bOc')['src']
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def semafor_article_list():
 
    residential_proxies = {'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'}
    ca_cert_path = 'tem_ca.crt'

    url = "https://www.semafor.com/vertical/tech"

    payload = {}
    headers = {
    'Cookie': 'semafor-ft-id=ff102ddd-04c9-41d9-8114-0e733d2e0c41'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=residential_proxies , verify=ca_cert_path)   
    # print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find_all('a')
        if articles:
            for article in articles:
                if article.get('href') == None:
                    continue
                link = article.get('href')
                if 'article' in link: 
                    url = "https://www.semafor.com" +link        
                    article_links.add(url)
                    # print(url)
        else:
            print("Article section was not found")            
        # print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})



def semafor_article_details(url="https://www.semafor.com/article/01/10/2025/us-supreme-court-to-hear-arguments-in-tiktok-ban-or-sale-case"):
    
    
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
        'Cookie': 'semafor-ft-id=ff102ddd-04c9-41d9-8114-0e733d2e0c41'
    }

    response = requests.request("GET", url, headers=headers,  proxies=proxies , verify=ca_cert_path)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("meta", {"property":"og:title"})['content'].split("|")[0].strip()
    # print(title)
    author_container = soup.find('span', class_="styles_authorName__nDYcq styles_layoutControl__bF5y8").find("a")
    author = author_container.text.strip()
    author_link = "https://www.semafor.com/" + author_container['href']
    author_info = semafor_author_details(author_link)     
    published = soup.find("meta", {"name":"article:published_time"})['content']
    date_str =published.split('T')[0].strip() 
    published_date = convert_date_format(date_str) 
    article_image = soup.find("meta", {"property":"og:image"})['content']
   
   
    body = ""
    paragraphs = soup.find(class_="style_title__n4CiQ").find_next('div').find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "semafor.com",
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

    total_article_links = semafor_article_list()

    articles_data = []
   
    for url in total_article_links:        
        article_details = semafor_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file  scraped_websites\zzsample outputs
    
    with open('0author_scripts/semafor/semafor_article_details.json', 'w') as f:
        json.dump(articles_data, f, indent=4)
   
    # print("Data fetched and stored in semafor_articles.json")
