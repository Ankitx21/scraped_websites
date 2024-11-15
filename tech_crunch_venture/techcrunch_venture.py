import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
import re

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL and proxies
base_url = 'https://techcrunch.com/category/venture/'
proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# Function to get all article URLs from the main page
def techcrunch_venture_article_urls():
    response = requests.get(base_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='loop-card__title-link')
    unique_links = [article['href'] for article in articles if article.get('href')]
    return unique_links


# Function to convert published date to 'dd-mm-yyyy' format
def techcrunch_venture_convert_published_date(date_str):
    try:
        # Remove the timezone part (e.g., "PST") using regex to capture only the date and time
        date_without_timezone = re.sub(r'\s\w{3}\s·\s', ' · ', date_str)
        
        # Parse the remaining part of the date string, e.g., "6:00 PM · November 13, 2024"
        date_obj = datetime.strptime(date_without_timezone, '%I:%M %p · %B %d, %Y')
        
        # Return the date in 'dd-mm-yyyy' format
        return date_obj.strftime('%d-%m-%Y')
    except ValueError:
        return None



# Function to scrape article details
def techcrunch_venture_article_details(article_url):
    response = requests.get(article_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract article title
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
    
    # Extract published date and formatted date
    published = soup.find('div', class_='wp-block-post-date').get_text(strip=True) if soup.find('div', class_='wp-block-post-date') else None
    published_date = None
    if published:
        # Use the full `published` date string for conversion
        published_date = techcrunch_venture_convert_published_date(published)
    
    # Extract author link
    author_tag = soup.find('a', class_='wp-block-tc23-author-card-name__link') or soup.find('a', class_='post-authors-list__author')
    author_link = author_tag['href'] if author_tag else ''
    
    # Extract article body
    body_div = soup.find('div', class_="entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained")
    body = ' '.join(p.get_text(strip=True) for p in body_div.find_all('p')) if body_div else None
    
    # Extract article images
    article_images = techcrunch_venture_article_images(soup)
    
    # Get author details using the author URL if available
    author_details = techcrunch_venture_author_details(author_link) if author_link else None
    
    return {
        'url': article_url,
        'title': title,
        'published': published,
        'published_date': published_date,
        'author_link': author_link,
        'body': body,
        'images': article_images,
        'author_details': author_details,
    }

# Function to extract article images
def techcrunch_venture_article_images(soup):
    images = []
    
    # Featured image
    featured_img = soup.find('figure', class_="wp-block-post-featured-image")
    if featured_img:
        img_tag = featured_img.find('img')
        if img_tag:
            images.append(img_tag['src'])
    
    # Additional large images
    large_images = soup.find_all('figure', class_="wp-block-image size-large is-resized")
    for figure in large_images:
        img_tag = figure.find('img')
        if img_tag:
            images.append(img_tag['src'])
    
    return images

# Function to fetch author details from the author URL
def techcrunch_venture_author_details(author_url):
    response = requests.get(author_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract author name
    author_name = soup.find('h1', class_='wp-block-techcrunch-author-archive-hero__title')
    author_name = author_name.get_text(strip=True) if author_name else None
    
    # Extract author image
    author_img = None
    img_figure = soup.find('figure', class_='tc23-author-archive-hero__media')
    if img_figure:
        img_tag = img_figure.find('img')
        if img_tag:
            author_img = img_tag['src']
    
    # Extract author Twitter and LinkedIn
    author_twitter = ''
    author_linkedin = ''
    social_links = soup.find_all('a', class_="wp-block-techcrunch-author-archive-hero__social-icon")
    for link in social_links:
        href = link.get('href')
        if 'twitter.com' in href:
            author_twitter = href
        elif 'linkedin.com' in href:
            author_linkedin = href
    
    return {
        'author_name': author_name,
        'author_img': author_img,
        'author_twitter': author_twitter,
        'author_linkedin': author_linkedin,
    }

# Function to fetch and print article details in structured format
def techcrunch_save():
    articles_data = []
    article_urls = techcrunch_venture_article_urls()
    
    for url in article_urls:
        # Fetch article details
        article_data = techcrunch_venture_article_details(url)
        articles_data.append(article_data)
        
        print(article_data)  # Print each article's details as a dictionary
    
    return articles_data

# Execute and retrieve all article details
all_articles_details = techcrunch_save()
