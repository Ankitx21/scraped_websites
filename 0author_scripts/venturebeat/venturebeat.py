from proxy.browser import browser
from bs4 import BeautifulSoup
from websites.venture.pitchbook import save_articles_with_api
from websites.contrib import categories
from tech.models import Articles, Website
from datetime import datetime
from proxy.sel import SBR_WEBDRIVER
import requests
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

def venturebeat_convert_published(published):
    """converts the published date to standard python date formate"""
    dt = published.split("T")[0]
    date_obj = datetime.strptime(dt, '%Y-%m-%d').date()
    return date_obj

def venturebeat_author_details(author_link):
    
    response= requests.get(author_link )
    print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_name = soup.find('span', class_='author-name').text.strip()
    print(author_name)
    author_img = soup.find('div' ,id='author-avatar').find('img')['src']
    print(author_img)

    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : "", "author_twitter" : ""}
    return author_details


def venturebeat_article_list():
    article_list = []
    blog_urls = ["https://venturebeat.com/"]
    for url in blog_urls : 
        response = browser(url=url)
        soup = BeautifulSoup(str(response), "html.parser")
        allheadings = soup.find_all("article")
        for heading in allheadings:
            a = heading.find("a")
            article_url = a['href']
            article_list.append(article_url)
    article_list = list(set(article_list))
    return article_list


def venturebeat_article_details(url="https://venturebeat.com/ai/ai-stack-attack-navigating-the-generative-tech-maze/"):
    body = ""
    response = browser(url=url)
    soup = BeautifulSoup(response, "html.parser")
    head_section = soup.find("header", class_="Article__header")
    title = head_section.find("h1", class_="article-title").text.strip()
    author = head_section.find(class_="Article__author-info").text.strip()

    author_link = head_section.find(class_="Article__author-info").find('a',class_='author url fn')['href']
    author_info = venturebeat_author_details(author_link)

    if "@" in author:
        author = author.split("@")[0]
    published_element = soup.find("time")
    published = published_element.text.strip()
    pub = published_element.get('datetime')
    published_date = venturebeat_convert_published(published=pub)
    paragraphs = soup.find("article").find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    payload = {
            'domain':"venturebeat.com",
            'title': title,
            'published': published,
            "published_date": published_date,
            'author': author,
            'author_details': author_info,
            'url': url,
            'body': body
        }
    return payload




def venturebeat_save():
    domain = "venturebeat.com"
    website = Website.objects.get(domain=domain)
    article_urls = venturebeat_article_list()
    for i, url in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=url).exists():
            art = Articles.objects.filter(url=url).first()
            article = {
                "author": art.author,
                'author_details': art.author_info,
                'title': art.title,
                "published": art.published,
                'url': art.url,
                "body" : art.body
            }
        else: 
            try: 
                article = venturebeat_article_details(url)
                art = Articles(
                    website = website,
                    url = article['url'],
                    title = article["title"],
                    author = article["author"],
                    author_details= article["author_info"],
                    body = article["body"],
                    published = article["published"],
                    published_date = article['published_date'],
                    category = categories['venture']
                )
                art.save()
            except Exception as e:
                print(e)
                pass 
    return article_urls

if __name__ == "__main__":
    venturebeat_article_list()

