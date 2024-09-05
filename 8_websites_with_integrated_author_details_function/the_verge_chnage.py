import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

def verge_tech_article_urls():
    base_url = "https://www.theverge.com"
    tech_url = f"{base_url}/tech"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'vmidv1=bc4a62af-a549-4def-8024-0fe2dddd4191; _chorus_geoip_continent=NA; _vm_consent_type=opt-out'
    }

    response = requests.get(tech_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs
    links = soup.find_all('a', class_='after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin')
    article_urls = [base_url + link['href'] for link in links if link.get('href')]

    return article_urls

def verge_tech_article_details(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'vmidv1=bc4a62af-a549-4def-8024-0fe2dddd4191; _chorus_geoip_continent=NA; _vm_consent_type=opt-out'
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', class_='inline font-polysans text-22 font-bold leading-110 md:text-33 lg:hidden')
    title = title_tag.text.strip() if title_tag else ""

    # Scrape the author name and URL using the <span> and <a> tags
    author_span = soup.find('span', class_='font-medium')
    author_tag = author_span.find('a') if author_span else None
    author_name = author_tag.text.strip() if author_tag else ""
    author_url = "https://www.theverge.com" + author_tag['href'] if author_tag else ""

    # Scrape the published date
    published_tag = soup.find('time', class_='duet--article--timestamp font-polysans text-12')
    published = published_tag.text.strip() if published_tag else ""
    published_date = published_tag['datetime'].split('T')[0] if published_tag else ""

    # Scrape the article body
    body_tag = soup.find('div', class_='duet--article--article-body-component-container clearfix sm:ml-auto md:ml-100 md:max-w-article-body lg:mx-100')
    body = body_tag.text.strip() if body_tag else ""

    # Scrape author details
    author_details = verge_tech_author_details(author_url) if author_url else {}

    # Return the article details, including author details
    article_details = {
        "title": title,
        "author_name": author_name,
        "author_details": author_details,  # Include the author details dictionary
        "published": published,
        "published_date": published_date,
        "body": body,
    }

    return article_details

def verge_tech_author_details(author_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the author name
    author_name_tag = soup.find('h1', class_='font-manuka text-100 leading-80 tracking-1 text-black dark:text-white md:text-160')
    author_name = author_name_tag.text.strip() if author_name_tag else ''
    
    # Scrape the author image URL
    author_img_tag = soup.find('img', class_='rounded-full')
    author_img = author_img_tag['src'] if author_img_tag else ''
    
    # Placeholder for LinkedIn and Twitter
    author_linkedin = ''
    author_twitter = ''
    
    author_details = {
        "author_name": author_name,
        "author_img": author_img,
        "author_linkedin": author_linkedin,
        "author_twitter": author_twitter
    }
    
    return author_details


def verge_save():
    domain = "theverge.com"
    website = Website.objects.get(domain=domain)
    article_urls = verge_tech_article_urls()
    for i, article_url in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=article_url).exists():
            art = Articles.objects.filter(url=article_url).first()
            article = {
                "author": art.author,
                "author_details": art.author_details,  # Use existing author details
                'title': art.title,
                "published": art.published,
                "published_date": art.published_date,
                'url': art.url,
                "body": art.body
            }
        else:
            try:
                article_details = verge_tech_article_details(article_url)
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author_name"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    # Assuming there's a category field; you might need to adjust this
                    category="tech"  # Replace with the appropriate category
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass
    return article_urls
