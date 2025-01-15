import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re


def convert_date_format(date_str): 
    return date_str



def to5_author_details(url="https://www.semafor.com/author/mizy-clifton"):
    response =requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    author_linkedin=author_twitter=author_img=''

    author_name = soup.find('meta', {'property':'og:title'})['content']
    author_img = soup.find('meta', {'property':'og:image'})['content']
   
    author_details = {"author_name": author_name, "author_img" : author_img, "author_linkedin" : author_linkedin, "author_twitter" : author_twitter}
    return author_details



def to5_article_list():
 
    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    url = "https://9to5google.com/"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers, data=payload ,proxies=proxies , verify=ca_cert_path)   
    # print(response.status_code)

    if response.status_code == 200:
        article_links =set()
        soup = BeautifulSoup(response.text ,'html.parser')

        articles = soup.find_all('a' ,class_="article__title-link")
        if articles:
            for article in articles:
                if article.get('href') == None:
                    continue
                link = article.get('href')

                if "https://9to5google.com" in link:
                    article_links.add(link)
                    # print(link)
        else:
            print("Article section was not found")            
        # print(len(article_links))
        return article_links
    
    else:
        print({'error': 'Failed to retrieve the page', 'status_code': response.status_code})


# to5_article_list()
url ="https://9to5toys.com/2025/01/13/amazon-fire-tablets-deals-2025/"

def to5_article_details(url):

    proxies ={'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'}
    ca_cert_path = 'ca.crt'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.request("GET", url, headers=headers,  proxies=proxies , verify=ca_cert_path)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("meta", {"property":"og:title"})['content']
    published = soup.find("meta", {"property":"article:published_time"})['content']
    date_str = published.split("T")[0]
    published_date = convert_date_format(date_str)
    article_image = soup.find("meta", {"property":"og:image"})['content']
    try:
        author_container = soup.find('span', class_="author-name").find("a")
    except:
        author_container = soup.find('a' ,class_="txt-sc")
    author = author_container.text.strip()
    author_link = author_container['href']
    author_info = to5_author_details(author_link)
    
    body = ""
    paragraphs = soup.find(class_="container med post-content").find_all("p")
    for para in paragraphs:
        body += para.text.strip()
    
    payload = {
        'domain': "9to5google.com",
        'title': title,
        'published': published,
        "published_date": published_date,  
        'author': author,
        "article_image": article_image,
        'author_details': author_info,
        'url': url,
        'body': body
    }
    return payload


if __name__ == "__main__":

    total_article_links = to5_article_list()
    # print(total_article_links)

