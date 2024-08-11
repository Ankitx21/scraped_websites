from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_e7bfdecb-zone-scraping_browser1:iv6mkqg7shne@brd.superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to YouTube Channel')
        driver.get('https://www.youtube.com/@CNBCtelevision/videos')
        time.sleep(10)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos = soup.find_all('a', id='video-title-link')

        for video in videos:
            title = video['title'].strip()
            url = 'https://www.youtube.com' + video['href']
            
            # Find the parent div that contains the time information
            metadata_div = video.find_next('div', id='metadata-line')
            if metadata_div:
                time_span = metadata_div.find_all('span', class_='inline-metadata-item style-scope ytd-video-meta-block')[1]
                time_text = time_span.get_text(strip=True)
            else:
                time_text = ''
            
            print(f'Title: {title}, URL: {url}, Time: {time_text}')

if __name__ == '__main__':
    main()
