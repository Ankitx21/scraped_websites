import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

# Function to scrape URLs
def edition_cnn_business_tech_article_list():
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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract article links based on class
    target_class = "container__link"
    links = soup.find_all('a', class_=target_class)
    hrefs = set(link.get('href') for link in links if link.get('href'))
    
    # Filter links based on date pattern
    date_pattern = re.compile(r'/\d{4}/\d{2}/\d{2}/')
    filtered_hrefs = {href for href in hrefs if date_pattern.search(href)}
    
    # Return complete URLs
    return ["https://edition.cnn.com" + href for href in filtered_hrefs]

# Function to parse date
def edition_cnn_business_convert_published(date_str):
    try:
        # Extract the date part from the string
        date_part = re.search(r'\w+ \d{1,2}, \d{4}', date_str).group(0)
        date_obj = datetime.strptime(date_part, '%B %d, %Y')
        return date_obj.strftime('%Y-%m-%d')
    except (ValueError, AttributeError) as e:
        print(f"Error parsing date: {e}")
        return 'No date found'

# Function to scrape article details
def edition_cnn_business_tech_article_details(article_url):
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
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract article heading
    heading = soup.find('h1', {'data-editable': 'headlineText'})
    heading_text = heading.get_text(strip=True) if heading else None
    
    # Extract author name and URL
    author_div = soup.find('div', class_='byline__names')
    author_tag = author_div.find('a', class_='byline__link') if author_div else None
    author_name = author_tag.find('span', class_='byline__name').get_text(strip=True) if author_tag else None
    author_url = author_tag.get('href') if author_tag else None

    # Adjust author URL to be relative to 'https://edition.cnn.com/'
    if author_url and 'profiles/' in author_url:
        author_url = author_url.replace('https://www.cnn.com/', 'https://edition.cnn.com/')
    
    # Extract published date
    timestamp_div = soup.find('div', class_='timestamp')
    date_str = timestamp_div.get_text(strip=True).replace('Updated', '').strip() if timestamp_div else None
    published_date = edition_cnn_business_convert_published(date_str) 
    
    # Extract article body
    article_body_div = soup.find('div', class_='article__content')
    article_body = article_body_div.get_text(strip=True) if article_body_div else None
    
    # Get author details using the author URL
    author_details = edition_cnn_author_details(author_url) if author_url else None
    
    return {
        'url': article_url,
        'title': heading_text,
        'author': author_name,
        'author_details': author_details,
        'published': date_str,
        'published_date': published_date,
        'body': article_body,

    }

# Function to get author details from author page
def edition_cnn_author_details(author_url):
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
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract author image
    author_img_tag = soup.find('img', class_='image__dam-img')
    author_img = author_img_tag.get('src') if author_img_tag else None
    
    # Extract author Twitter link
    author_twitter_tag = soup.find('a', class_='profile__social-link', href=re.compile(r'twitter\.com'))
    author_twitter = author_twitter_tag.get('href') if author_twitter_tag else None
    
    # LinkedIn link is not available on CNN, set it to None
    author_linkedin = None
    
    return {
        'author_name': soup.find('h1').get_text(strip=True) if soup.find('h1') else None,
        'author_img': author_img,
        'author_linkedin': author_linkedin,
        'author_twitter': author_twitter
    }

# Function to save CNN Business Tech articles to the database
def editon_cnn_business_save():
    domain = "edition.cnn.com"
    # Retrieve the website object for CNN
    website = Website.objects.get(domain=domain)
    
    # Get a list of article URLs from the CNN Business Tech section
    article_urls = edition_cnn_business_tech_article_list()
    
    # Loop through each article URL
    for i, article_url in enumerate(article_urls):
        try:
            # Scrape details from the article
            article_details = edition_cnn_business_tech_article_details(article_url)
            
            # Retrieve or create a new article object in the database
            article, created = Article.objects.get_or_create(
                url=article_details['url'],
                defaults={
                    'title': article_details['title'],
                    'author': article_details['author'],
                    'author_details': article_details['author_details'],
                    'published': article_details['published_date'],
                    'body': article_details['body'],
                    'website': website
                }
            )
            
            # If the article was not created (already exists), update its details
            if not created:
                article.title = article_details['title']
                article.author = article_details['author']
                article.author_details = article_details['author_details']
                article.published = article_details['published_date']
                article.body = article_details['body']
                article.save()

            print(f"Article saved: {article.title}")
        except Exception as e:
            print(f"Error saving article {i + 1}/{len(article_urls)}: {e}")

# Call the save function to start the scraping and saving process
editon_cnn_business_save()
