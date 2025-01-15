import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 
    # date_obj = datetime.strptime(date_str, "%Y%m%d")
    # date_str = date_obj.strftime("%Y-%m-%d")
    return date_str



def visual_capitalist_author_details(url):
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

    author_name = soup.find('meta', {'property':'og:title'})['content'].split(",")[0].strip()
    author_img = soup.find('meta', {'property':'og:image'})['content']
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def visual_capitalist_article_list():
 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    url = "https://www.visualcapitalist.com/"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find('div' , id='mvp-main-body-wrap').find_all('a' ,{'rel':'bookmark'})
        if articles:
            for article in articles:
                if article.get('href') == None:
                    continue
                link = article.get('href')    
                article_links.add(link)
                # print(link)
        else:
            print("Article section was not found")            
        print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})

# visual_capitalist_article_list()

def visual_capitalist_article_details(url="https://www.visualcapitalist.com/breaking-down-the-wealth-of-americas-top-20-billionaires/"):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'


    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("meta", {"property":"og:title"})['content']
    print(title)
    article_image = soup.find("meta", {"property":"og:image"})['content']
    # print(article_image)
    published = soup.find("meta", {"property":"article:published_time"})['content']
    # print(published)
    date_str = published.split('T')[0].strip()
    published_date = convert_date_format(date_str)

    # print(published_date)

    author_container = soup.find('span', class_="author-name vcard fn author").find("a")
    author = author_container.text.strip()
    author_link = author_container['href']
    # print(author)
    # print(author_link)
    author_info = visual_capitalist_author_details(author_link)
    # print(author_info)

    
    body = ""
    paragraphs = soup.find('div', id="mvp-content-main").find_all("p")[2:]
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "visualcapitalist.com",
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

    total_article_links = visual_capitalist_article_list()

    articles_data = []
   
    for url in total_article_links:        
        article_details = visual_capitalist_article_details(url)
        if article_details:
            articles_data.append(article_details)
    
    # Save scraped data to a JSON file  scraped_websites\zzsample outputs
    
    with open('0author_scripts/visualcapitalist/visual_capitalist_article_details.json', 'w') as f:
            json.dump(articles_data, f, indent=4)
    
   
   
    print("Data fetched and stored in visual_capitalist_article_details.json")



