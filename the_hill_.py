import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy and header details
proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
website_url = 'https://thehill.com/'

# Function to get all article URLs from the main page
def the_hill_article_urls():
    response = requests.get(website_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    unique_links = set()
    # Extract various article links
    just_in_articles = soup.find_all('a', class_='list-item__link | color-dark-gray')
    unique_links.update(article.get('href') for article in just_in_articles if article.get('href'))
    
    featured_articles = soup.find_all('div', class_='featured-cards__headline_list-right--bottom-headline | weight-semibold | leading-flat')
    unique_links.update(featured.find('a').get('href') for featured in featured_articles if featured.find('a'))
    
    popular_articles = soup.find_all('a', class_='most-popular-item__link | color-dark-gray text-400 leading-flat weight-bold | display-block')
    unique_links.update(popular.get('href') for popular in popular_articles if popular.get('href'))
    
    solo_article = soup.find('h1', class_='homepage-video-hero-right-rail--top-story__content_headline | weight-semibold | leading-flat')
    if solo_article:
        link_tag = solo_article.find('a')
        if link_tag:
            unique_links.add(link_tag.get('href'))
    
    return list(unique_links)

# Function to scrape article details
def the_hill_article_details(article_url):
    response = requests.get(article_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract article title
    title = soup.find('h1', class_="page-title").get_text(strip=True) if soup.find('h1', class_="page-title") else None
    
    # Extract author link and published date
    author_section = soup.find('section', class_="submitted-by | header__meta | text-transform-upper text-300 color-light-gray weight-semibold font-base desktop-only")
    author_link = author_section.find('a')['href'] if author_section and author_section.find('a') else None
    published_date = author_section.get_text(strip=True).split("-")[1].strip().split(" ")[0] if author_section else None
    
    # Extract article body
    body_content = soup.find('div', class_="article__text | body-copy | flow")
    body = ' '.join(p.get_text(strip=True) for p in body_content.find_all('p')) if body_content else None
    
    # Extract article images
    article_images = the_hill_article_images(soup)
    
    # Get author details using the author URL if available
    author_details = the_hill_author_details(author_link) if author_link else None
    
    return {
        'url': article_url,
        'title': title,
        'author_link': author_link,
        'published_date': published_date,
        'body': body,
        'images': article_images,
        'author_details': author_details,
    }

# Function to extract article image URLs
def the_hill_article_images(soup):
    images = []
    figures = soup.find_all('figure', class_="article__featured-image")
    for figure in figures:
        img_tag = figure.find('img')
        if img_tag and 'srcset' in img_tag.attrs:
            first_url = img_tag['srcset'].split(',')[0].split()[0]
            images.append(first_url)
    return images

# Function to fetch author details from the author URL
def the_hill_author_details(author_url):
    response = requests.get(author_url, headers=headers, proxies=proxies, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    author_img = soup.find('img', class_='author-page__author-image')['src'] if soup.find('img', class_='author-page__author-image') else None
    author_name = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
    twitter_section = soup.find('div', class_='author-page__author-container__info__social')
    author_twitter = twitter_section.find('a')['href'] if twitter_section and twitter_section.find('a') else None
    
    return {
        'author_img': author_img,
        'author_name': author_name,
        'author_twitter': author_twitter,
    }

# Function to fetch and print article details in structured format
def the_hill_save():
    articles_data = []
    article_urls = the_hill_article_urls()
    
    for url in article_urls:
        # Ensure full URL format
        full_url = 'https://thehill.com' + url if url.startswith('/') else url
        
        # Fetch article details
        article_data = the_hill_article_details(full_url)
        articles_data.append(article_data)
        
        print(article_data)  # Print each article's details as a dictionary
    
    return articles_data

# Execute and retrieve all article details
all_articles_details = the_hill_save()
