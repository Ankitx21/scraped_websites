from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Update the path as needed

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

    # Navigate to the articles page
    driver.get('https://www.theinformation.com/?rc=5tfbfm')

    # Wait for the articles to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flex"))
    )

    # Get the page source
    page_source = driver.page_source

finally:
    # Close the browser
    driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Base URL for constructing full links
base_url = 'https://www.theinformation.com'

# Find and print article links from the first section
article_divs_1 = soup.find_all('div', class_='mx-0 flex flex-col flex-nowrap gap-32 gap-x-0 border-0 border-b border-solid border-grayscale-gray pb-48 sm:flex-row sm:gap-28 lg:gap-56')
article_links_1 = []

for div in article_divs_1:
    a_tags = div.find_all('a', href=True)
    for a in a_tags:
        article_links_1.append(base_url + a['href'])

# Print the first set of article links
print("Article links from the first section:")
for link in article_links_1:
    print(link)

# Separation between links
print("\n" + "="*50 + "\n")

# Find and print article links from the second section
article_divs_2 = soup.find_all('div', class_='ml-0 mt-16 sm:ml-24 sm:mt-0')
article_links_2 = []

for div in article_divs_2:
    a_tags = div.find_all('a', href=True)
    for a in a_tags:
        article_links_2.append(base_url + a['href'])

# Print the second set of article links
print("Article links from the second section:")
for link in article_links_2:
    print(link)

# Separation between links
print("\n" + "="*50 + "\n")

# Find and print article links from the third section
article_divs_3 = soup.find_all('div', class_='border-0 border-b border-solid border-grayscale-gray px-16 py-32 sm:px-0 sm:py-48')
article_links_3 = []

for div in article_divs_3:
    a_tags = div.find_all('a', href=True)
    for a in a_tags:
        article_links_3.append(base_url + a['href'])

# Print the third set of article links
print("Article links from the third section:")
for link in article_links_3:
    print(link)
