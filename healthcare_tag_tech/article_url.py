from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_5f7bc336-zone-perplexity:1wd8dv0h6rss@brd.superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to https://www.healthcare-brew.com/tag/startups')
        driver.get('https://www.healthcare-brew.com/tag/startups')
        time.sleep(10)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('a', class_='css-0')

        for article in articles:
            url = article['href']
            full_url = f'https://www.healthcare-brew.com{url}'
            print(full_url)

if __name__ == '__main__':
    main()
