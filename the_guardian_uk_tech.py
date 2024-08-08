import time
from datetime import datetime
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

SBR_WEBDRIVER = 'https://brd-customer-hl_5f7bc336-zone-perplexity:1wd8dv0h6rss@brd.superproxy.io:9515'
BASE_URL = 'https://www.theguardian.com'

def theguardian_article_list(driver):
    """Get URLs from the main page."""
    print('Navigating to https://www.theguardian.com/uk/technology')
    driver.get(f'{BASE_URL}/uk/technology')
    time.sleep(10)  # Wait for the page to load

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all anchor tags with the specific class
    links = soup.find_all('a', class_='dcr-lv2v9o')

    # Extract href attributes
    urls = [urljoin(BASE_URL, link.get('href')) for link in links if link.get('href')]

    return urls

def theguardian_convert_published_from_url(url):
    """Extract and convert date from the URL to Python date format."""
    match = re.search(r'/(\d{4}/[a-z]{3}/\d{2})/', url)
    if match:
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, '%Y/%b/%d')
        return date_obj.strftime('%d/%m/%Y')
    else:
        return ''

def theguardian_article_details(url):
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

        # Get title from the specified div class
        title_div = soup.find('div', class_='dcr-cohhs3')
        title = title_div.find('h1') if title_div else None
        title_text = title.get_text(strip=True) if title else ''

        # Get author name
        author_div = soup.find('div', class_='dcr-1cfpnlw')
        author_tag = author_div.find('span') if author_div else None
        author_name = author_tag.get_text(strip=True) if author_tag else ''

        # get publsihed date

        published_str = soup.find('span', class_= 'dcr-u0h1qy')
        published = published_str.get_text(strip=True)

        # Get published date from URL
        published_date_str = theguardian_convert_published_from_url(url)

        # Get body
        body_div = soup.find('div', id='maincontent')
        body_text = body_div.get_text(strip=True) if body_div else ''

        if not body_text or not published_date_str:
            print(f'{url} skipping to next url')
            return None

        return {
            'url': url,
            'title': title_text,
            'author': author_name,
            'published': published,
            'published_date': published_date_str,
            'body': body_text
        }

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        urls = theguardian_article_list(driver)

        for url in urls:
            try:
                details = theguardian_article_details(url)
                if details:
                    print(details)  # Print or save the details as needed
                time.sleep(2)  # Adding delay between articles
            except Exception as e:
                print(f'Error scraping {url}: {e}')
                time.sleep(2)  # Wait before retrying the next article

if __name__ == '__main__':
    main()
