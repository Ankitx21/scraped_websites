from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import json

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

def scrape_urls(main_page_url):
    driver.get(main_page_url)
    
    # Wait for the elements with class 'css-0' to be visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'css-0'))
    )

    # Find all anchor elements with the class 'css-0'
    link_elements = driver.find_elements(By.CLASS_NAME, 'css-0')

    # Extract URLs from the anchor elements
    urls = [link.get_attribute('href') for link in link_elements]
    print(f"Found {len(urls)} links.")
    
    return urls

def scrape_article_details(url):
    driver.get(url)
    
    # Wait for the heading element to be visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'dist__StyledText-sc-c2df08e8-12.bhNlgo'))
    )

    # Scrape the heading
    heading = driver.find_element(By.CLASS_NAME, 'dist__StyledText-sc-c2df08e8-12.bhNlgo').text
    
    # Scrape the bio
    bio = driver.find_element(By.CLASS_NAME, 'dist__StyledText-sc-c2df08e8-12.khzzSY').text
    
    # Scrape the author name
    author_element = driver.find_element(By.CSS_SELECTOR, '.style__BylineWrapper-sc-def4103b-0.ozWZv.article-byline a')
    author_name = author_element.text
    
    # Scrape the date and convert it to Python date format
    date_text = driver.find_element(By.CSS_SELECTOR, '.article-details.css-k008qs time').text
    date = datetime.strptime(date_text, '%B %d, %Y').date()
    
    # Scrape the body content
    body_element = driver.find_element(By.CLASS_NAME, 'style__ArticleBodyWrapper-sc-7dd1f935-3.izwWZX.article-body-content')
    body_text = body_element.text

    return {
        'url': url,
        'heading': heading,
        'bio': bio,
        'author_name': author_name,
        'date': str(date),
        'body_text': body_text
    }

def save_to_json(data, filename='scraped_articles.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

try:
    main_page_url = "https://www.healthcare-brew.com/tag/startups"

    # Step 1: Scrape URLs
    urls = scrape_urls(main_page_url)

    # Step 2: Scrape details for each URL
    articles_data = []
    for url in urls:
        try:
            print(f"Scraping details from: {url}")
            article_details = scrape_article_details(url)
            articles_data.append(article_details)
            time.sleep(5)  # Add a delay between requests
        except Exception as e:
            print(f"Error scraping link {url}: {e}")

    # Step 3: Save to JSON
    save_to_json(articles_data)

finally:
    # Close the driver
    driver.quit()
