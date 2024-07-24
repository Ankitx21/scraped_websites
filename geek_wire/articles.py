from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

try:
    # Open the target webpage
    driver.get("https://www.geekwire.com/startups/")
    
    # Wait until the articles are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "entry-title"))
    )
    
    # Find all h2 tags with class 'entry-title'
    articles = driver.find_elements(By.CLASS_NAME, "entry-title")
    
    # Loop through the articles and print the title and href link
    for article in articles:
        a_tag = article.find_element(By.TAG_NAME, 'a')
        link = a_tag.get_attribute('href')
        print(f"Link: {link}")
        print()
        
finally:
    # Close the driver
    driver.quit()
