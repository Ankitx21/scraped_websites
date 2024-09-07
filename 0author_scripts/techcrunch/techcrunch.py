from datetime import datetime, timedelta
from proxy.browser import browser
from bs4 import BeautifulSoup
from tech.models import Articles, Website
from proxy.models import Proxy
import requests 
from websites.contrib import categories

def techcrunch_date(url):
    parts = url.split('/')
    year = parts[3]
    month = parts[4]
    day = parts[5]
    date_str = f"{year}-{month}-{day}"
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    return date_obj

# funtion to store author details 
#<-----------------------added
def techcrunch_author_details(author_link):

    response= requests.get(author_link)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_linkedin=''
    author_twitter=''
    author_name = soup.find('h1').text
    author_img = soup.find('div' ,class_='tc23-author-archive-hero__media').find('img')['src']
    author_social = soup.find('div',class_='tc23-author-archive-hero__socials social-icons').find_all('a',{'rel':'me noopener'})
    # for a in author_social:
    #     social = a.find('svg')['class']
    #     if social[0]=='share-linkedin':
    #         author_linkedin = a['href']
    #     else:
    #         author_twitter = a['href']

    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def techcrunch_article_list():
    article_urls = []
    url_list = ["https://techcrunch.com/", "https://techcrunch.com/page/2/"]
    proxy = Proxy.objects.first()
    proxies = proxy.get_proxy()
    for url in url_list:
        rsp = requests.get(url=url, proxies=proxies )
        response = rsp.text
        soup = BeautifulSoup(response, "html.parser")
        # Define the target style
        article_divs = soup.find_all(class_="wp-block-tc23-post-picker")
        print(len(article_divs))
        for article in article_divs:
            href = article.find("h2").find("a")
            
            article_urls.append(href['href'])
    print(len(article_urls), "total found")
    print("total articles found ", len(article_urls))
    return article_urls


def techcrunch_article_details(url="https://techcrunch.com/2024/05/15/temu-accused-of-breaching-eus-dsa-in-bundle-of-consumer-complaints/"):
    proxy = Proxy.objects.first()
    proxies = proxy.get_proxy()
    rsp = requests.get(url=url, proxies=proxies)
    response = rsp.text
    soup = BeautifulSoup(response, "html.parser")
    title = soup.find("main").find("h1", class_="wp-block-post-title").text.strip()
    author = soup.find(class_="wp-block-tc23-author-card-name").find("a").text.strip()
    author_link = soup.find(class_="wp-block-tc23-author-card-name").find("a")['href']
    published = soup.find(class_="wp-block-post-date").text.strip()
    published_date = techcrunch_date(url=url)
    body = ""
    paragraphs = soup.find(class_="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow").find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    # author details
    author_info= techcrunch_author_details(author_link)      #<-----------------------call to function
    payload = {
        'domain': "techcrunch.com",
        'title': title,
        'published': published,
        "published_date": published_date,    #<-----------------------added
        'author': author,
        'author_details': author_info,
        'url': url,
        'body': body
    }
    return payload


def techcrunch_save():
    domain = "techcrunch.com"
    website = Website.objects.get(domain=domain)
    article_urls = techcrunch_article_list()
    for i, article in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=article).exists():
            art = Articles.objects.filter(url=article).first()
            article = {
                "author": art.author,
                "author_details": art.author_details,  #<-----------------------added
                'title': art.title,
                "published": art.published,
                'url': art.url,
                "body": art.body
            }
        else:
            try: 
                article = techcrunch_article_details(article)
                art = Articles(
                    website=website,
                    url=article['url'],
                    title=article["title"],
                    author=article["author"],
                    author_details = article["author_details"],    #<-----------------------added
                    body=article["body"],
                    published=article["published"],
                    published_date=article['published_date'],
                    category=categories['venture']
                )
                art.save()
            except Exception as e:
                print(e)
                pass 
        # print(i, "/", len(article_urls))
    return article_urls



# def techcrunch_date(date_string):
#     # Split the string into its components
#     time_str, tz_str, date_str = date_string.split(' • ')

#     # Parse the time and date
#     datetime_str = f"{date_str} {time_str}"
#     naive_datetime = datetime.strptime(datetime_str, '%B %d, %Y %I:%M %p')

#     # Define timezone offsets (PDT is UTC-7, PST is UTC-8)
#     timezone_offsets = {
#         'PDT': -7,
#         'PST': -8,
#         # Add other timezones if needed
#     }

#     # Calculate the UTC offset in hours
#     if tz_str not in timezone_offsets:
#         raise ValueError(f"Unsupported timezone: {tz_str}")
    
#     offset_hours = timezone_offsets[tz_str]

#     # Convert to UTC by subtracting the offset
#     utc_datetime = naive_datetime - timedelta(hours=offset_hours)

#     return utc_datetime