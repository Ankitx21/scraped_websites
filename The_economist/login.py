from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    
    # Wait for the login link to be clickable and click on it
    login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/header/div[1]/div[1]/div/div[2]/a')))
    login_link.click()
    
    # Wait for the email input field to be visible
    email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[2]/lightning-input/lightning-primitive-input-simple/div/div/input')))
    
    # Enter email address
    email_input.send_keys("admin@inside.com")  # Replace with your email address

    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[3]/div/lightning-input/lightning-primitive-input-simple/div/div/input')))

    password.send_keys("1nsid3!!2202!")

    # clicking on the login button
    login_click= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[5]/lightning-button/button')))
    login_click.click()
    # Optional: Wait for some time after entering email
    time.sleep(5)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the browser
    driver.quit()
