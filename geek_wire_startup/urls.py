from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_b98daf99-zone-scraping_browser1:v8d41nyqlhv3@brd.superproxy.io:9222'

def main():
    print('Connecting to Scraping Browser...')
    
    # Set up Chrome options
    chrome_options = Options()
    
    # Connect to the remote WebDriver
    driver = webdriver.Remote(
        command_executor=SBR_WEBDRIVER,
        options=chrome_options
    )
    
    try:
        print('Connected! Navigating to https://www.geekwire.com/startups/')
        driver.get('https://www.geekwire.com/startups/')
        time.sleep(10)  # Wait for the page to load
        
        # Get the page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all articles with the class 'entry-title'
        articles = soup.find_all('h2', class_='entry-title')
        
        # Extract and print the article titles and links
        for article in articles:
            link = article.find('a')
            if link:
                url = link.get('href')
                print(f'URL: {url}')
                print('---')
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
