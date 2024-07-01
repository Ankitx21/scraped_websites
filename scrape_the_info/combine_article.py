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

def get_article_links(section_xpath):
    unique_links = set()
    # Locate the div tags with the specified XPath
    article_divs = driver.find_elements(By.XPATH, section_xpath)
    for div in article_divs:
        # Find all anchor tags within the div and get the href attribute
        a_tags = div.find_elements(By.TAG_NAME, 'a')
        for a in a_tags:
            href = a.get_attribute('href')
            if href and 'www.theinformation.com/articles/' in href:
                unique_links.add(href)
    return list(unique_links)

def scrape_article_details(article_url):
    driver.get(article_url)
    time.sleep(5)  # Wait for the article page to load

    # Extract the heading
    heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.my-8.font-suisse-works.text-headline-sm.text-black'))
    ).text

    # Extract the author name
    author_name = driver.find_element(By.CSS_SELECTOR, 'div.group.relative.inline-block a.author-name').text

    # Extract the publish date
    publish_date = driver.find_element(By.CSS_SELECTOR, 'div.flex.items-end.justify-end.md\\:justify-between time').text

    # Extract the body content
    body_content_div = driver.find_element(By.CSS_SELECTOR, 'div.flex.flex-col.md\\:flex-row.md\\:gap-72.xl\\:gap-112 div.flex.flex-1.flex-col div div.SE2jANfgnguT1IMXb9i2')
    body_content = ' '.join([p.text for p in body_content_div.find_elements(By.TAG_NAME, 'p')])

    return {
        "heading": heading,
        "author_name": author_name,
        "publish_date": publish_date,
        "body_content": body_content
    }

try:
    # Open the login page
    driver.get('https://www.theinformation.com/sessions/new')

    # Wait until the email input field is present
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )

    # Enter the email address
    email_field.send_keys('devs@inside.com')

    # Wait for a few seconds
    time.sleep(3)

    # Find the submit button and click it
    submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Continue with email"]')
    submit_button.click()

    # Wait until the password input field is present
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    # Enter the password
    password_field.send_keys('mzf7dzd*FDM.ujx7jrt')

    # Wait for a few seconds
    time.sleep(2)

    # Find the sign in button and click it
    sign_in_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Sign In"]')
    sign_in_button.click()

    # Wait for a few seconds to ensure the login completes
    time.sleep(5)

    # Find and click the "Read more" link
    read_more_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@data-testid="read-more-button"]'))
    )
    read_more_link.click()

    # Wait for the articles to load
    time.sleep(5)

    # Get article links from the first section
    article_links_1 = get_article_links('//div[contains(@class, "mx-0 flex flex-col flex-nowrap gap-32 gap-x-0 border-0 border-b border-solid border-grayscale-gray pb-48 sm:flex-row sm:gap-28 lg:gap-56")]')

    # Print the first set of article links
    print("Article links from the first section:")
    for link in article_links_1:
        print(link)

    # Separation between links
    print("\n" + "="*50 + "\n")

    # Get article links from the second section
    article_links_2 = get_article_links('//div[contains(@class, "ml-0 mt-16 sm:ml-24 sm:mt-0")]')

    # Print the second set of article links
    print("Article links from the second section:")
    for link in article_links_2:
        print(link)

    # Separation between links
    print("\n" + "="*50 + "\n")

    # Get article links from the third section
    article_links_3 = get_article_links('//div[contains(@class, "border-0 border-b border-solid border-grayscale-gray px-16 py-32 sm:px-0 sm:py-48")]')

    # Print the third set of article links
    print("Article links from the third section:")
    for link in article_links_3:
        print(link)

    # Combine all article links
    all_article_links = article_links_1 + article_links_2 + article_links_3

    # # Limit to first 10 articles for testing
    # all_article_links = all_article_links[:10]

    # List to store scraped data
    scraped_data = []

    # Scrape details for each article
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
    # Close the browser
    driver.quit()
