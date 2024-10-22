import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your Chrome user profile
user_data_dir = r'C:\Users\Ankit\AppData\Local\Google\Chrome\User Data'
profile_dir = 'Default'

# Initialize the undetected Chrome WebDriver with user profile
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument(f'--profile-directory={profile_dir}')  # Use the correct profile directory

# Initialize the undetected Chrome driver
driver = uc.Chrome(options=chrome_options)

# Open the Reuters website
driver.get("https://www.reuters.com/")

# Check if the user is already signed in by checking for the "Sign In" button
try:
    # Try to find the "Sign In" button (if it's present, the user is not signed in)
    sign_in_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fusion-app"]/header/div/div/div/div/div[3]/a[2]'))
    )
    
    # If found, proceed to sign in
    print("User is not signed in. Proceeding to sign in...")
    
    # Click the "Sign In" button
    sign_in_button.click()

    # Wait for the email input field to be available and input the email
    email_input = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))
    )
    email_input.send_keys("admin@inside.com")
    print("Email entered successfully.")
    
    # Wait for 2 seconds before entering the password
    time.sleep(2)

    # Wait for the password input field to be available and input the password
    password_input = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
    )
    password_input.send_keys("!Inside1104edisn!")
    print("Password entered successfully.")
    
    # Wait for 2 seconds before clicking the final "Sign In" button
    time.sleep(2)

    # Click the final "Sign In" button
    final_sign_in_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div/div[2]/div[1]/div/div/div/form/button/span/span'))
    )
    final_sign_in_button.click()
    print("Logged in successfully.")
    
    # Wait for login process to complete and dashboard to load
    time.sleep(5)

except Exception:
    # If "Sign In" button is not found, the user is already signed in
    print("User is already signed in.")

# Now click the Technology section
try:
    tech_section = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/header/div/div/div/div/div[2]/nav/ul/li[8]/div[1]'))
    )
    tech_section.click()
    print("Clicked on the Technology section.")

    time.sleep(10)
except Exception as e:
    print(f"Error occurred: {e}")

# Close the browser (optional)
driver.quit()
