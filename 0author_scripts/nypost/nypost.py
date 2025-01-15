import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 
    # date_obj = datetime.strptime(date_str, "%Y%m%d")
    # date_str = date_obj.strftime("%Y-%m-%d")
    return date_str



def nypost_author_details(url):
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.request("GET", url, headers=headers ,proxies=proxies , verify=ca_cert_path)   
    
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    author_linkedin=author_twitter=author_img=''

    author_name = soup.find('meta', {'property':'og:title'})['content'].split(" – ")[0].strip()
    author_img = soup.find('header', class_="archive__header").find('img')['src'] if soup.find('header', class_="archive__header").find('img') else ''
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def nypost_article_list():
 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    url = "https://nypost.com/tech/"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find_all('h3' ,class_="headline")
        
        if articles:
            for article in articles:
                anchor = article.find('a')
                if anchor.get('href') is None:
                        continue
                if "nypost.com" in anchor.get('href', '') and "video" not in anchor.get('href', ''):
                    link = anchor.get('href')    
                    article_links.add(link)
                
        else:
            print("Article section was not found")            
        # print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})


# nypost_article_list()


def nypost_article_details(url):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("meta", {"property":"og:title"})['content']
    # print(title)
    article_image = soup.find("meta", {"property":"og:image"})['content']
    published = soup.find("meta", {"property":"article:published_time"})['content']
    date_str = published.split("T")[0]
    published_date = convert_date_format(date_str)
   

    try:
        author_container = soup.find('div' , class_="byline__author")
        author = author_container.find('a').text.strip()
        author_url = author_container.find('a').get('href')
        author_info = nypost_author_details(author_url)
    except:
        author = soup.find('div' , class_="byline__author").text.strip()
        author_info ={"author_name": author, "author_img" :"", "author_linkedin" : "", "author_twitter" : ""}
    # print(author_info)

    body = ""
    paragraphs = soup.select('div.single__content.entry-content.m-bottom > p')
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "nypost.com",
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


# articles_detail = nypost_article_details("https://nypost.com/2025/01/14/tech/dont-bring-your-iphone-to-the-bathroom-when-you-shower-for-a-very-scary-reason-influencer-warns-a-little-psa/")


if __name__ == "__main__":

    total_article_links = nypost_article_list()

    articles_data = []
   
    for url in total_article_links:  
        print("scraping article details for: ", url)      
        article_details = nypost_article_details(url)
        if article_details:
            articles_data.append(article_details)

    with open('0author_scripts/nypost/nypost_article_details.json', 'w') as file:
        json.dump(articles_data, file, indent=4)

    print("Data has been written to the file")