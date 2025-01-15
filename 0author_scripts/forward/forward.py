

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 

    return date_str



def forward_author_details(url):
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
    'Cookie': '__cflb=02DiuGa6qVRENudqZq2tx9MXz9axRzib7ekjRYrNP9bSL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.request("GET", url, headers=headers ,proxies=proxies , verify=ca_cert_path)   
    
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    author_linkedin=author_twitter=author_img=''

    author_name = soup.find('title').text.split(" – ")[0].strip()
    author_info_section = soup.find('article', class_='flex-container author-info')
    if author_info_section:
        img_tag = author_info_section.find('img')
        if img_tag:
            author_img = img_tag['src']
        else:
            author_img = ''
    else:
        author_img = ''
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def forward_article_list():
 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    url = "https://forward.com/"
    payload = {}

    headers = {
    'Cookie': '__cflb=02DiuGa6qVRENudqZq2tx9MXz9axRzib7ekjRYrNP9bSL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find('main' , id='main').find_all('a')
        if articles:
            for article in articles:
                href = article.get('href')
                if href and "https://forward.com/" in href and any(keyword in href for keyword in ["culture", "opinion", "advice"]): 
                    if "yiddish" not in href: 
                        if article.get('href') == None:
                            continue
                        link = article.get('href')    
                        article_links.add(link)
                        print(link)
        else:
            print("Article section was not found")            
        print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})


# forward_article_list()

def forward_article_details(url):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
    'Cookie': '__cflb=02DiuGa6qVRENudqZq2tx9MXz9axRzib7ekjRYrNP9bSL',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("meta", {"property":"og:title"})['content']
    print(title)
    article_image = soup.find("meta", {"property":"og:image"})['content']
    # print(article_image)
    published = soup.find("meta", {"property":"article:published_time"})['content']
    # print(published)
    date_str = published.split("T")[0]
    published_date = convert_date_format(date_str)

    # print(published_date)
    author_container = soup.find('div' , class_="post-author").find('a')
    author = author_container.text.strip()
    author_link = author_container['href']
    author_info = forward_author_details(author_link)
    # print(author_info)

    body = ""
    paragraphs = soup.select('article > p')
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "forward.com",
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

    total_article_links = forward_article_list()

    articles_data = []
   
    for url in total_article_links:  
        print("scraping article details for: ", url)      
        article_details = forward_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    with open('0author_scripts/forward/forward_article_details.json', 'w') as f:
        json.dump(articles_data, f, indent=4)
        print("Data fetched and stored in forward_article_details.json")


