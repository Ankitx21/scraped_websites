import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tech.models import Articles, Website
from proxy.models import Proxy

def wired_business_article_urls():
    base_url = "https://www.wired.com"
    business_url = f"{base_url}/category/business/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'CN_geo_country_code=US; CN_segments=co.w2435; CN_xid=9fc02c25-0e59-4929-e64d-5f0f84aa3633; CN_xid_refresh=9fc02c25-0e59-4929-e64d-5f0f84aa3633; xid1=1'
    }

    response = requests.get(business_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article URLs
    links = soup.find_all('a', class_='SummaryItemHedLink-civMjp ejgyuy summary-item-tracking__hed-link summary-item__hed-link')
    article_urls = [base_url + link['href'] for link in links if link.get('href')]

    return article_urls

def wired_business_date(date_string):
    """
    Converts a date string to 'yyyy/mm/dd' format.
    """
    try:
        # Parse the date in 'MMM dd, yyyy' format
        parsed_date = datetime.strptime(date_string, "%b %d, %Y")
        return parsed_date.strftime("%Y/%m/%d")
    except ValueError:
        # If parsing fails, return an empty string
        return ""

def wired_author_details(author_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the author name
    author_name_tag = soup.find('h1', {'data-testid': 'ContributorHeaderName'})
    author_name = author_name_tag.text.strip() if author_name_tag else ''
    
    # Scrape the author image
    author_img_tag = soup.find('img', class_='ResponsiveImageContainer-eybHBd fptoWY responsive-image__image')
    author_img = author_img_tag['src'] if author_img_tag else ''
    
    # Scrape the author Twitter URL
    author_twitter_tag = soup.find('a', {'class': 'external-link SocialIconExternalLink-huuzOU cLGRzS social-icons__link social-icons__link--twitter'})
    author_twitter = author_twitter_tag['href'] if author_twitter_tag else ''
    
    # Placeholder for LinkedIn
    author_linkedin = ''
    
    author_details = {
        "author_name": author_name,
        "author_img": author_img,
        "author_linkedin": author_linkedin,
        "author_twitter": author_twitter
    }
    
    return author_details

def wired_business_article_details(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Cookie': 'CN_geo_country_code=US; CN_segments=co.w2435; CN_xid=9fc02c25-0e59-4929-e64d-5f0f84aa3633; CN_xid_refresh=9fc02c25-0e59-4929-e64d-5f0f84aa3633; xid1=1'
    }

    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape the article title
    title_tag = soup.find('h1', {'data-testid': 'ContentHeaderHed'})
    title = title_tag.text.strip() if title_tag else ""

    # Scrape the author name and URL
    author_tag = soup.find('a', class_='BaseWrap-sc-gjQpdd BaseText-ewhhUZ BaseLink-eNWuiM BylineLink-gEnFiw iUEiRd euNVPR jdMSdZ BDKtv byline__name-link button')
    author_name = author_tag.text.strip() if author_tag else ""
    author_url = "https://www.wired.com" + author_tag['href'] if author_tag else ""

    # Scrape the published date and published text
    published_tag = soup.find('time', {'data-testid': 'ContentHeaderPublishDate'})
    if published_tag and 'datetime' in published_tag.attrs:
        # If the datetime attribute is available, extract the date part only
        datetime_value = published_tag['datetime']
        published_date = datetime_value.split('T')[0]
    else:
        # Use the text content to extract the date
        published_date = ""
    
    # Extract the published text directly
    published = published_tag.text.strip() if published_tag else ""

    # Convert text date to 'yyyy/mm/dd' format if datetime attribute is missing
    if not published_date and published:
        # Extract the 'MMM dd, yyyy' part from the text
        date_part = " ".join(published.split()[:3])
        published_date = wired_business_date(date_part) if date_part else ""

    # Scrape the article body
    body_tag = soup.find('div', class_='body__inner-container')
    body = body_tag.get_text(separator="\n").strip() if body_tag else ""

    # Get author details if author URL is available
    author_details = wired_author_details(author_url) if author_url else {}

    # Combine article details with author details
    article_details = {
        "title": title,
        "author_name": author_name,
        "author_details": author_details,
        "published": published,
        "published_date": published_date,
        "body": body,

    }

    return article_details


def wired_save():
    domain = "wired.com"
    website = Website.objects.get(domain=domain)
    article_urls = wired_business_article_urls()

    for i, article_url in enumerate(article_urls):
        if Articles.objects.filter(website=website, url=article_url).exists():
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
                article_details = wired_business_article_details(article_url)
                art = Articles(
                    website=website,
                    url=article_url,
                    title=article_details["title"],
                    author=article_details["author_name"],
                    author_details=article_details["author_details"],  # Include author details
                    body=article_details["body"],
                    published=article_details["published"],
                    published_date=article_details["published_date"],
                    # Assuming there's a category field; you might need to adjust this
                    category="business"  # Replace with the appropriate category if different
                )
                art.save()
            except Exception as e:
                print(f"Error saving article: {e}")
                pass

    return article_urls
