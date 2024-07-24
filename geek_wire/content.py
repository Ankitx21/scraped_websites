from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def geekwire_convert_published(published):
    """Converts the published date to standard Python date format"""
    dt = published.split("T")[0]
    date_obj = datetime.strptime(dt, '%Y-%m-%d').date()
    return date_obj

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

try:
    # Open the target webpage
    url = "https://www.geekwire.com/2024/smart-light-switch-startup-deako-raises-3-4m-to-meet-growing-market-demand/"
    driver.get(url)

    # Wait until the elements are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "author"))
    )

    # Scrape author name
    author = driver.find_element(By.CLASS_NAME, "author").text
    print(f"Author: {author}")

    # Scrape header intro
    header_intro = driver.find_element(By.ID, "category-header-intro").text
    print(f"Header Intro: {header_intro}")

    # Scrape body content
    body_content = driver.find_element(By.CLASS_NAME, "entry-content").text
    print(f"Body Content: {body_content}")

    # Scrape published date and convert to standard Python date format
    published_element = driver.find_element(By.CLASS_NAME, "published")
    published_datetime = published_element.get_attribute("datetime")
    published_date = geekwire_convert_published(published_datetime)
    print(f"Published Date: {published_date}")

finally:
    # Close the driver
    driver.quit()
