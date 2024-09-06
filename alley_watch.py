import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

# Base URL for AlleyWatch
base_url = "https://www.alleywatch.com/"

# Define headers for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
    'Cookie': 'PHPSESSID=96gv4pbjtk4lnhe90ososkhdsd'
}

def alleywatch_convert_date(date_str):
    """Convert a date string to 'yyyy-mm-dd' format."""
    try:
        # Parse the date string using datetime
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        # Convert to 'yyyy-mm-dd' format
        return date_obj.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Error converting date: {e}")
        return ""

def alleywatch_article_urls():
    """Scrape the AlleyWatch homepage for article URLs."""
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs within <h3> tags with class "jeg_post_title"
    article_tags = soup.find_all('h3', class_='jeg_post_title')
    
    article_urls = []
    for tag in article_tags:
        article_url = tag.find('a')['href']
        # Extract the published date from the same section
        date_tag = tag.find_next('div', class_='jeg_meta_date')
        published_text = date_tag.text.strip().replace('•', '').replace('\n', '') if date_tag else ""
        
        # Convert published date to 'yyyy-mm-dd' format
        published_date = alleywatch_convert_date(published_text) if published_text else ""
        
        # Append article URL and published date
        article_urls.append(article_url)
    
    return article_urls

def alleywatch_article_details(article_url):
    """Scrape details from an AlleyWatch article."""
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', class_='jeg_post_title')
    title = title_tag.text.strip() if title_tag else ""

    # Scrape the author name and URL
    author_tag = soup.find('div', class_="jeg_meta_author")
    author_name = author_tag.find('a').text if author_tag else ""
    author_url = author_tag.find('a')['href'] if author_tag else ""

    # Scrape the published date
    published_tag = soup.find('div', class_='jeg_meta_date')
    published_text = published_tag.text.strip().replace('•', '').replace('\n', '') if published_tag else ""
    published_date = alleywatch_convert_date(published_text) if published_text else ""

    # Scrape the article body
    body_tag = soup.find('div', class_='content-inner')
    body = body_tag.text.strip() if body_tag else ""

    # Scrape author details
    author_details = alleywatch_author_details(author_url) if author_url else {}

    # Return the article details, including author details
    article_details = {
        "title": title,
        "author_name": author_name,
        "author_details": author_details,  # Include the author details dictionary
        "published": published_text,
        "published_date": published_date,
        "body": body,
    }

    return article_details

def alleywatch_author_details(author_url):
    """Scrape the author's details from their profile page."""
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the author name
    author_name_tag = soup.find('h3', class_='jeg_author_name')
    author_name = author_name_tag.text.strip() if author_name_tag else ""

    # Scrape the author image
    author_img_tag = soup.find('img', class_='avatar')
    author_img = author_img_tag['src'] if author_img_tag else ""

    # Scrape the author Twitter URL
    author_twitter_tag = soup.find('a', class_='twitter')
    author_twitter = author_twitter_tag['href'] if author_twitter_tag else ""

    # Scrape the author LinkedIn URL
    author_linkedin_tag = soup.find('a', class_='linkedin')
    author_linkedin = author_linkedin_tag['href'] if author_linkedin_tag else ""

    # Return author details as a dictionary
    author_details = {
        "author_name": author_name,
        "author_img": author_img,
        "author_twitter": author_twitter,
        "author_linkedin": author_linkedin
    }

    return author_details

def alleywatch_save():
    """Fetch articles, scrape their details, and save them in the database."""
    domain = "alleywatch.com"
    website = Website.objects.get(domain=domain)
    article_urls = alleywatch_article_urls()

    for article_url in article_urls:
        if Articles.objects.filter(website=website, url=article_url).exists():
            # If the article already exists, use existing details
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
                # Scrape and save new article details
                article_details = alleywatch_article_details(article_url)
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author_name"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    category="tech"  # Set an appropriate category
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass
    
    return article_urls