#     total_article_links = {'https://9to5google.com/2025/01/10/google-tv-nest-doorbell-responses/', 'https://9to5google.com/2025/01/10/google-drive-desktop-upload/', 'https://9to5google.com/2025/01/11/swippitt-instant-phone-charger-ces-2025/', 'https://9to5google.com/2025/01/10/deals-oneplus-nord-buds-3-pro-google-smart-tvs/', 'https://9to5google.com/2025/01/10/oneplus-12-vs-oneplus-13/', 'https://9to5mac.com/m4-max-m4-ultra-mac-studio/', 'https://9to5toys.com/2025/01/12/new-this-week-tech-ps5-lego/', 'https://9to5google.com/2025/01/10/galaxy-s25-ultra-s-pen-without-bluetooth/', 'https://9to5google.com/2025/01/09/chromecast-google-tv-2025-update/', 'https://electrek.co/2025/01/11/tenways-c-go-600pro-commuter-e-bike-is-as-smooth-as-it-gets/', 'https://9to5google.com/2025/01/10/pixelated-036/', 'https://9to5google.com/2025/01/09/google-tv-gemini-hands-on/', 'https://9to5google.com/2025/01/10/lenovo-2025-android-tablets-ces-hands-on/', 'https://spaceexplored.com/2025/01/11/blue-origin-delays-new-glenn-launch-due-to-recovery-weather/', 'https://spaceexplored.com/2025/01/11/starship-flight-7-spacex-delays-until-the-13th/', 'https://9to5google.com/2025/01/10/lenovo-legion-go-sold-out-small-android-tablets/', 'https://9to5google.com/2025/01/12/qi2-broken-promise/', 'https://connectthewatts.com/2025/01/10/carrier-donates-2-5m-in-air-purifiers-for-wildfire-relief/', 'https://9to5toys.com/2025/01/12/unlocked-512gb-galaxy-s24-ultra-deal/', 'https://9to5mac.com/2025/01/12/new-apple-watch-se-health-features/', 'https://9to5google.com/2025/01/10/youtube-music-top-songs-2/', 
# 'https://connectthewatts.com/2025/01/09/crunch-fitness-opens-doors-to-support-los-angeles-community-during-wildfires/', 'https://dronedj.com/2025/01/09/dji-o4-air-unit-buy/', 'https://9to5toys.com/2025/01/10/android-app-deals-freebies-exolotl-zian/', 'https://connectthewatts.com/2025/01/10/ringconn-showcases-breakthrough-wearables-at-ces-2025/', 'https://connectthewatts.com/2025/01/09/ai-powered-gym-management-software-revolutionizes-fitness-operations/', 'https://electrek.co/2025/01/11/ces2025-kubota-brings-electric-equipment-robots-and-hydrogen-to-ces/', 'https://9to5google.com/2025/01/11/lenovo-legion-tab-stylus-pen-support/', 'https://spaceexplored.com/2025/01/12/how-to-watch-blue-origins-inaugural-new-glenn-launch/', 'https://9to5google.com/2025/01/10/google-tv-buy-movies/', 'https://9to5toys.com/2025/01/12/anker-new-display-140w-wall-charger-purchase-deal/', 'https://9to5google.com/2025/01/09/gemini-overlay-redesign/', 'https://9to5google.com/2025/01/10/qi2-moving-coil-tech-demo-ces-2025/', 'https://spaceexplored.com/2025/01/11/bepicolombo-made-its-final-flyby-of-mercury-its-closest-yet/', 'https://dronedj.com/2025/01/11/flying-lion-hits-55000-drone-as-a-first-responder-missions/', 'https://spaceexplored.com/2025/01/11/starship-flight-7-spacex-completes-pre-launch-rehearsal/', 'https://9to5google.com/2025/01/10/google-discover-daily-listen-2/', 'https://9to5google.com/2025/01/10/samsung-galaxy-s25-specs-leak-images/', 'https://electrek.co/2025/01/11/volvo-dd25-electric-compactor-gets-to-work-in-yolo-county-california/', 'https://9to5google.com/2025/01/10/galaxy-s25-high-quality-render-leak-shows-off-the-best-parts-gallery/', 'https://9to5google.com/2025/01/12/google-store-sale-2025-pixel/', 'https://9to5toys.com/2025/01/11/this-weeks-best-deals-macbook-airpods-anker/', 'https://dronedj.com/2025/01/09/drone-company-teaming-up-with-spacex-and-openai-to-compete-on-major-defense-contracts/', 'https://9to5mac.com/2025/01/12/apple-ipad-11-a17-pro-chip/', 'https://electrek.co/2025/01/11/e-bike-makers-push-speed-reduction-updates-after-californias-stricter-new-laws/', 'https://9to5mac.com/2025/01/12/turn-your-iphone-into-retro-console-with-physical-buttons-with-this-case/', 'https://electrek.co/2025/01/12/the-days-of-superfast-super73-e-bikes-are-over-sort-of/', 'https://dronedj.com/2025/01/09/dji-flip-drone-launch-features/', 'https://9to5toys.com/2025/01/12/latest-beats-solo-buds-deal/', 'https://9to5google.com/2025/01/10/fitbit-app-cast-workout-video-tv/', 'https://dronedj.com/2025/01/10/la-firefighting-aircraft-grounded-after-drone-collision/', 'https://connectthewatts.com/2025/01/09/ai-wellness-unveils-mission-2025-at-ces/', 'https://9to5google.com/2025/01/10/oneplus-13-review-finally-this-one-truly-doesnt-settle/', 'https://9to5mac.com/2025/01/12/apple-homepad-home-hub-possible-delay/'}

    articles_data = []
    for url in total_article_links:    
        # print("Scraping article details from: ", url)    
        article_details = to5_article_details(url)
        if article_details:
            articles_data.append(article_details)

    with open('0author_scripts/9to5/9to5_article_details.json', 'w') as f:
            json.dump(articles_data, f, indent=4)
    
    # print("Data fetched and stored in 9to5_articles.json")