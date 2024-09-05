import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

def entrepreneur_article_urls():
    base_url = "https://www.entrepreneur.com"
    headers = {
    'Cookie': 'entrepreneur_permutive=c3yLwxqp1-; entrepreneur_permutive_cs=c3yLwxqp1-; geo={\'latitude\':\'39.030\',\'longitude\':\'-77.490\',\'city\':\'ashburn\',\'continent_code\':\'NA\',\'country_code\':\'US\',\'country_code3\':\'USA\',\'country_name\':\'united%20states\',\'postal_code\':\'20147\',\'region\':\'VA\',\'area_code\':\'703\',\'metro_code\':\'511\'}; language=en'
    }

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs
    links = soup.find_all('a', class_='text-base font-medium hover:underline leading-6')
    article_urls = [base_url + link['href'] for link in links if link.get('href')]

    return article_urls

def entrepreneur_article_details(article_url):
    headers = {
    'Cookie': 'entrepreneur_permutive=c3yLwxqp1-; entrepreneur_permutive_cs=c3yLwxqp1-; geo={\'latitude\':\'39.030\',\'longitude\':\'-77.490\',\'city\':\'ashburn\',\'continent_code\':\'NA\',\'country_code\':\'US\',\'country_code3\':\'USA\',\'country_name\':\'united%20states\',\'postal_code\':\'20147\',\'region\':\'VA\',\'area_code\':\'703\',\'metro_code\':\'511\'}; language=en'
    }
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', class_='tracking-tight font-extrabold text-gray-900 mb-4 text-[2.2rem] leading-[2.7rem] sm:text-[2.5rem] sm:leading-[2.9rem]')
    title = title_tag.text.strip() if title_tag else ""

    # Scrape the author name and URL
    author_tag = soup.find('a', class_='hover:underline uppercase font-semibold tracking-wider text-blue-600')
    author_name = author_tag.text.strip() if author_tag else ""
    author_url = "https://www.entrepreneur.com" + author_tag['href'] if author_tag else ""

    # Scrape the published date
    published_tag = soup.find('time', class_='block lg:inline-block mt-1 lg:mt-0 lg:ml-2')
    published = published_tag['datetime'].split('T')[0] if published_tag else ""

    # Scrape the published date
    published_tag = soup.find('time', class_='block lg:inline-block mt-1 lg:mt-0 lg:ml-2')
    published_date = published_tag['content'].split('T')[0] if published_tag else ""


    # Scrape the article body
    body_tag = soup.find('div', class_='gate-check')
    body = body_tag.text.strip() if body_tag else ""

    # Scrape author details
    author_details = entrepreneur_author_details(author_url) if author_url else {}

    # Return the article details, including author details
    article_details = {
        "title": title,
        "author_name": author_name,
        "author_url": author_url,
        "author_details": author_details,
        "published": published,
        "published_date": published_date,
        "body": body,
    }

    return article_details

def entrepreneur_author_details(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract author name
    author_name = soup.find('h1', class_='text-gray-900').get_text(strip=True) if soup.find('h1', class_='text-gray-900') else ''

    # Extract author image
    author_img = soup.find('div', class_='relative overflow-hidden flex-none').find('img')['src'] if soup.find('div', class_='relative overflow-hidden flex-none') else ''

    # Find the div that contains social media links
    social_links_div = soup.find('div', class_='mb-6')

    # Extract Twitter link if available
    author_twitter = ''
    if social_links_div:
        twitter_link_tag = social_links_div.find('a', class_='share-twitter')
        if twitter_link_tag and 'href' in twitter_link_tag.attrs:
            author_twitter = twitter_link_tag['href']

    # Extract LinkedIn link if available
    author_linkedin = ''
    if social_links_div:
        linkedin_link_tag = social_links_div.find('a', class_='share-linkedin')
        if linkedin_link_tag and 'href' in linkedin_link_tag.attrs:
            author_linkedin = linkedin_link_tag['href']

    # Store all author details in a dictionary, ensuring empty fields if not found
    author_details = {
        'author_name': author_name,
        'author_img': author_img,
        'author_twitter': author_twitter if author_twitter else '',
        'author_linkedin': author_linkedin if author_linkedin else ''
    }

    return author_details


def entrepreneur_save():
    domain = "entrepreneur.com"
    website = Website.objects.get(domain=domain)  # Assuming you have a Website model
    article_urls = entrepreneur_article_urls()
    
    for article_url in article_urls:
        if Articles.objects.filter(website=website, url=article_url).exists():
            # Fetch the existing article from the database
            art = Articles.objects.filter(url=article_url).first()
            article = {
                "author": art.author,
                "author_details": art.author_details,  # Use existing author details
                'title': art.title,
                "published": art.published,
                "published_date": art.published_date,
                'url': art.url,
                "body": art.body
            }
        else:
            try:
                # Get article details including author details
                article_details = entrepreneur_article_details(article_url)
                
                # Save the article to the database
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author_name"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    category="business"  # Replace with appropriate category if needed
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass
    return article_urls
