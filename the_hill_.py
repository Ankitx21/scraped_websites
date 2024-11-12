import requests
from bs4 import BeautifulSoup
import warnings
import urllib3

# Suppress InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy details
proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-temp_residential:0vzz285ew72o@brd.superproxy.io:22225'
}

# Headers (optional, but good practice to include a user-agent)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# URL to scrape
website_url = 'https://thehill.com/'

# Function to get article URLs from the main page
def get_article_urls():
    try:
        response = requests.get(website_url, headers=headers, proxies=proxies, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            unique_links = set()

            # Collecting article URLs
            just_in_articles = soup.find_all('a', class_='list-item__link | color-dark-gray')
            for article in just_in_articles:
                link = article.get('href')
                if link and link not in unique_links:
                    unique_links.add(link)

            featured_articles = soup.find_all('div', class_='featured-cards__headline_list-right--bottom-headline | weight-semibold | leading-flat')
            for featured in featured_articles:
                link_tag = featured.find('a')
                if link_tag:
                    link = link_tag.get('href')
                    if link and link not in unique_links:
                        unique_links.add(link)

            popular_articles = soup.find_all('a', class_='most-popular-item__link | color-dark-gray text-400 leading-flat weight-bold | display-block')
            for popular in popular_articles:
                link = popular.get('href')
                if link and link not in unique_links:
                    unique_links.add(link)

            solo_article = soup.find('h1', class_='homepage-video-hero-right-rail--top-story__content_headline | weight-semibold | leading-flat')
            if solo_article:
                link_tag = solo_article.find('a')
                if link_tag:
                    link = link_tag.get('href')
                    if link and link not in unique_links:
                        unique_links.add(link)

            return list(unique_links)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

# Function to extract article details and images for each URL
def the_hill_article_details(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            details = {}

            # Extract title
            details['title'] = soup.find('h1', class_="page-title").get_text(strip=True) if soup.find('h1', class_="page-title") else ''
            
            # Extract author link
            author_section = soup.find('section', class_="submitted-by | header__meta | text-transform-upper text-300 color-light-gray weight-semibold font-base desktop-only")
            details['author_link'] = author_section.find('a')['href'] if author_section and author_section.find('a') else ''
            
            # Extract published date
            details['published_date'] = author_section.get_text(strip=True).split("-")[1].strip().split(" ")[0] if author_section else ''
            
            # Extract article body
            body_content = soup.find('div', class_="article__text | body-copy | flow")
            details['body'] = ' '.join(p.get_text(strip=True) for p in body_content.find_all('p')) if body_content else ''
            
            # Extract first article image
            article_images = the_hill_article_images(soup)
            details['article_img'] = article_images[0] if article_images else ''
            
            return details
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

# Function to extract image URLs from the article
def the_hill_article_images(soup):
    images = []
    figures = soup.find_all('figure', class_="article__featured-image")
    
    for figure in figures:
        img_tag = figure.find('img')
        if img_tag and 'srcset' in img_tag.attrs:
            srcset = img_tag['srcset']
            first_url = srcset.split(',')[0].split()[0]
            images.append(first_url)
    
    return images

# Function to extract author details (author image, name, and Twitter link)
def the_hill_author_details(author_url):
    try:
        response = requests.get(author_url, headers=headers, proxies=proxies, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            author_details = {}

            author_details['author_img'] = soup.find('img', class_='author-page__author-image')['src'] if soup.find('img', class_='author-page__author-image') else 'NA'
            author_details['author_name'] = soup.find('h1').get_text(strip=True) if soup.find('h1') else ''
            
            twitter_section = soup.find('div', class_='author-page__author-container__info__social')
            author_details['author_twitter'] = twitter_section.find('a')['href'] if twitter_section and twitter_section.find('a') else ''
            
            return author_details
        else:
            print(f"Failed to retrieve the author page. Status code: {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

# Function to consolidate and save all article details
def the_hill_save():
    articles_data = []
    
    article_urls = get_article_urls()
    if article_urls:
        for url in article_urls:
            # Ensure full URL format
            if url.startswith('/'):
                url = 'https://thehill.com' + url

            article_data = the_hill_article_details(url)
            article_data['article_url'] = url
            
            # Fetch author details if available
            if article_data.get('author_link'):
                author_url = 'https://thehill.com' + article_data['author_link'] if article_data['author_link'].startswith('/') else article_data['author_link']
                author_details = the_hill_author_details(author_url)
                
                # Merge author details with article data
                article_data.update(author_details)
            else:
                # Default values if author details are missing
                article_data.update({
                    'author_img': '',
                    'author_name': '',
                    'author_twitter': ''
                })
            
            # Include LinkedIn field as an empty string
            article_data['author_linkedin'] = ""
            
            # Append the complete article data to the list
            articles_data.append(article_data)
            
            # Print the article data to see the output
            print(article_data)  # Each article's details will be printed as a dictionary
    
    return articles_data

# Execute and retrieve all article details in structured format
all_articles_details = the_hill_save()
