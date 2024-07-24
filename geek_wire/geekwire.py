from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

def geekwire_convert_published(published):
    """Converts the published date to standard Python date format"""
    dt = published.split("T")[0]
    date_obj = datetime.strptime(dt, '%Y-%m-%d').date()
    return date_obj

def get_article_links(driver):
    """Scrapes the article links from the GeekWire Startups page"""
    driver.get("https://www.geekwire.com/startups/")
    
    # Wait until the articles are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "entry-title"))
    )
    
    # Find all h2 tags with class 'entry-title'
    articles = driver.find_elements(By.CLASS_NAME, "entry-title")
    
    # Extract and return the links
    links = [article.find_element(By.TAG_NAME, 'a').get_attribute('href') for article in articles]
    return links

def scrape_article_details(driver, url):
    """Uses the article link to get the details of the article"""
    driver.get(url)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "author"))
    )
    
    # Initialize details
    author = ''
    header_intro = ''
    published_date = ''
    body_content = ''


    try:
        # Scrape author name
        author = driver.find_element(By.CLASS_NAME, "author").text
    except:
        author = 'N/A'

    try:
        # Scrape header intro
        header_intro = driver.find_element(By.ID, "category-header-intro").text
    except:
        header_intro = 'N/A'

    try:
        # Scrape body content
        body_content = driver.find_element(By.CLASS_NAME, "entry-content").text
    except:
        body_content = 'N/A'

    try:
        # Scrape published date and convert to standard Python date format
        published_element = driver.find_element(By.CLASS_NAME, "published")
        published_datetime = published_element.get_attribute("datetime")
        published_date = geekwire_convert_published(published_datetime)
    except:
        published_date = 'N/A'

    # Print the details
    print(f"URL: {url}")
    print(f"Author: {author}")
    print(f"Header Intro: {header_intro}")
    print(f"Body Content: {body_content}")
    print(f"Published Date: {published_date}")
    print('-' * 80)

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

try:
    # Get article links
    links = get_article_links(driver)

    # Loop through the article links and get details for each
    for link in links:
        scrape_article_details(driver, link)
        # Wait for 3 seconds before moving to the next URL
        time.sleep(3)
        
finally:
    # Close the driver
    driver.quit()
