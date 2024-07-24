from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

def scrape_article_details(url):
    driver.get(url)
    
    # Wait for the page to load
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
        'heading': heading,
        'bio': bio,
        'author_name': author_name,
        'date': date,
        'body_text': body_text
    }

# Example article URL
article_url = "https://www.healthcare-brew.com/stories/2024/07/15/digital-health-startups-continue-to-recover-from-a-tough-2023-closing-more-vc-deals"

try:
    article_details = scrape_article_details(article_url)
    for key, value in article_details.items():
        print(f"{key}: {value}\n")
finally:
    driver.quit()
