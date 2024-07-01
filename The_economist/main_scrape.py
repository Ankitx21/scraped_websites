from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Path to the ChromeDriver executable
chrome_driver_path = r'C:\Users\Ankit\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument(r'--user-data-dir=C:/Users/Ankit/AppData/Local/Google/Chrome/User Data')
chrome_options.add_argument('--profile-directory=Default')

# Initialize Chrome browser with options
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

try:
    # Navigate to the Economist website
    driver.get('https://www.economist.com/')
    
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
    
    # Now scrape all article links within the specified section
    sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-riwnn3')))
    
    article_links = []
    for section in sections:
        links = section.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute("href")
            if href:
                article_links.append(href)
    
    # Filter links to include only those with a date in the format /YYYY/MM/DD/
    date_pattern = re.compile(r'/\d{4}/\d{2}/\d{2}/')
    filtered_links = [href for href in article_links if date_pattern.search(href)]
    
    for href in filtered_links:
        print(href)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the browser
    driver.quit()
