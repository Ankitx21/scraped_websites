from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # Open the article page
    driver.get('https://www.theinformation.com/articles/apple-sets-bold-new-goals-for-automating-iphone-factories?rc=5tfbfm')

    # Wait for the article page to load
    time.sleep(5)

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

    # Print the results
    print("Heading:", heading)
    print("Author Name:", author_name)
    print("Publish Date:", publish_date)
    print("Body Content:", body_content)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
