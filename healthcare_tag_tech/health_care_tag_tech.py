import time
from datetime import datetime
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SBR_WEBDRIVER = 'https://brd-customer-hl_5f7bc336-zone-perplexity:1wd8dv0h6rss@brd.superproxy.io:9515'
BASE_URL = 'https://www.healthcare-brew.com'

def healthcare_article_list(driver):
    """Get URLs from the main page."""
    print('Navigating to https://www.healthcare-brew.com/tag/tech')
    driver.get(f'{BASE_URL}/tag/tech')
    time.sleep(2)  # Wait for the page to load

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the <a> tags with the specified class
    articles = soup.find_all('a', class_='css-0')

    # Extract URLs
    urls = [urljoin(BASE_URL, article['href']) for article in articles]

    return urls

def healthcare_convert_published(date_str):
    """Convert date string to Python date format."""
    date_obj = datetime.strptime(date_str, '%B %d, %Y')
    return date_obj.strftime('%Y-%m-%d')

def healthcare_article_details(url):
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
        title = soup.find('h1', class_='dist__StyledText-sc-90cce694-12 jJrukF')
        title_text = title.get_text(strip=True) 

        # Get author name
        author_div = soup.find('div', class_='style__BylineWrapper-sc-def4103b-0 ozWZv article-byline')
        author = author_div.find('a').get_text(strip=True) 

        published_str = soup.find('time', class_="dist__StyledText-sc-90cce694-12 iCiKHO")
        published = published_str.get_text(strip=True) 

        # Get published date
        date_str = soup.find('time', class_='dist__StyledText-sc-90cce694-12 iCiKHO')
        published_date = healthcare_convert_published(date_str.get_text(strip=True)) 

        # Get body
        body_div = soup.find('div', class_='style__ArticleBodyWrapper-sc-7dd1f935-3 izwWZX article-body-content')
        body_text = body_div.get_text(separator='\n', strip=True) 

        return {
            'url': url,
            'title': title_text,
            'author': author,
            'published': published,
            'published_date': published_date,
            'body': body_text
        }

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        urls = healthcare_article_list(driver)

        for url in urls:
            try:
                details = healthcare_article_details(url)
                if details:
                    print(details)  # Print or save the details as needed
                time.sleep(3)  # Adding delay between articles
            except Exception as e:
                print(f'Error scraping {url}: {e}')
                time.sleep(2)  # Wait before retrying the next article

if __name__ == '__main__':
    main()
