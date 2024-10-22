import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime

# Path to your Chrome user profile
user_data_dir = r'C:\Users\Ankit\AppData\Local\Google\Chrome\User Data'
profile_dir = 'Default'

# Initialize the undetected Chrome WebDriver with user profile
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument(f'--profile-directory={profile_dir}')  # Use the correct profile directory

# Initialize the undetected Chrome driver
driver = uc.Chrome(options=chrome_options)

# Function to get all article URLs from the Technology section
def get_article_urls():
    try:
        # Wait for the articles to load
        time.sleep(5)  # Adjust sleep time if necessary

        # Find all div elements with the specified class
        article_containers = driver.find_elements(By.CLASS_NAME, 'media-story-card__body__3tRWy')

        # Extract URLs
        article_urls = []
        for container in article_containers:
            # Find the anchor elements inside each container with data-testid
            heading_links = container.find_elements(By.CSS_SELECTOR, 'a[data-testid="Heading"], a[data-testid="Link"]')
            
            for link in heading_links:
                article_url = link.get_attribute('href')  # Get the URL from the <a> tag
                if article_url and re.search(r'\d', article_url):  # Check if URL contains any digits
                    article_urls.append(article_url)
        
        return article_urls

    except Exception as e:
        print(f"Error occurred while getting article URLs: {e}")
        return []

# Function to format the published date
def reuter_date(published_date_str):
    # Convert date string to a datetime object
    date_object = datetime.strptime(published_date_str, '%B %d, %Y')
    # Format it to the desired string format (YYYY-MM-DD)
    return date_object.strftime('%Y-%m-%d')

# Function to get article details from a given URL
def get_article_details(article_url):
    try:
        # Open the article URL
        driver.get(article_url)
        time.sleep(5)  # Wait for the article to load

        # Extract the heading
        heading = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="Heading"]').text

        # Extract the published date text
        published_date_str = driver.find_element(By.CLASS_NAME, 'date-line__date___kNbY').text

        # Format the published date using the reuter_date function
        published_date = reuter_date(published_date_str)

        # Extract the article body
        article_body = driver.find_element(By.CLASS_NAME, 'article-body__content__17Yit').text

        # Get author details
        author_details = reuter_author_details()

        # Get image URL
        image_url = reuter_images()

        # Return the article details as a dictionary
        return {
            'heading': heading,
            'published_date_str': published_date_str,
            'published_date': published_date,
            'body': article_body,
            'author_name': author_details['author_name'],
            'author_link': author_details['author_link'],
            'image_url': image_url  # Add image URL to the returned dictionary
        }

    except Exception as e:
        print(f"Error occurred while getting article details from {article_url}: {e}")
        return None

# Function to extract author details
def reuter_author_details():
    try:
        # Find the author link element
        author_link_element = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="Link"].author-name__author__au-bT')

        # Extract the author name and link
        author_name = author_link_element.text
        author_link = author_link_element.get_attribute('href')

        return {
            'author_name': author_name,
            'author_link': author_link
        }
    
    except Exception as e:
        print(f"Error occurred while getting author details: {e}")
        return {'author_name': None, 'author_link': None}

# Function to extract the first image URL
def reuter_images():
    try:
        # Locate the image container div
        image_container = driver.find_element(By.CLASS_NAME, 'styles__image-container__3hkY5')
        
        # Find the first image element within that container
        img_element = image_container.find_element(By.TAG_NAME, 'img')

        # Get the 'src' attribute from the image element
        image_url = img_element.get_attribute('src')

        return image_url

    except Exception as e:
        print(f"Error occurred while getting image URL: {e}")
        return None

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

    # Get all article URLs from the Technology section
    article_urls = get_article_urls()
    print("Filtered Article URLs containing numbers:")
    for url in article_urls:
        print(url)

        # Get article details for each URL
        article_details = get_article_details(url)
        if article_details:
            print(f"\nArticle Details:\nHeading: {article_details['heading']}\nPublished Date: {article_details['published_date_str']}\nFormatted Date: {article_details['published_date']}\nBody: {article_details['body'][:100]}...\nAuthor: {article_details['author_name']}\nAuthor Link: {article_details['author_link']}\nImage URL: {article_details['image_url']}")

    time.sleep(10)
except Exception as e:
    print(f"Error occurred: {e}")

# Close the browser (optional)
driver.quit()
