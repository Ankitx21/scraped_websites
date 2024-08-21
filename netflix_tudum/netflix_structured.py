import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.netflix.com"

def format_published_date(published_date):   
    formats = ['%B %d, %Y', '%b. %d, %Y']  
    date_obj = None
    for date_format in formats:
        try:
            date_obj = datetime.strptime(published_date, date_format)
            break
        except ValueError:
            pass

    if date_obj:
        return date_obj.strftime('%Y-%m-%d')
    else:
        return "Date format not recognized"


def netflix_article_list():
    
    # residential_proxies = {
    #         'http': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225',
    #         'https': 'http://brd-customer-hl_5f7bc336-zone-nad_webunlocker:nlevo8vx0tsw@brd.superproxy.io:22225'
    #     }
    # ca_cert_path = 'ca.crt'


    url = "https://www.netflix.com/tudum"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'nfvdid=BQFmAAEBEIVjxMD4AYAVtyg0dqHTCHVAGaqbqquuNQlfwQMMKXQS9qOaIdyqnY7aj02dEIAG61EfqRKU83NdDg8QiD_G2mE9Yo1DOJMk4oFv_D-QuOhYRA%3D%3D; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABRmKnCteEgK74guMrPoVbfT0Dl_crDPHGk.%26dt%3D1724245871782; NetflixId=v%3D3%26ct%3DBgjHlOvcAxLzAdKLqW0UmCVHH8JJU81N_EgJh_KpKQvU6fN31AuJz5JG5K1DFB_BE4Jz7rEg2K0YGaiKI8tuHoTRmQ9ukXy8WulnNAN5xvjIWcBDaWEWvMoXuEXWtBqyzexJSjRfJXzsm8dkOxQLrlA0CtP44Jhd02YhzND3Vl8kV47r2cRmMeSvI_z3blW0unUEtUKQUtKerxCNgNcvt_8rdZVs7UqPwDu5c6Lp98pjSTyMBgog0GhxMVBl4KqeeC3fFM-2GboP_gNKbR8xk1Jwv-fmh4FPWsom8-kAK9GEcP1L8kmvCjBH-X8PI4KA6BzHzHUh2coxBPfd1BgGIg4KDEuP2DCWd20b94LAhg..; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Aug+21+2024+19%3A20%3A19+GMT%2B0530+(India+Standard+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4576da69-de92-496c-a0ea-fd00594bbb3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; x-session=x-session%7C8b0ad27d-d56c-4b22-be63-c60eaebe889a%7C1724260321778%7C1724248229415',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload )
    print(response.status_code)
    
    if response.status_code == 200:
        article_links = []
        soup = BeautifulSoup(response.content, "html.parser")
        all_headings = soup.find_all("article")

        for heading in all_headings:
            a = heading.find("a")
            article_url = a['href']
            if not article_url.startswith(BASE_URL):
                article_url = BASE_URL + article_url 
            if 'articles' in article_url:  
                article_links.append(article_url)

        article_links = list(set(article_links))
        print(f"{len(article_links)} article links collected")
        return article_links
    else:
        print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
        return []


def netflix_article_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            missing_fields = []

            # Extract the title
            title_tag = soup.find('h1', class_=['css-1dsr7vp esmf2q82', 'css-16fe7e0 e6o0s157'])
            title = title_tag.text.strip() if title_tag else ""
            if not title:
                missing_fields.append("Title")

            # Extract the author
            author_tag = soup.find('div', class_='css-19pirhg esmf2q85')
            author = author_tag.text.strip()[3:] if author_tag else ""
            if not author:
                missing_fields.append("Author")

            # Extract the published date
            published_tag = soup.find('div', class_='css-1bmnxg7')
            if published_tag:
                published_date = format_published_date(published_tag.text.strip())
            else:
                published_date = ""
                missing_fields.append("Publish Date")

            # Extract the body content
            body_content = ""
            paragraphs = soup.find("div", class_=['use-styled-headings css-6ywxh8', 'css-6ywxh8']).find_all("p")
            if paragraphs:
                body_content = ' '.join([para.text.strip() for para in paragraphs])
            else:
                missing_fields.append("Body Content")

            if missing_fields:
                print(f"Missing fields for {url}: {', '.join(missing_fields)}")
                return None

            return {
                'url': url,
                'title': title,
                'published': published_tag.text.strip(),
                'publish_date': published_date,
                'author': author,
                'body': body_content
            }
        else:
            print({'url': url, 'error': 'Failed to retrieve the page', 'status_code': response.status_code})
            return None

    except Exception as e:
        print({'url': url, 'error': str(e)})
        return None


if __name__ == "__main__":
    articles = netflix_article_list()

    articles_data = []
    for i, article in enumerate(articles):
        print(f"Scraping {article}")
        article_details = netflix_article_details(url=article)
        if article_details:
            articles_data.append(article_details)
            # print(f"Payload found for article {i + 1}")

    # Save scraped data to a JSON file
    with open("zzsample outputs/tudum_Articles.json", "w") as json_file:
        json.dump(articles_data, json_file, indent=4)

    print("Data fetched and stored successfully!")
