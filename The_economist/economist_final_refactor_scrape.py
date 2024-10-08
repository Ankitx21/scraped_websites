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

def initialize_browser(chrome_driver_path, chrome_options):
    return webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

def login_to_site(driver):
    try:
        login_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/header/div[1]/div[1]/div/div[2]/a')))
        login_link.click()
        
        email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[2]/lightning-input/lightning-primitive-input-simple/div/div/input')))
        email_input.send_keys("admin@inside.com")  # Replace with your email address

        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[3]/div/lightning-input/lightning-primitive-input-simple/div/div/input')))
        password_input.send_keys("1nsid3!!2202!")  # Replace with your password

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div/div/div/div[2]/div/div/c-lwc-login-form/div/lightning-card/article/div[2]/slot/div[2]/div[5]/lightning-button/button')))
        login_button.click()
        
        time.sleep(10)  # Wait for some time after login
    except Exception as e:
        print("Login not required or login failed:", e)

def get_filtered_article_links(driver):
    sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-riwnn3')))
    article_links = []
    for section in sections:
        links = section.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute("href")
            if href:
                article_links.append(href)
    
    date_pattern = re.compile(r'/\d{4}/\d{2}/\d{2}/')
    filtered_links = [href for href in article_links if date_pattern.search(href)]
    return filtered_links

def scrape_article_data(driver, href):
    driver.get(href)
    time.sleep(5)  # Wait for the page to load
    
    article_data = {'url': href}
    
    try:
        h1_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[1]/section/h1')))
        article_data['title'] = h1_element.text
    except:
        article_data['title'] = None

    try:
        h2_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[1]/section/h2')))
        article_data['subtitle'] = h2_element.text
    except:
        article_data['subtitle'] = None

    try:
        publish_date_location_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[3]/div/div[1]/div/div')))
        article_data['publish_date_location'] = publish_date_location_element.text
    except:
        article_data['publish_date_location'] = None

    try:
        body_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/main/article/div/div[1]/div[3]/div/section/div')))
        article_data['body'] = body_element.text
        links_in_body = body_element.find_elements(By.TAG_NAME, 'a')
        article_data['links'] = [link.get_attribute('href') for link in links_in_body if link.get_attribute('href')]
    except:
        article_data['body'] = None
        article_data['links'] = []

    return article_data

def main():
    driver = initialize_browser(chrome_driver_path, chrome_options)
    all_articles_data = []

    try:
        driver.get('https://www.economist.com/')
        login_to_site(driver)
        filtered_links = get_filtered_article_links(driver)

        for href in filtered_links:
            print(f"Scraping: {href}")
            article_data = scrape_article_data(driver, href)
            all_articles_data.append(article_data)
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()

    with open('all_articles_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles_data, f, ensure_ascii=False, indent=4)

    print(json.dumps(all_articles_data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
