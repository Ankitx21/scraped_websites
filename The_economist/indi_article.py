from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json

# Path to the ChromeDriver executable
chrome_driver_path = r'C:\Users\Ankit\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument(r'--user-data-dir=C:/Users/Ankit/AppData/Local/Google/Chrome/User Data')
chrome_options.add_argument('--profile-directory=Default')

# Initialize Chrome browser with options
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

article_data = {}

try:
    # Navigate to the Economist article
    driver.get('https://www.economist.com/international/2024/06/26/the-rise-of-the-truly-cruel-summer')
    
    try:
        # Attempt to find and click the login link
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/header/div[1]/div[1]/div/div[2]/a')))
        login_link.click()
        
        # Wait for the email input field to be visible
        email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[2]/lightning-input/lightning-primitive-input-simple/div/div/input')))
        
        # Enter email address
        email_input.send_keys("admin@inside.com")  # Replace with your email address

        # Wait for the password input field to be visible
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[3]/div/lightning-input/lightning-primitive-input-simple/div/div/input')))
        
        # Enter password
        password_input.send_keys("1nsid3!!2202!")  # Replace with your password
        
        # Click on the login button
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[5]/lightning-button/button')))
        login_button.click()
        
        # Wait for some time after login (adjust as needed)
        time.sleep(10)
        
    except Exception as e:
        print("Login not required or login failed:", e)

    # Scrape the h1 tag text
    try:
        h1_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[1]/section/h1')))
        article_data['title'] = h1_element.text
    except Exception as e:
        print("Error scraping h1 tag:", e)

    # Scrape the h2 tag text
    try:
        h2_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[1]/section/h2')))
        article_data['subtitle'] = h2_element.text
    except Exception as e:
        print("Error scraping h2 tag:", e)

    # Scrape the publish date and location text
    try:
        publish_date_location_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[3]/div/div[1]/div/div')))
        article_data['publish_date_location'] = publish_date_location_element.text
    except Exception as e:
        print("Error scraping publish date and location:", e)

    # Scrape the body text
    try:
        body_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[3]/div/section/div')))
        article_data['body'] = body_element.text
        
        # Scrape all the links within the body
        links_in_body = body_element.find_elements(By.TAG_NAME, 'a')
        article_data['links'] = [link.get_attribute('href') for link in links_in_body if link.get_attribute('href')]
    except Exception as e:
        print("Error scraping body text or links:", e)

    # Save the data to a JSON file
    with open('article_data.json', 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the browser
    driver.quit()

# Print the scraped data for verification
print(json.dumps(article_data, ensure_ascii=False, indent=4))
