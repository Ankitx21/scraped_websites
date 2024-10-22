from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the ChromeDriver executable
chrome_driver_path = r'C:\Users\Ankit\Downloads\chromedriver-win64\chromedriver.exe'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument(r'--user-data-dir=C:\Users\Ankit\AppData\Local\Google\Chrome\User Data')
chrome_options.add_argument('--profile-directory=Default')  # Use the correct profile directory

# Initialize the WebDriver with the specified path and options
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Reuters website
url = "https://www.reuters.com/"
driver.get(url)

# Wait for 5 seconds to allow the page to load
time.sleep(5)

# Close the browser (optional)
driver.quit()
