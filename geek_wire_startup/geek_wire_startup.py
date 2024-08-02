import time
from datetime import datetime
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SBR_WEBDRIVER = 'https://brd-customer-hl_5f7bc336-zone-perplexity:1wd8dv0h6rss@brd.superproxy.io:9515'
BASE_URL = 'https://www.geekwire.com'

def geekwire_article_list(driver):
    """Get URLs from the main page."""
    print('Navigating to https://www.geekwire.com/startups/')
    driver.get(f'{BASE_URL}/startups/')
    time.sleep(2)  # Wait for the page to load

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the <h2> tags with the specified class
    articles = soup.find_all('h2', class_='entry-title')

    # Extract URLs
    urls = [article.find('a').get('href') for article in articles if article.find('a')]

    return urls

def geekwire_convert_published(date_str):
    """Convert date string to Python date format."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    return date_obj.strftime('%Y-%m-%d')

def geekwire_article_details(url):
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

        # Get title
        title = soup.find('h1', class_='entry-title')
        title_text = title.get_text(strip=True)

        # Get author name
        author_tag = soup.find('p', class_='byline author vcard small').find('a', class_='author url fn')
        author_name = author_tag.get_text(strip=True) 

        published_str = soup.find('time', class_='published')
        published = published_str.get_text(strip=True)

        # Get published date
        date_tag = soup.find('time', class_='published')
        published_date_str = geekwire_convert_published(date_tag['datetime']) 

        # Get body
        body = soup.find('div', class_='entry-content clearfix')
        body_text = body.get_text(strip=True)

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
        urls = geekwire_article_list(driver)

        for url in urls:
            try:
                details = geekwire_article_details(url)
                if details:
                    print(details)  # Print or save the details as needed
                time.sleep(2)  # Adding delay between articles
            except Exception as e:
                print(f'Error scraping {url}: {e}')
                time.sleep(2)  # Wait before retrying the next article

if __name__ == '__main__':
    main()
