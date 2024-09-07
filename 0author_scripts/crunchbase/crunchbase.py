import requests 
from bs4 import BeautifulSoup
from proxy.models import Proxy
from proxy.browser import browser
from websites.contrib import categories
from tech.models import Website, Articles
from datetime import datetime 

def crunchbase_date(published):
    date_object = datetime.strptime(published, '%B %d, %Y').date()
    return date_object 

def crunchbase_author_details(author_link):
    
    residential_proxies = {
            'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
        }
    ca_cert_path = 'ca.crt'
    response= requests.get(author_link, proxies=residential_proxies , verify=ca_cert_path )
    print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_linkedin=''
    author_twitter=''
    author_name = soup.find('h1').text.strip()
    author_img = soup.find('div' ,class_='herald-mod-desc').find('img')['data-src']
    # author_twitter = soup.find('a',class_='fa fa-twitter')['href']
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details

def crunchbase_article_list(page_count=1):
    if page_count  == 1:
        pages = ["https://news.crunchbase.com/"]
    else:
        pages = ["https://news.crunchbase.com/", "https://news.crunchbase.com/page/2/", "https://news.crunchbase.com/page/3/"]
    proxy = Proxy.objects.first()
    proxies = proxy.get_proxy()
    article_list = []
    for page in pages: 
        print(page)
        # response = requests.get(page, proxies=proxies)
        response = browser(url=page)
        soup = BeautifulSoup(response, "html.parser")
        # articles = soup.find_all("article", {"index": "omar3"})
        articles = soup.find_all("h2", {"class": "entry-title h3"})
        
        # print(len(articles))
        for article in articles:
            # url = article.find(class_="entry-title h3").find("a")['href']
            url = article.find("a")["href"]
            print("Url : ", url)
            article_list.append(url)
    # print(len(article_list), " Total articles found!")
    return article_list


def crunchbase_article_details(url="https://news.crunchbase.com/venture/climate-risk-software-startup-funding/"):
    response = browser(url=url)
    soup = BeautifulSoup(response, "html.parser")
    title = soup.find("header", class_="entry-header").find("h1").text.strip()
    published = soup.find(class_="meta-item herald-date").text.strip()
    published_date = crunchbase_date(published=published)   
    
    author = soup.find(class_="meta-item herald-author").text.strip()
    author_link = soup.find(class_="meta-item herald-author").find('a')['href']
    body = ""
    paragraphs = soup.find(class_="entry-content herald-entry-content").find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    body = body.split("Illustration:")[0]

    author_info = crunchbase_author_details(author_link)
    payload = {
            'domain':"news.crunchbase.com",
            'title': title,
            'published': published,
            "published_date": published_date,
            'author': author,
            'author_info':author_info,
            'url': url,
            'body': body, 
            "category": categories['venture']
        }
    
    return payload


def crunchbase_save():
    domain = "news.crunchbase.com"
    website = Website.objects.get(domain=domain)
    article_urls = crunchbase_article_list()
    for i,url in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=url).exists():
            art = Articles.objects.filter(url=url).first()
            article = {
                "author": art.author,
                'author_info':art.author_info,
                'title': art.title,
                "published": art.published,
                'url': art.url,
                "body" : art.body
            }
        else: 
            try: 
                article = crunchbase_article_details(url)
                # print(url, article)
                art = Articles(
                    website = website,
                    url = article['url'],
                    title = article["title"],
                    author = article["author"],
                    author_info = article["author_info"],
                    body = article["body"],
                    published = article["published"],
                    published_date = article['published_date'],
                    category = article['category']
                )
                art.save()
            except Exception as e : 
                
                pass
        # print(i, "/" , len(article_urls))
    return article
