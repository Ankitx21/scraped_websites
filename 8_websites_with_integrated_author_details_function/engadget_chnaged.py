import requests
from bs4 import BeautifulSoup
from tech.models import Articles, Website
from proxy.models import Proxy

def engadget_article_urls():
    url = "https://www.engadget.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article links
    articles = soup.find_all('h2', class_='My(0)')
    article_urls = []

    for article in articles:
        a_tag = article.find('a', href=True)
        if a_tag:
            article_urls.append("https://www.engadget.com" + a_tag['href'])
    
    return article_urls

def engadget_author_details(author_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the author name and image
    author_name = soup.find('h1', class_='Fz(24px)--sm Fz(34px)--md Fz(40px) Lh(40px) Fw(700) Pt(20px) Pstart(25px) My(0px)!').text.strip() if soup.find('h1', class_='Fz(24px)--sm Fz(34px)--md Fz(40px) Lh(40px) Fw(700) Pt(20px) Pstart(25px) My(0px)!') else ''
    author_img = soup.find('img', class_='W(100px) H(100px) Bdrs(50%)')['src'] if soup.find('img', class_='W(100px) H(100px) Bdrs(50%)') else ''
    
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

def engadget_article_details(article_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title = soup.find('h1', id='caas-lead-header-undefined').text.strip() if soup.find('h1', id='caas-lead-header-undefined') else None

    # Scrape the author name and URL
    author_tag = soup.find('span', class_='caas-author-byline-collapse').find('a', class_='link') if soup.find('span', class_='caas-author-byline-collapse') else None
    author_name = author_tag.text.strip() if author_tag else None
    author_url = author_tag['href'] if author_tag else None

    # Scrape the published date and the published text
    time_tag = soup.find('time', datetime=True)
    published_date = time_tag['datetime'].split('T')[0] if time_tag else None  # Just the date part
    published = time_tag.text.strip() if time_tag else None  # Full text

    # Scrape the article body
    body = soup.find('div', class_='caas-body').text.strip() if soup.find('div', class_='caas-body') else None

    # Get additional author details if author URL is available
    author_details = engadget_author_details(author_url) if author_url else {"author_name": author_name, "author_img": "", "author_linkedin": "", "author_twitter": ""}
    
    article_details = {
        "title": title,
        "author_details": author_details,
        "published_date": published_date,
        "published": published,
        "body": body
    }

    return article_details



def engadget_save():
    domain = "engadget.com"
    website = Website.objects.get(domain=domain)
    article_urls = engadget_article_urls()

    for article_url in article_urls:
        if Articles.objects.filter(website=website, url=article_url).exists():
            # Retrieve existing article details from the database
            art = Articles.objects.get(url=article_url)
            article = {
                "author": art.author,
                "author_details": art.author_details,
                'title': art.title,
                "published": art.published,
                "published_date": art.published_date,
                'url': art.url,
                "body": art.body
            }
        else:
            try:
                # Scrape article details
                article_details = engadget_article_details(article_url)
                
                # Save new article details to the database
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author_details"]["author_name"],
                    author_details=article_details["author_details"],
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    # Assuming there's a category field; you might need to adjust this
                    category="general"  # Replace with the appropriate category if needed
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass

    return article_urls
