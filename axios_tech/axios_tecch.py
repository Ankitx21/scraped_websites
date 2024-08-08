import re
import time
from datetime import datetime
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SBR_WEBDRIVER = 'https://brd-customer-hl_b98daf99-zone-scraping_browser1:v8d41nyqlhv3@brd.superproxy.io:9515'

# Regular expression to match dates in the format YYYY/MM/DD
DATE_PATTERN = re.compile(r'\d{4}/\d{2}/\d{2}')

def axios_article_list(driver):
    """Get URLs from the main page."""
    print('Navigating to https://www.axios.com/technology')
    driver.get('https://www.axios.com/technology')
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find all the <a> tags with the specified class
    links = soup.find_all('a', class_='font-regular font-sans leading-none inline-flex items-center no-underline Anchor_anchor__0918U')
    
    # Extract and filter URLs
    urls = []
    for link in links:
        url = urljoin('https://www.axios.com', link.get('href'))
        if DATE_PATTERN.search(url):
            urls.append(url)
    
    return urls

def axios_convert_published(url):
    """Convert date in URL to Python date format."""
    match = DATE_PATTERN.search(url)
    if match:
        date_str = match.group()
        return datetime.strptime(date_str, '%Y/%m/%d').date()
    return None

def axios_article_details(url):
    """Get details from the URL."""
    print(f'Scraping details from {url}')
    
    # Create a new browser session for each URL
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    options = ChromeOptions()
    options.add_argument('--headless')  # Ensure the browser is in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    with Remote(sbr_connection, options=options) as driver:
        driver.get(url)
        
        # Add a delay to prevent hitting navigation limits
        time.sleep(2)  # Adjust the delay as needed
        
        # Get the page source
        page_source = driver.page_source
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Get heading
        heading = soup.find('h1', {'data-cy': 'story-headline'})
        heading_text = heading.get_text(strip=True) if heading else 'N/A'
        
        # Get author name
        author = soup.find('li', {'data-cy': 'byline-author'})
        author_name = author.find('span').get_text(strip=True) if author else 'N/A'
        
         # Get published date
        published_date = axios_convert_published(url)
        published_date_str = published_date.strftime('%Y/%m/%d') if published_date else 'N/A'
        
        # Get body
        body = soup.find('div', class_='DraftjsBlocks_draftjs__fm3S2')
        body_text = body.get_text(strip=True) if body else 'N/A'
        
        return {
            'heading': heading_text,
            'author': author_name,
            'published_date': published_date_str,
            'body': body_text
        }

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        urls = axios_article_list(driver)
        
        for url in urls:
            details = axios_article_details(url)
            print(details)
            
            # Add a delay between requests
            time.sleep(3)  # Adjust the delay as needed

if __name__ == "__main__":
    main()
