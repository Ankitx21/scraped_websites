import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Base URL for AlleyWatch
base_url = "https://www.alleywatch.com/"

# Define headers for the request
headers = {
    'Cookie': 'PHPSESSID=96gv4pbjtk4lnhe90ososkhdsd'
}

def alley_watch_convert_date(date_str):
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
        published_date = ""
        if published_text:
            # Extract date part from the text
            date_str = published_text.split('•')[-1].strip()  # Extract date part
            published_date = convert_date(date_str)
        
        # Append article URL and published date
        article_urls.append((article_url, published_text, published_date))
    
    return article_urls

def alleywatch_article_details(article_url, published_text, published_date):
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', class_='jeg_post_title')
    title = title_tag.text.strip() if title_tag else ""

    # Author name is set as "alleywatch"
    author_name = "alleywatch"

    # Scrape the article body
    body_tag = soup.find('div', class_='content-inner')
    body = body_tag.text.strip() if body_tag else ""

    # Return the article details
    article_details = {
        "title": title,
        "author_name": author_name,
        "published": published_text,       # Raw published date
        "published_date": published_date,  # Formatted published date
        "body": body,
    }

    return article_details

# Example usage: scrape URLs and details
article_urls = alleywatch_article_urls()
for article_url, published_text, published_date in article_urls:
    article_details = alleywatch_article_details(article_url, published_text, published_date)
    if article_details:  # Only print if article details are found
        print(article_details)
