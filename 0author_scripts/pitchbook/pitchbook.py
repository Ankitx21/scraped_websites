# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv 


from bs4 import BeautifulSoup 
import requests 
import csv 

from django.conf import settings 
import json
from datetime import datetime 

def pitchbook_date(published):
    date_object = datetime.strptime(published, '%B %d, %Y').date()
    return date_object

def pitchbook_author_details(author_link):
    # 403 without proxy
    residential_proxies = {
            'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
        }
    ca_cert_path = 'ca.crt'

    response= requests.get(author_link, proxies=residential_proxies , verify=ca_cert_path )
    # print(response.status_code)
    soup = BeautifulSoup(response.text , 'html.parser')
    author_name = soup.find('h1', class_='AuthorPage-name').text.strip()
    print(author_name)
    author_img = soup.find('div' ,class_='AuthorPage-image').find('img')['srcset']
    print(author_img)

    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : "", "author_twitter" : ""}
    return author_details



def pitchbook_article_list(url):
    para = ""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") 
    # Enable JavaScript
    options.add_argument('--enable-javascript')
    
    # Enable cookies
    options.add_argument('--enable-cookies') 
    options.add_argument(r"--user-data-dir=C:\Users\CHANDAN\AppData\Local\Google\Chrome\User Data")
    options.add_argument(r'--profile-directory=Profile 30') #mass tor profile

    driver  = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    with open("pitbook.csv", 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
                # for row in data:
                #     csv_writer.writerow(row)
        try:
            for i in range(1, 2):
                print("working on : ", url)
                rows = []
                driver.get(url)
                time.sleep(1)
                article_list_container = driver.find_element(
                    By.XPATH,
                    "//bsp-list-loadmore[@style=' --color-button-bg:#40c2c9; --color-button-secondary-bg:#267479; --color-button-text:#051c38; --color-button-secondary-text:#051c38;']"
                    )   
                # print(len(article_list_container))
                articles = article_list_container.find_elements(By.XPATH, "//div[@class='PageList-items-item']")
                for article in articles:
                    article_url = article.find_element(By.TAG_NAME, 'a').get_attribute("href")
                    print(i, article_url, url)
                    # row = [article_url]
                    rows.append([i, article_url, url])
                    # print(url.get_attribute("href"))
                articles_sidebar = driver.find_elements(By.XPATH, "//div[@class='flickity-slider']//div[@class='PagePromo-media']")
                for side_article in articles_sidebar:
                    side_article_url = side_article.get_attribute("href")
                    rows.append([i, side_article_url, url])
                print("Total articles found : ", len(rows), )
                csv_writer.writerows(rows)
                url = f"https://pitchbook.com/news?p={i}"
        except Exception as e :
            print(e)
        
            


def pitchbook_article_details(url):
    proxy_url = f"http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225"

    # set selenium-wire options to use the proxy
    seleniumwire_options = {
        "proxy": {
            "http": proxy_url,
            "https": proxy_url
        },
    }

    # set Chrome options to run in headless mode
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    options.add_argument("start-maximized")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-dev-shm-usage')

    service = Service("driver/chromedriver")

    # initialize the Chrome driver with service, selenium-wire options, and chrome options
    driver = webdriver.Chrome(
        service=service,
        seleniumwire_options=seleniumwire_options,
        options=options
    )
    para = ""
    driver.save_screenshot("pitchbook.png")
    # options = webdriver.ChromeOptions()
    # # options.add_argument("--headless=new") 
    # # Enable JavaScript
    # options.add_argument('--enable-javascript')

    # # Enable cookies
    # options.add_argument('--enable-cookies') 
    # options.add_argument(r"--user-data-dir=C:\Users\CHANDAN\AppData\Local\Google\Chrome\User Data")
    # options.add_argument(r'--profile-directory=Profile 17') #mass tor profile
    # artile_url_list = get_article_url(limit=400)
    # driver  = webdriver.Chrome(options=options)
    count = 15
    # for article_url in artile_url_list[64:]:
    try:
        article_url = url 
        driver.get(article_url)
        print(count, article_url)
        time.sleep(2)
        head_div = driver.find_element(By.XPATH, "//div[@class='Page-lead-content']")
        title = head_div.find_element(By.TAG_NAME, "h1").text
        # print("title", title)
        author = head_div.find_element(By.XPATH, "//div[@class='Page-authors']").find_element(By.TAG_NAME, "span").text
        author_link = head_div.find_element(By.XPATH, "//div[@class='Page-authors']").find_element(By.TAG_NAME, "a").get_attribute('href')
        author_info = pitchbook_author_details(author_link)
        # print("author", author)  
        published = head_div.find_element(By.XPATH, "//div[@class='Page-datePublished']").text.strip()
        published_date = pitchbook_date(published=published)
        # print("published", published)
        main_div = driver.find_element(By.XPATH, "//main[@class='Page-main']").find_elements(By.TAG_NAME, "p")
        # print("total para ", len(main_div))
        for p in main_div:
            para += p.text
        
        # print(para)
        payload = {
            'domain':"pitchbook.com",
            'title': title,
            'published': published,
            "published_date": published_date,
            'author': author,
            'author_details': author_info,
            'url': article_url,
            'body': para
        }
        count += 1
        # save_articles_with_api(url="https://webscrapper.inside-ai.xyz/create_article", payload=payload)
        return payload
    except Exception as e :
        print(e)



def get_article_url(limit):
    article_list = []
    with open("pitbook.csv", "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        count = 0
        for row in reader:
            count += 1
            if row[1] != "":
                url_break = str(row[1]).split("https://pitchbook.com/news/")[1].split("/")
                if url_break[0] == "articles":
                    article_list.append(row[1])
            if count == limit:
                break
        print(len(article_list))
        article_list = list(set(article_list))
        print(len(article_list))
        return article_list



def save_articles_with_api(url, payload):
    try:
        # Making the API call
        response = requests.post(url, data=payload)

        # Checking the response status
        if response.status_code == 200:
            # If the response is successful (status code 200), print the response text
            print("API call successful:")
            print(response.text)
        else:
            # If the response is not successful, print the status code and reason
            print(f"API call failed with status code {response.status_code}: {response.reason}")
    
    except Exception as e:
        # If any exception occurs during the API call, print the exception
        print(f"An error occurred: {e}")


# Example payload and URL
url = "https://webscrapper.inside-ai.xyz/create_article"
payload = {
    'domain': 'test.com',
    'title': 'An Update ',
    'published': 'June 4, 2019',
    'author': 'Barry Cooks',
    'url': 'https://www.digitalocean.com/blog/an-i',
    'body': 'hello'
}

if __name__ == "__main__":
    # pitchbookp_article_list(url="https://www.pitchbook.com/tag/developers/")
    # pitchbook_article_details("https://www.pitchbook.com/story/this-ai-bot-fills-out-job-applications-for-you-while-you-sleep/")
    article_url_list = ["https://pitchbook.com/news/articles/market-map-green-industry-powers-carbon-tech", 
                        "https://pitchbook.com/news/articles/top-quantum-computing-startups-capital-raised"]
    pitchbook_article_details()
    # pitchbook_article_list(url="https://pitchbook.com/news")
    # pitchbook_login()
    # get_article_url(limit=200)