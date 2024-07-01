from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Update the path as needed

# Base URL for constructing full links
base_url = 'https://www.theinformation.com'

def login(email, password):
    """Logs into the website using the provided email and password."""
    driver.get('https://www.theinformation.com/sessions/new')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-email"))).send_keys(email)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Continue with email"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Sign In"]').click()
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="read-more-button"]'))).click()
    time.sleep(5)

def get_article_links(section_xpath):
    """Extracts article links from a specified section."""
    unique_links = set()
    article_divs = driver.find_elements(By.XPATH, section_xpath)
    for div in article_divs:
        a_tags = div.find_elements(By.TAG_NAME, 'a')
        for a in a_tags:
            href = a.get_attribute('href')
            if href and 'www.theinformation.com/articles/' in href:
                unique_links.add(href)
    return list(unique_links)

def scrape_article_details(article_url):
    """Scrapes the details of an article given its URL."""
    driver.get(article_url)
    time.sleep(5)
    heading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.my-8.font-suisse-works.text-headline-sm.text-black'))).text
    author_name = driver.find_element(By.CSS_SELECTOR, 'div.group.relative.inline-block a.author-name').text
    publish_date = driver.find_element(By.CSS_SELECTOR, 'div.flex.items-end.justify-end.md\\:justify-between time').text
    body_content_div = driver.find_element(By.CSS_SELECTOR, 'div.flex.flex-col.md\\:flex-row.md\\:gap-72.xl\\:gap-112 div.flex.flex-1.flex-col div div.SE2jANfgnguT1IMXb9i2')
    body_content = ' '.join([p.text for p in body_content_div.find_elements(By.TAG_NAME, 'p')])
    return {
        "heading": heading,
        "author_name": author_name,
        "publish_date": publish_date,
        "body_content": body_content
    }

def main():
    """Main function to orchestrate the scraping process."""
    try:
        # Login to the website
        login('devs@inside.com', 'mzf7dzd*FDM.ujx7jrt')

        # Extract article links
        section_xpaths = [
            '//div[contains(@class, "mx-0 flex flex-col flex-nowrap gap-32 gap-x-0 border-0 border-b border-solid border-grayscale-gray pb-48 sm:flex-row sm:gap-28 lg:gap-56")]',
            '//div[contains(@class, "ml-0 mt-16 sm:ml-24 sm:mt-0")]',
            '//div[contains(@class, "border-0 border-b border-solid border-grayscale-gray px-16 py-32 sm:px-0 sm:py-48")]'
        ]
        all_article_links = []
        for xpath in section_xpaths:
            all_article_links.extend(get_article_links(xpath))

        # Scrape details for each article
        scraped_data = []
        for link in all_article_links:
            article_data = scrape_article_details(link)
            scraped_data.append(article_data)

        # Save the scraped data to a JSON file
        with open('scraped_articles.json', 'w') as f:
            json.dump(scraped_data, f, indent=4)

        print("Scraping completed and data saved to scraped_articles.json")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
