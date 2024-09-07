import time
from datetime import datetime
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


SBR_WEBDRIVER = 'https://brd-customer-hl_5f7bc336-zone-temp_selenium:bsvbctc0hfwx@brd.superproxy.io:9515'
BASE_URL = 'https://www.healthcare-brew.com'

def healthcare_convert_published(date_str):
    """Convert date string to Python date format."""
    date_obj = datetime.strptime(date_str, '%B %d, %Y')
    return date_obj.strftime('%Y-%m-%d')

def healthcare_author_details(author_link):
    
    # print('author details...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(author_link)
        time.sleep(2) 
        page_source = driver.page_source
            # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        author_linkedin=author_twitter=author_img=author_name =''
        body = soup.find('body' ,class_='chakra-ui-light')
        if body:
            author_name = soup.find('h1' , class_='dist__StyledText-sc-9c73a528-12 hUhQQi style__AuthorInfo-sc-550ae33a-4 bkfzOg').text.strip()
            author_img = soup.find('div' ,class_='style__ProfilePicture-sc-550ae33a-1 jcpEMN').find('img')['src']
        else:
            print('no body ')
    
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details

def healthcare_article_list():
    """Get URLs from the main page."""
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Navigating to https://www.healthcare-brew.com/tag/tech')
        driver.get(f'{BASE_URL}/tag/tech')
        time.sleep(2)  # Wait for the page to load

        # screenshot_path = 'screenshot.png'
        # driver.save_screenshot(screenshot_path)
        # print('screenshot taken')
        # Get the page source
        page_source = driver.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all the <a> tags with the specified class
        articles = soup.find_all('a' ,class_='style__PreviewCardLink-sc-2ac974f6-0 HNmvy preview')
        if articles:
            print('articles found ')
            urls = [urljoin(BASE_URL, article['href']) for article in articles]    
        else: 
            print('no article found')

    return urls

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
        title = soup.find('h1', class_='dist__StyledText-sc-9c73a528-12 levHKW')
        title_text = title.get_text(strip=True) 

        # Get author name
        author_div = soup.find('div', class_='style__BylineWrapper-sc-def4103b-0 ozWZv article-byline')

        author_link ='https://www.healthcare-brew.com' + author_div.find('a')['href']
        author_info = healthcare_author_details(author_link)
        # print(author_info)
        author = author_div.find('a').get_text(strip=True) 

        published_str = soup.find('time', class_="dist__StyledText-sc-9c73a528-12 eAQvaB")
        published = published_str.get_text(strip=True) 

        # # Get published date
        published_date = healthcare_convert_published(published) 

        # # Get body
        body_div = soup.find('div', class_='style__ArticleBodyWrapper-sc-f998fa3-3 eshBvq article-body-content')
        body_text = body_div.get_text(separator='\n', strip=True) 

        return {
            'url': url,
            'title': title_text,
            'author': author,
            'author_info': author_info,
            'published': published,
            'published_date': published_date,
            'body': body_text
        }

def main():

    urls = healthcare_article_list()
    articles_data = []
    for url in urls:
        try:    
            details = healthcare_article_details(url)
            if details:
                articles_data.append(details)
            time.sleep(1)  # Adding delay between articles
        except Exception as e:
            print(f'Error scraping {url}: {e}')
            time.sleep(2)  # Wait before retrying the next article

    with open('healthcare_articles.json' ,'w') as json_file:
                json.dump(articles_data ,json_file ,indent=4)
    print("Data fetched and stored in healthcare_articles.json")


if __name__ == '__main__':
    main()