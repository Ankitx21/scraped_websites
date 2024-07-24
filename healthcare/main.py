from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver with untrusted certificate (uc) option
driver = Driver(uc=True)

try:
    # Open the target webpage
    driver.get("https://www.healthcare-brew.com/tag/startups")
    
    # Wait for the elements with class 'css-0' to be visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'css-0'))
    )

    # Find all anchor elements with the class 'css-0'
    link_elements = driver.find_elements(By.CLASS_NAME, 'css-0')

    # Print the number of links found
    print(f"Found {len(link_elements)} links.")

    # Iterate through each link element and print the href attribute
    for link in link_elements:
        try:
            link_url = link.get_attribute('href')
            print(link_url)
        except Exception as e:
            print(f"Error finding link: {e}")

finally:
    # Close the driver
    driver.quit()
