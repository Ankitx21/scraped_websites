from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_b98daf99-zone-scraping_browser1:v8d41nyqlhv3@brd.superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to https://www.theguardian.com/uk/technology')
        driver.get('https://www.theguardian.com/uk/technology')
        time.sleep(10)  # Wait for the page to load

        # Get page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all anchor tags with the specific class
        links = soup.find_all('a', class_='dcr-lv2v9o')

        # Extract href attributes
        article_links = [link.get('href') for link in links]

        # Print the links
        for article_link in article_links:
            print(f"https://www.theguardian.com{article_link}")

if __name__ == '__main__':
    main()
