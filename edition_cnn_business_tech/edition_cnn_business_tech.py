import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Proxies and certificate path
residential_proxies = {
    'http': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_5f7bc336-zone-residential_proxy2:j61wavrugcvs@brd.superproxy.io:22225'
}
ca_cert_path = 'ca.crt'

# URL and headers
url = "https://edition.cnn.com/business/tech"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.6',
    'cookie': 'wbdFch=368a482c867f2186221f0aeb56e1ec749e2ef90b; countryCode=IN; FastAB=0=5189,1=9107,2=2878,3=7743,4=7276,5=6772,6=1589,7=3841,8=0805,9=4969,10=8584,11=0685,12=3549,13=6687,14=6276,15=6662,16=7091,17=7832,18=8650,19=2326; usprivacy=1---; FastAB_Zion=5.1; s_ecid=MCMID%7C07480088709520616564237507128275873012; AMCVS_7FF852E2556756057F000101%40AdobeOrg=1; s_cc=true; stateCode=KA; _sp_ses.f5fb=*; sato=1; umto=1; nexus-web-application-identifier=fdc15c95-006c-4f02-a819-7db7e74d901c|1722311063110; SecGpc=1; geoData=bagalkot|KA|587314|IN|AS|530|broadband|16.480|75.100|356004; cnprevpage_pn=%2Fbusiness%2F; _dd_s=logs=1&id=740207b1-0cca-406f-abe6-b01c4b736113&created=1722310663321&expire=1722312121015; _sp_id.f5fb=459eb680-9fee-49d9-88b7-9a98b43be2f1.1722084009.4.1722311221.1722104477.8d17cf80-9349-4027-bf4e-b358e068ed21; s_sq=cnn-adbp-domestic%3D%2526c.%2526a.%2526activitymap.%2526page%253D%25252Fbusiness%25252F%2526link%253DTech%2526region%253DpageHeader%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c; AMCV_7FF852E2556756057F000101%40AdobeOrg=179643557%7CMCIDTS%7C19935%7CMCMID%7C07480088709520616564237507128275873012%7CMCAID%7CNONE%7CMCOPTOUT-1722318421s%7CNONE%7CvVersion%7C5.5.0; wbdFch=6e3372d1f0b30a1c132db0f7aefe3dc3e7d2c4c2; SecGpc=1; countryCode=IN; geoData=davangere|KA|577006|IN|AS|530|broadband|14.460|75.910|356004; stateCode=KA',
    'priority': 'u=0, i',
    'referer': 'https://edition.cnn.com/business',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

# Function to scrape URLs
def edition_cnn_business_tech_article_list():
    response = requests.get(url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    soup = BeautifulSoup(response.text, 'html.parser')
    target_class = "container__link"
    links = soup.find_all('a', class_=target_class)
    hrefs = set(link.get('href') for link in links if link.get('href'))
    date_pattern = re.compile(r'/\d{4}/\d{2}/\d{2}/')
    filtered_hrefs = {href for href in hrefs if date_pattern.search(href)}
    return ["https://edition.cnn.com" + href for href in filtered_hrefs]

# Function to parse date
def edition_cnn_business_convert_published(date_str):
    try:
        # Extract the date part from the string
        date_part = re.search(r'\w+ \d{1,2}, \d{4}', date_str).group(0)
        date_obj = datetime.strptime(date_part, '%B %d, %Y')
        return date_obj.strftime('%m/%d/%Y')
    except (ValueError, AttributeError) as e:
        print(f"Error parsing date: {e}")
        return 'No date found'

# Function to scrape article details
def edition_cnn_business_tech_article_details(article_url):
    response = requests.get(article_url, headers=headers, proxies=residential_proxies, verify=ca_cert_path)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    heading = soup.find('h1', {'data-editable': 'headlineText'})
    heading_text = heading.get_text(strip=True) if heading else 'No heading found'
    
    author_div = soup.find('div', class_='byline__names')
    author_name = author_div.find('span', class_='byline__name').get_text(strip=True) if author_div and author_div.find('span', class_='byline__name') else 'No author found'
    
    timestamp_div = soup.find('div', class_='timestamp')
    date_str = timestamp_div.get_text(strip=True).replace('Updated', '').strip() if timestamp_div else 'No date found'
    published_date = edition_cnn_business_convert_published(date_str) if timestamp_div else 'No date found'
    
    article_body_div = soup.find('div', class_='article__content')
    article_body = article_body_div.get_text(strip=True) if article_body_div else 'No content found'
    
    return {
        'url': article_url,
        'heading': heading_text,
        'author': author_name,
        'published_date': published_date,
        'content': article_body
    }

# Main function
def main():
    print("Scraping CNN Tech page for articles...")
    urls = edition_cnn_business_tech_article_list()
    for url in urls:
        print(f"Scraping article: {url}")
        article = edition_cnn_business_tech_article_details(url)
        print(f"URL: {article['url']}")
        print(f"Heading: {article['heading']}")
        print(f"Author: {article['author']}")
        print(f"Published Date: {article['published_date']}")
        print(f"Content: {article['content']}")  # Print first 200 characters of the content
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
